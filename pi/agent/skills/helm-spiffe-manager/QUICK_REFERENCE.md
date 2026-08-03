# Quick Reference: Helm SPIFFE Manager

## Common Tasks

### ✨ Add a New Service (All Brands)

**Request:**
```
Add spiffe rule for 'notification-service' in poma-notifications-{stage} namespace
with ROLE_POST_INTROSPECT_V2 for all brands
```

**Expected Result:**
```yaml
"[spiffe://cluster.local/ns/poma-notifications-{{ .Env.MAM_STAGE }}/sa/notification-service-{{ (index $brandMappoma .Env.MAM_BRAND | default .Env.MAM_BRAND) }}-{{ .Env.MAM_STAGE }}]":
  - ROLE_POST_INTROSPECT_V2
```

---

### 🎯 Add Brand-Specific Rule

**Request:**
```
Add spiffe rule for 'special-service' in gmx brand only
Namespace: poma-special, Stage: live, Role: ROLE_POST_JWT
```

**Expected Result:**
```yaml
{{- if eq .Env.MAM_BRAND "gmx" }}
"[spiffe://cluster.local/ns/poma-special-live/sa/special-service-gmxnet-live-sa]":
  - ROLE_POST_JWT
{{- end }}
```

---

### 🧪 Add QA-Only Testing Rule

**Request:**
```
Add temporary test rule for dev environment only
Service: debug-endpoint in poma-testing
Roles: ROLE_POST_TOKEN_CREATE, ROLE_POST_DECODE_JWT
Stage: qa (dev only)
```

**Expected Result:**
```yaml
{{- if eq .Env.MAM_STAGE "qa" }}
"[spiffe://cluster.local/ns/poma-testing-dev/sa/debug-endpoint-dev]":
  - ROLE_POST_TOKEN_CREATE
  - ROLE_POST_DECODE_JWT
{{- end }}
```

---

### 📝 Update Existing Rule (Add Roles)

**Request:**
```
Update existing poumo-oauth2-{stage}/refreshtokenservice rule for all brands
Add ROLE_POST_JWT to its existing roles
```

**Expected Result:**
```yaml
# Find existing rule, append to roles list
"[spiffe://cluster.local/ns/poumo-oauth2-{{ .Env.MAM_STAGE }}/sa/refreshtokenservice-{{ .Env.MAM_BRAND }}-{{ .Env.MAM_STAGE }}]":
  - ROLE_POST_TOKEN_CREATE      # existing
  - ROLE_POST_TOKEN_REVOCATION  # existing
  - ROLE_POST_JWT               # NEW
```

---

### 🔄 Multiple Brands (Not All)

**Request:**
```
Add spiffe rule for acc and uli brands only
Service: special-auth in poma-special-services
Role: ROLE_POST_INTROSPECT_V2
```

**Expected Result:**
```yaml
{{- if or (eq .Env.MAM_BRAND "acc") (eq .Env.MAM_BRAND "uli") }}
"[spiffe://cluster.local/ns/poma-special-services-{{ .Env.MAM_STAGE }}/sa/special-auth-{{ (index $brandMappoma .Env.MAM_BRAND | default .Env.MAM_BRAND) }}-{{ .Env.MAM_STAGE }}]":
  - ROLE_POST_INTROSPECT_V2
{{- end }}
```

---

### ❌ Remove Rule

**Request:**
```
Remove the deprecated 'legacy-gateway' spiffe rule
from storageservices namespace (all brands and stages)
```

**Skill Action:**
1. Find all matching rules
2. Show which ones will be removed
3. Request confirmation
4. Delete from config

---

## Request Templates

### Template 1: Basic Addition
```
Add spiffe rule for [SERVICE_NAME] in [NAMESPACE] namespace
Roles: [ROLE1], [ROLE2]
Scope: [all brands / specific brands / specific stage]
```

### Template 2: Update Existing
```
Update spiffe rule for [SERVICE_NAME] in [NAMESPACE]
Add/Remove roles: [ROLES]
Affected brands: [list or "all"]
Affected stages: [list or "all"]
```

