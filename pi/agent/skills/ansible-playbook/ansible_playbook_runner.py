"""
Ansible Playbook Runner with OpenSearch Export

Discovers, validates, and executes Ansible playbooks with structured logging.
"""

import json
import logging
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import structlog
import yaml
from requests import Session
from requests.exceptions import RequestException

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

log = structlog.get_logger(__name__)


class PlaybookRunner:
    """Manages Ansible playbook discovery, validation, and execution."""

    LOG_DIR = Path.home() / ".ansible_playbook_runner" / "logs"
    OTEL_ENDPOINT = "http://localhost:4317"
    LOGBACK_FORMAT = "%(asctime)s %(levelname)-5s [%(threadName)s] %(message)s"
    CONFIRMATION_STRING = "I confirm deployment to LIVE"
    
    # Fixed list of available clusters
    FIXED_CLUSTERS = [
        "piotr-test-cluster",
        "laser-cas",
        "laser-cassandra",
    ]

    def __init__(
        self,
        cassandra_root: Optional[str] = None,
        otel_endpoint: Optional[str] = None,
        disable_opensearch: bool = False,
    ):
        """
        Initialize the runner.

        Args:
            cassandra_root: Path to cassandra-ansible project
            otel_endpoint: OTEL collector endpoint
            disable_opensearch: If True, skip OpenSearch export
        """
        self.cassandra_root = Path(cassandra_root or "/Users/panisko/projects/cassandra-ansible")
        self.playbooks_dir = self.cassandra_root / "playbooks"
        self.inventories_dir = self.cassandra_root / "inventories"
        self.otel_endpoint = otel_endpoint or os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", self.OTEL_ENDPOINT)
        self.disable_opensearch = disable_opensearch or os.getenv("DISABLE_OPENSEARCH_EXPORT", "").lower() == "1"
        self.debug = os.getenv("ANSIBLE_DEBUG", "").lower() == "1"

        # Ensure log directory
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)

        log.msg(
            "playbook_runner_initialized",
            cassandra_root=str(self.cassandra_root),
            otel_endpoint=self.otel_endpoint,
            opensearch_enabled=not self.disable_opensearch,
        )

    def discover_playbooks(self) -> List[str]:
        """
        Discover all available playbooks.

        Returns:
            List of playbook names (without .yml extension)

        Raises:
            FileNotFoundError: If playbooks directory doesn't exist
        """
        if not self.playbooks_dir.exists():
            raise FileNotFoundError(f"Playbooks directory not found: {self.playbooks_dir}")

        playbooks = []
        for yml_file in sorted(self.playbooks_dir.glob("*.yml")):
            playbooks.append(yml_file.stem)

        log.msg("playbooks_discovered", count=len(playbooks), playbooks=playbooks)
        return playbooks

    def get_fixed_clusters(self) -> List[str]:
        """
        Get the fixed list of available clusters.

        Returns:
            List of cluster names
        """
        log.msg("clusters_retrieved", count=len(self.FIXED_CLUSTERS), clusters=self.FIXED_CLUSTERS)
        return self.FIXED_CLUSTERS

    def fetch_datacenters_and_brands(
        self, cluster: str, stage: str
    ) -> Tuple[List[str], List[str]]:
        """
        Fetch available datacenters and brands for a cluster and stage.

        Uses scripts/fetch_hosts.py to dynamically discover inventory.

        Args:
            cluster: Cluster name
            stage: Stage (qa/live)

        Returns:
            Tuple of (datacenters, brands) - sorted lists of unique values
        """
        datacenters = set()
        brands = set()

        try:
            # Call fetch_hosts.py --list to get inventory
            result = subprocess.run(
                [
                    "python3",
                    str(self.cassandra_root / "scripts" / "fetch_hosts.py"),
                    "--cluster",
                    cluster,
                    "--stage",
                    stage,
                    "--list",
                ],
                cwd=str(self.cassandra_root),
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                log.warning(
                    "datacenter_discovery_failed",
                    cluster=cluster,
                    stage=stage,
                    stderr=result.stderr,
                )
                return [], []

            try:
                inventory = json.loads(result.stdout)
            except json.JSONDecodeError as e:
                log.warning(
                    "datacenter_discovery_parse_error",
                    cluster=cluster,
                    stage=stage,
                    error=str(e),
                )
                return [], []

            # Extract datacenters from inventory groups
            # The inventory structure has group names like 'de_kae_bs', 'de_rhr_bap' etc.
            if isinstance(inventory, dict):
                for key in inventory.keys():
                    # Skip meta and all groups, cluster group
                    if key not in ("_meta", "all", f"{cluster}_".replace("-", "_")):
                        # These are datacenter groups
                        if key and not key.startswith("_"):
                            datacenters.add(key)
                    # Extract brand from cluster name if present
                    if key == "all" and "vars" in inventory.get(key, {}):
                        if "brand" in inventory[key]["vars"]:
                            brands.add(inventory[key]["vars"]["brand"])

            # Add default brands if none found
            if not brands:
                brands.add("all")

            datacenters_list = sorted(list(datacenters))
            brands_list = sorted(list(brands))

            log.msg(
                "datacenter_discovery_successful",
                cluster=cluster,
                stage=stage,
                datacenters=datacenters_list,
                brands=brands_list,
            )

            return datacenters_list, brands_list

        except subprocess.TimeoutExpired:
            log.error(
                "datacenter_discovery_timeout",
                cluster=cluster,
                stage=stage,
            )
            return [], []
        except Exception as e:
            log.exception(
                "datacenter_discovery_error",
                cluster=cluster,
                stage=stage,
                error=str(e),
            )
            return [], []

    def parse_required_variables(self, playbook_name: str) -> List[str]:
        """
        Parse playbook YAML to detect required variables.

        Args:
            playbook_name: Playbook name without .yml extension

        Returns:
            List of variable names (e.g., ['datacenter_name', 'cluster'])
        """
        playbook_path = self.playbooks_dir / f"{playbook_name}.yml"

        if not playbook_path.exists():
            log.warning("playbook_not_found", playbook=playbook_name)
            return []

        try:
            with open(playbook_path) as f:
                content = yaml.safe_load(f)

            if not isinstance(content, list):
                return []

            required_vars = set()

            for play in content:
                if not isinstance(play, dict):
                    continue

                # Extract vars defined in play
                play_vars = play.get("vars", {})
                if isinstance(play_vars, dict):
                    for var_name, var_value in play_vars.items():
                        # null or unset values are considered required
                        if var_value is None:
                            required_vars.add(var_name)

                # Extract common required variables from plays
                # e.g., hosts: "{{ datacenter_name }}"
                hosts = play.get("hosts", "")
                if isinstance(hosts, str):
                    var_matches = re.findall(r"\{\{\s*(\w+)\s*\}\}", hosts)
                    required_vars.update(var_matches)

            log.msg("playbook_variables_parsed", playbook=playbook_name, variables=list(required_vars))
            return sorted(list(required_vars))

        except Exception as e:
            log.exception("playbook_parse_error", playbook=playbook_name, error=str(e))
            return []

    def prompt_for_variables(self, playbook_name: str, stage: str, provided_vars: Dict[str, str]) -> Dict[str, str]:
        """
        Prompt user for required variables not already provided.

        Args:
            playbook_name: Playbook name
            stage: Execution stage (qa/live)
            provided_vars: Variables already provided via CLI

        Returns:
            Complete dictionary of variables
        """
        required_vars = self.parse_required_variables(playbook_name)
        result_vars = provided_vars.copy()

        # Define common variable defaults and prompts
        var_config = {
            "cluster": {
                "prompt": "Cluster",
                "required": True,
            },
            "stress_profile": {
                "prompt": "Stress profile",
                "default": "profiles/sample-stress.yaml",
                "required": False,
            },
        }

        for var_name in required_vars:
            if var_name in result_vars:
                continue

            config = var_config.get(var_name, {"prompt": var_name, "required": True})
            prompt_text = config["prompt"]
            default = config.get("default", "")
            required = config.get("required", False)

            if default:
                prompt_text += f" [{default}]"

            prompt_text += ": "

            while True:
                user_input = input(prompt_text).strip()

                if not user_input:
                    if default:
                        user_input = default
                    elif required:
                        print(f"  ⚠️  {var_name} is required")
                        continue

                if user_input:
                    result_vars[var_name] = user_input
                    break

        log.msg("variables_collected", playbook=playbook_name, stage=stage, vars_count=len(result_vars))
        return result_vars

    def confirm_live_execution(self) -> bool:
        """
        Prompt user to confirm live environment execution.

        Returns:
            True if user confirms, False otherwise
        """
        print("\n" + "=" * 70)
        print("⚠️  LIVE ENVIRONMENT DETECTED ⚠️")
        print("=" * 70)
        print("This playbook will execute against PRODUCTION infrastructure.")
        print("To proceed, retype exactly:")
        print()
        print(f'    {self.CONFIRMATION_STRING}')
        print()

        user_input = input("Confirmation: ").strip()

        if user_input == self.CONFIRMATION_STRING:
            log.msg("live_execution_confirmed")
            return True

        print("❌ Confirmation mismatch. Execution cancelled.")
        log.warning("live_execution_cancelled")
        return False

    def run_playbook(self, playbook_name: str, stage: str, extra_vars: Dict[str, str]) -> Tuple[int, str, str]:
        """
        Execute Ansible playbook via uv.

        Args:
            playbook_name: Playbook name
            stage: Stage (qa/live)
            extra_vars: Extra variables to pass to ansible

        Returns:
            Tuple of (returncode, stdout, stderr)
        """
        playbook_path = self.playbooks_dir / f"{playbook_name}.yml"

        # Build ansible-playbook command
        cmd = [
            "uv",
            "run",
            "ansible-playbook",
            str(playbook_path),
            "-i",
            str(self.playbooks_dir / "../scripts/fetch_hosts.py"),
            "-e",
            f"@{self.inventories_dir / stage / 'all.yml'}",
        ]

        # Add extra variables
        for key, value in extra_vars.items():
            cmd.extend(["-e", f"{key}={value}"])

        # Prepare environment variables for fetch_hosts.py
        env = os.environ.copy()
        env["STAGE"] = stage
        
        # Extract cluster and brand from extra_vars for fetch_hosts.py
        if "cluster" in extra_vars:
            env["CLUSTER"] = extra_vars["cluster"]
        if "brand" in extra_vars:
            env["BRAND"] = extra_vars["brand"]
        if "datacenter_name" in extra_vars:
            env["DATACENTER"] = extra_vars["datacenter_name"]

        log.msg("playbook_execution_started", playbook=playbook_name, stage=stage, cmd=" ".join(cmd))

        start_time = time.time()

        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.cassandra_root),
                capture_output=True,
                text=True,
                timeout=3600,  # 1 hour timeout
                env=env,
            )

            duration = time.time() - start_time

            log.msg(
                "playbook_execution_completed",
                playbook=playbook_name,
                returncode=result.returncode,
                duration_seconds=duration,
            )

            return result.returncode, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            log.error("playbook_execution_timeout", playbook=playbook_name)
            return 124, "", "Playbook execution timed out after 1 hour"
        except Exception as e:
            log.exception("playbook_execution_error", playbook=playbook_name, error=str(e))
            return 1, "", str(e)

    def format_logback_message(self, level: str, message: str) -> str:
        """Format message according to logback.xml pattern."""
        now = datetime.utcnow().isoformat() + "Z"
        thread_name = "main"
        # Pattern: %date{ISO8601} %-5level [%thread] %msg%n
        return f"{now} {level:<5} [{thread_name}] {message}"

    def export_to_opensearch(
        self,
        playbook_name: str,
        stage: str,
        variables: Dict[str, str],
        returncode: int,
        stdout: str,
        stderr: str,
        duration: float,
    ) -> bool:
        """
        Export execution logs to OpenSearch via OTEL.

        Args:
            playbook_name: Playbook name
            stage: Execution stage
            variables: Variables used
            returncode: Playbook return code
            stdout: Standard output
            stderr: Standard error
            duration: Execution duration in seconds

        Returns:
            True if export successful, False otherwise
        """
        if self.disable_opensearch:
            log.msg("opensearch_export_disabled")
            return True

        try:
            # Build log entry
            log_entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "level": "INFO" if returncode == 0 else "ERROR",
                "playbook": playbook_name,
                "stage": stage,
                "status": "success" if returncode == 0 else "failed",
                "duration_seconds": duration,
                "returncode": returncode,
                "variables": variables,
                "stdout": stdout[-5000:] if stdout else "",  # Limit to 5000 chars
                "stderr": stderr[-5000:] if stderr else "",
            }

            # Format as logback message
            message = self.format_logback_message(log_entry["level"], json.dumps(log_entry))

            # Save locally
            log_file = self.LOG_DIR / f"{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"
            with open(log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")

            # Send to OTEL via HTTP/gRPC (simplified HTTP JSON export)
            # Note: Full OTLP implementation would require protobuf
            with Session() as session:
                session.timeout = 5
                response = session.post(
                    f"{self.otel_endpoint}/v1/logs",
                    json={"logs": [log_entry]},
                    headers={"Content-Type": "application/json"},
                )
                response.raise_for_status()

            log.msg("opensearch_export_successful", playbook=playbook_name)
            return True

        except RequestException as e:
            log.warning("opensearch_export_failed", playbook=playbook_name, error=str(e))
            return False
        except Exception as e:
            log.exception("opensearch_export_error", playbook=playbook_name, error=str(e))
            return False

    def interactive_mode(self) -> int:
        """
        Run in interactive mode with menu.

        Flow:
        1. Select playbook from list
        2. Select cluster from available clusters
        3. Select stage (QA/Live)
        4. Provide required variables
        5. Confirm and execute

        Returns:
            Exit code
        """
        try:
            # Step 1: Select Playbook
            playbooks = self.discover_playbooks()

            if not playbooks:
                print("❌ No playbooks found in", self.playbooks_dir)
                return 1

            print("\n" + "=" * 70)
            print("📚 Available Playbooks:")
            print("=" * 70)
            for idx, name in enumerate(playbooks, 1):
                print(f"  {idx:2d}) {name}")

            while True:
                try:
                    choice = int(input("\nSelect playbook (number): ")) - 1
                    if 0 <= choice < len(playbooks):
                        selected_playbook = playbooks[choice]
                        break
                    print("  ❌ Invalid selection")
                except ValueError:
                    print("  ❌ Please enter a number")

            print(f"\n✅ Selected: {selected_playbook}")

            # Step 2: Select Cluster
            clusters = self.get_fixed_clusters()

            if not clusters:
                print("❌ No clusters found")
                return 1

            print("\n" + "=" * 70)
            print("🖥️  Available Clusters:")
            print("=" * 70)
            for idx, name in enumerate(clusters, 1):
                print(f"  {idx:2d}) {name}")

            while True:
                try:
                    choice = int(input("\nSelect cluster (number): ")) - 1
                    if 0 <= choice < len(clusters):
                        selected_cluster = clusters[choice]
                        break
                    print("  ❌ Invalid selection")
                except ValueError:
                    print("  ❌ Please enter a number")

            print(f"\n✅ Selected: {selected_cluster}")
            extra_vars = {"cluster": selected_cluster}

            # Step 3: Select Stage
            print("\n" + "=" * 70)
            print("⚙️  Stage Selection:")
            print("=" * 70)
            print("  [1] qa (default)")
            print("  [2] live (production)")

            stage_choice = input("\nSelect stage [1]: ").strip() or "1"
            stage = "live" if stage_choice == "2" else "qa"
            print(f"\n✅ Selected: {stage}")

            # Confirm live
            if stage == "live" and not self.confirm_live_execution():
                return 1

            # Step 4: Discover Datacenters and Brands
            print(f"\n🔍 Discovering datacenters and brands for {selected_cluster} ({stage})...")
            datacenters, brands = self.fetch_datacenters_and_brands(selected_cluster, stage)

            if not datacenters:
                print("❌ No datacenters found for this cluster and stage")
                print(f"   Try running manually: python3 scripts/fetch_hosts.py --cluster {selected_cluster} --stage {stage} --list")
                return 1

            # Step 5: Select Datacenter
            print("\n" + "=" * 70)
            print("📍 Available Datacenters:")
            print("=" * 70)
            for idx, dc in enumerate(datacenters, 1):
                print(f"  {idx:2d}) {dc}")

            while True:
                try:
                    choice = int(input("\nSelect datacenter (number): ")) - 1
                    if 0 <= choice < len(datacenters):
                        selected_datacenter = datacenters[choice]
                        break
                    print("  ❌ Invalid selection")
                except ValueError:
                    print("  ❌ Please enter a number")

            print(f"\n✅ Selected: {selected_datacenter}")
            extra_vars["datacenter_name"] = selected_datacenter

            # Step 6: Select Brand (if multiple available)
            selected_brand = "all"
            if brands and len(brands) > 1:
                print("\n" + "=" * 70)
                print("🏷️  Available Brands:")
                print("=" * 70)
                for idx, brand in enumerate(brands, 1):
                    print(f"  {idx:2d}) {brand}")

                default_idx = 1
                while True:
                    try:
                        choice = input(f"\nSelect brand (number) [{default_idx}]: ").strip() or str(default_idx)
                        choice = int(choice) - 1
                        if 0 <= choice < len(brands):
                            selected_brand = brands[choice]
                            break
                        print("  ❌ Invalid selection")
                    except ValueError:
                        print("  ❌ Please enter a number")

                print(f"\n✅ Selected: {selected_brand}")
                extra_vars["brand"] = selected_brand

            # Step 7: Collect additional variables
            print("\n" + "=" * 70)
            print("🔧 Required Variables:")
            print("=" * 70)
            extra_vars = self.prompt_for_variables(selected_playbook, stage, extra_vars)

            # Step 5: Execute
            print("\n" + "=" * 70)
            print(f"▶️  Executing {selected_playbook} ({stage})...")
            print("=" * 70)
            start_time = time.time()
            returncode, stdout, stderr = self.run_playbook(selected_playbook, stage, extra_vars)
            duration = time.time() - start_time

            # Display result
            status = "✅ SUCCESS" if returncode == 0 else "❌ FAILED"
            print(f"\n{status} (duration: {duration:.1f}s)")

            if stdout:
                print("\n📋 Output (last 2000 chars):")
                print("-" * 70)
                print(stdout[-2000:])

            if stderr:
                print("\n⚠️  Errors (last 1000 chars):")
                print("-" * 70)
                print(stderr[-1000:])

            # Export logs
            self.export_to_opensearch(selected_playbook, stage, extra_vars, returncode, stdout, stderr, duration)

            return returncode

        except KeyboardInterrupt:
            print("\n⏹️  Cancelled by user")
            return 130

    def direct_mode(self, playbook_name: str, args: Dict[str, str]) -> int:
        """
        Run in direct mode with CLI arguments.

        Args:
            playbook_name: Playbook name
            args: CLI arguments (stage, variables, etc.)

        Returns:
            Exit code
        """
        stage = args.get("stage", "qa")

        # Confirm live
        if stage == "live" and not self.confirm_live_execution():
            return 1

        # Collect variables
        extra_vars = self.prompt_for_variables(playbook_name, stage, args)

        # Execute
        print(f"\n▶️  Executing {playbook_name} ({stage})...")
        start_time = time.time()
        returncode, stdout, stderr = self.run_playbook(playbook_name, stage, extra_vars)
        duration = time.time() - start_time

        # Display result
        status = "✅ SUCCESS" if returncode == 0 else "❌ FAILED"
        print(f"\n{status} (duration: {duration:.1f}s)")

        if stdout:
            print("\n📋 Output:")
            print(stdout)

        if stderr:
            print("\n⚠️  Errors:")
            print(stderr)

        # Export logs
        self.export_to_opensearch(playbook_name, stage, extra_vars, returncode, stdout, stderr, duration)

        return returncode


def main() -> int:
    """Entry point for CLI."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Run Ansible playbooks with safety checks and OpenSearch logging"
    )
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode (default)")
    parser.add_argument("playbook", nargs="?", help="Playbook name")
    parser.add_argument("--stage", "-s", default="qa", help="Stage: qa or live")
    parser.add_argument("--datacenter", "-d", dest="datacenter_name", help="Datacenter name")
    parser.add_argument("--cluster", "-c", help="Cluster name")
    parser.add_argument("--profile", help="Stress profile or custom variable")
    parser.add_argument("--cassandra-root", help="Cassandra Ansible project root")
    parser.add_argument("--otel-endpoint", help="OTEL collector endpoint")
    parser.add_argument("--disable-opensearch", action="store_true", help="Skip OpenSearch export")

    args = parser.parse_args()

    runner = PlaybookRunner(
        cassandra_root=args.cassandra_root,
        otel_endpoint=args.otel_endpoint,
        disable_opensearch=args.disable_opensearch,
    )

    if not args.playbook or args.interactive:
        return runner.interactive_mode()

    # Direct mode
    extra_vars = {}
    if args.datacenter_name:
        extra_vars["datacenter_name"] = args.datacenter_name
    if args.cluster:
        extra_vars["cluster"] = args.cluster
    if args.profile:
        extra_vars["stress_profile"] = args.profile

    return runner.direct_mode(args.playbook, {"stage": args.stage, **extra_vars})


if __name__ == "__main__":
    sys.exit(main())
