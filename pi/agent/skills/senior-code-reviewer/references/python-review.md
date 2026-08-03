# Python Code Review Guide

Language-specific considerations for Python code review.

## PEP 8 Style Guide

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| **Functions/Variables** | lowercase_with_underscores | `get_user_by_id()`, `user_name` |
| **Classes** | CapWords | `UserRepository`, `PaymentProcessor` |
| **Constants** | UPPERCASE_WITH_UNDERSCORES | `MAX_RETRIES`, `DEFAULT_TIMEOUT` |
| **Private** | _leading_underscore | `_internal_method()`, `_private_var` |
| **Dunder** | __double_underscore__ | `__init__()`, `__str__()` |

❌ **Bad:**
```python
def GetUser(ID):  # CapWords for function, all-caps for variable
    pass

maxRetries = 5  # camelCase for constant
```

✅ **Good:**
```python
def get_user(user_id):
    pass

MAX_RETRIES = 5
```

### Imports

Group imports in this order:
1. Standard library
2. Third-party packages
3. Local imports

❌ **Bad:**
```python
import os
import requests
from my_module import helper
import sys
from flask import Flask
```

✅ **Good:**
```python
import os
import sys

import requests
from flask import Flask

from my_module import helper
```

### Line Length

- Target: 79 characters (docstrings)
- Limit: 99 characters (code)

Use implicit line continuation:

❌ **Bad:**
```python
result = some_function_with_long_name(argument1, argument2, argument3, argument4, argument5)
```

✅ **Good:**
```python
result = some_function_with_long_name(
    argument1,
    argument2,
    argument3,
    argument4,
    argument5
)
```

## Type Hints (PEP 484)

Always use type hints for production code:

```python
from typing import Optional, List, Dict, Tuple, Union

def get_user(user_id: int) -> Optional[Dict[str, str]]:
    """Get user by ID."""
    pass

def process_items(items: List[str]) -> Dict[str, int]:
    """Process list of items."""
    pass

def split_name(name: str) -> Tuple[str, str]:
    """Split full name into first and last."""
    pass

def parse_value(value: Union[str, int]) -> str:
    """Parse value that could be string or int."""
    pass
```

### Enable Type Checking

Configure `pyproject.toml`:
```toml
[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

Run: `mypy your_module.py`

## Docstrings (PEP 257)

### Google Style Docstrings

```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Calculate discounted price.
    
    Args:
        price: Original price in dollars
        discount_percent: Discount as percentage (0-100)
        
    Returns:
        Discounted price in dollars
        
    Raises:
        ValueError: If price is negative or discount_percent not 0-100
        
    Examples:
        >>> calculate_discount(100, 10)
        90.0
    """
    if price < 0:
        raise ValueError(f"price must be non-negative, got {price}")
    if not (0 <= discount_percent <= 100):
        raise ValueError(f"discount_percent must be 0-100, got {discount_percent}")
    
    return price * (1 - discount_percent / 100)
```

### NumPy Style (Alternative)

```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Calculate discounted price.
    
    Parameters
    ----------
    price : float
        Original price in dollars
    discount_percent : float
        Discount as percentage (0-100)
        
    Returns
    -------
    float
        Discounted price in dollars
        
    Raises
    ------
    ValueError
        If price is negative or discount_percent not 0-100
    """
    pass
```

## Common Pitfalls

### 1. Mutable Default Arguments

❌ **Bad:**
```python
def add_to_list(value, lst=[]):  # Default mutable object is shared!
    lst.append(value)
    return lst

add_to_list(1)  # [1]
add_to_list(2)  # [1, 2] - unexpected!
```

✅ **Good:**
```python
def add_to_list(value, lst=None):
    if lst is None:
        lst = []
    lst.append(value)
    return lst

add_to_list(1)  # [1]
add_to_list(2)  # [2] - correct
```

### 2. Loop Variable Leaking

❌ **Bad:**
```python
for item in items:
    process(item)

