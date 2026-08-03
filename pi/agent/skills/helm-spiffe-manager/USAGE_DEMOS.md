# Usage Demo & Examples

This document shows example conversations with the helm-spiffe-manager skill.

## Example 1: Simple Service Addition

### User Request

```
Add a SPIFFE rule for 'notification-service' in the poma-notifications namespace.
It should apply to all brands and stages with ROLE_POST_INTROSPECT_V2.
```

### Skill Response - Phase 1: Clarification

```
🔍 Parsing your request...

✅ I understand you want to:
- Service: notification-service
- Namespace: poma-notifications-{stage}
- Brands: All brands (acc, gmx, gcom, mcom, uli, webde)
- Stages: All stages (qa, live)
- Roles: ROLE_POST_INTROSPECT_V2

This will create 1 universal rule that applies to all brands and stages.
Confirm? Or should I adjust?
```

### User Confirms

```
Yes, that's correct.
```

### Skill Response - Phase 2-4: Generate & Review

```
📋 PROPOSED CHANGE

I'm adding the following SPIFFE rule to spiffe-id-to-authorities section:

┌────────────────────────────────────────────────────────────────┐
│ NEW RULE:                                                      │
│                                                                │
│ "[spiffe://cluster.local/ns/poma-notifications-{{ .Env.MAM_STAGE }}/sa/notification-service-{{ (index $brandMappoma .Env.MAM_BRAND | default .Env.MAM_BRAND) }}-{{ .Env.MAM_STAGE }}]":
│   - ROLE_POST_INTROSPECT_V2                                  │
└────────────────────────────────────────────────────────────────┘

📊 Summary of changes:
  - New rules added: 1
  - Existing rules modified: 0
  - Rules removed: 0
  - Total lines added: 3

📍 Placement: After 'poma-sid2' rules, before 'poumo-oauth2' section

✅ Validation passed:
  ✓ Valid SPIFFE URI format
  ✓ Valid role name (ROLE_POST_INTROSPECT_V2)
  ✓ No duplicate IDs detected
  ✓ Correct YAML indentation (2 spaces)
  ✓ Valid template variables

Ready to apply? (yes/no/modify)
```

### User Approves

```
yes, apply the changes
```

### Skill Response - Phase 5: Apply

```
✨ Applying changes...

✅ Changes merged into helm-values/common.yml
✅ YAML syntax validated
✅ No errors detected

📝 File updated:
   - helm-values/common.yml

🔄 Git status (if available):
   Modified: helm-values/common.yml
   
💡 Next steps:
   1. Review the change: git diff helm-values/common.yml
   2. Test in dev environment
   3. Commit with message: "Add notification-service SPIFFE rule"
   4. Deploy to QA first, then to production

✨ Complete!
```

---

## Example 2: Brand-Specific Rule

### User Request

```
Add a spiffe rule for acc brand only
Service: special-auth in poma-access namespace
Role: ROLE_POST_JWT
This is for a new identity verification flow, see RANT-5678
```

### Skill Response - Phase 1: Clarification

```
🔍 Parsing your request...

⚠️  I detected a brand-specific requirement. Let me clarify:

✅ Understood:
- Service: special-auth
- Namespace: poma-access
- Brand: acc (specific)
- Stages: All stages (qa, live)?
- Roles: ROLE_POST_JWT

❓ Questions:
  1. Should this apply to BOTH qa and live, or just one stage?
  2. Jira reference: RANT-5678 - should I add this as a comment?

Please clarify:
```

### User Response

```
Both qa and live stages. Yes, add the RANT-5678 reference.
```

### Skill Response - Phase 2-4: Generate & Review

