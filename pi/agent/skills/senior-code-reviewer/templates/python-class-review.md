# Code Review Template - Python Example

This template shows how a thorough code review is structured.

## Before Review

```python
# Original code to review
def process_user_data(data):
    result = []
    for i in range(len(data)):
        if data[i]['age'] > 18:
            result.append(data[i]['name'])
    return result

def get_user(user_id):
    user = db.query("SELECT * FROM users WHERE id = " + str(user_id))
    return user

def save_config(filename, config):
    try:
        with open(filename, 'w') as f:
            json.dump(config, f)
    except:
        pass
    return True
```

---

## Review Structure

### 1. Summary

```
## 📋 Code Review: User Data Processing

**Date:** 2024-01-15
**Reviewer:** Senior Code Reviewer
**Files:** user_processing.py
**Lines:** 25

### Issues Found
- Total: 11 issues
- Critical: 2 (SQL injection, error handling)
- High: 3 (missing validation, no type hints, non-Pythonic)
- Medium: 4 (documentation, naming)
- Low: 2 (minor optimization)
```

---

### 2. Issues by Severity

#### 🔴 CRITICAL: SQL Injection Vulnerability

**Location:** `get_user()` function, line 9

**Issue:**
```python
user = db.query("SELECT * FROM users WHERE id = " + str(user_id))
```

**Problem:** String concatenation with user input allows SQL injection
```
GET /user/1; DROP TABLE users; --
```

**Fix:**
```python
def get_user(user_id: int) -> Optional[Dict]:
    # Use parameterized query
    user = db.query("SELECT * FROM users WHERE id = ?", (user_id,))
    return user
```

**Impact:** CRITICAL - System can be compromised
**Effort:** Low (1-2 minutes to fix)

---

#### 🔴 CRITICAL: Silent Error Handling

**Location:** `save_config()` function, line 16

**Issue:**
```python
try:
    with open(filename, 'w') as f:
        json.dump(config, f)
except:
    pass  # Silent failure!
```

**Problem:** 
- Catches all exceptions (including KeyboardInterrupt)
- Returns True even if save failed
- Caller doesn't know configuration wasn't saved

**Fix:**
```python
def save_config(filename: str, config: dict) -> bool:
    """Save configuration to file.
    
    Args:
        filename: Path to config file
        config: Configuration dictionary
        
    Returns:
        True if successful
        
    Raises:
        IOError: If file cannot be written
        ValueError: If config contains non-serializable data
    """
    if not isinstance(config, dict):
        raise TypeError(f"config must be dict, got {type(config)}")
    
    if not filename:
        raise ValueError("filename cannot be empty")
    
    try:
        # Validate JSON serializability first
        json.dumps(config)
    except (TypeError, ValueError) as e:
        raise ValueError(f"config not JSON serializable: {e}")
    
    try:
        with open(filename, 'w') as f:
            json.dump(config, f)
        return True
    except IOError as e:
        raise IOError(f"Cannot write to {filename}: {e}")
```

**Impact:** CRITICAL - Data loss/corruption risk
**Effort:** Low (5 minutes)

---

#### 🟠 HIGH: No Input Validation

**Location:** `process_user_data()` function, line 1

**Issue:**
```python
def process_user_data(data):  # No validation
    result = []
    for i in range(len(data)):
        if data[i]['age'] > 18:  # Assumes key exists
            result.append(data[i]['name'])  # Assumes key exists
```

**Problem:**
- No type checking for `data`
- No handling for missing keys
- No handling for invalid types