# `item` still exists here - unexpected!
print(item)  # Last item is still accessible
```

❌ **Use list comprehension/generator:**
```python
# Good - scope controlled
results = [process(item) for item in items]
# Or
for item in items:
    process(item)
# Now `item` is truly local (by convention)
```

### 3. Comparing to None

❌ **Bad:**
```python
if value == None:  # Wrong operator
    pass

if value is not None:  # Use this instead
    pass
```

✅ **Good:**
```python
if value is None:
    pass

if value is not None:
    pass
```

### 4. String Concatenation in Loops

❌ **Bad:**
```python
result = ""
for item in items:
    result += str(item) + ", "  # Inefficient - creates new string each iteration
```

✅ **Good:**
```python
result = ", ".join(str(item) for item in items)
```

### 5. Exception Handling

❌ **Bad:**
```python
try:
    risky_operation()
except:  # Catches all exceptions including KeyboardInterrupt!
    pass

try:
    risky_operation()
except Exception:  # Still too broad
    pass
```

✅ **Good:**
```python
try:
    risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise
except AnotherError as e:
    logger.warning(f"Retry recommended: {e}")
```

### 6. Using Global

❌ **Bad:**
```python
counter = 0

def increment():
    global counter  # Avoid global state
    counter += 1
```

✅ **Good:**
```python
class Counter:
    def __init__(self):
        self.value = 0
    
    def increment(self):
        self.value += 1

counter = Counter()
counter.increment()
```

## Context Managers

Always use context managers for resources:

❌ **Bad:**
```python
f = open('file.txt')
content = f.read()
f.close()  # What if read() raises exception?
```

✅ **Good:**
```python
with open('file.txt') as f:
    content = f.read()  # File closed automatically
```

## List Comprehensions

Use comprehensions for clarity:

❌ **Bad:**
```python
squares = []
for x in numbers:
    squares.append(x ** 2)
```

✅ **Good:**
```python
squares = [x ** 2 for x in numbers]

# With filter
even_squares = [x ** 2 for x in numbers if x % 2 == 0]

# Generator for memory efficiency
squares = (x ** 2 for x in numbers)
```

## Testing Python Code

### Use pytest

```python
import pytest

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def test_divide_happy_path():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_divide_floats():
    assert abs(divide(10, 3) - 3.333) < 0.01

def test_divide_negative():
    assert divide(-10, 2) == -5
```

### Run tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=my_module

# Run specific test
pytest test_file.py::test_function
```

## Code Quality Tools

### Auto-format with Black

```bash
# Install
pip install black

# Format file
black your_file.py

# Configure in pyproject.toml
[tool.black]
line-length = 88
target-version = ['py39']
```

### Lint with ruff

```bash
# Install
pip install ruff

# Check
ruff check your_file.py

# Fix automatically
ruff check --fix your_file.py
```

### Type check with mypy

```bash
# Install
pip install mypy

# Check
mypy your_file.py
```

### Recommended setup

```toml
[tool.ruff]
line-length = 88
target-version = "py39"

[tool.mypy]
python_version = "3.9"
warn_return_any = true
disallow_untyped_defs = true

[tool.black]
line-length = 88
target-version = ['py39']
```

Run in CI: `ruff check . && mypy . && black --check .`

## Python Checklist

- [ ] Follows PEP 8 naming conventions
- [ ] Uses type hints for all functions
- [ ] Docstrings present and complete
- [ ] No mutable default arguments
- [ ] Proper exception handling (specific exceptions)
- [ ] No global state
- [ ] Uses context managers for resources
- [ ] List comprehensions for clarity
- [ ] Pytest tests with good coverage
- [ ] Passes ruff, mypy, black checks
- [ ] No commented-out code
- [ ] No unused imports

## Reference

- [PEP 8 - Style Guide](https://pep8.org/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [Google Style Guide - Python](https://google.github.io/styleguide/pyguide.html)
