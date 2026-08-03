# Installation & Implementation Guide

## Skill Location

```
/Users/panisko/.pi/agent/skills/helm-spiffe-manager/
├── SKILL.md                           # Main skill definition
├── README.md                          # Usage guide & examples
├── QUICK_REFERENCE.md                 # Common tasks & templates
├── CONFIGURATION_REFERENCE.md         # Current config analysis
├── helm_spiffe_manager.py             # Python implementation
└── IMPLEMENTATION.md                  # This file
```

## Quick Start

### 1. Use the Skill in Pi

```bash
/skill:helm-spiffe-manager Add spiffe rule for the new 'analytics-service' \
in the poma-analytics-{stage} namespace with ROLE_POST_INTROSPECT_V2 for all brands
```

### 2. Or Trigger Automatically

```bash
I need to update helm-values/common.yml to add spiffe configuration for a new service...
[Pi detects spiffe update need and invokes helm-spiffe-manager skill automatically]
```

---

## How the Skill Works

### Phase 1: Understanding Your Request

The skill:
1. Parses your natural language description
2. Identifies key elements:
   - Service name
   - Namespace
   - Brands (which brands this applies to)
   - Stages (qa, live, or both)
   - Roles/permissions needed
3. Asks clarifying questions if anything is ambiguous

### Phase 2: Parsing Current Config

The skill:
1. Loads `helm-values/common.yml`
2. Extracts the `spiffe-id-to-authorities` section
3. Parses all 183+ existing SPIFFE rules
4. Identifies placement patterns and existing services

### Phase 3: Generating Proposed Changes

Based on your request and current config, the skill:
1. Generates valid SPIFFE URI with proper templates
2. Selects correct `$brandMap` variable if needed
3. Wraps in conditionals (brand/stage) if necessary
4. Formats as proper YAML with correct indentation

### Phase 4: Review & Diff

The skill shows:
```
CURRENT:
  "[spiffe://cluster.local/ns/poma-service/sa/service]":
    - ROLE_POST_INTROSPECT_V2

PROPOSED ADDITION:
+ "[spiffe://cluster.local/ns/poma-analytics-{{ .Env.MAM_STAGE }}/sa/analytics-{{ (index $brandMappoma .Env.MAM_BRAND | default .Env.MAM_BRAND) }}-{{ .Env.MAM_STAGE }}]":
+   - ROLE_POST_INTROSPECT_V2

📊 Summary:
  - New rules: 1
  - Modified rules: 0
  - Removed rules: 0
  - Lines added: 4
  - Lines removed: 0
```

### Phase 5: Approval & Application

You respond:
- ✅ "Apply changes"
- ❌ "No, modify to..."
- 🔄 "Cancel"

Then the skill:
1. Validates YAML syntax
2. Checks for duplicates
3. Merges into `helm-values/common.yml`
4. Optionally commits to git
5. Reports success

---

## Implementation Details

### Python Tool Architecture

The skill has 3 main components:

#### 1. SpiffeConfigManager Class
```python
class SpiffeConfigManager:
    - load_config()              # Load YAML from file
    - extract_spiffe_section()   # Extract spiffe rules
    - parse_spiffe_rules()       # Parse existing rules
    - validate_spiffe_id()       # Validate URI format
    - validate_roles()           # Validate role names
    - generate_spiffe_rule_yaml()  # Generate new rule
    - suggest_placement()        # Suggest where to place
    - diff_sections()            # Generate readable diff
    - to_json_diff()            # JSON diff for parsing
```

#### 2. CLI Interface
Accessible via Python:
```bash
# Parse current rules
python helm_spiffe_manager.py parse

# Validate a rule
python helm_spiffe_manager.py validate "spiffe://..." ROLE_NAME

# Get placement suggestions
python helm_spiffe_manager.py suggest "description"
```

#### 3. Validation Rules

**SPIFFE ID Format:**
- Must start with `spiffe://cluster.local/`
- Can include template variables: `{{ .Env.VAR }}`
- Must be enclosed in `[brackets]` in YAML

**Role Names:**
- Validated against known list (17 roles)
- Case-sensitive: `ROLE_POST_JWT` not `role_post_jwt`

**Brand Names:**
- Restricted to: acc, gmx, gcom, mcom, uli, webde

**Stage Names:**
- Valid: qa (maps to dev), live (maps to prelive)

---

## Configuration File Format

The target file: `helm-values/common.yml`

### Location of SPIFFE Config

```yaml
secrets:
  applicationoverride:
    mountPath: /srv/config
    triggerReload: true
    content:
      application-override.yml: |
        vault:
          ...
        hammer:
          security:
            xfcc:
              anonymous-authorities: ROLE_ANONYMOUS
              spiffe-id-to-authorities:     # ← START HERE
                "[spiffe://...]":            # Rule 1
                  - ROLE_POST_JWT
                "[spiffe://...]":            # Rule 2
                  - ROLE_POST_INTROSPECT_V2
                {{- if eq .Env.MAM_BRAND "gmx" }}
                "[spiffe://...]":            # Conditional Rule
                  - ROLE_POST_INTROSPECT
                {{- end }}
```

### Indentation Important!

Must use **2-space indentation**:
```yaml
              spiffe-id-to-authorities:  # Level 1 (14 spaces)
                "[spiffe://...]":          # Level 2 (16 spaces)
                  - ROLE_X               # Level 3 (18 spaces)
                {{- if ... }}            # Level 2 (14 spaces)
                "[spiffe://...]":        # Level 3 (16 spaces)
                  - ROLE_Y               # Level 4 (18 spaces)
                {{- end }}               # Level 2 (14 spaces)
```

