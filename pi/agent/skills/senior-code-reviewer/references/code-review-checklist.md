# Code Review Checklist

Use this comprehensive checklist to assess code readiness for production.

## 1. Documentation (40 points)

### Function/Method Documentation
- [ ] **Public functions have docstrings** (5 pts) - Every public function/method should have a docstring explaining purpose, arguments, return values, and exceptions
- [ ] **Complex logic is commented** (5 pts) - Non-obvious algorithms or business logic should have explanatory comments
- [ ] **Type hints present** (5 pts) - All parameters and return values should have type annotations
- [ ] **Edge cases documented** (5 pts) - Document boundary conditions and special cases (e.g., null handling, empty collections)
- [ ] **Exceptions documented** (5 pts) - Document all exceptions that can be raised and why

### Module/Class Documentation
- [ ] **Module docstring exists** (5 pts) - Overview of the module's purpose
- [ ] **Class docstring exists** (5 pts) - Explain the class's responsibility and usage

### README & Examples
- [ ] **Usage examples provided** (3 pts) - Show how to use the code/API
- [ ] **README is clear** (2 pts) - First-time user can understand purpose and usage

**Score:** __/40

## 2. Security (30 points)

### Input Validation
- [ ] **All external inputs validated** (5 pts) - Check type, range, format, length of all user/external input
- [ ] **No SQL injection** (5 pts) - Use parameterized queries; never string-concatenate SQL
- [ ] **No command injection** (3 pts) - Avoid shell commands with user input; use process APIs
- [ ] **Path traversal protected** (3 pts) - Validate file paths; prevent ../../../etc/passwd attacks
- [ ] **No XXE vulnerabilities** (2 pts) - Disable XML external entities if parsing XML
- [ ] **No CSRF tokens needed** (2 pts) - (If applicable) Verify CSRF protection for state-changing operations

### Data Protection
- [ ] **Sensitive data encrypted** (2 pts) - Passwords, tokens, PII should be encrypted at rest
- [ ] **No credentials in code** (2 pts) - Use environment variables or secure vaults
- [ ] **No sensitive info in logs** (2 pts) - Don't log passwords, tokens, or PII
- [ ] **Secure defaults** (2 pts) - Security-sensitive settings default to secure values

**Score:** __/30

## 3. Performance (20 points)

### Algorithm Efficiency
- [ ] **No O(n²) in hot paths** (5 pts) - Avoid nested loops over large collections
- [ ] **Correct data structures** (5 pts) - Use appropriate collections (dict vs list, set vs list, etc.)
- [ ] **No unnecessary allocations** (3 pts) - Avoid creating objects in loops when possible
- [ ] **Caching used appropriately** (3 pts) - Cache results of expensive operations
- [ ] **Database queries optimized** (4 pts) - No N+1 queries; use pagination for large result sets

**Score:** __/20

## 4. Maintainability (10 points)

### Code Quality
- [ ] **Functions < 20 lines** (3 pts) - Long functions are harder to understand and test
- [ ] **Cyclomatic complexity ≤ 10** (3 pts) - Too many branches makes testing difficult
- [ ] **Clear naming conventions** (2 pts) - Variable/function names clearly indicate purpose
- [ ] **DRY principle followed** (2 pts) - No significant code duplication

**Score:** __/10

## 5. Testing (40 points - Optional but Recommended)

### Coverage
- [ ] **Unit tests exist** (10 pts) - At least 70% code coverage
- [ ] **Happy path tested** (10 pts) - Main functionality works as expected
- [ ] **Error paths tested** (10 pts) - Exception handling is tested
- [ ] **Edge cases tested** (5 pts) - Boundary conditions covered (empty input, null, max values)
- [ ] **Integration tests exist** (5 pts) - (If applicable) Components work together correctly

**Score:** __/40

## 6. Error Handling (10 points)

### Exception Safety
- [ ] **No bare except:** (3 pts) - Specific exceptions caught, not all exceptions ignored
- [ ] **No silent failures** (3 pts) - All errors either handled or logged
- [ ] **Meaningful error messages** (2 pts) - Errors explain what went wrong
- [ ] **Resources cleaned up** (2 pts) - Resources released even when errors occur

**Score:** __/10

---

## Production Readiness Score

Add up all scores:

- Documentation: __/40
- Security: __/30
- Performance: __/20
- Maintainability: __/10
- Testing: __/40
- Error Handling: __/10

**TOTAL: __/150**

### Thresholds

- **135-150 (90-100%)**: ✅ **Ready for Production** - High quality, well-tested
- **120-134 (80-89%)**: ⚠️ **Good - Minor Issues** - Ready with recommendations addressed
- **105-119 (70-79%)**: 🔴 **Needs Work** - Major issues must be addressed before production
- **< 105 (< 70%)**: ❌ **Not Ready** - Significant refactoring required

---

## Language-Specific Additions

### Python
- [ ] Follows PEP 8 style guide
- [ ] Type hints present (PEP 484)
- [ ] Docstrings follow PEP 257
- [ ] Uses context managers for resource cleanup
- [ ] Avoids mutable default arguments

### JavaScript/TypeScript
- [ ] TypeScript strict mode enabled
- [ ] No `any` types without justification
- [ ] Async/await properly handled
- [ ] Error propagation clear
- [ ] No callback hell (use promises/async)

### Java
- [ ] Uses checked exceptions appropriately
- [ ] Immutable objects preferred
- [ ] Try-with-resources used
- [ ] Null-safe patterns (Optional, nullability annotations)

---

## Severity Levels for Issues Found

When reviewing, classify issues by severity:

### 🔴 CRITICAL - Must Fix Before Production
- Security vulnerabilities (SQL injection, XXE, etc.)
- Unhandled exceptions that could crash system
- Incorrect algorithm affecting correctness
- Data corruption risks

### 🟠 HIGH - Should Fix Before Merge
- Input validation gaps
- Missing error handling
- Performance issues in hot paths
- Inadequate testing of critical paths

### 🟡 MEDIUM - Should Address
- Documentation gaps
- Code duplication
- Overly complex functions
- Missing edge case handling

### 🟢 LOW - Nice to Have
- Naming improvements
- Code style issues
- Minor optimization suggestions
- Documentation enhancements

---

## Sign-Off Template

```markdown
## Code Review Sign-Off

**Reviewer:** [Name]  
**Date:** [Date]  
**Commit:** [SHA]  

### Checklist
- [ ] Code review completed
- [ ] Checklist score: __/150 (__%)
- [ ] No CRITICAL issues
- [ ] Security review passed
- [ ] Performance acceptable
- [ ] Tests adequate
- [ ] Documentation complete

### Summary
[Brief description of review findings and recommendations]

### Issues Found
- [Issue 1 - Severity]
- [Issue 2 - Severity]

### Recommendations
1. [Recommendation 1]
2. [Recommendation 2]

**STATUS:** [ ] APPROVED | [ ] NEEDS CHANGES | [ ] REJECTED

**Sign-off:** ___________________
```

---

## See Also

- [NASA Coding Guidelines](nasa-guidelines.md)
- [Code Smells](code-smells.md)
- [Security Best Practices](security-best-practices.md)