```
📋 PROPOSED CHANGE

I'm adding a brand-specific conditional rule:

┌────────────────────────────────────────────────────────────────┐
│ NEW CONDITIONAL RULE (ACC BRAND ONLY):                        │
│                                                                │
│ {{- if eq .Env.MAM_BRAND "acc" }}                           │
│ "[spiffe://cluster.local/ns/poma-access-{{ .Env.MAM_STAGE }}/sa/special-auth-1and1-{{ .Env.MAM_STAGE }}-sa]":
│   - ROLE_POST_JWT                                             │
│ {{- end }}                                                    │
│ # RANT-5678: Identity verification flow                      │
└────────────────────────────────────────────────────────────────┘

📊 Summary:
  - New conditional rule: 1
  - Applies to: acc brand only
  - Affects stages: qa (dev namespace), live (prelive namespace)
  - Lines added: 5

📍 Placement: In conditional section after other acc-specific rules

⚠️  Notes:
  - Uses brand mapping: acc → 1and1
  - Wrapped in brand conditional
  - Comment added for reference

✅ Validation passed:
  ✓ Valid SPIFFE URI format
  ✓ Valid conditional syntax
  ✓ Correct brand mapping
  ✓ Valid role name

Ready to apply? (yes/no/modify)
```

### User Approves

```
Looks good, apply it
```

### Skill Response - Phase 5: Apply

```
✨ Applying changes...

✅ Changes merged into helm-values/common.yml
✅ YAML syntax validated
✅ No errors detected

📝 Updated section:
   Location: hammer.security.xfcc.spiffe-id-to-authorities
   
📊 Statistics:
   - Rules before: 183
   - Rules after: 184
   - Conditional blocks: Now 47 (was 46)

💡 Deployment notes:
   - This change only affects acc brand
   - No impact on gmx, gcom, mcom, uli, webde brands
   - Test in QA acc environment first

✨ Complete!
```

---

## Example 3: Update Existing Rule

### User Request

```
The refreshtokenservice needs to support token introspection.
Add ROLE_POST_INTROSPECT_V2 to its existing rules in poumo-oauth2 namespace.
Currently it has JWT and token creation roles.
```

### Skill Response - Phase 1: Clarification

```
🔍 Parsing your request...

✅ Found existing rule:
   Namespace: poumo-oauth2-{stage}
   Service: refreshtokenservice
   Current roles:
     - ROLE_POST_TOKEN_CREATE
     - ROLE_POST_TOKEN_REVOCATION
     - ROLE_POST_JWT
     - ROLE_POST_DECODE_JWT

📋 Proposed change:
   ADD: ROLE_POST_INTROSPECT_V2

   New roles will be:
     - ROLE_POST_TOKEN_CREATE
     - ROLE_POST_TOKEN_REVOCATION
     - ROLE_POST_JWT
     - ROLE_POST_DECODE_JWT
     - ROLE_POST_INTROSPECT_V2  ← NEW

❓ This applies to ALL brands and both stages?
   Confirm or modify?
```

### User Confirms

```
Yes, apply to all brands and stages.
```

### Skill Response - Phase 2-4: Generate & Review

```
📋 PROPOSED CHANGE

Updating existing SPIFFE rule:

┌────────────────────────────────────────────────────────────────┐
│ BEFORE:                                                        │
│ "[spiffe://cluster.local/ns/poumo-oauth2-{{ .Env.MAM_STAGE }}/sa/poumo-istio-refreshtokenservice-rest-{{ .Env.MAM_BRAND }}-{{ .Env.MAM_STAGE }}]":
│   - ROLE_POST_TOKEN_CREATE                                    │
│   - ROLE_POST_TOKEN_REVOCATION                                │
│   - ROLE_POST_JWT                                             │
│   - ROLE_POST_DECODE_JWT                                      │
│                                                                │
│ AFTER:                                                         │
│ "[spiffe://cluster.local/ns/poumo-oauth2-{{ .Env.MAM_STAGE }}/sa/poumo-istio-refreshtokenservice-rest-{{ .Env.MAM_BRAND }}-{{ .Env.MAM_STAGE }}]":
│   - ROLE_POST_TOKEN_CREATE                                    │
│   - ROLE_POST_TOKEN_REVOCATION                                │
│   - ROLE_POST_JWT                                             │
│   - ROLE_POST_DECODE_JWT                                      │
│   - ROLE_POST_INTROSPECT_V2  ← NEW                           │
└────────────────────────────────────────────────────────────────┘

📊 Summary:
  - Existing rules modified: 1
  - New roles added: 1
  - Brands affected: ALL (6 brands)
  - Stages affected: ALL (qa, live)

✅ Validation passed:
  ✓ Rule exists
  ✓ New role is valid
  ✓ No duplicate roles
  ✓ Syntax correct

Ready to apply? (yes/no/modify)
```

