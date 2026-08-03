# Helm SPIFFE Manager - Implementation Guide

## Overview

This skill manages SPIFFE identity configuration in `helm-values/common.yml`. It intelligently parses, validates, and modifies the `hammer.security.xfcc.spiffe-id-to-authorities` section based on natural language descriptions.

## Features

✅ **Parse & Validate**
- Parse existing SPIFFE rules from YAML
- Validate SPIFFE URI format
- Validate role names against known list
- Check template variable syntax

✅ **Intelligent Generation**
- Suggest rule placement based on description
- Auto-detect brand/stage conditionals
- Generate properly formatted YAML
- Preserve existing indentation/formatting

✅ **User-Friendly Workflow**
- Ask clarifying questions if ambiguous
- Show side-by-side diffs
- Interactive approval/rejection flow
- Detailed change summary

✅ **Safety Checks**
- Validate all changes before applying
- Detect duplicate spiffe IDs
- Warn about missing brand mappings
- Preserve comments and structure

## Usage Examples

### Example 1: Add a New Service Rule

**User prompt:**
```
Add a SPIFFE rule for the new 'analytics-service' in the 
poma-analytics-{stage} namespace. It should have 
ROLE_POST_INTROSPECT_V2 permission and apply to all brands.
```

**Skill actions:**
1. Parse current YAML
2. Suggest placement in poma section
3. Generate rule:
   ```yaml
   "[spiffe://cluster.local/ns/poma-analytics-{{ .Env.MAM_STAGE }}/sa/analytics-service-{{ (index $brandMappoma .Env.MAM_BRAND | default .Env.MAM_BRAND) }}-{{ .Env.MAM_STAGE }}]":
     - ROLE_POST_INTROSPECT_V2
   ```
4. Show diff and ask for approval

---

### Example 2: Brand-Specific Update

**User prompt:**
```
Update gmx brand only - add ROLE_POST_JWT to the 
poma-password-change service in the live stage.
```

**Skill actions:**
1. Find existing poma-password-change rules
2. Detect gmx-specific request
3. Generate conditional addition:
   ```yaml
   {{- if eq .Env.MAM_BRAND "gmx" }}
   "[spiffe://cluster.local/ns/poma-password-change-live/sa/password-change-gmxnet-live-sa]":
     - ROLE_POST_JWT
   {{- end }}
   ```
4. Show context and request approval

---

### Example 3: Stage-Specific Conditional

**User prompt:**
```
Add rule for dev/qa testing only: the 'test-integration-service'
in poma-testing namespace should have ROLE_POST_TOKEN_CREATE.
This is temporary for testing.
```

**Skill actions:**
1. Detect qa stage requirement
2. Generate stage-conditional rule:
   ```yaml
   {{- if eq .Env.MAM_STAGE "qa" }}
   "[spiffe://cluster.local/ns/poma-testing-dev/sa/test-integration-service-dev]":
     - ROLE_POST_TOKEN_CREATE
   {{- end }}
   ```
3. Add comment: `# TEMPORARY - Testing only`
4. Request approval with warning

---

## Workflow

### Phase 1: Clarification
If your request is ambiguous, the skill asks:
- "Which brands? (all or specific: gmx, acc, etc.)"
- "Which stages? (qa only, live, or both?)"
- "Should this be universal or conditional?"

### Phase 2: Generation
The skill:
- Parses current configuration
- Generates proposed changes
- Validates all syntax
- Checks for conflicts/duplicates

### Phase 3: Review
You see:
```diff
Current:
  spiffe-id-to-authorities:
    "[spiffe://cluster.local/ns/poma-service/sa/service]":
      - ROLE_POST_INTROSPECT

Proposed:
+ "[spiffe://cluster.local/ns/poma-service/sa/service]":
+   - ROLE_POST_INTROSPECT
+ "[spiffe://cluster.local/ns/poma-analytics/sa/analytics]":
+   - ROLE_POST_INTROSPECT_V2

New rules: 1
Modified rules: 0
Removed rules: 0
```

### Phase 4: Approval
You respond:
- ✅ "Looks good, apply the changes"
- ❌ "No, modify X and try again"
- 🔄 "Cancel"

### Phase 5: Apply
The skill:
- Merges changes into YAML
- Validates file syntax
- Commits changes (with git if available)
- Reports success

---

## Supported Role Types

The skill validates against these known roles:

