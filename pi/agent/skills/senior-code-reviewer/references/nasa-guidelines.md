# NASA Coding Guidelines

Based on **NASA/JPL (Jet Propulsion Laboratory) Critical Code Rules**, these guidelines prioritize safety, reliability, and maintainability for mission-critical systems.

## 10 Core Rules (NASA JPL C Rules)

### 1. Simplicity and Clarity

**Rule:** Restrict the use of global variables, pointers, recursion, and complex control structures.

**Rationale:** Complex code is error-prone and difficult to verify. Simpler code is more reliable.

**Examples:**

❌ **Bad:**
```python
# Complex nested conditions and global state
cache = {}
def process(data):
    global cache
    if data and isinstance(data, dict):
        for k, v in data.items():
            if k in cache and cache[k] > 0:
                cache[k] -= 1
            else:
                cache[k] = v
    return cache
```

✅ **Good:**
```python
def process(data: dict, cache: dict) -> dict:
    """
    Process data and update cache safely.
    
    Args:
        data: Input data dictionary
        cache: Mutable cache dictionary
        
    Returns:
        Updated cache
        
    Raises:
        ValueError: If data is None or not a dict
    """
    if not data or not isinstance(data, dict):
        raise ValueError("data must be a non-empty dictionary")
    
    for key, value in data.items():
        cache[key] = value
    
    return cache
```

### 2. Fail-Safe Defaults

**Rule:** All functions must validate their inputs and handle all possible error cases explicitly.

**Rationale:** Failures should be safe and visible, never silently incorrect.

**Examples:**

❌ **Bad:**
```python
def parse_age(age_string):
    return int(age_string)  # Crashes on invalid input
```

✅ **Good:**
```python
def parse_age(age_string: str) -> int:
    """
    Parse age from string.
    
    Args:
        age_string: String representation of age
        
    Returns:
        Integer age value
        
    Raises:
        ValueError: If age_string is not a valid positive integer
        TypeError: If age_string is not a string
    """
    if not isinstance(age_string, str):
        raise TypeError(f"age_string must be str, got {type(age_string)}")
    
    try:
        age = int(age_string.strip())
    except ValueError:
        raise ValueError(f"'{age_string}' is not a valid integer")
    
    if age < 0:
        raise ValueError(f"age must be non-negative, got {age}")
    
    return age
```

### 3. Restricted Scope

**Rule:** Keep data and code dependencies local. Functions should be small (10-20 lines), with maximum cyclomatic complexity of 10.

**Rationale:** Limited scope reduces debugging difficulty and makes code easier to understand.

**Examples:**

❌ **Bad:**
```python
def handle_user_request(request):
    global app_state, logger, config, cache
    # 150 lines of nested conditionals...
    # Cyclomatic complexity: 47
```

✅ **Good:**
```python
def validate_user_request(request: dict) -> bool:
    """Validate user request format. (10 lines)"""
    required_fields = {'user_id', 'action', 'timestamp'}
    return required_fields.issubset(request.keys())

def extract_user_id(request: dict) -> int:
    """Extract and validate user ID. (5 lines)"""
    user_id = request.get('user_id')
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError(f"Invalid user_id: {user_id}")
    return user_id

def handle_user_request(request: dict, app_state: AppState) -> Response:
    """Orchestrate user request handling. (15 lines)"""
    try:
        if not validate_user_request(request):
            return Response(status=400, message="Invalid request")
        
        user_id = extract_user_id(request)
        result = app_state.process(user_id, request['action'])
        return Response(status=200, data=result)
        
    except ValueError as e:
        return Response(status=400, message=str(e))
    except Exception as e:
        return Response(status=500, message="Internal error")
```

### 4. Input Validation

**Rule:** Check all input from untrusted sources. Never assume input is valid.

**Rationale:** Most security vulnerabilities stem from invalid input assumptions.

**Examples:**

❌ **Bad:**
```python
@app.route('/user/<id>')
def get_user(id):
    return db.query(f"SELECT * FROM users WHERE id = {id}")  # SQL injection!
```

✅ **Good:**
```python
from typing import Optional

@app.route('/user/<id>')
def get_user(id: str) -> dict:
    """
    Retrieve user by ID.
    
    Args:
        id: User identifier (validated)
        
    Returns:
        User data dict
        
    Raises:
        ValueError: If id format is invalid
        NotFoundError: If user doesn't exist
    """
    # Validate input format
    if not id or not isinstance(id, str):
        raise ValueError("id must be a non-empty string")
    
    if not id.isdigit():
        raise ValueError(f"id must contain only digits, got: {id}")
    
    user_id = int(id)
    
    if user_id <= 0:
        raise ValueError(f"id must be positive, got: {user_id}")
    
    # Use parameterized query (prepared statement)
    user = db.query("SELECT * FROM users WHERE id = ?", (user_id,))
    
    if not user:
        raise NotFoundError(f"User {user_id} not found")
    
    return user
```

