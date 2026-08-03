# SPIFFE Configuration Reference

## Current Configuration Analysis

This document captures the existing SPIFFE rules in `helm-values/common.yml` for reference when adding new rules.

### Extracted from common.yml

**Last Updated**: June 2024
**Total SPIFFE Rules**: ~80+ individual rules
**Brands Supported**: acc, gmx, gcom, mcom, uli, webde
**Stages**: qa (dev), live (prelive)

---

## Service Namespaces by Category

### 1. User Management & Authentication

#### poumo-oauth2-{stage}
**Services:**
- refreshtokenservice (Token refresh)
- ums-securitytokenservice (Security tokens)

**Pattern:**
```yaml
"[spiffe://cluster.local/ns/poumo-oauth2-{{ .Env.MAM_STAGE }}/sa/...]":
  - ROLE_POST_TOKEN_CREATE
  - ROLE_POST_TOKEN_REVOCATION
  - ROLE_POST_JWT
  - ROLE_POST_DECODE_JWT
```

#### poumo-ums-{stage}
**Services:**
- ums-loginservice (User login)
- ums-credentialstore → account-management-facade (Account mgmt)

**Roles:**
- JWT operations (JWT, DECODE_JWT)
- Introspection (INTROSPECT_V2)
- Credential management

#### poumo-passport-{stage}
**Services:**
- passportservice-rest

**Roles:**
- ROLE_POST_INTROSPECT_V2

#### poumo-ums-credentialstore-{stage}
**Services:**
- account-management-facade-rest

**Roles:**
- ROLE_POST_INTROSPECT_V2

---

### 2. Password & Security Management

#### poumo-password-change (Conditional: not acc)
**Services:**
- password-change-{brandmappoma}-{stage}-sa

**Conditional:**
```yaml
{{- if ne .Env.MAM_BRAND "acc" }}
"[spiffe://cluster.local/ns/poumo-password-change/sa/password-change-{{ (index $brandMappoma .Env.MAM_BRAND | default .Env.MAM_BRAND) }}-{{ .Env.MAM_STAGE }}-sa]":
  - ROLE_POST_JWT
  - ROLE_POST_DECODE_JWT
  - ROLE_POST_INTROSPECT_V2
{{- end }}
```

#### poumo-securitycontacts-{stage}
**Services:**
- security-contact-admin-bff-rest

**Roles:**
- ROLE_POST_JWT
- ROLE_POST_DECODE_JWT
- ROLE_POST_INTROSPECT_V2

#### poumo-account-recovery-assistant-{stage}
**Services:**
- account-recovery-assistant

**Roles:**
- ROLE_POST_JWT
- ROLE_POST_DECODE_JWT

---

### 3. Mail & Webmailer Services

#### poma-webmailer-{stage}
**Services:**
- webmailer-compose-graphql (multi-brand)
- webmailer-mailboss (conditional stages)
- webmailer-cats-1and1 (specific)
- poma-istio-download-service

**Special Staging Rules:**
- `poma-webmailer-dev` (qa only)
- `poma-webmailer-prelive` (live only)
- `poma-webmailer-qa` (qa only)

**Roles:**
- ROLE_POST_INTROSPECT
- ROLE_POST_INTROSPECT_V1
- ROLE_POST_INTROSPECT_V2

---

### 4. Smart Inbox & Tracking

#### poma-smartinbox-{stage}
**Services:**
- poma-istio-track-and-trace-account-service (fe, fec variants)

**Conditional:** Only for webde and gmx brands

**Roles:**
- ROLE_POST_INTROSPECT

#### poma-alerts-{stage}
**Services:**
- poma-istio-alerts-processing-service

**Conditional:** Only for webde and gmx brands

**Roles:**
- ROLE_POST_INTROSPECT

**Special Staging:**
- `poma-alerts-dev` (qa only)
- `poma-alerts-prelive` (live only)

#### dpo-tracking-gateway-{stage}
**Services:**
- tracking-gateway-{brandmap}-{stage}

**Special:** Multiple tracking-gateway variants per brand (gmxat, gmxch, etc.)

**Roles:**
- ROLE_POST_INTROSPECT_V2

**Special Staging:**
- `dpo-tracking-gateway-dev` (qa only)
- `dpo-tracking-gateway-pilot` (live only)
- `dpo-tracking-gateway-prelive` (live only)

---

### 5. Message/Mail Flow Services

#### poma-sid2-{stage}
**Services:**
- confix-{brandmappoma}-{stage}-sa
- poma-istio-smart-search-middleware (multiple variants)
- poma-istio-contract-middleware-manni
- poma-istio-smart-action-service

**Special Staging:**
- `poma-sid2-dev` (qa only)
- `poma-sid2-prelive` (live only)

**Multi-brand Support:**
- gcom has gmxes, gmxfr, gmxcouk variants
- Each brand has standard + variant

**Roles:**
- ROLE_POST_INTROSPECT
- ROLE_POST_INTROSPECT_V2