- `ROLE_POST_JWT` - Can issue JWT tokens
- `ROLE_POST_DECODE_JWT` - Can decode JWT tokens
- `ROLE_POST_INTROSPECT` - Can introspect tokens (v1)
- `ROLE_POST_INTROSPECT_V1` - Token introspection v1
- `ROLE_POST_INTROSPECT_V2` - Token introspection v2
- `ROLE_POST_TOKEN_CREATE` - Can create tokens
- `ROLE_POST_TOKEN_REVOCATION` - Can revoke tokens
- `ROLE_POST_OAUTH2_TOKEN` - OAuth2 token operations
- `ROLE_POST_NO_ID_AUTH_*` - No-ID authentication variants
- `ROLE_ANONYMOUS` - Anonymous access

---

## Brand Name Mappings

The skill uses these mappings for different service families:

### POMA Services (`$brandMappoma`)
- gmx → gmxnet
- mcom → mailcom
- gcom → gmxint / gmxes / gmxfr
- uli → netid
- acc → 1and1

### MAP Services (`$brandMap`)
- gmx → gmxnet
- mcom → mailcom
- gcom → gmxint
- uli → netid
- acc → 1and1

### SecureToken Services (`$brandMapsecuretoken`)
- acc → 1and1access

---

## Common Patterns

### Multi-Brand Rule (All Brands)
```yaml
"[spiffe://cluster.local/ns/poma-service/sa/service-{{ (index $brandMappoma .Env.MAM_BRAND | default .Env.MAM_BRAND) }}-{{ .Env.MAM_STAGE }}]":
  - ROLE_POST_INTROSPECT_V2
```

### Single-Brand Rule
```yaml
{{- if eq .Env.MAM_BRAND "gmx" }}
"[spiffe://cluster.local/ns/poma-service/sa/service-gmxnet-{{ .Env.MAM_STAGE }}]":
  - ROLE_POST_INTROSPECT_V2
{{- end }}
```

### Stage-Conditional (QA Only)
```yaml
{{- if eq .Env.MAM_STAGE "qa" }}
"[spiffe://cluster.local/ns/poma-service-dev/sa/service-dev]":
  - ROLE_POST_TOKEN_CREATE
{{- end }}
```

### Brand + Stage Conditional
```yaml
{{- if and (eq .Env.MAM_BRAND "acc") (eq .Env.MAM_STAGE "qa") }}
"[spiffe://cluster.local/ns/poma-service-dev/sa/service-1and1-dev]":
  - ROLE_POST_INTROSPECT_V2
{{- end }}
```

---

## Troubleshooting

### Q: "Unknown role: ROLE_X"
**A**: The role name might be custom. Check the list above or verify in Slack/docs.

### Q: "Invalid template syntax"
**A**: Template variables must use `{{ .Env.VAR_NAME }}` format, not `${VAR_NAME}` or bare strings.

### Q: "Spiffe ID not starting with spiffe://"
**A**: All spiffe IDs must follow: `spiffe://cluster.local/ns/namespace/sa/service-account`

### Q: "Duplicate spiffe ID detected"
**A**: This spiffe ID already exists. Update the existing rule instead of adding a new one.

---

## Best Practices

1. **Test in QA First**
   - Add rules to qa stage first
   - Verify they work
   - Then promote to live

2. **Document Changes**
   - Include Jira ticket reference
   - Add comments for non-obvious rules
   - Explain why conditional logic is needed

3. **One Change at a Time**
   - Separate unrelated changes
   - Makes review and debugging easier
   - Easier to revert if needed

4. **Review Diffs Carefully**
   - Check namespace names
   - Verify service account naming
   - Confirm role assignments

5. **Use Consistent Formatting**
   - Follow existing indentation (2 spaces)
   - Use same condition patterns
   - Group related rules together

---

## CLI Commands

The underlying Python tool provides CLI commands for validation:

```bash
# Validate a spiffe rule
python helm_spiffe_manager.py validate \
  "spiffe://cluster.local/ns/poma-service/sa/service" \
  ROLE_POST_INTROSPECT_V2

# Parse current rules
python helm_spiffe_manager.py parse

# Get placement suggestions
python helm_spiffe_manager.py suggest \
  "Add rule for analytics service in poma namespace for gmx brand"
```

All return JSON output for programmatic processing.

---

## Integration with Pi

Use the skill in Pi:

```
/skill:helm-spiffe-manager Add a spiffe rule for the new notification-service 
in poma-notifications namespace with ROLE_POST_INTROSPECT_V2 for all brands
```

Or trigger it automatically:
```
I need to update the helm-values/common.yml with a new spiffe configuration...
[Pi detects spiffe update need and invokes helm-spiffe-manager skill]
```
