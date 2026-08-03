# 🚀 Helm SPIFFE Manager - Start Here

**Welcome!** This skill helps you safely manage SPIFFE identity configuration in `helm-values/common.yml`.

## ⚡ Quick Start (2 minutes)

### 1. Understand What This Is

The `helm-spiffe-manager` skill is a **SPIFFE configuration assistant**. It helps you:
- ✅ Add new SPIFFE rules
- ✅ Update existing rules  
- ✅ Remove deprecated rules
- ✅ Handle complex brand/stage conditionals
- ✅ Validate everything before applying

### 2. Use It Now

In Pi, just ask:

```
/skill:helm-spiffe-manager Add a spiffe rule for 'my-new-service' 
in the poma-services namespace with ROLE_POST_INTROSPECT_V2 
for all brands
```

That's it! The skill will:
1. Ask clarifying questions if needed
2. Show you what it will change (diff view)
3. Wait for your approval
4. Apply when you say "yes"

### 3. See What You're Dealing With

Current configuration has:
- **183 SPIFFE rules** already defined
- **6 brands** supported (acc, gmx, gcom, mcom, uli, webde)
- **2 stages** (qa/dev and live/prelive)
- **Complex conditionals** for brand/stage combinations

## 📚 Documentation

Read these files in order:

### For Using the Skill:
1. **QUICK_REFERENCE.md** (5 min read)
   - Common tasks with templates
   - Error reference
   - Tips & tricks

2. **USAGE_DEMOS.md** (10 min read)
   - 6 realistic examples
   - What the skill outputs
   - Error handling

### For Understanding Your Config:
3. **CONFIGURATION_REFERENCE.md** (reference)
   - All 14 service categories
   - Brand-specific rules
   - Common patterns
   - Current structure

### For Deep Dives:
4. **README.md** (detailed guide)
   - How the skill works (5 phases)
   - All supported roles
   - All brand mappings
   - Validation rules

5. **SKILL.md** (skill definition)
   - Communication protocol
   - Configuration formats
   - Best practices

6. **IMPLEMENTATION.md** (technical)
   - Architecture details
   - Integration with Pi
   - Testing

## 🎯 Common Tasks

### Add a Rule (All Brands & Stages)
```
Add spiffe for [SERVICE] in [NAMESPACE] namespace 
with roles [ROLE1], [ROLE2]
```

### Add Brand-Specific Rule
```
Add spiffe for [SERVICE] in [NAMESPACE]
for [BRAND] brand only with [ROLE]
```

### Update Existing Rule
```
Add [ROLE] to existing [SERVICE] in [NAMESPACE]
```

### Test/Debug Only (QA)
```
Add temporary spiffe rule for QA testing
service: [NAME], roles: [ROLES]
stage: qa only
reference: [JIRA]
```

## ✅ Checklist Before Using

Before making a request, verify:
- [ ] Service name is correct
- [ ] Namespace follows pattern (e.g., `poma-service-{stage}`)
- [ ] Role is valid (see QUICK_REFERENCE.md)
- [ ] Brand name is correct (acc, gmx, gcom, mcom, uli, webde)
- [ ] You understand if it's conditional or universal
- [ ] Have a Jira reference (for documentation)

## ⚠️ Important Notes

**DO:**
- ✅ Ask clarifying questions
- ✅ Review diffs carefully
- ✅ Test in QA first
- ✅ Add Jira references
- ✅ Document why rules exist

**DON'T:**
- ❌ Add rules without understanding the pattern
- ❌ Use invalid role names
- ❌ Apply to live without testing QA first
- ❌ Remove rules without confirmation
- ❌ Ignore validation errors

## 🔍 Validation Quick Reference

**Valid Brands:**
- acc, gmx, gcom, mcom, uli, webde

**Valid Stages:**
- qa (maps to dev), live (maps to prelive)

**Valid Roles:**
- ROLE_POST_JWT
- ROLE_POST_DECODE_JWT
- ROLE_POST_INTROSPECT
- ROLE_POST_INTROSPECT_V1
- ROLE_POST_INTROSPECT_V2
- ROLE_POST_TOKEN_CREATE
- ROLE_POST_TOKEN_REVOCATION
- ROLE_POST_OAUTH2_TOKEN
- ROLE_POST_NO_ID_AUTH_*
- ROLE_ANONYMOUS

## 📞 Support

**Stuck?** Read these in order:
1. **QUICK_REFERENCE.md** - Error reference section
2. **USAGE_DEMOS.md** - Find similar example
3. **CONFIGURATION_REFERENCE.md** - Check current patterns

**Questions?**
- "What's the current structure?" → CONFIGURATION_REFERENCE.md
- "How do I do X?" → QUICK_REFERENCE.md or USAGE_DEMOS.md
- "How does it work?" → README.md
- "What are the rules?" → SKILL.md

## 🎓 Learning Path

**5-minute intro:**
```
1. Read this file (README_START_HERE.md)
2. Read QUICK_REFERENCE.md
3. Try one simple example
```

**30-minute mastery:**
```
1. Read USAGE_DEMOS.md (all 6 examples)
2. Read QUICK_REFERENCE.md (all sections)
3. Review CONFIGURATION_REFERENCE.md (at least section headers)
4. Try adding a rule for your service
```

**Expert level:**
```
1. Read all documentation
2. Review IMPLEMENTATION.md
3. Understand the Python tool
4. Help others with complex patterns
```

## 🚀 Try Your First Change

**Example: Add analytics service**

```
/skill:helm-spiffe-manager Add spiffe rule for analytics-service 
in poma-analytics namespace with ROLE_POST_INTROSPECT_V2 
for all brands
```

**Expected interaction:**
```
Skill: ✅ I'll add this rule to all brands and stages.
       Ready to review the change?

You: Yes

Skill: [Shows diff with new rule]
       Apply? (yes/no/modify)

You: yes

Skill: ✨ Complete! Rule added to helm-values/common.yml
```

## 📋 File Structure

```
/Users/panisko/.pi/agent/skills/helm-spiffe-manager/
│
├── README_START_HERE.md              ← YOU ARE HERE
├── QUICK_REFERENCE.md                ← Next: Common tasks
├── USAGE_DEMOS.md                    ← Then: Real examples
├── CONFIGURATION_REFERENCE.md        ← Reference: Current config
├── README.md                         ← Details: How it all works
├── SKILL.md                          ← Protocol: Communication rules
├── IMPLEMENTATION.md                 ← Technical: Architecture
│
└── helm_spiffe_manager.py            ← Python tool (CLI)
```

## 💡 Pro Tips

**Tip 1:** Always provide Jira reference
```
Add rule for RANT-5678: new service needs auth
```

**Tip 2:** Ask for help with ambiguous requests
```
Should this apply to all brands or just gmx?
```

**Tip 3:** Review diffs carefully before applying
```
Show me the change first - don't apply yet
```

**Tip 4:** Test in QA before going to production
```
Add to qa environment first
```

**Tip 5:** Use comments for complex conditionals
```
Add reason/JIRA reference for conditional logic
```

## 🎯 Your Next Steps

1. **Read QUICK_REFERENCE.md** (5 minutes)
2. **Review USAGE_DEMOS.md** example #1 (5 minutes)
3. **Try your first rule addition** (2 minutes)
4. **Read CONFIGURATION_REFERENCE.md** when you need to understand patterns

---

**Ready?** Let's go! Ask the skill for your first change:

```
/skill:helm-spiffe-manager [your request]
```

Good luck! 🚀