### 5. Explicit Error Handling

**Rule:** All possible errors must be caught and handled explicitly. Never use bare `except:` or ignore exceptions.

**Rationale:** Silent failures are catastrophic in critical systems.

**Examples:**

❌ **Bad:**
```python
def save_config(filename, config):
    try:
        with open(filename, 'w') as f:
            json.dump(config, f)
    except:
        pass  # Silently ignore all errors!
```

✅ **Good:**
```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def save_config(filename: str, config: dict) -> bool:
    """
    Save configuration to file.
    
    Args:
        filename: Path to config file
        config: Configuration dictionary
        
    Returns:
        True if successful
        
    Raises:
        TypeError: If config is not a dict
        IOError: If file cannot be written
        ValueError: If config contains non-serializable data
    """
    if not isinstance(config, dict):
        raise TypeError(f"config must be dict, got {type(config)}")
    
    if not filename or not isinstance(filename, str):
        raise ValueError("filename must be non-empty string")
    
    try:
        # Validate JSON serializability
        json.dumps(config)
    except (TypeError, ValueError) as e:
        raise ValueError(f"config contains non-serializable data: {e}")
    
    try:
        # Write to temporary file first (atomic operation)
        temp_filename = f"{filename}.tmp"
        with open(temp_filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Atomic rename
        import os
        os.rename(temp_filename, filename)
        
        logger.info(f"Config saved to {filename}")
        return True
        
    except IOError as e:
        logger.error(f"Failed to write config: {e}")
        raise IOError(f"Cannot write to {filename}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error saving config: {e}")
        raise
```

### 6. Automatic Resource Management

**Rule:** Use language constructs for automatic resource cleanup. Release all resources even on error paths.

**Rationale:** Resource leaks can cause cascading failures.

**Examples:**

❌ **Bad:**
```python
def read_file(filename):
    f = open(filename, 'r')
    data = f.read()
    f.close()
    process(data)  # If process() crashes, file handle leaks
    return data
```

✅ **Good:**
```python
def read_file(filename: str) -> str:
    """Read file with guaranteed cleanup."""
    try:
        with open(filename, 'r') as f:
            data = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")
    except IOError as e:
        raise IOError(f"Cannot read {filename}: {e}")
    
    return data  # File automatically closed, even if this raises
```

### 7. Defensive Copying

**Rule:** Copy mutable data when passing to functions. Verify copied data before use.

**Rationale:** Prevents unexpected data modification by callers.

**Examples:**

❌ **Bad:**
```python
def process_list(items):
    # Caller can modify original list
    items.append("malicious")  # Modifies caller's list!
    return len(items)
```

✅ **Good:**
```python
from typing import List

def process_list(items: List[str]) -> int:
    """
    Process list safely.
    
    Args:
        items: List to process
        
    Returns:
        Count of items
    """
    if not isinstance(items, list):
        raise TypeError(f"items must be list, got {type(items)}")
    
    # Create defensive copy
    items_copy = items.copy()
    
    # Verify copy integrity
    if not all(isinstance(item, str) for item in items_copy):
        raise ValueError("All items must be strings")
    
    return len(items_copy)  # Original untouched
```

### 8. Single Responsibility Principle

**Rule:** Each function/module should have one clear purpose.

**Rationale:** Single responsibility makes testing and maintenance easier.

**Examples:**

❌ **Bad:**
```python
def process_order(order):
    # Multiple responsibilities: validation, calculation, storage
    if not order.get('items'):
        raise ValueError("No items")
    
    total = sum(item['price'] * item['qty'] for item in order['items'])
    
    with open('orders.csv', 'a') as f:
        f.write(f"{order['id']},{total}\n")
    
    requests.post('https://payment-api.com', json={'amount': total})
```

✅ **Good:**
```python
def validate_order(order: dict) -> None:
    """Validate order structure. Single responsibility."""
    if not order or not isinstance(order, dict):
        raise TypeError("order must be dict")
    if 'items' not in order or not order['items']:
        raise ValueError("order must have items")
    if 'id' not in order:
        raise ValueError("order must have id")

def calculate_total(items: List[dict]) -> float:
    """Calculate order total. Single responsibility."""
    if not items:
        raise ValueError("items cannot be empty")
    return sum(item['price'] * item['qty'] for item in items)

def save_order(order_id: str, total: float, storage: OrderStorage) -> None:
    """Save order to storage. Single responsibility."""
    storage.save(order_id, total)

def charge_payment(order_id: str, total: float, payment_client) -> None:
    """Charge payment. Single responsibility."""
    payment_client.charge(order_id, total)

def process_order(order: dict, storage: OrderStorage, payment: PaymentClient) -> None:
    """Orchestrate order processing."""
    validate_order(order)
    total = calculate_total(order['items'])
    save_order(order['id'], total, storage)
    charge_payment(order['id'], total, payment)
```

