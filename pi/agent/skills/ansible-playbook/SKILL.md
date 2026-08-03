---
name: ansible-playbook
description: Run Ansible playbooks against Cassandra clusters with built-in safety checks for live environments, automatic variable detection, interactive prompts, and OpenSearch logging via OTEL. Uses fixed cluster list and dynamic datacenter discovery via fetch-hosts.
---

# Ansible Playbook Runner

Execute Ansible playbooks with safety guardrails, intelligent variable detection, and structured logging to OpenSearch.

## Quick Start

### Interactive Mode (Recommended)
```bash
/skill:ansible-playbook
```
This starts an interactive menu with the following flow:
1. **Select playbook** from auto-discovered list
2. **Select cluster** from fixed list
3. **Select stage** (QA is default, LIVE requires confirmation)
4. **Select datacenter** (auto-discovered from selected cluster & stage)
5. **Select brand** (optional, auto-discovered)
6. **Provide required variables** (custom vars, etc.)
7. **Review and execute**

### Direct Execution
```bash
/skill:ansible-playbook run rolling-restart --stage live --datacenter de_rhr_bap
```

## Features

### 🔒 Safety Checks
- **QA by default**: Uses `qa` stage unless explicitly specified
- **Live confirmation**: For production environments, displays a confirmation prompt requiring manual retype
- **Variable validation**: Detects required variables from playbooks and prompts for them
- **Dry-run preview**: Shows the exact command before execution

### 🖥️ Cluster Selection
Uses a fixed list of available clusters:
- `piotr-test-cluster` — Default QA test cluster
- `laser-cas` — Laser Cassandra cluster
- `laser-cassandra` — Laser Cassandra (alias)

Shows all clusters in interactive menu for easy selection.

### 📍 Dynamic Datacenter Discovery
Uses `scripts/fetch-hosts` to dynamically discover:
- Available datacenters for the selected cluster and stage
- Available brands for the cluster
- Actual hosts and their cassandra datacenter assignments

### 🎯 Intelligent Variable Detection
Automatically detects playbook variables:
- Retrieves available datacenters from `fetch-hosts` based on selected cluster and stage
- Retrieves available brands from `fetch-hosts`
- Custom vars defined in playbooks → prompts user
- Pre-populates datacenter from inventory discovery

### 📊 Logging & Telemetry
- Captures playbook output (stdout, stderr, returncode)
- Records execution metadata (duration, variables, status)
- Exports to OpenSearch via OTEL collector
- Logback.xml format: `ISO8601 LEVEL [thread] message`

### 🔍 Playbook Discovery
Automatically discovers all `.yml` files in the `playbooks/` directory.

## Prerequisites

1. **Python 3.9+** with uv package manager
2. **Ansible** (via uv in project)
3. **OTEL Collector** running (optional; logging works without it)
   - Expected at: `http://localhost:4317` (OTLP gRPC)
4. **ssh-agent** or configured SSH keys for Ansible authentication
5. **Inventory service** accessible for `fetch-hosts` to discover datacenters
   - Default: `https://pocu-reporting.server.lan/minventory/facts`

## Configuration

### Cassandra Ansible Project
The skill operates within `/Users/panisko/projects/cassandra-ansible/`:
```
playbooks/         # Auto-discovered
inventories/       # Stage-specific inventory
scripts/
  fetch-hosts   # Dynamic inventory script
ansible.cfg        # Ansible configuration
Makefile           # Defines run commands
```

### OpenSearch & OTEL
Config sourced from `/Users/panisko/projects/aiops_shipit/podman/configs/`:
- `otel-collector-remote.yaml` — OTEL endpoint and auth
- `logback.xml` — Log format pattern

The skill auto-configures based on these files.

## Usage Examples

### Example 1: Interactive Playbook Selection
```bash
/skill:ansible-playbook

# → Presents menu:
#   📚 Available Playbooks:
#   1) configure_cassandra
#   2) rolling_restart_dc
#   3) shutdown_dc
#   4) status_and_health
#   ...
#   Select playbook (number): 2
#
#   🖥️  Available Clusters:
#   1) piotr-test-cluster
#   2) laser-cas
#   3) laser-cassandra
#   Select cluster (number): 2
#
#   ⚙️  Stage Selection:
#   1) qa (default)
#   2) live (production)
#   Select stage [1]: 2
#
#   ⚠️  LIVE ENVIRONMENT DETECTED
#   This will modify a production cluster.
#   To proceed, retype exactly: I confirm deployment to LIVE
#   > I confirm deployment to LIVE
#
#   🔍 Discovering datacenters for laser-cas (live)...
#   📍 Available Datacenters:
#   1) de_kae_bs
#   2) de_rhr_bap
#   Select datacenter (number): 1
#
#   🏷️  Available Brands:
#   1) all
#   Select brand (number) [1]: 1
#
#   → Executing rolling-restart playbook...
```

### Example 2: Direct Command
```bash
/skill:ansible-playbook run rolling-restart --stage live --datacenter de_rhr_bap
```

### Example 3: QA Execution (Default)
```bash
/skill:ansible-playbook run status_and_health
# Automatically uses stage=qa
```

