# Ansible Playbook Pi Skill

A comprehensive Pi skill for discovering, validating, and executing Ansible playbooks with production safety checks and structured logging to OpenSearch.

## Features

🔒 **Safety First**
- QA environment by default
- Explicit live confirmation with retype requirement
- Automatic variable detection and validation
- Dry-run preview before execution

🚀 **Easy to Use**
- Interactive menu: playbook → cluster → stage → variables
- Direct CLI mode for automation
- Automatic playbook discovery from `playbooks/` directory
- Automatic cluster discovery from multiple sources
- Smart variable detection from YAML
- Intelligent prompting for required variables

📊 **Full Observability**
- Structured logs in JSON format
- Logback.xml-compliant formatting
- OpenSearch export via OTEL
- Local log retention for offline access

## Quick Start

### Interactive Mode (Recommended)
```bash
/skill:ansible-playbook
```

### Direct Mode
```bash
/skill:ansible-playbook run rolling-restart --stage live --datacenter de_rhr_bap
```

## Installation

Already installed at: `~/.pi/agent/skills/ansible-playbook/`

Verify:
```bash
ls ~/.pi/agent/skills/ansible-playbook/
```

First-time setup:
```bash
# Ensure cassandra-ansible project exists
test -d /Users/panisko/projects/cassandra-ansible || echo "Project missing"

# Install dependencies
cd /Users/panisko/projects/cassandra-ansible && uv sync

# Run skill
/skill:ansible-playbook
```

## Documentation

| Document | Purpose |
|----------|---------|
| **SKILL.md** | Main skill documentation & overview |
| **CONFIG.md** | Configuration, environment vars, OTEL setup |
| **EXAMPLES.md** | Usage examples & troubleshooting |
| **SETUP.md** | Installation & development guide |
| **README.md** | This file |

## Key Capabilities

### Playbook Discovery
Automatically finds all `.yml` files in `playbooks/` directory:
```bash
configure_cassandra
rolling_restart_dc
shutdown_dc
status_and_health
stress_test
add_node
decommission_node
nodetool_repair
... (and more)
```

### Cluster Discovery
Automatically finds all available clusters from:
- `clusters/` directory (cluster definitions)
- `fetch_hosts.py` inventory output
- Sensible defaults

### Variable Detection
Intelligently detects required variables:
```yaml
vars:
  datacenter_name: null        # ← Detected as required
  cluster: piotr-test-cluster  # ← Optional (has value)
```

### Live Environment Safety
```
⚠️  LIVE ENVIRONMENT DETECTED ⚠️
To proceed, retype exactly: I confirm deployment to LIVE
```

### Structured Logging
```json
{
  "timestamp": "2026-05-28T12:34:56Z",
  "level": "INFO",
  "playbook": "rolling_restart_dc",
  "stage": "qa",
  "status": "success",
  "duration_seconds": 145.2,
  "returncode": 0,
  "variables": {"datacenter_name": "de_rhr_bap"},
  "stdout": "...",
  "stderr": ""
}
```

## Architecture

```
ansible_playbook_runner.py          # Core module (1800 lines)
├── PlaybookRunner class
│   ├── discover_playbooks()         # Find all .yml files
│   ├── parse_required_variables()   # Extract vars from YAML
│   ├── prompt_for_variables()       # Interactive prompts
│   ├── confirm_live_execution()     # Safety gate
│   ├── run_playbook()               # Execute via uv run
│   ├── format_logback_message()     # Format logs
│   ├── export_to_opensearch()       # Send to OTEL
│   ├── interactive_mode()           # Menu-driven UI
│   └── direct_mode()                # CLI arguments

scripts/run.sh                      # Main entry point
scripts/run-interactive.sh          # Interactive menu

tests/test_ansible_playbook_runner.py  # 300+ lines of tests
├── TestPlaybookDiscovery
├── TestVariableParsing
├── TestLiveConfirmation
├── TestLogFormatting
├── TestOpenSearchExport
└── ... (9 test classes total)
```

## Dependencies

- **pyyaml** — Parse Ansible playbooks
- **requests** — Export logs to OTEL
- **structlog** — Structured logging
- **python-dotenv** — Environment configuration
- **pytest** — Testing framework

