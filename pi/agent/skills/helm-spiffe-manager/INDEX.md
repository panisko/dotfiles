# 📑 Helm SPIFFE Manager - Documentation Index

## 🚀 Start Here

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [README_START_HERE.md](README_START_HERE.md) | **Entry point** - Quick start guide | 5 min |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | **Cheat sheet** - Common tasks & templates | 5 min |
| [USAGE_DEMOS.md](USAGE_DEMOS.md) | **Examples** - 6 realistic scenarios | 10 min |

---

## 📚 Learn More

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [SKILL.md](SKILL.md) | **Definition** - Skill capabilities & protocol | 5 min |
| [README.md](README.md) | **Guide** - How the skill works (5-phase workflow) | 10 min |
| [IMPLEMENTATION.md](IMPLEMENTATION.md) | **Technical** - Architecture & integration | 15 min |
| [CONFIGURATION_REFERENCE.md](CONFIGURATION_REFERENCE.md) | **Reference** - Current config analysis | Reference |

---

## 🛠️ Tool Reference

| File | Purpose |
|------|---------|
| [helm_spiffe_manager.py](helm_spiffe_manager.py) | Python CLI tool (executable) |

---

## 📖 Reading Paths

### ⚡ Fast Track (15 minutes)
1. README_START_HERE.md
2. QUICK_REFERENCE.md
3. Try your first rule

### 📚 Complete Learning (45 minutes)
1. README_START_HERE.md
2. QUICK_REFERENCE.md
3. USAGE_DEMOS.md (all 6 examples)
4. CONFIGURATION_REFERENCE.md (skim)
5. Try your first rule

### 🔬 Deep Dive (90 minutes)
1. All of "Complete Learning" path
2. README.md (full)
3. IMPLEMENTATION.md (full)
4. SKILL.md (full)
5. CONFIGURATION_REFERENCE.md (full)
6. Understand Python tool

---

## 🎯 Find What You Need

**"I want to..."** | **Read this** | **Time**
---|---|---
Add a new SPIFFE rule | USAGE_DEMOS.md #1 + QUICK_REFERENCE.md | 5 min
Add brand-specific rule | USAGE_DEMOS.md #2 + CONFIGURATION_REFERENCE.md | 10 min
Update existing rule | USAGE_DEMOS.md #3 | 5 min
Understand my config | CONFIGURATION_REFERENCE.md | 10 min
Understand how it works | README.md + SKILL.md | 20 min
Debug an error | QUICK_REFERENCE.md (errors) + USAGE_DEMOS.md #5-6 | 5 min
See all examples | USAGE_DEMOS.md | 15 min
Get technical details | IMPLEMENTATION.md | 15 min

---

## ✨ Key Features

### Add Rules
- ✅ For all brands & stages
- ✅ For specific brands
- ✅ For specific stages
- ✅ With complex conditionals

### Update Rules
- ✅ Add roles to existing rules
- ✅ Modify conditionals
- ✅ Add documentation

### Safety First
- ✅ Validate SPIFFE IDs
- ✅ Validate role names
- ✅ Detect duplicates
- ✅ Show diffs before applying
- ✅ Ask for confirmation

### Intelligence
- ✅ Understand natural language
- ✅ Ask clarifying questions
- ✅ Suggest placement
- ✅ Handle brand mappings
- ✅ Respect conditionals

---

## 📊 Quick Stats

**Current Configuration:**
- Total SPIFFE Rules: **183**
- Supported Brands: **6** (acc, gmx, gcom, mcom, uli, webde)
- Supported Stages: **2** (qa/dev, live/prelive)
- Service Categories: **14**
- Valid Roles: **12+** variants

**Skill Implementation:**
- Lines of code: **430+**
- Documentation pages: **8**
- Total documentation: **88 KB**
- External dependencies: **None**

---

## 🎓 Learning Objectives

After reading this documentation, you'll understand:

- ✅ How to use the helm-spiffe-manager skill
- ✅ SPIFFE configuration structure
- ✅ Brand & stage patterns
- ✅ How to add/update/remove rules
- ✅ Validation requirements
- ✅ Common error handling
- ✅ Best practices

---

## 💡 Quick Reference: Valid Values

**Brands:** acc, gmx, gcom, mcom, uli, webde

**Stages:** qa (dev), live (prelive)

**Roles:** ROLE_POST_JWT, ROLE_POST_DECODE_JWT, ROLE_POST_INTROSPECT, 
ROLE_POST_INTROSPECT_V1, ROLE_POST_INTROSPECT_V2, ROLE_POST_TOKEN_CREATE,
ROLE_POST_TOKEN_REVOCATION, ROLE_POST_OAUTH2_TOKEN, ROLE_POST_NO_ID_AUTH_*,
ROLE_ANONYMOUS

---

## 🚀 Get Started

1. **Read:** README_START_HERE.md (5 min)
2. **Learn:** USAGE_DEMOS.md example #1 (5 min)
3. **Try:** Use the skill with:
   ```
   /skill:helm-spiffe-manager Add a test spiffe rule for demo-service 
                               in poma-demo namespace with 
                               ROLE_POST_INTROSPECT_V2 for all brands
   ```

---

## 📞 Support

**Documentation organized by:**
- **Getting started:** README_START_HERE.md
- **Common tasks:** QUICK_REFERENCE.md
- **Examples:** USAGE_DEMOS.md
- **Reference:** CONFIGURATION_REFERENCE.md
- **Details:** README.md, SKILL.md, IMPLEMENTATION.md

**Each document has:**
- Clear structure & headings
- Table of contents
- Cross-references
- Examples
- Troubleshooting sections

---

## 📋 File Manifest

```
helm-spiffe-manager/
├── INDEX.md                         ← You are here
├── README_START_HERE.md             ← Start here
├── QUICK_REFERENCE.md               ← Cheat sheet
├── USAGE_DEMOS.md                   ← 6 examples
├── CONFIGURATION_REFERENCE.md       ← Config analysis
├── README.md                        ← Full guide
├── SKILL.md                         ← Skill definition
├── IMPLEMENTATION.md                ← Technical details
└── helm_spiffe_manager.py           ← Python tool
```

---

## ✅ Verification

The skill is **ready to use**:
- ✅ All files created
- ✅ Python tool tested (183 rules parsed)
- ✅ Validation working
- ✅ Documentation complete
- ✅ No external dependencies

**Location:** `/Users/panisko/.pi/agent/skills/helm-spiffe-manager/`

---

## 🎉 Next Step

→ Read **[README_START_HERE.md](README_START_HERE.md)** (5 minutes)

Good luck! 🚀
