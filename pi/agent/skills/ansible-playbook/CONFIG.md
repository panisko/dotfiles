# Ansible Playbook Runner - Configuration Guide

## Project Structure

```
cassandra-ansible/
├── playbooks/              # Auto-discovered by runner
│   ├── configure_cassandra.yml
│   ├── rolling_restart_dc.yml
│   ├── shutdown_dc.yml
│   ├── status_and_health.yml
│   └── ...
├── inventories/            # Stage-specific inventory & vars
│   ├── qa/
│   │   ├── all.yml
│   │   ├── de_rhr_bap.yml
│   │   └── de_kae_bs.yml
│   └── live/
│       ├── all.yml
│       └── ...
├── roles/                  # Ansible roles
├── scripts/                # Helper scripts
├── ansible.cfg             # Ansible configuration
├── Makefile                # Build targets
└── pyproject.toml          # Python dependencies
```

## OpenSearch & OTEL Setup

### Source Configuration
Configurations are sourced from:
```
aiops_shipit/podman/configs/
├── otel-collector-remote.yaml    # OTEL endpoint & auth
├── logback.xml                   # Log format pattern
└── cassandra.yaml                # Cassandra config
```

### OTEL Collector Configuration

The runner reads from `otel-collector-remote.yaml`:

```yaml
exporters:
  otlp_grpc:
    endpoint: "otel-umo-ha.shared01.dpo.org.mam.dev:4317"
    auth:
      authenticator: basicauth/client
    tls:
      insecure_skip_verify: true
```

**Local defaults:**
- Endpoint: `http://localhost:4317` (can override via `OTEL_EXPORTER_OTLP_ENDPOINT`)
- Port: 4317 (OTLP gRPC)
- Auth: Read from config if OTEL running remotely

### Logback Pattern

Log format from `logback.xml`:
```
%date{ISO8601} %-5level [%thread] %msg%n
```

Produces:
```
2026-05-28T12:34:56Z INFO  [main] Playbook started: rolling_restart_dc
2026-05-28T12:34:58Z ERROR [main] Connection timeout to node cassandra-1
```

The runner formats all exports to match this pattern.

## Environment Variables

### Optional
```bash
# Custom cassandra-ansible root (default: /Users/panisko/projects/cassandra-ansible)
export CASSANDRA_ANSIBLE_ROOT=/custom/path

# Custom OTEL endpoint (default: http://localhost:4317)
export OTEL_EXPORTER_OTLP_ENDPOINT=http://custom-otel:4317

# Disable OpenSearch export (logs still saved locally)
export DISABLE_OPENSEARCH_EXPORT=1

# Enable debug output
export ANSIBLE_DEBUG=1
```

### Auto-Detected
```bash
# Loaded from otel-collector-remote.yaml if available
OTEL_AUTH_ENABLED          # If basicauth configured
OTEL_EXPORTER_USERNAME     # From config
OTEL_EXPORTER_PASSWORD     # From config (⚠️  handle securely)
```

## Python Dependencies

The runner uses `uv` to manage dependencies. Required packages:

```toml
[project]
dependencies = [
    "pyyaml>=6.0",           # Parse Ansible playbooks
    "requests>=2.31.0",      # Export to OTEL
    "structlog>=24.1.0",     # Structured logging
    "python-dotenv>=1.0.0",  # Environment config
]
```

These are automatically installed via `uv sync` when the runner starts.

## Logging

### Local Log Storage

Logs saved to: `~/.ansible_playbook_runner/logs/`

```
~/.ansible_playbook_runner/logs/
├── 2026-05-28.jsonl       # Date-based log file
├── 2026-05-27.jsonl
└── latest.json            # Latest execution
```

Each entry is JSON:
```json
{
  "timestamp": "2026-05-28T12:34:56Z",
  "level": "INFO",
  "playbook": "rolling_restart_dc",
  "stage": "qa",
  "status": "success",
  "duration_seconds": 145.2,
  "returncode": 0,
  "variables": {
    "datacenter_name": "de_rhr_bap",
    "cluster": "piotr-test-cluster"
  },
  "stdout": "...truncated to 5000 chars...",
  "stderr": ""
}
```

### OpenSearch Index

Logs exported to OpenSearch index: `ansible-playbooks-YYYY-MM-DD`

Query recent playbook executions:
```json
GET /ansible-playbooks-2026-05-28/_search
{
  "query": {
    "match": {
      "playbook": "rolling_restart_dc"
    }
  },
  "sort": [{"timestamp": "desc"}]
}
```

## Security Considerations

### Live Environment Confirmation

The runner requires explicit confirmation for live environments:

1. User specifies `--stage live`
2. Runner displays warning banner
3. User must retype exactly: `I confirm deployment to LIVE`
4. Misspelling or abort cancels execution

### Sensitive Variables

Variables containing secrets (passwords, tokens) are:
- ✅ Masked in console output
- ✅ Truncated in log exports (5000 char limit)
- ⚠️  Stored in OpenSearch (treat as sensitive data)
- ⚠️  Saved in local log files with appropriate permissions (mode 0600)

**Recommendation:** Don't pass sensitive data as CLI args. Use Ansible vault or environment variables instead.

### SSH Keys & Ansible Auth

The runner executes under current user context. Ensure:

```bash
# SSH keys configured
ssh-add ~/.ssh/id_rsa

# Or use ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa

# Verify access to inventory hosts
ssh user@first-cassandra-node uptime
```

## Playbook Variable Detection

### Automatic Detection

The runner scans playbooks for required variables in this order:

1. **Vars with null value** (explicitly required):
   ```yaml
   - name: My Play
     vars:
       datacenter_name: null    # ← Detected as required
   ```

