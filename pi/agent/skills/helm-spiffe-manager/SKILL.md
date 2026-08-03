---
name: helm-spiffe-manager
description: "Manages SPIFFE identity configuration in helm-values/common.yml. Use to add, update, or remove spiffe-id-to-authorities rules based on natural language descriptions. Handles templating, brand mappings, and stage conditions intelligently."
argument-hint: "Describe the SPIFFE rule change: 'Add spiffe for service X in brand Y', 'Update password-change rules for all brands', etc."
compatibility: opencode
---

# Helm SPIFFE Manager Skill

## When to Use
- Adding new SPIFFE identity rules for services
- Updating existing SPIFFE mappings for specific brands
- Removing deprecated SPIFFE identities
- Bulk updating across brands or stages
- Adding conditional rules for specific stage/brand combinations

## How It Works

### 1. Parse & Understand
The skill reads `helm-values/common.yml` and parses:
- Current `spiffe-id-to-authorities` structure
- Brand name mappings (poma, securetoken, etc.)
- Conditional logic patterns (stage/brand checks)

### 2. Generate Changes
Based on your description, the skill:
- Identifies the appropriate location in the config
- Generates YAML-compliant SPIFFE rules
- Applies brand/stage templates correctly
- Preserves existing rules and formatting

### 3. Review & Approve
- Shows side-by-side diff of changes
- Highlights new/modified/removed rules
- Allows you to approve, reject, or request modifications

### 4. Apply
- Merges changes into the YAML
- Validates syntax
- Updates the file

## Usage Examples

### Add a new SPIFFE rule for a single service

```
Add SPIFFE rule for the new 'profile-service' in gmx brand 
with ROLE_POST_INTROSPECT_V2 permission
```

The skill will:
- Detect it's a new service registration
- Create the proper spiffe:// URI format
- Place it in the correct section
- Add brand template variable if multi-brand

### Update rules for a namespace across all brands

```
Update all rules in poma-sid2-{stage} namespace for 
tracking-service to include ROLE_POST_JWT in live stage
```

The skill will:
- Find all matching rules
- Add the new role to existing authority lists
- Preserve other roles
- Show what changed for each brand

### Add conditional stage-specific rules

```
Add spiffe rules for dev environment only:
- confix-dev-service with ROLE_POST_INTROSPECT_V2
- Should only apply when MAM_STAGE=qa
```

The skill will:
- Wrap in `{{- if eq .Env.MAM_STAGE "qa" }}` conditions
- Use the correct namespace reference
- Maintain consistent formatting

### Remove deprecated rules

```
Remove all spiffe rules for the old 'legacy-gateway' 
service from storage namespace
```

## Communication Protocol

1. **Clarifying Questions**: Ask if the description is ambiguous
   - Which brands? (all, or specific ones?)
   - Which stages? (qa, live, or both?)
   - Stage-specific or universal?

2. **Present Options**: If multiple interpretations exist
   - Option A: Add service as brand-specific (one rule per brand)
   - Option B: Add as universal (single template rule for all)
   - Which approach?

3. **Show the Diff**: Always display changes before applying
   - Line numbers and context
   - Color-coded additions/removals
   - Brand/stage conditions highlighted

4. **Get Approval**: Wait for explicit confirmation
   - "Looks good, apply the changes"
   - "No, modify X and try again"
   - "Cancel"

## Configuration Formats Supported

### Basic SPIFFE rule (all stages/brands)
```yaml
"[spiffe://cluster.local/ns/poma-service/sa/service-account]":
  - ROLE_POST_INTROSPECT_V2
```

### With brand template variable
```yaml
"[spiffe://cluster.local/ns/poma-service-{{ .Env.MAM_STAGE }}/sa/service-{{ (index $brandMap .Env.MAM_BRAND | default .Env.MAM_BRAND) }}-{{ .Env.MAM_STAGE }}]":
  - ROLE_POST_INTROSPECT
```

### Conditional by brand
```yaml
{{- if eq .Env.MAM_BRAND "gcom" }}
"[spiffe://cluster.local/ns/...]":
  - ROLE_POST_INTROSPECT
{{- end }}
```

### Conditional by stage
```yaml
{{- if eq .Env.MAM_STAGE "qa" }}
"[spiffe://cluster.local/ns/...]":
  - ROLE_POST_INTROSPECT_V2
{{- end }}
```

## Validation Rules

The skill validates:
- ✅ Valid Go template syntax ({{ .Env.MAM_BRAND }}, etc.)
- ✅ Proper YAML indentation (2 spaces)
- ✅ Valid SPIFFE URI format
- ✅ Known role names (ROLE_POST_*)
- ✅ No duplicate spiffe identities
- ✅ Consistent with existing brand mappings

## Brand & Stage Mappings

The skill understands and uses:

**Brands**: acc, gmx, gcom, mcom, uli, webde

**Brand name mappings** (for poma services):
- gmx → gmxnet
- mcom → mailcom
- gcom → gmxint / gmxcom / gmxes / gmxfr
- uli → netid
- acc → 1and1

**Stages**: qa (dev), live (prelive)

**Namespaces by service family**:
- poma-sid2-{stage} (confix, smart-search, etc.)
- poumo-oauth2-{stage} (token services)
- poumo-ums-{stage} (user management)
- etc.

## Best Practices

1. **Be Specific**: Include namespace, service, and brand/stage scope
2. **One Change at a Time**: If unrelated, split into separate requests
3. **Review Changes Carefully**: SPIFFE controls critical authentication
4. **Document Source**: Reference the Jira/issue requesting the change
5. **Test in QA First**: Add to qa/dev before promoting to live

## Limitations

- Cannot create brand mappings (only use existing ones)
- Cannot validate actual service account existence in cluster
- Cannot modify vault path structure
- Will not remove rules without explicit confirmation

## See Also

- `helm-values/common.yml` - Main configuration file
- `helm-values/qa/` - QA environment overrides
- `helm-values/live/` - Live environment overrides