### Template 3: Complex Conditional
```
Add spiffe rule with condition:
- Service: [NAME]
- Namespace: [NS]
- Roles: [ROLES]
- Only for: [BRAND=value AND/OR STAGE=value]
- Reason/Jira: [RANT-XXXX]
```

---

## Validation Checklist

Before requesting a change, verify:

- [ ] Service account name is correct
- [ ] Namespace follows pattern (e.g., `poma-service-{stage}`)
- [ ] All roles are valid (see role list)
- [ ] Brand names are correct (acc, gmx, gcom, mcom, uli, webde)
- [ ] Stage names are correct (qa, live)
- [ ] No duplicate spiffe IDs already exist
- [ ] Understand if this should be conditional or universal
- [ ] Have Jira ticket reference for documentation

---

## Error Reference

| Error | Fix |
|-------|-----|
| `Unknown role: ROLE_X` | Check role name against known list |
| `Invalid SPIFFE URI` | Must start with `spiffe://cluster.local/` |
| `Duplicate SPIFFE ID` | This ID exists; update instead of add |
| `Invalid template syntax` | Use `{{ .Env.VAR }}` not `${VAR}` |
| `Unknown brand: X` | Use only: acc, gmx, gcom, mcom, uli, webde |
| `Invalid stage: X` | Use only: qa (dev), live (prelive) |

---

## Tips & Tricks

### Tip 1: Finding Service Names
Look in your service account naming:
- Service account: `poumo-istio-refreshtokenservice-rest-gmx-qa`
- Service name: `refreshtokenservice` or `refreshtokenservice-rest`

### Tip 2: Brand Mapping Variables
Different services use different brand mappings:
- POMA services (most): `$brandMappoma` → gmx→gmxnet, gcom→gmxint
- MAP services (tracking, etc.): `$brandMap` → gmx→gmxnet, gcom→gmxint
- SecureToken services: `$brandMapsecuretoken` → acc→1and1access

The skill handles this automatically!

### Tip 3: Namespace Stages
- Live environment uses `poma-service-live` and `poma-service-prelive`
- QA environment uses `poma-service-qa` and `poma-service-dev`
- Use `{{ .Env.MAM_STAGE }}` to make it dynamic

### Tip 4: Stage Mapping in Rules
When you say "qa stage only":
- Common namespace: `poma-service-dev` (in dev account)
- Namespace in template: `poma-service-{{ .Env.MAM_STAGE }}`
- Wrapped in: `{{- if eq .Env.MAM_STAGE "qa" }}`

### Tip 5: Review All Impacts
When updating a namespace rule, it affects:
- **All brands** using that namespace (unless conditional)
- **All stages** using that namespace (unless conditional)
- **All service accounts** in that namespace

Check what already exists first!

---

## Common Namespaces Reference

| Namespace | Purpose | Stage Pattern |
|-----------|---------|---|
| `poma-sid2-{stage}` | Confix, smart-search | Stage-aware |
| `poumo-oauth2-{stage}` | Token services | Stage-aware |
| `poumo-ums-{stage}` | User management | Stage-aware |
| `poumo-passport-{stage}` | Passport service | Stage-aware |
| `poma-webmailer-{stage}` | Mail services | Stage-aware + prelive |
| `pocam-*-{stage}` | Mobile/config services | Stage-aware |
| `poma-smartinbox-{stage}` | Inbox services | Stage-aware |
| `dpo-tracking-gateway-{stage}` | Tracking | Stage-aware |
| `bso-mobilesales-{stage}` | Mobile sales | Stage-aware |

---

## When to Use Skill

✅ **Use this skill when:**
- Adding new service to SPIFFE rules
- Updating existing SPIFFE rules
- Adding/removing roles from services
- Creating brand/stage-specific overrides
- Maintaining the SPIFFE configuration

❌ **Don't use this skill for:**
- Validating actual service accounts exist (ask DevOps)
- Changing vault paths (contact security)
- Modifying non-SPIFFE config sections
- Emergency access (escalate to team lead)

---

## Support & Questions

- **Uncertain about namespace?** → Ask the skill, it will suggest
- **Not sure which role?** → Describe what permission is needed
- **Need to check current state?** → Request to "Show current rules for [namespace]"
- **Want to audit changes?** → Request "List all changes in last N commits"
