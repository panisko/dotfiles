# Security Review Checklist Template

Use this detailed checklist for security-focused code reviews.

## Input Validation (25 points)

### Data Type Validation
- [ ] **All parameters type-checked** (5 pts)
  - Validate parameter types immediately upon function entry
  - Use type hints and runtime checks
  
- [ ] **No unsafe type coercion** (5 pts)
  - Don't implicitly convert user input
  - Example: Don't do `int(user_input)` without try/except

- [ ] **Length/size limits enforced** (5 pts)
  - Validate string lengths
  - Validate collection sizes
  - Prevent buffer overflows
  
- [ ] **Range validation for numbers** (5 pts)
  - Check min/max bounds
  - Validate for negative/zero where inappropriate
  - Example: User ID must be positive
  
- [ ] **Whitelist, not blacklist** (5 pts)
  - Allow known-good values
  - Don't try to block all bad values

### Format Validation
- [ ] **Email format validated** (3 pts)
  - Use proper email validation regex or library
  
- [ ] **URL format validated** (3 pts)
  - Prevent SSRF attacks
  - Validate protocol (http/https only?)
  
- [ ] **File paths validated** (3 pts)
  - Prevent path traversal (../)
  - Validate file extensions
  - Check within allowed directory
  
- [ ] **Dates/timestamps validated** (3 pts)
  - Proper format
  - Reasonable ranges

**Subtotal: __/25**

## SQL & Database (20 points)

- [ ] **No string concatenation in queries** (10 pts)
  ```python
  # Bad
  db.query(f"SELECT * FROM users WHERE id = {user_id}")
  
  # Good
  db.query("SELECT * FROM users WHERE id = ?", (user_id,))
  ```

- [ ] **Parameterized queries used everywhere** (10 pts)
  - Use prepared statements
  - Framework ORM layer prevents injection
  - Even for stored procedures, use parameters

**Subtotal: __/20**

## Authentication & Authorization (20 points)

- [ ] **Authentication enforced on all protected endpoints** (5 pts)
  - No missing auth checks
  - Proper credential validation

- [ ] **Session tokens validated** (5 pts)
  - Tokens checked on every request
  - Token expiration enforced
  - Invalid tokens rejected
  
- [ ] **Authorization checks in place** (5 pts)
  - Users can't access others' data
  - Permissions checked before returning data
  - Admin checks performed
  
- [ ] **No credential exposure in URLs** (5 pts)
  - Passwords not in URLs
  - API keys not logged
  - No credentials in error messages

**Subtotal: __/20**

## Data Protection (15 points)

- [ ] **Sensitive data encrypted at rest** (5 pts)
  - Passwords: bcrypt/argon2 (not SHA)
  - PII: encryption (not hashing)
  - API keys: secrets vault
  
- [ ] **Encrypted in transit** (5 pts)
  - HTTPS/TLS enforced
  - Secure cookies (HttpOnly, Secure, SameSite)
  - No unencrypted sensitive data transmission
  
- [ ] **Secrets not in code** (5 pts)
  - No hardcoded API keys, passwords, tokens
  - Use environment variables or vaults
  - No secrets in git history

**Subtotal: __/15**

## Error Handling & Logging (15 points)

- [ ] **Errors don't leak information** (5 pts)
  - Generic error messages to users
  - Detailed errors logged server-side
  - Stack traces never shown to users
  - Database structure not revealed
  
- [ ] **Sensitive data not logged** (5 pts)
  - No passwords in logs
  - No credit cards in logs
  - No personal data in logs
  - Use placeholder values in logs
  
- [ ] **All exceptions handled** (5 pts)
  - No bare except clauses
  - No silent failures
  - Errors always reported somehow

**Subtotal: __/15**

## API Security (10 points)

- [ ] **Rate limiting implemented** (3 pts)
  - Prevents brute force attacks
  - Throttles bad actors
  
- [ ] **CORS properly configured** (3 pts)
  - Only trusted origins allowed
  - Credentials not overly permissive
  