### 9. No Global Variables

**Rule:** Avoid global variables; pass state explicitly as parameters.

**Rationale:** Global state makes code unpredictable and difficult to test.

**Examples:**

❌ **Bad:**
```python
# Global state - BAD!
db_connection = None
current_user = None
config = {}

def process_order(order_id):
    global db_connection, current_user
    # Relies on implicit global state
    order = db_connection.get_order(order_id)
    log_action(f"Order {order_id} processed by {current_user}")
```

✅ **Good:**
```python
def process_order(
    order_id: int,
    db: Database,
    current_user: User,
    logger: Logger
) -> Order:
    """
    Process order. All dependencies explicit.
    
    Args:
        order_id: Order identifier
        db: Database connection
        current_user: User performing operation
        logger: Logger instance
        
    Returns:
        Processed order
    """
    order = db.get_order(order_id)
    logger.info(f"Order {order_id} processed by {current_user.name}")
    return order
```

### 10. Complete Testing

**Rule:** Achieve high code coverage (target 100%), test all error paths, test boundary conditions.

**Rationale:** Untested code will fail in production.

**Examples:**

❌ **Bad:**
```python
def calculate_discount(price, discount_percent):
    return price * (1 - discount_percent / 100)

# Only test happy path
assert calculate_discount(100, 10) == 90
```

✅ **Good:**
```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Calculate discounted price.
    
    Args:
        price: Original price
        discount_percent: Discount percentage (0-100)
        
    Returns:
        Discounted price
        
    Raises:
        ValueError: If price is negative or discount_percent invalid
    """
    if price < 0:
        raise ValueError(f"price cannot be negative: {price}")
    if not (0 <= discount_percent <= 100):
        raise ValueError(f"discount_percent must be 0-100: {discount_percent}")
    
    return price * (1 - discount_percent / 100)


# Test suite - comprehensive
def test_calculate_discount():
    # Normal case
    assert calculate_discount(100, 10) == 90
    
    # Edge cases
    assert calculate_discount(100, 0) == 100  # No discount
    assert calculate_discount(100, 100) == 0  # Full discount
    assert calculate_discount(0, 50) == 0  # Free item
    
    # Precision
    assert abs(calculate_discount(99.99, 33.33) - 66.66) < 0.01
    
    # Error cases
    with pytest.raises(ValueError, match="cannot be negative"):
        calculate_discount(-10, 5)
    
    with pytest.raises(ValueError, match="must be 0-100"):
        calculate_discount(100, 150)
    
    with pytest.raises(ValueError, match="must be 0-100"):
        calculate_discount(100, -5)
```

## Key Metrics

When reviewing code against NASA standards, measure:

| Metric | Target | Rationale |
|--------|--------|-----------|
| **Function Length** | 10-20 lines | Easy to understand, test |
| **Cyclomatic Complexity** | ≤ 10 | Fewer execution paths = easier to test |
| **Code Coverage** | ≥ 95% (ideally 100%) | All error paths tested |
| **Test/Code Ratio** | 1:1 minimum | Comprehensive test coverage |
| **Global Variables** | 0 | Explicit dependency management |
| **Nested Depth** | ≤ 3 levels | Avoid cognitive overload |
| **Comments/Code** | 25-30% | Self-documenting code preferred |
| **Error Handling** | 100% of exceptions caught | No silent failures |

## Application to Different Languages

While originally C-focused, NASA principles apply universally:

### Python
- Use type hints (PEP 484)
- Prefer built-in error handling (try/except)
- Use context managers (with statements)
- Avoid global state; use dependency injection

### JavaScript/TypeScript
- Use async/await with proper error handling
- Enforce TypeScript strict mode
- Avoid global namespace pollution
- Use error boundaries

### Java
- Favor composition over inheritance
- Use try-with-resources for resource cleanup
- Enforce immutability (final keyword)
- Use checked exceptions explicitly

### C/C++
- Follow strict coding rules (limit constructs)
- Use assertions for error checking
- Prefer stack allocation over heap
- Explicit memory management

## Reference

- **Original:** NASA/JPL "C Style Guidelines" - George Elam, et al.
- **Extended:** "The Power of 10: Rules for Developing Safety-Critical Code" - Gerald J. Holzmann
- **Application:** These principles apply to all programming languages and contexts

## Checklist for NASA Compliance

- [ ] Functions are 10-20 lines max
- [ ] Cyclomatic complexity ≤ 10
- [ ] All inputs validated
- [ ] All error cases handled explicitly
- [ ] No global variables
- [ ] No silent failures
- [ ] Code coverage ≥ 95%
- [ ] Automatic resource cleanup
- [ ] Defensive copying of mutable data
- [ ] Clear, descriptive naming
