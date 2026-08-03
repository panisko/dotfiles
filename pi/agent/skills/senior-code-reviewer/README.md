# Senior Code Reviewer Skill - Usage Guide

A comprehensive code review skill for pi that improves code quality across multiple dimensions.

## What This Skill Does

This skill acts as a **senior engineer code reviewer** that:

- **Improves Documentation** - Ensures clear, complete docstrings, type hints, and examples
- **Enhances Security** - Identifies vulnerabilities, validates inputs, prevents injection attacks
- **Optimizes Performance** - Finds inefficient algorithms, suggests optimizations
- **Enforces Best Practices** - Applies NASA guidelines, SOLID principles, language conventions
- **Reduces Bugs** - Catches edge cases, improves error handling, validates assumptions
- **Improves Maintainability** - Reduces complexity, improves naming, eliminates code smells

## Quick Start

### Review Any Code

```bash
/skill:senior-code-reviewer <file_path>
```

**Example:**
```bash
/skill:senior-code-reviewer src/user_service.py
```

### Detailed Review with Examples

```bash
/skill:senior-code-reviewer <file_path> --deep --with-examples
```

### Focus on Specific Areas

```bash
/skill:senior-code-reviewer auth.py --focus security,performance
```

## Features

### 1. Multi-Dimensional Review

Each review covers:

- **Documentation** (40 points) - Docstrings, type hints, comments, README quality
- **Security** (30 points) - Input validation, SQL injection, XSS, data protection
- **Performance** (20 points) - Algorithm efficiency, data structures, caching
- **Maintainability** (10 points) - Code clarity, naming, complexity metrics

### 2. Prioritized Issues

Issues are classified by severity:

- 🔴 **CRITICAL** - Security vulnerabilities, data loss risks, system crashes
- 🟠 **HIGH** - Significant bugs, poor practices, test failures
- 🟡 **MEDIUM** - Code quality, readability, maintainability
- 🟢 **LOW** - Minor improvements, nice-to-haves

### 3. Professional Output

Each review includes:

- Summary of issues found
- Detailed explanations with code examples
- Before/after comparisons
- Implementation roadmap
- Effort estimation

### 4. Language-Specific Guidance

Specialized reviews for:

- Python (PEP 8, type hints, docstrings)
- JavaScript/TypeScript (ESLint, strict mode, async/await)
- Java (SOLID principles, immutability, null safety)
- C/C++ (Memory safety, NASA JPL rules)

### 5. Reference Documentation

Comprehensive guides included:

- **NASA Coding Guidelines** - Mission-critical code standards
- **Security Best Practices** - OWASP Top 10, input validation, encryption
- **Code Smells** - Anti-patterns to avoid
- **Clean Code Principles** - SOLID, naming, error handling
- **Language-Specific Guides** - Python, JavaScript, Java, C/C++

## Usage Examples

### Example 1: Quick Security Review

```
/skill:senior-code-reviewer payment_processor.py --focus security
```

Output includes:
- SQL injection checks
- Input validation gaps
- Sensitive data exposure risks
- Authentication/authorization issues
- Cryptographic weaknesses

### Example 2: Performance Optimization

```
/skill:senior-code-reviewer database.py --focus performance --deep
```

Output includes:
- Algorithm complexity analysis
- Query optimization suggestions
- Memory efficiency improvements
- Caching opportunities
- Data structure recommendations

### Example 3: Documentation Improvement

```
/skill:senior-code-reviewer api.py --focus documentation --with-examples
```

Output includes:
- Missing docstrings
- Type hint recommendations
- Comment quality assessment
- Example code suggestions
- README improvements

### Example 4: Complete Enterprise Review

```
/skill:senior-code-reviewer auth_module.py --strict --deep --with-examples
```

Applies strictest standards (NASA/JPL guidelines) with:
- Complete analysis of all dimensions
- Code examples for all improvements
- Enterprise-grade quality bar

## Understanding the Output

### Report Structure

```
## 📋 Code Review: [Function/File Name]

### Summary
- Files analyzed: N
- Total issues: N
- Critical: X | High: Y | Medium: Z | Low: W

### Issues by Priority

#### 🔴 CRITICAL: [Issue Title]
- **Location:** Where in the code
- **Problem:** What's wrong and why it matters
- **Impact:** Security | Performance | Reliability
- **Fix:** Specific recommendation with code example
- **Effort:** Time to implement

...

### Improved Code
[Refactored version with inline comments]

### Implementation Roadmap
1. [Fix critical issues first]
2. [Address high-priority items]
3. [Tackle medium-priority improvements]
4. [Consider low-priority enhancements]

### Before/After Metrics
- Cyclomatic Complexity: 15 → 8 (↓ 47%)
- Code Coverage: 60% → 95% (↑ 58%)
- Security Score: 3/10 → 9/10 (↑ 200%)

### Production Readiness
✅ Ready for production after addressing CRITICAL issues
```

## Options & Flags

### Review Depth

- **No flag:** Standard review (5-10 minutes)
- `--deep` - Detailed analysis with explanations (15-30 minutes)
- `--shallow` - Quick scan for obvious issues (2-5 minutes)