2. **Template variables in hosts**:
   ```yaml
   - name: My Play
     hosts: "{{ datacenter_name }}"    # ← Detected from template
   ```

3. **Pre-tasks with assertions**:
   ```yaml
   pre_tasks:
     - assert:
         that:
           - datacenter_name is defined    # ← Indicates required var
   ```

### Common Variables

| Variable | Playbook(s) | Default | Example |
|----------|-------------|---------|---------|
| `datacenter_name` | rolling_restart_dc, shutdown_dc | de_rhr_bap,de_kae_bs | de_rhr_bap |
| `stress_profile` | stress_test | profiles/sample-stress.yaml | profiles/custom.yaml |

## Cluster Discovery

The runner auto-discovers clusters from multiple sources in this order:

1. **`clusters/` directory** (highest priority)
   - Scans for cluster definition files
   - Each file = one cluster
   - Sorted alphabetically
   - Example: `clusters/my-prod-cluster`, `clusters/staging-cluster`

2. **`fetch_hosts.py` script output**
   - Runs `uv run python scripts/fetch_hosts.py --list`
   - Extracts cluster names from JSON inventory
   - Useful for dynamic/external inventories

3. **Fallback defaults** (lowest priority)
   - `piotr-test-cluster` if nothing found
   - Ensures UI always has at least one option

### Adding New Clusters

Simply create a file in `clusters/` directory:
```bash
touch /Users/panisko/projects/cassandra-ansible/clusters/my-new-cluster
```

Next time you run the skill in interactive mode, the new cluster will appear in the cluster selection menu.

### Discovered Clusters in Interactive Mode

After selecting a playbook, you're prompted to select a cluster:
```
🗄️  Available Clusters:
  1) piotr-test-cluster
  2) my-prod-cluster
  3) staging-cluster

Select cluster (number): 1
```

The selected cluster is used as the default value for the `cluster` variable passed to the playbook.

## Troubleshooting

### "Playbooks directory not found"
```bash
# Verify path
ls /Users/panisko/projects/cassandra-ansible/playbooks/

# Or override
export CASSANDRA_ANSIBLE_ROOT=/Users/panisko/projects/cassandra-ansible
```

### "OTEL endpoint unreachable"
```bash
# Verify collector running
netstat -an | grep 4317

# Or test connectivity
curl -X POST http://localhost:4317/v1/logs -H "Content-Type: application/json"

# Disable OTEL export if not available
export DISABLE_OPENSEARCH_EXPORT=1
```

### "Ansible authentication failed"
```bash
# Check SSH connectivity
ssh -v user@cassandra-node-1 uptime

# Verify inventory
uv run ansible-playbook --inventory scripts/fetch_hosts.py --list-hosts

# Check ansible.cfg
cat ansible.cfg
```

### "Variable not detected"
Edit the playbook to explicitly define required vars:

**Before:**
```yaml
- name: My Play
  hosts: "{{ dc_name }}"
  tasks: ...
```

**After:**
```yaml
- name: My Play
  vars:
    dc_name: null          # Now the runner will ask
  hosts: "{{ dc_name }}"
  tasks: ...
```

## Advanced Usage

### Custom OTEL Endpoint (Remote Collector)

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://remote-otel.example.com:4317
/skill:ansible-playbook run rolling-restart --stage qa
```

### Dry Run (Preview Command)

```bash
# The runner shows the exact ansible-playbook command before execution
# Review and confirm before it runs
/skill:ansible-playbook run configure_cassandra --stage qa
```

### Batch Execution

```bash
# Run multiple playbooks sequentially
for playbook in status_and_health nodetool_repair status_and_health; do
  /skill:ansible-playbook run "$playbook" --stage qa --datacenter de_rhr_bap
  sleep 10  # Wait between executions
done
```

### Monitor Logs in Real-Time

```bash
# Follow latest executions
tail -f ~/.ansible_playbook_runner/logs/$(date +%Y-%m-%d).jsonl

# Or query OpenSearch
curl -u admin:password \
  'https://opensearch.example.com/ansible-playbooks-*/_search?sort=timestamp:desc' \
  | jq '.hits.hits[] | .._source'
```

## Performance Tuning

### Ansible Parallelism

Edit `ansible.cfg`:
```ini
[defaults]
forks = 10  # Default: 5
# Increase for large clusters
```

### Connection Timeout

```ini
[defaults]
timeout = 60  # Seconds
# Increase for slow networks
```

### Playbook Timeout

The runner enforces a 1-hour timeout per playbook. Override:

```bash
# Would require code change in ansible_playbook_runner.py
# See: runner.run_playbook() timeout=3600
```

## API Integration

The runner is designed for both CLI and programmatic use:

```python
from ansible_playbook_runner import PlaybookRunner

runner = PlaybookRunner()
playbooks = runner.discover_playbooks()
print(playbooks)

# Execute
code, stdout, stderr = runner.run_playbook(
    "rolling_restart_dc",
    stage="qa",
    extra_vars={"datacenter_name": "de_rhr_bap"}
)

# Export logs
runner.export_to_opensearch(
    "rolling_restart_dc",
    "qa",
    {"datacenter_name": "de_rhr_bap"},
    code,
    stdout,
    stderr,
    duration=145.2
)
```

## Related Documentation

- [Ansible Documentation](https://docs.ansible.com/)
- [Cassandra Ansible README](/Users/panisko/projects/cassandra-ansible/README.md)
- [OpenTelemetry Protocol](https://opentelemetry.io/docs/specs/otlp/)
- [Logback Manual](https://logback.qos.ch/manual/configuration.html)
- [Skill Specification](https://agentskills.io/specification)
