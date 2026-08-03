# Ansible Playbook Skill - Examples & Troubleshooting

## Quick Start Examples

### 1. Interactive Menu (Recommended for First-Time Use)

```bash
/skill:ansible-playbook
```

**Output:**
```
╔════════════════════════════════════════════════════════════════╗
║         Ansible Playbook Runner - Interactive Menu             ║
╚════════════════════════════════════════════════════════════════╝

📚 Available Playbooks:
  1) add_node
  2) assassinate_node
  3) cleanup_nodes
  4) configure_cassandra
  5) decommission_node
  6) nodetool_cleanup
  7) nodetool_repair
  8) rolling_restart_dc
  9) shutdown_dc
 10) status_and_health
 11) stress_test

Select playbook (number): 8

✅ Selected: rolling_restart_dc

🗄️  Available Clusters:
  1) piotr-test-cluster
  2) my-prod-cluster
  3) staging-cluster

Select cluster (number): 1

✅ Selected: piotr-test-cluster

⚙️  Stage Selection:
  [1] qa (default)
  [2] live (production)
Select stage [1]: 1

✅ Selected: qa

🔧 Required Variables:
Datacenter [de_rhr_bap,de_kae_bs]: de_rhr_bap

======================================================================
▶️  Executing rolling_restart_dc (qa)...
======================================================================

PLAY [Rolling restart Cassandra datacenter] ***

TASK [Ensure datacenter_name is set] ***
ok: [cassandra-1]

... (ansible output) ...

✅ SUCCESS (duration: 145.2s)

📋 Output (last 2000 chars):
PLAY [Rolling restart Cassandra datacenter] ***

TASK [Ensure datacenter_name is set] ***
ok: [cassandra-1]

... (truncated) ...
```
```

### 2. Direct Execution - Status Check (QA)

```bash
/skill:ansible-playbook run status_and_health
```

Since it's QA (default) and no required variables, executes immediately:
```
▶️  Executing status_and_health (qa)...
✅ SUCCESS (duration: 12.5s)
```

### 3. Rolling Restart - Production

```bash
/skill:ansible-playbook run rolling-restart --stage live --datacenter de_rhr_bap
```

**Output (requires confirmation):**
```
Datacenter [de_rhr_bap,de_kae_bs]: de_rhr_bap

======================================================================
⚠️  LIVE ENVIRONMENT DETECTED ⚠️
======================================================================
This playbook will execute against PRODUCTION infrastructure.
To proceed, retype exactly:

    I confirm deployment to LIVE

Confirmation: I confirm deployment to LIVE

▶️  Executing rolling_restart_dc (live)...
✅ SUCCESS (duration: 342.1s)
```

### 4. Configuration Playbook with Custom Cluster

```bash
/skill:ansible-playbook run configure_cassandra --cluster my-prod-cluster --stage live
```

### 5. Stress Test with Custom Profile

```bash
/skill:ansible-playbook run stress_test \
  --stage qa \
  --datacenter de_rhr_bap \
  --profile profiles/my-custom-profile.yaml
```

### 6. Dry Run Preview

The runner always shows the command before execution:

```bash
/skill:ansible-playbook run decommission_node --stage qa
```

**Preview:**
```
Running command:
  uv run ansible-playbook playbooks/decommission_node.yml \
    -i scripts/fetch_hosts.py \
    -e @inventories/qa/all.yml \
    -e datacenter_name=de_rhr_bap
```

Review before confirming execution continues.

## Logs & Monitoring

### View Recent Executions

```bash
# List all log files
ls -la ~/.ansible_playbook_runner/logs/

# View today's logs
tail -f ~/.ansible_playbook_runner/logs/$(date +%Y-%m-%d).jsonl

# Query specific playbook
grep '"playbook":"rolling_restart_dc"' ~/.ansible_playbook_runner/logs/*.jsonl
```

### Sample Log Entry

```json
{
  "timestamp": "2026-05-28T14:32:18Z",
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
  "stdout": "PLAY [Rolling restart Cassandra datacenter] **...",
  "stderr": ""
}
```

### OpenSearch Query (if available)

```bash
# Find all failed playbook executions today
curl -u admin:password \
  'https://opensearch.example.com/ansible-playbooks-2026-05-28/_search' \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "match": {
        "status": "failed"
      }
    },
    "sort": [{"timestamp": "desc"}]
  }' | jq .

# Count playbook executions by stage
curl -u admin:password \
  'https://opensearch.example.com/ansible-playbooks-*/_search' \
  -H 'Content-Type: application/json' \
  -d '{
    "aggs": {
      "by_stage": {
        "terms": {
          "field": "stage"
        }
      }
    }
  }' | jq .
```

## Troubleshooting

### Issue: "Playbooks directory not found"

**Cause:** The skill cannot locate the cassandra-ansible project

**Solution:**
```bash
# Option 1: Verify default location
ls /Users/panisko/projects/cassandra-ansible/playbooks/

# Option 2: Override path
export CASSANDRA_ANSIBLE_ROOT=/custom/path/cassandra-ansible
/skill:ansible-playbook
```

### Issue: "OTEL endpoint unreachable"

**Cause:** OpenSearch/OTEL collector not running or unreachable

**Symptoms:**
```
⚠️  opensearch_export_failed: Connection refused to http://localhost:4317
```

**Solution:**
```bash
# Option 1: Verify collector is running
docker ps | grep otel

# Option 2: Check connectivity
telnet localhost 4317

# Option 3: Use custom endpoint
export OTEL_EXPORTER_OTLP_ENDPOINT=http://remote-otel.example.com:4317
/skill:ansible-playbook