---

### 6. Mobile Services

#### pocam-android-{stage}
#### pocam-ios-{stage}
**Services:**
- config-set-service-{os}-{brand}-{stage}

**Special Environments:**
- `pocam-android-qa`, `pocam-android-dev`
- `pocam-ios-qa`, `pocam-ios-dev`
- `pocam-android-prelive`, `pocam-android-live`
- `pocam-ios-prelive`, `pocam-ios-live`

**Roles:**
- ROLE_POST_INTROSPECT_V2

---

### 7. Portal & E-Commerce

#### pocam-customernotification-{stage}
**Services:**
- cnp-subscription-internal-{brand}-{stage}
- cnp-subscription-external-{brand}-{stage}

**Special Staging:**
- `pocam-customernotification-dev` (qa only - "any")
- `pocam-customernotification-qa` (qa only - specific brands)
- `pocam-customernotification-live` (live only)

**Roles:**
- ROLE_POST_INTROSPECT_V2

#### bso-portalsubscriptions-{stage}
**Services:**
- age-verification-service
- hermes-partner-shop

**Special Variants (qa):**
- hermes-partner-shop-qa, hermes-partner-shop-ac1

**Roles:**
- ROLE_POST_INTROSPECT_V2

#### bso-mobilesales-{stage}
**Services:**
- in-app-products-facade
- entry-points-facade

**Special Staging:**
- `bso-mobilesales-dev` (qa only)
- `bso-mobilesales-qa` (qa only - entry-points-facade-ac1, -entry-points-facade)
- `bso-mobilesales-live` (live only)

**Roles:**
- ROLE_POST_INTROSPECT_V2

---

### 8. Data & Configuration Services

#### poumo-um-data-facade-{stage}
**Services:**
- um-data-facade-{brandmappoma}-{stage}

**Multi-brand Support:**
- um-data-facade-gmxnet-{stage}
- um-data-facade-webde-{stage}
- um-data-facade-gmxcom-{stage}
- um-data-facade-mailcom-{stage}

**Special (acc brand):**
- um-1and1-datafacade-1and1access-{stage}

**Roles:**
- ROLE_POST_INTROSPECT_V2

#### poma-navigator-{stage}
**Services:**
- config-set-service-{brandmapsecuretoken}-{stage}

**Conditional:** Not uli, not acc

**Special Staging:**
- `poma-navigator-prelive` (live only)

**Roles:**
- ROLE_POST_INTROSPECT_V2

#### popp-mdh-frontend-{stage}
**Services:**
- settings-cats-{brandmapsecuretoken}-{stage}

**Conditional:** Not uli, not acc

**Special Staging:**
- `popp-mdh-frontend-prelive` (live only)

**Roles:**
- ROLE_POST_INTROSPECT_V2

---

### 9. Infrastructure & Platform Services

#### pocam-infrastructurecomponents-{stage}
**Services:**
- pocam-istio-hsp2-serviceaccount
- pocam-istio-pacs2-serviceaccount
- spellcheck-http-service-{brandmap}-{stage}

**Special (live):**
- `pocam-infrastructurecomponents-1and1` (no stage suffix)

**Roles:**
- ROLE_POST_INTROSPECT_V2

#### storageservices-restfs-gateway-{stage}
**Services:**
- storageservices-istio-restfs-gateway-web-{brandmap}-{stage}

**Special Staging:**
- `storageservices-restfs-gateway-prelive` (live only)

**Roles:**
- ROLE_POST_INTROSPECT_V2

#### poma-corelab-{stage}
**Services:**
- corelab-istio-client-signal-service-{brandmap}-{stage}

**Conditional:** Not webde, not gmx

**Roles:**
- ROLE_POST_INTROSPECT_V2

---

### 10. Regulation & Compliance

#### posas-accsec-{stage}
**Services:**
- obligation-generator-{brand}-{stage}

**Multi-brand Support:**
- Standard brand rules
- Special gcom rule for gmxcom variant
- Special mcom rule for mailcom variant

**Roles:**
- ROLE_POST_INTROSPECT_V2
- ROLE_POST_JWT
- ROLE_POST_DECODE_JWT

---

### 11. Account/Access Control Services

#### poumo-accesscontrolservice-{stage}
**Services:**
- poumo-istio-accesscontrolservice-rest-{brand}-weblogin-{stage}
- poumo-istio-accesscontrolservice-rest-{brand}-other-{stage}

**Roles:**
- ROLE_POST_INTROSPECT_V2

---

### 12. Bootstrap & Infrastructure Services

#### poumo-1reg-bootstrap-{stage}
**Services:**
- poumo-istio-reg-bundle-{brandmappoma}-{stage}

**Special (gcom):**
- poumo-istio-reg-bundle-gmxes-{stage}
- poumo-istio-reg-bundle-gmxfr-{stage}
- poumo-istio-reg-bundle-gmxcouk-{stage}