**Fix:**
```python
from typing import List, Dict, Any

def process_user_data(data: List[Dict[str, Any]]) -> List[str]:
    """
    Extract names of adult users.
    
    Args:
        data: List of user dictionaries with 'age' and 'name' keys
        
    Returns:
        List of names for users with age > 18
        
    Raises:
        TypeError: If data is not a list
        ValueError: If any user record is invalid
    """
    if not isinstance(data, list):
        raise TypeError(f"data must be list, got {type(data)}")
    
    adult_names = []
    
    for i, user in enumerate(data):
        # Validate user record
        if not isinstance(user, dict):
            raise ValueError(f"User at index {i} must be dict, got {type(user)}")
        
        # Check required fields
        if 'age' not in user:
            raise ValueError(f"User at index {i} missing 'age' field")
        if 'name' not in user:
            raise ValueError(f"User at index {i} missing 'name' field")
        
        # Validate field types
        if not isinstance(user['age'], (int, float)):
            raise ValueError(f"User at index {i} age must be number, got {type(user['age'])}")
        if not isinstance(user['name'], str):
            raise ValueError(f"User at index {i} name must be string, got {type(user['name'])}")
        
        # Process
        if user['age'] > 18:
            adult_names.append(user['name'])
    
    return adult_names
```

**Impact:** HIGH - Runtime errors on invalid data
**Effort:** Medium (10 minutes)

---

#### 🟠 HIGH: Missing Type Hints

**Location:** All functions

**Issue:**
```python
def process_user_data(data):  # No type information
    pass

def get_user(user_id):  # What type is user_id?
    pass
```

**Fix:** Add type hints to all functions (see above)

**Impact:** HIGH - Harder to understand, catch errors
**Effort:** Low (5 minutes)

---

#### 🟡 MEDIUM: Non-Pythonic Code

**Location:** `process_user_data()` function, line 3

**Issue:**
```python
# Looping by index is not Pythonic
for i in range(len(data)):
    if data[i]['age'] > 18:
        result.append(data[i]['name'])
```

**Fix:**
```python
# Use list comprehension
adult_names = [
    user['name'] 
    for user in data 
    if user.get('age', 0) > 18
]

# Or use filter
adult_names = list(map(
    lambda user: user['name'],
    filter(lambda user: user.get('age', 0) > 18, data)
))

# Prefer comprehension for readability
```

**Impact:** MEDIUM - Readability and maintainability
**Effort:** Very Low (2 minutes)

---

#### 🟡 MEDIUM: Missing Module Docstring

**Location:** Top of file

**Issue:** No documentation explaining module purpose.

**Fix:**
```python
"""
User data processing utilities.

This module provides functions for processing and validating user data,
including extraction of adult users and configuration management.

Classes:
    (none)

Functions:
    process_user_data: Extract names of adult users
    get_user: Retrieve user by ID
    save_config: Persist configuration to file
"""
```

**Impact:** MEDIUM - First-time users confused
**Effort:** Very Low (3 minutes)

---

### 3. Improved Code

**Complete refactored version:**

