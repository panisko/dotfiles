#!/bin/bash

# Interactive menu for selecting and running playbooks
# This script provides a terminal UI for the ansible-playbook runner

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CASS_ROOT="${CASSANDRA_ANSIBLE_ROOT:-/Users/panisko/projects/cassandra-ansible}"

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_header() {
    clear
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║         Ansible Playbook Runner - Interactive Menu             ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo
}

show_help() {
    cat <<EOF
${BLUE}Ansible Playbook Runner${NC}

${GREEN}Usage:${NC}
  Interactive:  ./run-interactive.sh
  Direct:       ./run.sh <playbook-name> [--stage live|qa] [--datacenter NAME]

${GREEN}Examples:${NC}
  # Interactive menu
  ./run-interactive.sh

  # Direct execution
  ./run.sh rolling-restart --stage qa --datacenter de_rhr_bap

  # Live execution (requires confirmation)
  ./run.sh shutdown_dc --stage live --datacenter de_kae_bs

${GREEN}Available Options:${NC}
  --stage STAGE              qa (default) or live
  --datacenter DATACENTER    Datacenter name
  --cluster CLUSTER          Cluster name
  --profile PATH             Stress profile or custom variable
  --disable-opensearch       Skip OpenSearch export
  --otel-endpoint URL        Custom OTEL endpoint

${YELLOW}⚠️  Safety Checks:${NC}
  • QA is default - explicit --stage live required for production
  • Live stage requires manual confirmation
  • Logs exported to OpenSearch (can be disabled)

EOF
}

check_cassandra_root() {
    if [ ! -d "$CASS_ROOT" ]; then
        echo -e "${RED}❌ Error: Cassandra Ansible project not found at:${NC}"
        echo "   $CASS_ROOT"
        echo
        echo -e "${YELLOW}Set CASSANDRA_ANSIBLE_ROOT to override:${NC}"
        echo "   export CASSANDRA_ANSIBLE_ROOT=/path/to/cassandra-ansible"
        return 1
    fi

    if [ ! -f "$CASS_ROOT/pyproject.toml" ]; then
        echo -e "${RED}❌ Error: pyproject.toml not found at:${NC}"
        echo "   $CASS_ROOT/pyproject.toml"
        return 1
    fi
}

ensure_skill_dependencies() {
    echo -e "${GREEN}Installing skill dependencies...${NC}"
    cd "$SKILL_DIR" || exit 1
    uv sync --quiet 2>/dev/null || {
        echo -e "${YELLOW}Syncing skill dependencies...${NC}"
        uv sync
    }
}

ensure_cassandra_dependencies() {
    echo -e "${GREEN}Installing ansible dependencies...${NC}"
    cd "$CASS_ROOT" || exit 1
    uv sync --quiet 2>/dev/null || {
        echo -e "${YELLOW}Syncing cassandra-ansible dependencies...${NC}"
        uv sync
    }
}

main() {
    show_header
    
    if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
        show_help
        return 0
    fi

    # Verify cassandra-ansible project exists
    check_cassandra_root || return 1

    # Ensure all dependencies installed
    ensure_skill_dependencies
    ensure_cassandra_dependencies

    echo -e "${GREEN}Starting interactive playbook runner...${NC}"
    echo

    # Export environment for Python module
    export CASSANDRA_ANSIBLE_ROOT="$CASS_ROOT"
    export OTEL_EXPORTER_OTLP_ENDPOINT="${OTEL_EXPORTER_OTLP_ENDPOINT:-http://localhost:4317}"
    export DISABLE_OPENSEARCH_EXPORT="${DISABLE_OPENSEARCH_EXPORT:-0}"
    export ANSIBLE_DEBUG="${ANSIBLE_DEBUG:-0}"

    # Run the Python module in interactive mode via uv (from skill directory)
    cd "$SKILL_DIR" || exit 1
    uv run python ansible_playbook_runner.py --interactive "$@"
}

main "$@"