# Option 4: Disable OpenSearch export (logs stay local)
export DISABLE_OPENSEARCH_EXPORT=1
/skill:ansible-playbook
```

### Issue: "Ansible authentication failed"

**Symptoms:**
```
FAILED - SSH Error: Permission denied (publickey)
```

**Solutions:**
```bash
# 1. Verify SSH connectivity
ssh cassandra-1 uptime

# 2. Add SSH key to agent
ssh-add ~/.ssh/id_rsa

# 3. Check SSH config
cat ~/.ssh/config
cat ansible.cfg

# 4. Test inventory
cd /Users/panisko/projects/cassandra-ansible
uv run ansible-playbook --inventory scripts/fetch_hosts.py --list-hosts
```

### Issue: "Variable not detected - prompted repeatedly"

**Cause:** Playbook doesn't define variables in a way the runner recognizes

**Solution:** Edit the playbook to explicitly define required vars:

```yaml
# Before:
- name: My Play
  hosts: "{{ dc_name }}"

# After:
- name: My Play
  vars:
    dc_name: null  # ← Signals required
  hosts: "{{ dc_name }}"
```

### Issue: "Live confirmation failed - typo"

**Symptoms:**
```
❌ Confirmation mismatch. Execution cancelled.
```

**Solution:**
- Retype exactly: `I confirm deployment to LIVE`
- Case-sensitive: must be exact
- No extra spaces or punctuation

### Issue: "Playbook timeout after 1 hour"

**Cause:** Long-running playbook exceeds 1-hour timeout

**Symptoms:**
```
❌ FAILED (exit code: 124)
Playbook execution timed out after 1 hour
```

**Solution:**
```bash
# Option 1: Wait for operation to complete naturally (check logs)
tail -f ~/.ansible_playbook_runner/logs/$(date +%Y-%m-%d).jsonl

# Option 2: Modify timeout in Python code
# File: ansible_playbook_runner.py, line ~340
# Change: timeout=3600 to timeout=7200  (2 hours)

# Option 3: Run playbook directly (not via skill)
cd /Users/panisko/projects/cassandra-ansible
uv run ansible-playbook playbooks/stress_test.yml ...
```

### Issue: "Python dependency error"

**Symptoms:**
```
ModuleNotFoundError: No module named 'pyyaml'
```

**Solutions:**
```bash
# Reinstall dependencies
cd /Users/panisko/projects/cassandra-ansible
uv sync --upgrade

# Or reinstall globally
uv pip install --force-reinstall pyyaml requests structlog

# Verify installation
python3 -c "import yaml; print(yaml.__version__)"
```

### Issue: "Unable to access inventory"

**Cause:** Inventory scripts or variables not accessible

**Solutions:**
```bash
# Test inventory script
cd /Users/panisko/projects/cassandra-ansible
./scripts/fetch_hosts.py --list

# Check required inventory vars
cat inventories/qa/all.yml
cat inventories/qa/group_vars/*.yml

# Verify paths in Makefile
grep -E "(INVENTORY|VARS_FILES)" Makefile
```

## Advanced Troubleshooting

### Enable Debug Output

```bash
export ANSIBLE_DEBUG=1
/skill:ansible-playbook run status_and_health
```

This shows:
- Full Python stack traces
- Ansible verbose output
- HTTP request/response details

### Manual Playbook Execution (Bypass Skill)

```bash
cd /Users/panisko/projects/cassandra-ansible

# Exact command the skill uses:
uv run ansible-playbook playbooks/rolling_restart_dc.yml \
  -i scripts/fetch_hosts.py \
  -e @inventories/qa/all.yml \
  -e datacenter_name=de_rhr_bap
```

### Check Skill Health

```bash
# List available playbooks
python3 /Users/panisko/.pi/agent/skills/ansible-playbook/ansible_playbook_runner.py --help

# Run discovery
python3 << 'EOF'
from ansible_playbook_runner import PlaybookRunner
runner = PlaybookRunner()
playbooks = runner.discover_playbooks()
for pb in playbooks:
    vars_needed = runner.parse_required_variables(pb)
    print(f"{pb}: needs {vars_needed}")
EOF
```

## Performance Tips

### Faster Execution

1. **Reduce Ansible parallelism** (if cluster is small):
   ```bash
   # Edit ansible.cfg
   [defaults]
   forks = 5  # Less overhead
   ```

2. **Increase parallelism** (if cluster is large):
   ```bash
   [defaults]
   forks = 20  # More parallel tasks
   ```

3. **Use gather_facts: no** in playbooks (if possible):
   ```yaml
   - name: My Play
     hosts: "{{ datacenter_name }}"
     gather_facts: no  # Skip expensive fact gathering
   ```

4. **Check connection timeout**:
   ```bash
   [defaults]
   timeout = 30  # Seconds
   ```

## Integration with Other Tools

### Slack Notifications

```bash
# After playbook execution, notify Slack
WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK"

STATUS="$?"
if [ $STATUS -eq 0 ]; then
  curl -X POST "$WEBHOOK_URL" -d \
    '{"text":"✅ rolling_restart_dc completed successfully"}'
else
  curl -X POST "$WEBHOOK_URL" -d \
    '{"text":"❌ rolling_restart_dc failed with code '$STATUS'"}'
fi
```

### Monitoring & Alerting

```bash
# Query OpenSearch for failed executions
curl -s 'http://localhost:9200/ansible-playbooks-*/_search' \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {"range": {"timestamp": {"gte": "now-1h"}}},
    "aggs": {"failures": {"terms": {"field": "status"}}}
  }' | jq .
```

## Getting Help

1. Check logs: `~/.ansible_playbook_runner/logs/`
2. Review configuration: `/Users/panisko/.pi/agent/skills/ansible-playbook/CONFIG.md`
3. Check Ansible docs: `https://docs.ansible.com/`
4. Review playbook: `/Users/panisko/projects/cassandra-ansible/playbooks/`
