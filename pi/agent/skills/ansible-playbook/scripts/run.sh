#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CASSANDRA_ANSIBLE_ROOT="${CASSANDRA_ANSIBLE_ROOT:-/Users/panisko/projects/cassandra-ansible}"

# Verify cassandra-ansible project exists
if [ ! -d "$CASSANDRA_ANSIBLE_ROOT" ]; then
    echo "❌ Error: Cassandra Ansible project not found at:"
    echo "   $CASSANDRA_ANSIBLE_ROOT"
    echo
    echo "Set CASSANDRA_ANSIBLE_ROOT to override:"
    echo "   export CASSANDRA_ANSIBLE_ROOT=/path/to/cassandra-ansible"
    exit 1
fi

if [ ! -f "$CASSANDRA_ANSIBLE_ROOT/pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found at:"
    echo "   $CASSANDRA_ANSIBLE_ROOT/pyproject.toml"
    exit 1
fi

# Install/sync skill dependencies (in skill directory)
echo "📦 Installing skill dependencies..."
cd "$SKILL_DIR" || exit 1
uv sync --quiet 2>/dev/null || {
    echo "Installing skill dependencies..."
    uv sync
}

# Install/sync cassandra-ansible dependencies
echo "📦 Installing ansible dependencies..."
cd "$CASSANDRA_ANSIBLE_ROOT" || exit 1
uv sync --quiet 2>/dev/null || {
    echo "Installing ansible dependencies..."
    uv sync
}

# Export environment variables for the Python module
export CASSANDRA_ANSIBLE_ROOT="$CASSANDRA_ANSIBLE_ROOT"
export OTEL_EXPORTER_OTLP_ENDPOINT="${OTEL_EXPORTER_OTLP_ENDPOINT:-http://localhost:4317}"
export DISABLE_OPENSEARCH_EXPORT="${DISABLE_OPENSEARCH_EXPORT:-0}"
export ANSIBLE_DEBUG="${ANSIBLE_DEBUG:-0}"

# Run Python module via uv (from skill directory where pyproject.toml is)
echo "▶️  Starting playbook runner..."
echo

cd "$SKILL_DIR" || exit 1
uv run python ansible_playbook_runner.py "$@"