- [ ] **API version isolation** (2 pts)
  - Old API versions don't bypass security
  - Deprecation process in place
  
- [ ] **Request validation** (2 pts)
  - Content-Type validated
  - Max payload size enforced

**Subtotal: __/10**

## Injection Attacks (10 points)

- [ ] **No command injection** (3 pts)
  - Use process/subprocess with list of args
  - Never use shell=True with user input
  ```python
  # Bad
  os.system(f"ls {user_path}")
  
  # Good
  subprocess.run(['ls', user_path])
  ```

- [ ] **No LDAP injection** (2 pts)
  - Escape special characters
  - Use LDAP libraries, not string building
  
- [ ] **No XXE (XML External Entities)** (2 pts)
  - Disable external entities in XML parsers
  - Use safe parsing libraries
  
- [ ] **No template injection** (3 pts)
  - Don't use `eval()` or `exec()` with user input
  - Use safe template engines
  - Escape template variables

**Subtotal: __/10**

## Dependencies & Libraries (5 points)

- [ ] **No known vulnerabilities** (3 pts)
  - Run `pip-audit` or similar
  - Dependencies kept updated
  - Vulnerable versions not allowed
  
- [ ] **Dependencies from trusted sources** (2 pts)
  - Don't use typo-squatted packages
  - Verify package authenticity

**Subtotal: __/5**

## Code Quality for Security (5 points)

- [ ] **No obvious bugs** (3 pts)
  - Off-by-one errors
  - Null pointer dereferences
  - Buffer overflows
  
- [ ] **Type safety** (2 pts)
  - Type hints present
  - Weak types that could hide bugs avoided

**Subtotal: __/5**

## Security-Specific Requirements (Varies)

### For Payment Systems (Add 20 points)
- [ ] PCI DSS compliance considerations
- [ ] Credit card data never stored (use tokenization)
- [ ] CVV never transmitted/stored
- [ ] Encryption of card data

### For Authentication Systems (Add 20 points)
- [ ] Password complexity requirements
- [ ] Account lockout after failed attempts
- [ ] Secure password reset flow
- [ ] Multi-factor authentication capability

### For APIs (Add 15 points)
- [ ] API keys properly managed
- [ ] Rate limiting by user/IP
- [ ] Request signing/HMAC verification
- [ ] API versioning strategy

---

## Total Security Score

```
Input Validation:       __/25
SQL & Database:         __/20
Auth & Authorization:   __/20
Data Protection:        __/15
Error Handling:         __/15
API Security:           __/10
Injection Prevention:   __/10
Dependencies:           __/5
Code Quality:           __/5
                        ───────
Base Score:            __/125

Additional (if applicable):
+ Payment Systems:      __/20
+ Authentication:       __/20
+ API Security:         __/15
                        ───────
TOTAL:                 __/125+
```

## Thresholds

- **100+**: ✅ **Secure** - Ready for production
- **80-99**: ⚠️ **Acceptable** - Address medium-priority issues
- **60-79**: 🔴 **Needs Work** - Fix high-priority issues before production
- **< 60**: ❌ **Insecure** - Major refactoring required

## Critical Issues (Must Fix)

Any of these must be fixed before production deployment:

- [ ] SQL injection vulnerabilities
- [ ] Command injection vulnerabilities
- [ ] XXE vulnerabilities
- [ ] Hardcoded credentials
- [ ] No authentication on sensitive endpoints
- [ ] Unencrypted sensitive data transmission
- [ ] Information leakage in error messages
- [ ] No input validation
- [ ] Silent error handling (try/except pass)

## Sign-Off

**Security Score:** __/125+ (__%)

**Critical Issues Found:** Yes / No

**Status:** ✅ SECURE | ⚠️ ACCEPTABLE | 🔴 NEEDS WORK | ❌ INSECURE

**Reviewed by:** _________________
**Date:** _________________
**Sign-off:** _________________

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Security Best Practices](../references/security-best-practices.md)
- [NASA Guidelines](../references/nasa-guidelines.md)
