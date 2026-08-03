#!/usr/bin/env python3
"""
Helm SPIFFE Manager Tool

Manages SPIFFE identity configuration in helm-values/common.yml
Supports adding, updating, and removing spiffe-id-to-authorities rules.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SpiffeRule:
    """Represents a single SPIFFE rule."""
    spiffe_id: str
    roles: List[str]
    is_conditional: bool = False
    condition: Optional[str] = None
    comment: Optional[str] = None


class SpiffeConfigManager:
    """Manages SPIFFE configuration in helm-values/common.yml"""

    # Known brand mappings
    BRAND_MAPS = {
        "poma": {
            "gmx": "gmxnet",
            "mcom": "mailcom",
            "gcom": "gmxint",
            "uli": "netid",
            "acc": "1and1",
        },
        "securetoken": {
            "acc": "1and1access",
        },
    }

    KNOWN_BRANDS = ["acc", "gmx", "gcom", "mcom", "uli", "webde"]
    KNOWN_STAGES = ["qa", "live", "dev", "prelive"]
    KNOWN_ROLES = [
        "ROLE_POST_JWT",
        "ROLE_POST_DECODE_JWT",
        "ROLE_POST_INTROSPECT",
        "ROLE_POST_INTROSPECT_V1",
        "ROLE_POST_INTROSPECT_V2",
        "ROLE_POST_TOKEN_CREATE",
        "ROLE_POST_TOKEN_REVOCATION",
        "ROLE_POST_OAUTH2_TOKEN",
        "ROLE_POST_NO_ID_AUTH_LEGACY",
        "ROLE_POST_NO_ID_AUTH_GUID_AND_UAS_ACCOUNT_ID",
        "ROLE_POST_NO_ID_AUTH_CCGUID",
        "ROLE_ANONYMOUS",
    ]

    def __init__(self, config_path: Path = None):
        """Initialize manager with path to common.yml"""
        if config_path is None:
            config_path = Path.cwd() / "helm-values" / "common.yml"
        self.config_path = config_path
        self.original_content = None
        self.load_config()

    def load_config(self) -> str:
        """Load the current configuration file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, "r") as f:
            self.original_content = f.read()
        return self.original_content

    def extract_spiffe_section(self) -> str:
        """Extract the spiffe-id-to-authorities section."""
        if "spiffe-id-to-authorities:" not in self.original_content:
            return None

        # Find the section start
        start = self.original_content.find("spiffe-id-to-authorities:")
        # Find where the next top-level key starts
        remainder = self.original_content[start:]
        lines = remainder.split("\n")
        
        section_lines = [lines[0]]  # Start with the key
        base_indent = None
        
        for i, line in enumerate(lines[1:], 1):
            if not line.strip():
                section_lines.append(line)
                continue
            
            # Check indentation
            if base_indent is None and line.strip():
                base_indent = len(line) - len(line.lstrip())
            
            # If we hit a line with same or less indentation than base, we're done
            current_indent = len(line) - len(line.lstrip())
            if line.strip() and current_indent <= base_indent - 2:
                break
            
            section_lines.append(line)
        
        return "\n".join(section_lines)

    def parse_spiffe_rules(self, section: str) -> List[SpiffeRule]:
        """Parse SPIFFE rules from the section."""
        rules = []
        lines = section.split("\n")
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Look for spiffe patterns: "[spiffe://..."
            if '"[spiffe://' in line:
                # Extract spiffe ID
                match = re.search(r'"(\[spiffe://[^\]]+\])":', line)
                if match:
                    spiffe_id = match.group(1)
                    roles = []
                    
                    # Parse roles (should be indented list below)
                    i += 1
                    while i < len(lines):
                        role_line = lines[i]
                        if role_line.strip().startswith("- ROLE_"):
                            role = role_line.strip()[2:]  # Remove "- "
                            roles.append(role)
                            i += 1
                        elif role_line.strip() and not role_line.strip().startswith("#"):
                            break
                        else:
                            i += 1
                    
                    if roles:
                        rules.append(SpiffeRule(spiffe_id=spiffe_id, roles=roles))
                    continue
            
            i += 1
        
        return rules

    def validate_spiffe_id(self, spiffe_id: str) -> Tuple[bool, Optional[str]]:
        """Validate SPIFFE ID format."""
        # Remove brackets if present
        test_id = spiffe_id.replace("[", "").replace("]", "")
        
        # Check if it's a valid spiffe URI or template
        if not test_id.startswith("spiffe://"):
            return False, "Must start with spiffe://"
        
        # Allow template variables
        if "{{" in test_id or "{{-" in test_id:
            # Basic template validation
            if not re.search(r'{{\s*\.Env\.\w+', test_id):
                return False, "Invalid template syntax"
        
        return True, None

    def validate_roles(self, roles: List[str]) -> Tuple[bool, Optional[str]]:
        """Validate role names."""
        for role in roles:
            if role not in self.KNOWN_ROLES:
                return False, f"Unknown role: {role}"
        return True, None

    def generate_spiffe_rule_yaml(
        self,
        spiffe_id: str,
        roles: List[str],
        condition: Optional[str] = None,
        indent: int = 14,
    ) -> str:
        """Generate YAML for a SPIFFE rule."""
        indent_str = " " * indent
        base_indent = " " * (indent - 2)
        
        # Format the spiffe ID with brackets
        if not spiffe_id.startswith("["):
            spiffe_id = f"[{spiffe_id}]"
        if not spiffe_id.endswith("]"):
            spiffe_id = spiffe_id.rstrip("]") + "]"
        
        yaml_lines = []
        
        if condition:
            yaml_lines.append(f"{base_indent}{{{{- {condition} }}}}")
        
        yaml_lines.append(f'{indent_str}"{spiffe_id}":')
        for role in roles:
            yaml_lines.append(f"{indent_str}  - {role}")
        
        if condition:
            yaml_lines.append(f"{base_indent}{{{{- end }}}}")
        
        return "\n".join(yaml_lines)

    def suggest_placement(self, description: str) -> Dict[str, Any]:
        """Suggest where to place a new rule based on description."""
        suggestion = {
            "namespace_pattern": None,
            "service_name": None,
            "brands": None,
            "stages": None,
            "is_conditional": False,
            "condition_type": None,  # "brand", "stage", "both", "none"
        }
        
        # Extract namespace hints
        namespace_patterns = [
            "poma-sid2", "poumo-oauth2", "poumo-ums", "poumo-passport",
            "pocam-", "poma-webmailer", "dpo-tracking", "bso-",
            "poumo-password-change", "poumo-account-recovery",
        ]
        for pattern in namespace_patterns:
            if pattern.lower() in description.lower():
                suggestion["namespace_pattern"] = pattern
                break
        
        # Check for brand mentions
        for brand in self.KNOWN_BRANDS:
            if f" {brand} " in f" {description.lower()} ":
                if suggestion["brands"] is None:
                    suggestion["brands"] = []
                suggestion["brands"].append(brand)
        
        # Check for stage mentions
        for stage in self.KNOWN_STAGES:
            if f" {stage} " in f" {description.lower()} ":
                if suggestion["stages"] is None:
                    suggestion["stages"] = []
                suggestion["stages"].append(stage)
        
        # Determine if conditional
        if suggestion["brands"] and len(suggestion["brands"]) < len(self.KNOWN_BRANDS):
            suggestion["is_conditional"] = True
            suggestion["condition_type"] = "brand"
        
        if suggestion["stages"]:
            if suggestion["condition_type"] == "brand":
                suggestion["condition_type"] = "both"
            else:
                suggestion["condition_type"] = "stage"
            suggestion["is_conditional"] = True
        
        # Extract service name
        words = description.lower().split()
        for i, word in enumerate(words):
            if word in ["service", "gateway", "facade", "middleware"]:
                if i > 0:
                    suggestion["service_name"] = words[i - 1]
                break
        
        return suggestion

    def diff_sections(self, original: str, modified: str) -> str:
        """Generate a diff between original and modified sections."""
        orig_lines = original.split("\n")
        mod_lines = modified.split("\n")
        
        diff_lines = []
        i, j = 0, 0
        
        while i < len(orig_lines) or j < len(mod_lines):
            if i >= len(orig_lines):
                diff_lines.append(f"+ {mod_lines[j]}")
                j += 1
            elif j >= len(mod_lines):
                diff_lines.append(f"- {orig_lines[i]}")
                i += 1
            elif orig_lines[i] == mod_lines[j]:
                diff_lines.append(f"  {orig_lines[i]}")
                i += 1
                j += 1
            else:
                # Try to find next matching line
                found = False
                for k in range(i + 1, min(i + 5, len(orig_lines))):
                    if orig_lines[k] == mod_lines[j]:
                        for m in range(i, k):
                            diff_lines.append(f"- {orig_lines[m]}")
                        i = k
                        found = True
                        break
                
                if not found:
                    diff_lines.append(f"- {orig_lines[i]}")
                    diff_lines.append(f"+ {mod_lines[j]}")
                    i += 1
                    j += 1
        
        return "\n".join(diff_lines)

    def to_json_diff(self, original: str, modified: str) -> str:
        """Return diff as JSON for programmatic parsing."""
        orig_lines = original.split("\n")
        mod_lines = modified.split("\n")
        
        changes = {
            "added": [],
            "removed": [],
            "modified": [],
            "total_lines_added": 0,
            "total_lines_removed": 0,
        }
        
        # Simple diff - count spiffe rules
        for line in mod_lines:
            if '"[spiffe://' in line and '"[spiffe://' not in original:
                changes["added"].append(line.strip())
                changes["total_lines_added"] += 1
        
        for line in orig_lines:
            if '"[spiffe://' in line and '"[spiffe://' not in modified:
                changes["removed"].append(line.strip())
                changes["total_lines_removed"] += 1
        
        return json.dumps(changes, indent=2)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: helm-spiffe-manager.py <command> [args...]")
        print("Commands:")
        print("  validate <spiffe-id> <roles...>  - Validate a SPIFFE rule")
        print("  parse                            - Parse and display current rules")
        print("  suggest <description>            - Suggest placement for new rule")
        sys.exit(1)
    
    command = sys.argv[1]
    manager = SpiffeConfigManager()
    
    if command == "validate":
        if len(sys.argv) < 4:
            print("Error: validate requires spiffe-id and roles")
            sys.exit(1)
        
        spiffe_id = sys.argv[2]
        roles = sys.argv[3:]
        
        valid_id, msg = manager.validate_spiffe_id(spiffe_id)
        if not valid_id:
            print(json.dumps({"valid": False, "error": msg}))
            sys.exit(1)
        
        valid_roles, msg = manager.validate_roles(roles)
        if not valid_roles:
            print(json.dumps({"valid": False, "error": msg}))
            sys.exit(1)
        
        print(json.dumps({"valid": True}))
    
    elif command == "parse":
        section = manager.extract_spiffe_section()
        if section:
            rules = manager.parse_spiffe_rules(section)
            print(json.dumps({
                "count": len(rules),
                "rules": [
                    {"spiffe_id": r.spiffe_id, "roles": r.roles}
                    for r in rules
                ]
            }, indent=2))
        else:
            print(json.dumps({"count": 0, "rules": []}))
    
    elif command == "suggest":
        if len(sys.argv) < 3:
            print("Error: suggest requires description")
            sys.exit(1)
        
        description = " ".join(sys.argv[2:])
        suggestion = manager.suggest_placement(description)
        print(json.dumps(suggestion, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