### User Approves

```
Apply it
```

### Skill Response - Phase 5: Apply

```
✨ Applying changes...

✅ Changes merged into helm-values/common.yml
✅ YAML syntax validated
✅ No errors detected

📝 Updated rule:
   Service: refreshtokenservice-rest
   Namespace: poumo-oauth2-{stage}
   Change type: Role addition
   
📊 Impact:
   - All 6 brands affected: acc, gmx, gcom, mcom, uli, webde
   - All 2 stages affected: qa (dev), live (prelive)
   - Estimated pods affected: 12+

💡 Deployment notes:
   - This change affects all refresh token service instances
   - May require pod restart to apply new permissions
   - Monitor token introspection calls post-deployment

✨ Complete!
```

---

## Example 4: QA-Only Testing Rule (Temporary)

### User Request

```
Add a temporary debug rule for testing the new gcom integration.
Service: debug-gcom-integration in poma-testing
Stage: qa only (not for live)
Roles: ROLE_POST_TOKEN_CREATE, ROLE_POST_DECODE_JWT
This is temporary for RANT-6789 and should be removed after testing.
```

### Skill Response - Phase 1: Clarification

```
🔍 Parsing your request...

⚠️  This is a temporary QA-only rule. I need to clarify:

✅ Understood:
- Service: debug-gcom-integration
- Namespace: poma-testing (with -dev suffix)
- Brands: gcom only
- Stage: qa only (not live)
- Roles: ROLE_POST_TOKEN_CREATE, ROLE_POST_DECODE_JWT
- Type: TEMPORARY for RANT-6789

❓ Questions:
  1. Estimated duration? (for removal reminder)
  2. Should I add "TEMPORARY - Remove after RANT-6789" comment?

Please confirm:
```

### User Response

```
Yes, add that comment. Should be removed after July 15, 2024.
```

### Skill Response - Phase 2-4: Generate & Review

```
📋 PROPOSED CHANGE

Adding TEMPORARY QA-ONLY testing rule:

┌────────────────────────────────────────────────────────────────┐
│ NEW TEMPORARY RULE (QA ONLY):                                 │
│                                                                │
│ {{- if eq .Env.MAM_STAGE "qa" }}                            │
│ {{- if eq .Env.MAM_BRAND "gcom" }}                          │
│ "[spiffe://cluster.local/ns/poma-testing-dev/sa/debug-gcom-integration-gmxint-dev]":
│   - ROLE_POST_TOKEN_CREATE                                    │
│   - ROLE_POST_DECODE_JWT                                      │
│ # TEMPORARY - Remove after RANT-6789 (expires 2024-07-15)   │
│ {{- end }}                                                    │
│ {{- end }}                                                    │
└────────────────────────────────────────────────────────────────┘

📊 Summary:
  - New temporary rule: 1
  - Applies to: gcom brand, qa stage ONLY
  - Expires: 2024-07-15
  - Lines added: 7

⚠️  WARNINGS:
  - This is a TEMPORARY rule
  - Affects QA environment only
  - Will NOT affect live environment
  - Expiration date: July 15, 2024

✅ Validation passed:
  ✓ Valid SPIFFE URI format
  ✓ Valid conditional syntax
  ✓ Correct brand mapping
  ✓ Valid role names
  ✓ Expiration documented

Ready to apply? (yes/no/modify)
```

### User Approves

```
Apply the changes. I'll follow up on RANT-6789 for removal.
```

### Skill Response - Phase 5: Apply

```
✨ Applying changes...

✅ Changes merged into helm-values/common.yml
✅ YAML syntax validated
✅ No errors detected

⏰ REMINDER SET:
   This rule expires: 2024-07-15
   Jira: RANT-6789
   Action: Remove before expiration

📝 Updated section:
   Location: QA-only conditional section
   
📊 Statistics:
   - Temporary rules: Now 3 (was 2)
   - Rules expiring soon: RANT-6789
   
💡 Important notes:
   ⚠️  This rule only exists in QA namespace
   ⚠️  Live environment is not affected
   ⚠️  Remember to remove after testing!
   ⚠️  Add to sprint cleanup tasks

✨ Complete! Remember to remove this rule by July 15, 2024.
```

