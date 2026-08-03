# Quick Reference Card

## One-Page Reference Guide for Code Reviews

### Review Dimensions

| Dimension | Focus | Target Score |
|-----------|-------|---------------|
| **Documentation** | Docstrings, type hints, comments | 40 pts |
| **Security** | Input validation, injection, data protection | 30 pts |
| **Performance** | Algorithm complexity, optimization | 20 pts |
| **Maintainability** | Simplicity, clarity, naming | 10 pts |
| **Testing** | Coverage, edge cases | 40 pts (optional) |

**Production Ready: 90% (135/150 points)**

---

## NASA Principles (10 Rules)

1. **Simplicity** - Restrict global variables, pointers, recursion
2. **Fail-Safe** - Check all inputs, handle all errors explicitly
3. **Scope** - Keep functions small (10-20 lines), complexity ≤ 10
4. **Input** - Validate all untrusted data
5. **Errors** - Catch exceptions explicitly, never silent fails
6. **Resources** - Auto-cleanup with try/finally or context managers
7. **Defense** - Copy mutable data, verify before use
8. **SRP** - Each function/class has one responsibility
9. **Globals** - Avoid global state; pass explicitly
10. **Testing** - 100% coverage of all paths including errors

---

## Security Checklist - Quick Version

- [ ] All inputs validated (type, range, format)
- [ ] No SQL concatenation (use parameterized queries)
- [ ] Auth on protected endpoints
- [ ] Sensitive data encrypted
- [ ] No credentials in code
- [ ] Error messages don't leak info
- [ ] Sensitive data not logged
- [ ] Specific exceptions caught (no bare except)

**Score: 8/8 = Ready**

---

## Code Smells - 10 Most Critical

1. **Duplicated Code** → Extract to function
2. **Long Methods** → Break into smaller functions
3. **Complex Conditionals** → Extract methods, use guards
4. **Magic Numbers** → Use named constants
5. **Long Parameter Lists** → Create config object
6. **Poorly Named** → Use clear, descriptive names
7. **Comments Explaining Bad Code** → Improve code instead
8. **No Error Handling** → Catch/validate/report
9. **Global State** → Pass as parameters
10. **No Tests** → Write tests for all paths

---

## Common Critical Issues

🔴 **STOP - Fix Before Production:**
- SQL/Command injection
- Hardcoded secrets
- No input validation
- Silent error handling
- XXE vulnerabilities
- Unencrypted sensitive data

🟡 **Address Before Merge:**
- Missing docstrings
- No type hints
- Insufficient error handling
- High cyclomatic complexity
- No tests

---

## Function Audit (5 minutes)

Ask these questions:

1. **Does it do ONE thing?** Yes / No
2. **Is it < 20 lines?** Yes / No
3. **Are all inputs validated?** Yes / No
4. **Are exceptions caught explicitly?** Yes / No
5. **Are resources auto-cleaned?** Yes / No

**All YES = Good function**

---

## Documentation Audit (3 minutes)

- [ ] Docstring: What does it do?
- [ ] Parameters: Types and descriptions?
- [ ] Returns: Type and description?
- [ ] Raises: Exceptions and when?
- [ ] Examples: Working example?

---

## Testing Audit (2 minutes)

- [ ] Happy path tested? Yes / No
- [ ] All errors tested? Yes / No
- [ ] Edge cases tested? Yes / No
- [ ] Coverage ≥ 80%? Yes / No

---

## Review Time Estimates

| Task | Time |
|------|------|
| Quick scan | 5 min |
| Standard review | 15-20 min |
| Deep review | 30-45 min |
| With examples | +10 min |
| Testing setup | +15 min |

---

## Command Cheat Sheet

```bash
# Quick review
/skill:senior-code-reviewer file.py

# Deep security review
/skill:senior-code-reviewer file.py --focus security --deep

# With examples
/skill:senior-code-reviewer file.py --with-examples

# Strict NASA standards
/skill:senior-code-reviewer file.py --strict

# Format as JSON
/skill:senior-code-reviewer file.py --format json

# Compare versions
/skill:senior-code-reviewer --compare old.py new.py
```

---

## Issue Severity Matrix

|  | Critical | High | Medium | Low |
|---|----------|------|--------|-----|
| **Security** | Injection | Validation gap | Auth logic | Audit info |
| **Performance** | O(n²) loop | Inefficient algo | Redundant | Minor opt |
| **Docs** | Missing input | No types | Unclear | Style |
| **Quality** | Crash | Wrong result | Confusing | Messy |

---

## Production Readiness Checklist

- [ ] All CRITICAL issues fixed
- [ ] Input validation complete
- [ ] Error handling explicit
- [ ] Security review passed
- [ ] Type hints present
- [ ] Docstrings complete
- [ ] Tests ≥ 80% coverage
- [ ] No hardcoded secrets
- [ ] Performance acceptable
- [ ] Code approved by reviewer

**Ready to Deploy: ✅**

---

## Reference Document Map

- **Getting Started:** README.md
- **NASA Standards:** nasa-guidelines.md
- **Security:** security-best-practices.md
- **Code Smells:** code-smells.md
- **Clean Code:** clean-code-principles.md
- **Python:** python-review.md
- **Examples:** templates/python-class-review.md
- **Checklist:** code-review-checklist.md

---

## Common Questions

**Q: How long should a function be?**
A: 10-20 lines maximum

**Q: What's good test coverage?**
A: Minimum 80%, target 95-100%

**Q: What's acceptable complexity?**
A: Cyclomatic complexity ≤ 10

**Q: Do I need type hints?**
A: Yes, for production code

**Q: What about comments?**
A: Explain WHY, not WHAT. Code should be self-explanatory.

---

## Emergency Fixes (If Behind Schedule)

1. **Fix CRITICAL security issues** (non-negotiable)
2. **Add input validation** (prevent crashes)
3. **Add docstrings** to public functions
4. **Add basic error handling**
5. **Write happy-path tests**

**Then schedule follow-up:** Code review, full testing, refactoring

---

See full documentation in References section.