### Example 4: With Extra Variables
```bash
/skill:ansible-playbook run stress_test --datacenter de_rhr_bap --profile profiles/custom.yaml
```

## Supported Clusters

The skill uses a fixed list of clusters:
- `piotr-test-cluster` — Default QA test cluster
- `laser-cas` — Laser Cassandra cluster
- `laser-cassandra` — Laser Cassandra cluster (alias)

## Supported Playbooks

The skill auto-discovers playbooks. Common ones include:
- `configure_cassandra` — Install and configure Cassandra
- `rolling_restart_dc` — Rolling restart within a datacenter
- `shutdown_dc` — Gracefully shutdown datacenter
- `status_and_health` — Check cluster status
- `stress_test` — Run stress tests
- `add_node` — Add node to cluster
- `decommission_node` — Gracefully remove node
- `nodetool_repair` — Execute nodetool repair

## Log Output

Playbook logs are exported to OpenSearch with structure:
```json
{
  "timestamp": "2026-05-28T12:34:56Z",
  "level": "INFO",
  "playbook": "rolling_restart_dc",
  "stage": "qa",
  "datacenter": "de_rhr_bap",
  "status": "success|failed",
  "duration_seconds": 145.2,
  "variables": {"datacenter_name": "de_rhr_bap", ...},
  "stdout": "...",
  "stderr": "...",
  "returncode": 0
}
```

Logs appear in OpenSearch index: `ansible-playbooks-YYYY-MM-DD`

View logs locally in `~/.ansible_playbook_runner/logs/`:
```bash
ls ~/.ansible_playbook_runner/logs/
tail -f ~/.ansible_playbook_runner/logs/latest.json
```

## Environment Variables

Override defaults:
```bash
# Use different Cassandra Ansible project
CASSANDRA_ANSIBLE_ROOT=/custom/path /skill:ansible-playbook

# Use different OTEL endpoint
OTEL_EXPORTER_OTLP_ENDPOINT=http://custom-otel:4317 /skill:ansible-playbook

# Disable OpenSearch export (local logging only)
DISABLE_OPENSEARCH_EXPORT=1 /skill:ansible-playbook

# Verbose output
ANSIBLE_DEBUG=1 /skill:ansible-playbook

# Override fetch-hosts URL (if different from default)
fetch-hosts_URL=https://custom-inventory.lan/api/facts /skill:ansible-playbook
```

## Troubleshooting

### "Cannot find playbooks directory"
Verify `/Users/panisko/projects/cassandra-ansible/playbooks/` exists and contains `.yml` files.

### "OTEL collector unreachable"
- Verify OTEL collector running: `telnet localhost 4317`
- Check OpenSearch credentials in `otel-collector-remote.yaml`
- Logs still saved locally in `~/.ansible_playbook_runner/logs/`

### "Ansible authentication failed"
Ensure SSH keys configured:
```bash
ssh-add ~/.ssh/id_rsa
ssh-agent bash
```

### "Variable not detected"
Edit playbook to define vars in `vars:` block at play level:
```yaml
- name: My Play
  vars:
    required_var: null
```

### "No datacenters found for cluster"
- Verify `fetch-hosts` can reach the inventory service
- Check cluster name is correct (use one of the fixed clusters)
- Verify stage (qa or live) is correct
- Run manually to debug:
  ```bash
  cd /Users/panisko/projects/cassandra-ansible
  python3 scripts/fetch-hosts --cluster laser-cas --stage qa --list
  ```

## Implementation Details

### Scripts

| Script | Purpose |
|--------|---------|
| `run.sh` | Main entry point; dispatches to interactive or direct modes |
| `ansible_playbook_runner.py` | Core Python module |

### Architecture

1. **Playbook Discovery** — Scan `playbooks/` for `.yml` files
2. **Cluster Selection** — Present fixed list of clusters
3. **Stage Selection** — Choose qa (default) or live
4. **Datacenter Discovery** — Call `fetch-hosts --list` to discover available datacenters and brands
5. **User Selection** — Prompt for datacenter and brand
6. **Variable Detection** — Parse YAML to find required variables
7. **User Input** — Prompt for missing variables and confirmation
8. **Pre-flight Checks** — Validate stage, enforce LIVE confirmation
9. **Execution** — Run `uv run ansible-playbook` with captured output, using fetch-hosts as dynamic inventory
10. **Post-processing** — Format logs per logback.xml pattern
11. **Export** — Send to OpenSearch via OTEL (async, non-blocking)

### Python Dependencies

- `pyyaml` — Parse playbooks
- `requests` — HTTP requests for OTEL export and fetch-hosts interaction
- `python-dotenv` — Environment config
- `structlog` — Structured logging

All installed via `uv add` in the project.

## References

- [Ansible Documentation](https://docs.ansible.com/)
- [Cassandra Ansible README](file:///Users/panisko/projects/cassandra-ansible/README.md)
- [OpenTelemetry Protocol](https://opentelemetry.io/docs/specs/otlp/)
- [Logback Configuration](https://logback.qos.ch/manual/configuration.html)