### Review Focus

```bash
--focus security              # Security vulnerabilities
--focus performance           # Performance optimization
--focus documentation         # Doc quality and completeness
--focus readability          # Code clarity and naming
--focus testing              # Test coverage and quality
--focus complexity           # Cyclomatic complexity
```

Combine multiple: `--focus security,performance,documentation`

### Strictness Level

- `--strict` - Enforce NASA/JPL guidelines (highest bar)
- (default) - Production-ready standards
- `--lenient` - Teaching/learning mode (more forgiving)

### Output Format

- (default) - Markdown formatted report
- `--format json` - Structured JSON output
- `--format html` - HTML report

### Comparison

```bash
--compare old_version.py  # Highlight improvements
```

## Reference Documents

All documentation is in the `references/` directory:

### Core Guidelines
- **nasa-guidelines.md** - NASA JPL coding standards with examples
- **clean-code-principles.md** - Readability, maintainability, SOLID
- **code-smells.md** - Anti-patterns and how to fix them
- **security-best-practices.md** - OWASP, input validation, encryption

### Language Guides
- **python-review.md** - PEP 8, type hints, docstrings, common pitfalls
- **javascript-review.md** - ESLint, TypeScript, async/await
- **java-review.md** - Immutability, null safety, design patterns
- **c-review.md** - Memory safety, NASA C rules

### Assessment Tools
- **code-review-checklist.md** - Comprehensive checklist (150 points)
- **documentation-template.md** - Documentation best practices

## Templates

Templates in `templates/` directory show exemplary reviews:

- **python-class-review.md** - Complete Python code review example
- **javascript-api-review.md** - JavaScript API endpoint review
- **security-checklist.md** - Security-focused review template
- **performance-template.md** - Performance optimization review

## Integration with Your Workflow

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

pi --skill senior-code-reviewer src/ --focus critical
if [ $? -ne 0 ]; then
    echo "Code review failed - address critical issues"
    exit 1
fi
```

### CI/CD Pipeline

```yaml
# .github/workflows/code-review.yml
- name: Code Review
  run: |
    pi --skill senior-code-reviewer src/ \
       --strict \
       --format json > review.json
    
    # Fail if critical issues found
    if grep -q '"severity": "CRITICAL"' review.json; then
      exit 1
    fi
```

### Pre-Merge PR Check

```bash
# Review files changed in PR
pi --skill senior-code-reviewer $(git diff main --name-only)
```

## Production Readiness Score

The skill uses a 150-point scoring system:

```
Documentation: 40 points
Security:      30 points
Performance:   20 points
Maintainability: 10 points
Testing:       40 points (optional)
Error Handling: 10 points
─────────────────────────
Total:        150 points
```

**Thresholds:**
- **135-150 (90-100%)**: ✅ Ready for Production
- **120-134 (80-89%)**: ⚠️ Good, Minor Issues
- **105-119 (70-79%)**: 🔴 Needs Work
- **< 105 (< 70%)**: ❌ Significant Refactoring Needed

## Tips for Best Results

1. **Start with security** - Use `--focus security` first for critical code
2. **Use `--deep` for complex code** - More thorough analysis takes a bit longer
3. **Review by module** - Don't review entire projects at once; focus on critical/new code
4. **Check NASA guide** - Read `references/nasa-guidelines.md` for highest quality bar
5. **Use templates** - Look at `templates/` for exemplary review structure
6. **Fix CRITICAL first** - Always address security/data-loss issues before other improvements

## When to Use

✅ **Perfect for:**
- Code review before merge
- Security audit of sensitive modules
- Performance optimization pass
- Improving legacy code quality
- Preparing for production deployment
- Onboarding developers (learning resource)

❌ **Not ideal for:**
- Quick syntax fixes (use linters instead)
- Simple renaming (use IDE refactoring)
- Whitespace/formatting (use auto-formatters)
- Minor styling preferences

## Limitations

- Review is based on code analysis; actual deployment testing still needed
- Recommendations are guidelines; use your judgment for your context
- Doesn't replace human code review, but enhances it
- Performance analysis is static; real profiling may reveal different bottlenecks

## Getting Help

1. **Read the references** - Start with `references/nasa-guidelines.md`
2. **Check templates** - See `templates/python-class-review.md` for examples
3. **Review checklist** - Use `references/code-review-checklist.md` manually
4. **Ask for specific focus** - Use `--focus <area>` for detailed analysis

## Troubleshooting

**Q: Review takes too long**
A: Use `--shallow` instead of `--deep`, or `--focus` on specific areas

**Q: Recommendations don't match my coding style**
A: You have final authority - recommendations are guidelines, not mandates

**Q: How is this different from linters?**
A: Linters catch syntax; this reviews logic, security, performance, and design

**Q: Can I use this in my CI/CD?**
A: Yes! Use `--format json` and parse the output to fail builds on critical issues

---

## See Also

- [NASA Coding Guidelines](references/nasa-guidelines.md)
- [Code Review Checklist](references/code-review-checklist.md)
- [Clean Code Principles](references/clean-code-principles.md)
- [Security Best Practices](references/security-best-practices.md)