---

## Example 5: Error Case - Invalid Input

### User Request

```
Add a rule with ROLE_INVALID_PERMISSION for service test-service
```

### Skill Response - Validation Error

```
❌ VALIDATION ERROR

I found an issue with your request:

  Role name not recognized: ROLE_INVALID_PERMISSION
  
Valid SPIFFE roles are:
  ✓ ROLE_POST_JWT
  ✓ ROLE_POST_DECODE_JWT
  ✓ ROLE_POST_INTROSPECT
  ✓ ROLE_POST_INTROSPECT_V1
  ✓ ROLE_POST_INTROSPECT_V2
  ✓ ROLE_POST_TOKEN_CREATE
  ✓ ROLE_POST_TOKEN_REVOCATION
  ✓ ROLE_POST_OAUTH2_TOKEN
  ✓ ROLE_POST_NO_ID_AUTH_LEGACY
  ✓ ROLE_POST_NO_ID_AUTH_GUID_AND_UAS_ACCOUNT_ID
  ✓ ROLE_POST_NO_ID_AUTH_CCGUID
  ✓ ROLE_ANONYMOUS

Did you mean one of these?
  - ROLE_POST_INTROSPECT_V2 (most common)
  - ROLE_POST_INTROSPECT
  
Or is this a custom role? If so, I'll need to:
  1. Confirm it's documented
  2. Add it to the known roles list
  3. Get approval from team lead

Please clarify or provide the correct role name.
```

---

## Example 6: Duplicate Detection

### User Request

```
Add spiffe rule for refreshtokenservice in poumo-oauth2 namespace
```

### Skill Response - Conflict Detection

```
⚠️  CONFLICT DETECTED

This rule already exists in the configuration:

Existing:
"[spiffe://cluster.local/ns/poumo-oauth2-{{ .Env.MAM_STAGE }}/sa/poumo-istio-refreshtokenservice-rest-{{ .Env.MAM_BRAND }}-{{ .Env.MAM_STAGE }}]":
  - ROLE_POST_TOKEN_CREATE
  - ROLE_POST_TOKEN_REVOCATION
  - ROLE_POST_JWT
  - ROLE_POST_DECODE_JWT

Did you want to:
  A) Add new roles to this existing rule?
  B) Create a NEW different rule (different service or namespace)?
  C) Replace this rule entirely?
  D) Cancel

Please choose:
```

---

## Common Workflow Tips

### Tip 1: Get Current State First

```
Before proposing a new rule, ask:
"Show me all existing rules for poma-notifications namespace"

The skill will list all current rules, helping you avoid duplicates.
```

### Tip 2: Use Jira References

```
Always include ticket references:
"Add rule for RANT-5678: new service X needs role Y"

This documents why the rule exists for future audits.
```

### Tip 3: Stage-Specific Rules

```
For QA-only testing:
"Add QA-only rule for testing, stage: qa only"

For live only:
"Add production rule, stage: live only"

This prevents accidents!
```

### Tip 4: Review Changes Before Committing

```
After applying, always:
1. git diff helm-values/common.yml
2. Review the exact changes
3. Test in dev environment
4. Then promote to prod
```

### Tip 5: Document Conditionals

```
When using conditionals, explain why:
"Add gcom-only rule because gmxint requires special auth flow"

This helps future maintainers understand the logic.
```

---

## Summary

The helm-spiffe-manager skill provides:

✅ **Intelligent parsing** of your requests
✅ **Automatic validation** of all inputs
✅ **Safe generation** of YAML rules
✅ **Clear diffs** before applying
✅ **Helpful error messages** when something's wrong
✅ **Guided workflow** with clarifying questions
✅ **Audit trail** with Jira references
✅ **Expiration tracking** for temporary rules

Use it to safely and confidently manage your SPIFFE configuration!