All installed via `uv add` in cassandra-ansible project.

## Configuration

### Environment Variables

```bash
# Optional overrides
export CASSANDRA_ANSIBLE_ROOT=/custom/cassandra-ansible
export OTEL_EXPORTER_OTLP_ENDPOINT=http://custom-otel:4317
export DISABLE_OPENSEARCH_EXPORT=1
export ANSIBLE_DEBUG=1
```

### Logging Output

Logs saved to: `~/.ansible_playbook_runner/logs/`

Query via:
```bash
tail -f ~/.ansible_playbook_runner/logs/$(date +%Y-%m-%d).jsonl
```

## Examples

### Status Check (QA)
```bash
/skill:ansible-playbook run status_and_health
```

### Rolling Restart (Production)
```bash
/skill:ansible-playbook run rolling-restart --stage live --datacenter de_rhr_bap
```

### Stress Test
```bash
/skill:ansible-playbook run stress_test --datacenter de_rhr_bap --profile profiles/custom.yaml
```

See [EXAMPLES.md](EXAMPLES.md) for 20+ example scenarios and troubleshooting.

## Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=ansible_playbook_runner --cov-report=html

# Specific test
pytest tests/test_ansible_playbook_runner.py::TestPlaybookExecution -v
```

Test coverage includes:
- ✅ Playbook discovery (files, sorting, error cases)
- ✅ Variable parsing (required vars, templates, assertions)
- ✅ Interactive mode (menu flow, user input, selection)
- ✅ Direct mode (CLI args, variable override)
- ✅ Live confirmation (correct phrase, typos, cancellation)
- ✅ Log formatting (ISO8601, levels, threading)
- ✅ OpenSearch export (local save, OTEL HTTP, error handling)
- ✅ Playbook execution (success, failure, timeout, system errors)

## Security

✅ **Input Validation**
- Playbook names validated against discovered files
- Variables validated before interpolation
- Live confirmation requires exact phrase

✅ **Secrets Handling**
- No hardcoded credentials
- Sensitive vars masked from console
- Truncated in log exports (5000 chars)
- SSH keys via ssh-agent

✅ **Error Handling**
- Graceful timeouts (1 hour)
- Comprehensive exception handling
- Detailed error logs for debugging

## Project Structure

```
~/.pi/agent/skills/ansible-playbook/
├── SKILL.md                           # Main documentation (6.8 KB)
├── CONFIG.md                          # Configuration guide (9 KB)
├── EXAMPLES.md                        # Usage examples (10 KB)
├── SETUP.md                           # Installation (7.8 KB)
├── README.md                          # This file
├── pyproject.toml                     # Python dependencies
├── ansible_playbook_runner.py         # Core module (18 KB)
├── scripts/
│   ├── run.sh                         # Main entry point (1.2 KB)
│   └── run-interactive.sh             # Interactive menu (2 KB)
└── tests/
    └── test_ansible_playbook_runner.py # 300 lines of tests
```

## Troubleshooting

### Common Issues

**"Playbooks directory not found"**
```bash
export CASSANDRA_ANSIBLE_ROOT=/Users/panisko/projects/cassandra-ansible
```

**"OTEL endpoint unreachable"**
```bash
export DISABLE_OPENSEARCH_EXPORT=1  # Use local logging only
```

**"Ansible authentication failed"**
```bash
ssh-add ~/.ssh/id_rsa  # Add SSH key to agent
```

See [EXAMPLES.md#Troubleshooting](EXAMPLES.md#troubleshooting) for 10+ solutions.

## Roadmap

Future enhancements:
- [ ] Playbook syntax validation (ansible-lint integration)
- [ ] Execution history browser
- [ ] Batch playbook scheduling
- [ ] Slack/Teams notifications
- [ ] Webhook support for CI/CD
- [ ] Metrics export to Prometheus
- [ ] Multi-cluster support

## License

MIT

## Support

- **Docs:** See linked markdown files in this directory
- **Issues:** Check logs at `~/.ansible_playbook_runner/logs/`
- **Skill Standard:** https://agentskills.io/specification

---

**Created:** 2026-05-28  
**Version:** 1.0.0  
**Status:** Production-ready