```python
"""
User data processing utilities.

This module provides functions for processing and validating user data,
including extraction of adult users and configuration management.
"""

from typing import List, Dict, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)


def process_user_data(data: List[Dict[str, Any]]) -> List[str]:
    """
    Extract names of adult users.
    
    Args:
        data: List of user dictionaries with 'age' and 'name' keys
        
    Returns:
        List of names for users with age > 18
        
    Raises:
        TypeError: If data is not a list or contains non-dict items
        ValueError: If any user record is missing required fields
        
    Examples:
        >>> users = [
        ...     {'name': 'Alice', 'age': 25},
        ...     {'name': 'Bob', 'age': 17},
        ... ]
        >>> process_user_data(users)
        ['Alice']
    """
    if not isinstance(data, list):
        raise TypeError(f"data must be list, got {type(data)}")
    
    adult_names = []
    
    for i, user in enumerate(data):
        # Validate user record structure
        if not isinstance(user, dict):
            raise ValueError(
                f"User at index {i} must be dict, got {type(user)}"
            )
        
        # Check required fields
        if 'age' not in user:
            raise ValueError(f"User at index {i} missing 'age' field")
        if 'name' not in user:
            raise ValueError(f"User at index {i} missing 'name' field")
        
        # Validate field types
        if not isinstance(user['age'], (int, float)):
            raise ValueError(
                f"User at index {i}: age must be number, "
                f"got {type(user['age'])}"
            )
        if not isinstance(user['name'], str):
            raise ValueError(
                f"User at index {i}: name must be string, "
                f"got {type(user['name'])}"
            )
        
        # Extract adult names
        if user['age'] > 18:
            adult_names.append(user['name'])
    
    logger.debug(f"Found {len(adult_names)} adult users")
    return adult_names


def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve user by ID.
    
    Args:
        user_id: User identifier
        
    Returns:
        User data dictionary, or None if not found
        
    Raises:
        TypeError: If user_id is not an integer
        ValueError: If user_id is not positive
        
    Note:
        Uses parameterized query to prevent SQL injection.
    """
    if not isinstance(user_id, int):
        raise TypeError(f"user_id must be int, got {type(user_id)}")
    
    if user_id <= 0:
        raise ValueError(f"user_id must be positive, got {user_id}")
    
    # Parameterized query prevents SQL injection
    try:
        user = db.query("SELECT * FROM users WHERE id = ?", (user_id,))
        return user
    except Exception as e:
        logger.error(f"Failed to retrieve user {user_id}: {e}")
        raise


def save_config(filename: str, config: Dict[str, Any]) -> bool:
    """
    Save configuration to file.
    
    Args:
        filename: Path to config file
        config: Configuration dictionary
        
    Returns:
        True if successful
        
    Raises:
        TypeError: If arguments are wrong types
        ValueError: If config is not JSON serializable
        IOError: If file cannot be written
    """
    if not isinstance(filename, str) or not filename:
        raise TypeError("filename must be non-empty string")
    
    if not isinstance(config, dict):
        raise TypeError(f"config must be dict, got {type(config)}")
    
    # Validate JSON serializability
    try:
        json.dumps(config)
    except (TypeError, ValueError) as e:
        raise ValueError(f"config not JSON serializable: {e}")
    
    # Write to file
    try:
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info(f"Config saved to {filename}")
        return True
    except IOError as e:
        logger.error(f"Cannot write to {filename}: {e}")
        raise
```

---

### 4. Metrics Before/After

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Lines of Code** | 25 | 120 | (detailed, but better) |
| **Cyclomatic Complexity** | 8 | 3 | ↓ 63% |
| **Documented Functions** | 0% | 100% | ↑ 100% |
| **Type Hints** | 0% | 100% | ↑ 100% |
| **Input Validation** | 0% | 100% | ↑ 100% |
| **Error Handling** | Poor | Comprehensive | ✓ |
| **SQL Injection Risk** | HIGH | ELIMINATED | ✓ |
| **Testability** | Hard | Easy | ✓ |

---

### 5. Implementation Checklist

- [ ] Apply all CRITICAL fixes (SQL injection, error handling)
- [ ] Add type hints to all functions
- [ ] Add comprehensive input validation
- [ ] Update docstrings with Google-style format
- [ ] Replace index-based loops with comprehensions
- [ ] Add logging statements
- [ ] Write unit tests for all functions
- [ ] Run pytest with coverage reporting
- [ ] Run mypy type checker
- [ ] Run black formatter
- [ ] Run ruff linter

---

### 6. Estimated Effort

- **Review Time:** 20 minutes
- **Fixes Time:** 45 minutes
- **Testing:** 30 minutes
- **Total:** ~1.5 hours

---

### 7. Sign-Off

**Status:** ✅ APPROVED FOR PRODUCTION (after fixes applied)

**Sign-off:** Code is now production-ready with all critical issues resolved.

---

## See Also

- [NASA Guidelines](../references/nasa-guidelines.md)
- [Code Review Checklist](../references/code-review-checklist.md)
- [Python Review Guide](../references/python-review.md)
- [Security Best Practices](../references/security-best-practices.md)