**Roles:**
- ROLE_POST_OAUTH2_TOKEN

---

### 13. Mail Flow Services

#### mf-sct-services-{stage}
**Services:**
- sct-mail-targeting-service-{brandmap}-{stage}

**Special Staging:**
- `mf-sct-services-dev` (qa only)
- `mf-sct-services-prelive` (live only)

**Roles:**
- ROLE_POST_INTROSPECT_V2

---

### 14. Calendar & Webmailer (Stage/Brand Conditional)

#### popp-calendar-{stage}
**Services:**
- calendar-{brandmap}-{stage}-sa

**Conditional:** Not uli

**Special Staging:**
- `popp-calendar-dev` (qa only)
- `popp-calendar-prelive` (live only)

**Roles:**
- ROLE_POST_INTROSPECT_V2

---

## Brand-Specific Rules

### Brand: gmx
- **Extra services:** tracking-gateway-gmxat, tracking-gateway-gmxch
- **Special namespace:** dpo-tracking-gateway specific rules
- **Conditional:** Used in `or (eq .Env.MAM_BRAND "webde") (eq .Env.MAM_BRAND "gmx")`

### Brand: gcom
- **Multi-region:** gmxcom, gmxes, gmxfr, gmxcouk variants
- **Extra rules:** Multiple entries for each region
- **Conditional:** Special handling in poumo-1reg-bootstrap, poma-sid2

### Brand: acc
- **Special services:** 1and1 specific variants
- **Exclusion:** Excluded from password-change rules (ne acc)
- **Special mapping:** 1and1access for securetoken services

### Brand: uli
- **Limited services:** Fewer rules than other brands
- **Exclusion:** Not included in some services (ne uli)

### Brand: webde
- **Grouped with gmx:** Often combined in conditionals (or webde gmx)

### Brand: mcom
- **Special handling:** dc-specific workarounds in some cases

---

## Common Patterns

### Pattern 1: Universal Rule (All Brands & Stages)
```yaml
"[spiffe://cluster.local/ns/poma-service-{{ .Env.MAM_STAGE }}/sa/service-{{ (index $brandMappoma .Env.MAM_BRAND | default .Env.MAM_BRAND) }}-{{ .Env.MAM_STAGE }}-sa]":
  - ROLE_POST_INTROSPECT_V2
```

### Pattern 2: Stage-Conditional (QA Only)
```yaml
{{- if eq .Env.MAM_STAGE "qa" }}
"[spiffe://cluster.local/ns/poma-service-dev/sa/service-dev-sa]":
  - ROLE_POST_INTROSPECT_V2
{{- end }}
```

### Pattern 3: Brand-Conditional
```yaml
{{- if eq .Env.MAM_BRAND "gcom" }}
"[spiffe://cluster.local/ns/poma-service/sa/service-gmxes-sa]":
  - ROLE_POST_INTROSPECT_V2
{{- end }}
```

### Pattern 4: Both Brand & Stage Conditional
```yaml
{{- if and (eq .Env.MAM_BRAND "acc") (eq .Env.MAM_STAGE "qa") }}
"[spiffe://cluster.local/ns/poma-service-dev/sa/service-1and1-dev-sa]":
  - ROLE_POST_INTROSPECT_V2
{{- end }}
```

### Pattern 5: Multiple Brand OR
```yaml
{{- if or ( eq .Env.MAM_BRAND "webde") ( eq .Env.MAM_BRAND "gmx") }}
"[spiffe://cluster.local/ns/poma-service-{{ .Env.MAM_STAGE }}/sa/service-{{ (index $brandMap .Env.MAM_BRAND | default .Env.MAM_BRAND) }}-{{ .Env.MAM_STAGE }}]":
  - ROLE_POST_INTROSPECT
{{- end }}
```

---

## Key Templates & Variables

### Available Brand Maps
```
$brandMappoma   - POMA services (most services)
$brandMap       - MAP/tracking services
$brandMapsecuretoken - SecureToken services (limited brands)
```

### Environment Variables
```
{{ .Env.MAM_BRAND }}     - Brand: acc, gmx, gcom, mcom, uli, webde
{{ .Env.MAM_STAGE }}     - Stage: qa or live
{{ .Env.MAM_DC }}        - Data center (if needed)
```

### Namespace Patterns
```
{service}-{{ .Env.MAM_STAGE }}              - Stage-aware
{service}-dev / {service}-prelive           - Explicit stage
{service}                                    - Static
```

---

## Adding New Rules: Quick Checklist

- [ ] Identify target namespace pattern
- [ ] Determine brand scope (all or specific?)
- [ ] Determine stage scope (all or specific?)
- [ ] Check for existing brand mappings
- [ ] Select appropriate $brandMap if needed
- [ ] Choose role(s) from known list
- [ ] Wrap in conditionals if needed
- [ ] Add comment for tricky logic
- [ ] Validate against current config
- [ ] Test proposed change
