---
name: senior-code-reviewer
description: Senior engineer code review that improves readability, performance, and security. Enhances documentation, sanitizes inputs, follows NASA/industry guidelines. Use when refactoring code, improving quality, or preparing for production.
---

# Senior Code Reviewer

Professional code review and improvement service that elevates code quality to enterprise standards. Comprehensive analysis of readability, performance, security, and best practices.

## Overview

This skill provides streamlined, actionable code review with automatic fixes:

- **File-Based Review**: Reviews target file, applies critical fixes, documents remaining issues
- **Automatic Fixes**: Creates `_FIXED` version with critical issues resolved
- **Concise Output**: Focused reporting with TODO section in original file
- **Smart Prioritization**: Critical fixes auto-applied; other findings documented for manual review
- **Multiple Dimensions**: Security, Performance, Documentation, Maintainability, Best Practices

## Quick Start

### Review File and Auto-Fix Critical Issues

```
/skill:senior-code-reviewer <file>
```

**Result:**
- `original.py` → Updated with TODO section listing remaining findings
- `original_FIXED.py` → New file with critical fixes applied

### Focus on Specific Areas

```
/skill:senior-code-reviewer <file> --focus security,performance
```

### Apply All Recommendations (Including Non-Critical)

```
/skill:senior-code-reviewer <file> --aggressive
```

## How It Works

The skill performs automated review and remediation:

### 1. Code Analysis
- Identify language and framework
- Assess structure and detect issues
- Categorize findings by severity (CRITICAL, HIGH, MEDIUM, LOW)

### 2. Auto-Fix Phase
- Apply all CRITICAL fixes to new `_FIXED` file
- Preserve original for reference
- Maintain code style and conventions

### 3. Document Remaining Issues
- Add `# TODO: Code Review Findings` section to original file
- List HIGH, MEDIUM, LOW findings
- Include brief fix recommendations
- Keep output concise (focused, actionable)

## What Gets Reviewed

### Security (Auto-Fixed if CRITICAL)
- Input validation and sanitization
- SQL/command injection vulnerabilities  
- Path traversal risks
- Sensitive data exposure
- Error message leakage
- Insecure patterns

### Performance (Documented in TODO)
- Algorithm complexity (Big O)
- Unnecessary loops/redundancy
- Memory efficiency
- Collection optimization
- Database query efficiency

### Documentation (Documented in TODO)
- Missing docstrings
- Type hints absent
- Unexplained complex logic
- Edge case handling

### Best Practices (Auto-Fixed if CRITICAL, else TODO)
- Input validation
- Error handling gaps
- Function length > 50 lines
- Cyclomatic complexity > 15
- Missing exception handling

## Usage Examples

### Example 1: Quick File Review

```bash
/skill:senior-code-reviewer src/utils.py
```

**Output:**
```
✅ Code Review Complete: src/utils.py
🔧 Critical fixes applied → src/utils_FIXED.py
📝 Remaining findings → Added TODO section to src/utils.py

Summary: 1 CRITICAL (fixed) | 2 HIGH | 3 MEDIUM | 2 LOW
```

**Files created/modified:**
- `src/utils.py` - Original + TODO section with findings
- `src/utils_FIXED.py` - New file with critical fixes applied

### Example 2: Security-Focused Review

```bash
/skill:senior-code-reviewer auth_module.py --focus security
```

**Only security-related findings reviewed and documented**

### Example 3: Aggressive Mode (Fix More Issues)

```bash
/skill:senior-code-reviewer database.py --aggressive
```

**Result:** `database_FIXED.py` includes CRITICAL + HIGH fixes applied

## Severity Levels

- **CRITICAL** ✅ Auto-fixed in `_FIXED` file
  - Security vulnerabilities
  - Missing input validation
  - Unhandled exceptions
  - Dangerous patterns

- **HIGH** 📝 Listed in TODO
  - Poor error handling
  - Validation gaps
  - Performance issues

- **MEDIUM** 📝 Listed in TODO
  - Missing docstrings
  - Naming inconsistencies
  - Code duplication

- **LOW** 📝 Listed in TODO
  - Style suggestions
  - Minor refactoring
  - Documentation improvements

## Options

- `--focus <areas>` - Prioritize specific review areas (security, performance, documentation, readability, testing, complexity)
- `--aggressive` - Apply HIGH and MEDIUM fixes too (not just CRITICAL)
- `--strict` - Enforce NASA/JPL standards (only CRITICAL fixes safe to auto-apply)
- `--no-fixed-file` - Skip creating `_FIXED` version; only update original with TODO
- `--dry-run` - Show what would be fixed without applying changes
- `--format json` - Output findings as JSON (for CI/CD integration)

## Reference Documents

