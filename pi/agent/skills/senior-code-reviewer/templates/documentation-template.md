# Documentation Template

Use this template to ensure complete, professional documentation.

## Module/Package Documentation

```markdown
# Module Name

Brief one-line description of what this module does.

## Overview

Detailed paragraph explaining:
- What the module does
- When you should use it
- Key features or capabilities
- Any dependencies or prerequisites

## Installation

```bash
pip install module-name
# or
poetry add module-name
```

## Quick Start

```python
from module_name import MyClass

# Basic usage example
obj = MyClass(param="value")
result = obj.do_something()
print(result)  # Output: expected result
```

## Features

- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Usage

### Basic Usage

Explain the most common use case with example.

### Advanced Usage

Explain less common but important features.

### Configuration

Document all configuration options.

## API Reference

### Classes

#### ClassName

```python
class ClassName:
    """Short description."""
```

**Description:** Detailed explanation

**Methods:**
- `method_name(param)`: What it does
- `another_method()`: What it does

### Functions

#### function_name

```python
function_name(param1: Type1, param2: Type2) -> ReturnType:
    """One-line description."""
```

**Description:** Detailed explanation with context

**Parameters:**
- `param1` (Type1): Description
- `param2` (Type2): Description

**Returns:** (ReturnType) Description of return value

**Raises:** (ExceptionType) Description of when raised

**Examples:**
```python
result = function_name(arg1, arg2)
print(result)  # Expected output
```

## Examples

### Example 1: Basic Use Case

Complete working example showing most common usage.

### Example 2: Advanced Use Case

Example showing advanced features.

### Example 3: Error Handling

Example showing proper error handling.

## Configuration

Document all configuration options:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `option1` | str | "default" | What it controls |
| `option2` | int | 100 | What it controls |

## Troubleshooting

### Problem: Something doesn't work

**Symptom:** Description of the problem

**Cause:** Why this happens

**Solution:** How to fix it

```bash
# Code to fix the issue
```

### Problem: Error message "X"

**Solution:** Step-by-step instructions

## Contributing

Guidelines for contributing to this project.

## License

License information.

## See Also

- [Related Module](link)
- [Documentation](link)
```

---

## Function Documentation

### Google Style

```python
def my_function(param1: str, param2: int) -> Dict[str, Any]:
    """
    One-line summary of what the function does.
    
    Extended description explaining more details about the function,
    including any important context or usage notes.
    
    Args:
        param1: Description of param1, type and usage
        param2: Description of param2, type and usage
        
    Returns:
        Description of return value and its structure
        
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not int
        
    Note:
        Any special notes about the function
        
    Warning:
        Any warnings about usage
        
    Examples:
        >>> result = my_function("test", 42)
        >>> print(result)
        {'status': 'success', 'data': [...]}
        
        >>> my_function("", 42)  # Raises ValueError
        Traceback (most recent call last):
            ...
        ValueError: param1 cannot be empty
    """
    pass
```

### NumPy Style

```python
def my_function(param1: str, param2: int) -> Dict[str, Any]:
    """
    One-line summary of what the function does.
    
    Extended description explaining more details.
    
    Parameters
    ----------
    param1 : str
        Description of param1
    param2 : int
        Description of param2
        
    Returns
    -------
    Dict[str, Any]
        Description of return value and structure
        
    Raises
    ------
    ValueError
        When param1 is empty
    TypeError
        When param2 is not int
        
    Notes
    -----
    Any special notes about the function
    
    Examples
    --------
    >>> result = my_function("test", 42)
    >>> print(result)
    {'status': 'success', 'data': [...]}
    """
    pass
```

---

## Class Documentation

```python
class MyClass:
    """
    One-line summary of what this class does.
    
    Extended description explaining the class purpose, typical usage,
    and important details about its behavior.
    
    Attributes:
        attr1: Description of attribute1
        attr2: Description of attribute2
        
    Examples:
        >>> obj = MyClass(param="value")
        >>> result = obj.process()
        >>> print(result)
        processed_value
    """
    
    def __init__(self, param: str) -> None:
        """
        Initialize MyClass.
        
        Args:
            param: Description of initialization parameter
            
        Raises:
            ValueError: If param is invalid
        """
        pass
    
    def public_method(self, arg: int) -> str:
        """
        One-line description of what this method does.
        
        Args:
            arg: Description of argument
            
        Returns:
            Description of return value
        """
        pass
    
    def _private_method(self) -> None:
        """Private method description (single underscore = internal use)."""
        pass
```

---

## Code Comment Guidelines

### Good Comments

✅ Explain **why**, not what:
```python
# Request timeout is set to 35 seconds because:
# - Most responses return within 30 seconds
# - 5-second buffer prevents premature timeouts
# - Aligns with monitoring alert threshold (40s)
REQUEST_TIMEOUT = 35
```

✅ Clarify complex algorithms:
```python
def calculate_discount(amount, tier):
    # Using logarithmic scaling to smooth tier transitions
    # Prevents sharp jumps between discount levels
    base_discount = math.log(tier + 1) * 0.05
    return base_discount * amount
```

✅ Explain workarounds:
```python
# TODO: Replace with proper UUID comparison once database migrates to UUID type
# Current database stores UUIDs as strings, causing comparison issues
user_id_str = str(user_id)
```

### Bad Comments

❌ Restate what code already says:
```python
# Increment counter
counter += 1

# Check if user is adult
if age >= 18:
    pass
```

❌ Leave permanent TODOs:
```python
# FIXME: This is a hack
# TODO: Refactor this later
# NOTE: This might break eventually
```

### Solution: Write Better Code

```python
# Instead of explaining counter increment, use better naming:
login_attempts += 1

# Instead of explaining age check, use better naming:
is_adult = age >= 18
if is_adult:
    grant_access()
```

---

## README Structure

```markdown
# Project Name

One-line description

## Status

Build status badges, version, etc.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```bash
pip install project-name
```

## Quick Start

```python
# Minimal working example
```

## Documentation

Links to full documentation

## Examples

- Example 1 with link
- Example 2 with link

## API

Link to API documentation

## Configuration

How to configure the project

## Contributing

Contributing guidelines

## License

License info

## Citation

How to cite this project

## Support

How to get help
```

---

## Checklist for Documentation

- [ ] Module docstring present and complete
- [ ] All public functions/classes have docstrings
- [ ] All parameters documented with types
- [ ] Return values documented
- [ ] Exceptions documented (which can be raised and when)
- [ ] Usage examples provided
- [ ] Complex logic explained with comments
- [ ] Type hints present for all functions
- [ ] README is clear and complete
- [ ] API documentation links provided
- [ ] No outdated documentation
- [ ] No placeholder comments left behind

## Tools

- **Document generation:** Sphinx, pdoc3
- **Style checking:** pydocstyle
- **Type checking:** mypy
- **Documentation host:** Read the Docs, GitHub Pages

---

## See Also

- [Google Style Guide - Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [NumPy Documentation Style](https://numpydoc.readthedocs.io/en/latest/format.html)
