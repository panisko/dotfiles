# Setup & Installation Guide

## Installation

The skill is auto-discovered by Pi from `~/.pi/agent/skills/ansible-playbook/`.

### Verification

```bash
# Verify skill installation
ls -la ~/.pi/agent/skills/ansible-playbook/

# Output should include:
# -rw-r--r--  SKILL.md                          # Main skill file
# -rwxr-xr-x  scripts/run.sh                     # Executable scripts
# -rwxr-xr-x  scripts/run-interactive.sh
# -rw-r--r--  ansible_playbook_runner.py         # Core module
# -rw-r--r--  pyproject.toml                     # Dependencies
# -rw-r--r--  CONFIG.md                          # Configuration guide
# -rw-r--r--  EXAMPLES.md                        # Usage examples
# -rw-r--r--  SETUP.md                           # This file
# drwxr-xr-x  tests/                             # Unit tests
```

### First Run

```bash
# Option 1: Interactive menu (recommended)
/skill:ansible-playbook

# Option 2: Direct command
/skill:ansible-playbook run status_and_health --stage qa
```

On first run, the skill will:
1. Verify cassandra-ansible project location
2. Install Python dependencies via `uv sync`
3. Discover available playbooks
4. Prompt for required variables
5. Execute and log results

## Prerequisites

### System Requirements