- [NASA Coding Guidelines](references/nasa-guidelines.md) - JPL-mandated C coding rules, applicable to all languages
- [Google Style Guide](references/google-style-guide.md) - General best practices
- [Clean Code Principles](references/clean-code-principles.md) - Readability and maintainability
- [OWASP Top 10](references/owasp-top-10.md) - Security vulnerabilities
- [PEP 257](references/pep-257.md) - Python docstring conventions
- [Code Review Checklist](references/code-review-checklist.md) - Complete assessment criteria

## Output Format

### Console Summary
```
✅ Code Review Complete: filename.py
🔧 Critical fixes applied → filename_FIXED.py
📝 Remaining findings → Added to filename.py (see TODO section)

Summary: 3 CRITICAL (fixed) | 2 HIGH | 1 MEDIUM | 1 LOW
```

### TODO Section (Added to Original File)
```python
# TODO: Code Review Findings
# Generated: 2026-05-28
# Review: senior-code-reviewer
#
# HIGH:
#   - Missing input validation on process_data() (Line 42)
#   - Exception handling incomplete in parse_config() (Line 87)
#
# MEDIUM:
#   - Add docstring to helper_function() (Line 156)
#   - Optimize O(n²) loop in calculate_total() (Line 203)
#
# LOW:
#   - Consider using dataclass for User structure (Line 15)
#   - Inconsistent variable naming conventions (Lines 34, 78)
```

### Fixed File (`filename_FIXED.py`)
- Original code with all CRITICAL fixes applied
- Input validation added
- Error handling improved
- Security vulnerabilities patched
- Maintains code style and readability

## Supported Languages

- **Python** (PEP 8, PEP 257, type hints)
- **JavaScript/TypeScript** (Google style, ESLint)
- **Java** (Google style)
- **C/C++** (NASA/JPL rules with --strict)
- **Go** (effective Go)
- **Rust** (idioms)

## Standards & References

- [NASA Coding Guidelines](references/nasa-guidelines.md) - Highest safety standards
- [Google Style Guide](references/google-style-guide.md) - General best practices
- [Clean Code Principles](references/clean-code-principles.md) - Readability
- [OWASP Top 10](references/owasp-top-10.md) - Security
- [PEP 257](references/pep-257.md) - Python docstrings

## Integration with CI/CD

```bash
# Review and auto-fix in CI pipeline
pi --skill senior-code-reviewer src/module.py --format json

# Fail build on CRITICAL or HIGH (dry-run first)
pi --skill senior-code-reviewer src/module.py --dry-run --format json
```

JSON output includes `severity_distribution` for automated thresholds.

## When to Use This Skill

✅ Use when:
- Pre-production code review with auto-fixes
- Security-focused code audit
- Improving legacy code incrementally
- PR review automation
- Code quality gates
- Learning best practices (see TODO findings)

❌ Don't use for:
- Syntax/style fixes (use linters: pylint, eslint)
- IDE refactoring (variable renaming)
- Auto-formatting (use black, prettier)

## Common Questions

**Q: What gets auto-fixed?**
A: CRITICAL issues only (security vulnerabilities, missing input validation, dangerous patterns). See `_FIXED` file.

**Q: What about non-critical findings?**
A: Listed in TODO section of original file for manual review. Use `--aggressive` to auto-fix HIGH/MEDIUM too.

**Q: How do I apply the fixes?**
A: Review `_FIXED` file, compare to original, then adopt changes. Use `--dry-run` to preview first.

**Q: Can I merge FIXED code directly?**
A: Recommended: Review diff first, test, then merge. Automatic fixes follow best practices but your code patterns matter.

**Q: What if I disagree with a fix?**
A: You maintain final authority. Keep original file, adjust `_FIXED` as needed, or delete and keep current code.

**Q: How does this differ from linters?**
A: Linters catch syntax/style. This applies semantic fixes (validation, error handling, security patterns) and documents architectural improvements.

## File Output Workflow

```
Input: mycode.py
   |
   v
+--Review & Analyze--+
   |
   +-- Critical Fixes
   |       |
   |       v
   |  mycode_FIXED.py (NEW)
   |
   +-- Other Findings
           |
           v
   mycode.py + TODO section (UPDATED)
```

## Key Workflows

### Workflow 1: Quick Review + Auto-Fix
```bash
$ /skill:senior-code-reviewer app.py
# Outputs: app_FIXED.py + TODO in app.py
# Action: Review _FIXED, test, merge if satisfied
```

### Workflow 2: Dry-Run Before Committing
```bash
$ /skill:senior-code-reviewer app.py --dry-run
# Shows what WOULD be fixed without applying
# No files created
```

### Workflow 3: CI/CD Gate
```bash
$ /skill:senior-code-reviewer app.py --format json
# Exits non-zero if CRITICAL or HIGH found
# JSON includes severity_distribution for threshold checks
```