---

## Usage Scenarios

### Scenario 1: New Service Registration

**User:** "Add spiffe rule for new-notification-service in poma-notifications namespace"

**Skill Process:**
1. Asks: "Which brands? (all or specific)"
2. Asks: "Which stages? (qa, live, or both)"
3. Asks: "Which roles? (ROLE_POST_*)"
4. Generates rule with brand templates
5. Shows diff
6. Applies on approval

### Scenario 2: Update Existing Rule

**User:** "Add ROLE_POST_JWT to the refreshtokenservice rule"

**Skill Process:**
1. Finds existing refreshtokenservice rule
2. Identifies its current roles
3. Appends new role to list
4. Shows updated rule
5. Applies on approval

### Scenario 3: Conditional Rule

**User:** "Add spiffe for debug-service in gmx brand only for qa stage"

**Skill Process:**
1. Detects brand + stage specificity
2. Wraps in: `{{- if and (eq .Env.MAM_BRAND "gmx") (eq .Env.MAM_STAGE "qa") }}`
3. Generates QA-namespace rule
4. Adds conditional comment
5. Shows diff
6. Applies on approval

---

## Error Handling

### Validation Errors

| Error | Solution |
|-------|----------|
| `Unknown role: ROLE_X` | Check role is in known list; ask team if custom |
| `Invalid SPIFFE URI` | Must start with `spiffe://cluster.local/` |
| `Invalid template syntax` | Use `{{ .Env.VAR }}` not `${VAR}` |
| `Duplicate SPIFFE ID` | This rule exists; request update instead |
| `Unknown brand` | Use only: acc, gmx, gcom, mcom, uli, webde |

### User Input Errors

**Ambiguous request** → Skill asks clarifying questions

**Multiple interpretations** → Skill presents options (Option A/B/C)

**Conflicting rules** → Skill warns and requests confirmation

---

## Testing the Implementation

### Test 1: Parse Existing Rules

```bash
cd /Users/panisko/projects/poumo/accesstokenservice-rest
python3 ~/.pi/agent/skills/helm-spiffe-manager/helm_spiffe_manager.py parse | jq '.count'
# Output: 183
```

### Test 2: Validate a Rule

```bash
python3 ~/.pi/agent/skills/helm-spiffe-manager/helm_spiffe_manager.py validate \
  "spiffe://cluster.local/ns/poma-test/sa/test" \
  ROLE_POST_INTROSPECT_V2
# Output: {"valid": true}
```

### Test 3: Get Suggestions

```bash
python3 ~/.pi/agent/skills/helm-spiffe-manager/helm_spiffe_manager.py suggest \
  "Add new service for gmx brand in poma-test namespace"
# Output: {..., "brands": ["gmx"], "is_conditional": true, ...}
```

---

## Integration with Pi

### Automatic Trigger

Pi detects SPIFFE-related requests and auto-invokes:
```
When user says: "I need to add/update/change spiffe configuration"
→ Pi uses helm-spiffe-manager skill
```

### Manual Invocation

```
/skill:helm-spiffe-manager [your request]
```

### Skill Metadata

The SKILL.md file defines:
- `name`: helm-spiffe-manager
- `description`: Complete description of capability
- `argument-hint`: Hints for what to describe
- `compatibility`: opencode (Python tool compatible)

---

## File Structure

```
/Users/panisko/.pi/agent/skills/helm-spiffe-manager/
│
├── SKILL.md
│   └── Main skill definition + metadata
│       ├── When to use
│       ├── How it works
│       ├── Usage examples
│       ├── Communication protocol
│       ├── Configuration formats
│       ├── Validation rules
│       └── Best practices
│
├── README.md
│   └── Implementation & usage guide
│       ├── Overview & features
│       ├── Usage examples (3 detailed)
│       ├── Workflow (5 phases)
│       ├── Supported roles & mappings
│       ├── Common patterns
│       ├── Troubleshooting
│       └── Best practices
│
├── QUICK_REFERENCE.md
│   └── Quick lookup for common tasks
│       ├── Common tasks with templates
│       ├── Request templates
│       ├── Validation checklist
│       ├── Error reference
│       ├── Tips & tricks
│       ├── Namespace reference
│       └── When to use
│
├── CONFIGURATION_REFERENCE.md
│   └── Analysis of current configuration
│       ├── Extracted rules analysis
│       ├── Service namespaces by category
│       ├── Brand-specific rules
│       ├── Common patterns
│       ├── Key templates & variables
│       └── Checklist for adding
│
└── helm_spiffe_manager.py
    └── Python implementation
        ├── SpiffeConfigManager class
        ├── SPIFFE/role validation
        ├── Rule generation
        ├── Diff generation
        ├── Placement suggestions
        └── CLI interface
```

---

## Next Steps

1. **Test the skill**: Run manual tests to verify tool works with your config
2. **Try a simple request**: Add a simple test rule to verify workflow
3. **Document patterns**: Record patterns used in your environment
4. **Team training**: Show team how to use the skill for updates
5. **Iterate**: Refine based on actual usage patterns

---

## Support

**For questions about**:
- **Using the skill**: See README.md and QUICK_REFERENCE.md
- **Current configuration**: See CONFIGURATION_REFERENCE.md
- **How it works**: See SKILL.md protocol section
- **Troubleshooting**: See README.md troubleshooting section

**For issues**:
- Validation errors → Check known roles/brands/stages
- Ambiguous requests → Provide more specific description
- Tool errors → Check Python version (3.7+), no external deps needed