- **Python 3.9+** (check: `python3 --version`)
- **uv package manager** (check: `uv --version`)
- **ssh-agent** with configured keys for Ansible authentication
- **Ansible** (installed via cassandra-ansible's `pyproject.toml`)

### Directory Structure

Required:
```
/Users/panisko/projects/cassandra-ansible/
├── playbooks/               ← Must exist with .yml files
├── inventories/             ← Must exist with stage dirs
├── scripts/fetch_hosts.py    ← Inventory script
├── ansible.cfg              ← Ansible config
└── pyproject.toml           ← Dependencies
```

Optional:
```
/Users/panisko/projects/aiops_shipit/podman/configs/
├── otel-collector-remote.yaml  ← OTEL config (read-only)
└── logback.xml                 ← Log format (read-only)
```

### SSH Configuration

For Ansible to authenticate to nodes:

```bash
# 1. Ensure SSH key exists
test -f ~/.ssh/id_rsa && echo "SSH key found" || echo "SSH key missing"

# 2. Start SSH agent (if not running)
eval "$(ssh-agent -s)"

# 3. Add key to agent
ssh-add ~/.ssh/id_rsa

# 4. Test connectivity to a cluster node
ssh cassandra-1 "echo OK" 2>&1 | head -3
```

## Configuration

### Environment Variables (Optional)

```bash
# Override defaults
export CASSANDRA_ANSIBLE_ROOT=/custom/path/cassandra-ansible
export OTEL_EXPORTER_OTLP_ENDPOINT=http://custom-otel:4317
export DISABLE_OPENSEARCH_EXPORT=1
export ANSIBLE_DEBUG=1

# Then run
/skill:ansible-playbook
```

### Python Dependencies

The skill automatically installs dependencies via `uv sync`:

- **pyyaml** — Parse Ansible playbooks
- **requests** — Export logs to OTEL
- **structlog** — Structured logging
- **python-dotenv** — Environment variables

Verify installation:
```bash
python3 -c "import yaml, requests, structlog, dotenv; print('OK')"
```

### Logging Configuration

Logs are automatically saved to: `~/.ansible_playbook_runner/logs/`

**Directory structure:**
```
~/.ansible_playbook_runner/
└── logs/
    ├── 2026-05-28.jsonl      # Date-based log files
    ├── 2026-05-27.jsonl
    └── latest.json           # Latest execution
```

Each log entry is JSON with structured fields:
- `timestamp` — ISO8601 UTC
- `level` — INFO/ERROR/WARNING
- `playbook` — Playbook name
- `stage` — qa/live
- `status` — success/failed
- `duration_seconds` — Execution time
- `returncode` — Ansible exit code
- `variables` — Variables used
- `stdout` — Playbook output (truncated to 5000 chars)
- `stderr` — Error output (truncated to 5000 chars)

## Running Tests

The skill includes unit tests using pytest:

```bash
# Run all tests
pytest ~/.pi/agent/skills/ansible-playbook/tests/ -v

# Run specific test class
pytest ~/.pi/agent/skills/ansible-playbook/tests/test_ansible_playbook_runner.py::TestPlaybookDiscovery -v

# Run with coverage
pytest ~/.pi/agent/skills/ansible-playbook/tests/ --cov=ansible_playbook_runner
```

### Test Coverage

The test suite covers:
- ✅ Playbook discovery and parsing
- ✅ Variable detection and prompting
- ✅ Live environment confirmation
- ✅ Log formatting (logback pattern)
- ✅ OpenSearch export
- ✅ Playbook execution (mocked)
- ✅ Interactive and direct modes
- ✅ Error handling

Run tests before deploying:
```bash
cd ~/.pi/agent/skills/ansible-playbook
pytest tests/ -v --tb=short
```

## Uninstallation

To remove the skill:

```bash
# Backup logs (optional)
cp -r ~/.ansible_playbook_runner/logs ~/.ansible_playbook_runner/logs.backup

# Remove skill
rm -rf ~/.pi/agent/skills/ansible-playbook/

# Clear logs
rm -rf ~/.ansible_playbook_runner/
```

## Integration with Pi Agent

The skill is automatically discovered by Pi. To verify:

```bash
# In Pi CLI, list available skills
/skill:

# Should show: "ansible-playbook: Run Ansible playbooks..."
```

Load the skill:
```bash
/skill:ansible-playbook
```

Force reload (in case of code changes):
```bash
# Restart Pi agent or use:
/skill:ansible-playbook --reload
```

## Troubleshooting Setup

### "Playbooks directory not found"

```bash
# Verify installation
ls -la /Users/panisko/projects/cassandra-ansible/playbooks/

# If missing, clone project
cd /Users/panisko/projects
git clone <cassandra-ansible-repo> cassandra-ansible
cd cassandra-ansible
uv sync
```

### "Python dependencies not installed"

```bash
# Reinstall dependencies
cd /Users/panisko/projects/cassandra-ansible
uv sync --upgrade

# Verify installation
uv run python3 -c "import yaml, requests, structlog"
```

### "SSH authentication fails"

```bash
# Verify SSH setup
ssh-add -l  # Should show your key

# If empty, add key:
ssh-add ~/.ssh/id_rsa

# Test connectivity:
ssh -v cassandra-1 uptime 2>&1 | grep -E "(Offering|Authentication|success)"
```

### "Permission denied" errors

```bash
# Make scripts executable
chmod +x ~/.pi/agent/skills/ansible-playbook/scripts/*.sh

# Verify
ls -la ~/.pi/agent/skills/ansible-playbook/scripts/
```

## Performance Tuning

### For Large Clusters

```bash
# Increase Ansible parallelism
# Edit /Users/panisko/projects/cassandra-ansible/ansible.cfg
[defaults]
forks = 20  # Default: 5
timeout = 120  # Increase connection timeout
```

### For Slow Networks

```bash
# Increase timeouts
[defaults]
timeout = 120
gather_timeout = 60
command_timeout = 60
```

## Development & Customization

### Adding New Playbooks

1. Create playbook in `/Users/panisko/projects/cassandra-ansible/playbooks/`:
   ```yaml
   ---
   - name: My Custom Play
     hosts: "{{ datacenter_name }}"
     vars:
       my_var: null  # Mark as required
     tasks:
       - name: Do something
         debug:
           msg: "Hello"
   ```

2. Playbook automatically discovered by runner

3. Run via skill:
   ```bash
   /skill:ansible-playbook run my_custom_play --datacenter de_rhr_bap
   ```

### Extending the Runner

Edit `ansible_playbook_runner.py` to add features:

```python
class PlaybookRunner:
    def custom_method(self):
        """Add custom functionality."""
        pass
```

Then:
```bash
cd /Users/panisko/projects/cassandra-ansible
pytest  # Verify changes
uv run python ansible_playbook_runner.py  # Test manually
```

## Support & Documentation

- **Skill docs:** `~/.pi/agent/skills/ansible-playbook/SKILL.md`
- **Configuration:** `~/.pi/agent/skills/ansible-playbook/CONFIG.md`
- **Examples:** `~/.pi/agent/skills/ansible-playbook/EXAMPLES.md`
- **This guide:** `~/.pi/agent/skills/ansible-playbook/SETUP.md`

For Pi skill standard:
- **Pi Skills Standard:** https://agentskills.io/specification
- **Pi Documentation:** `/opt/homebrew/Cellar/pi-coding-agent/*/libexec/lib/node_modules/@earendil-works/pi-coding-agent/docs/`
