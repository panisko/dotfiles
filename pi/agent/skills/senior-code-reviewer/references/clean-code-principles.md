# Clean Code Principles

Based on Robert C. Martin's "Clean Code" and industry best practices.

## 1. Meaningful Names

### Use Names That Reveal Intent

❌ **Bad:**
```python
def get_data(d1, d2):
    if d1 < d2:
        return d1
    return d2

x = get_data(12, 5)
```

✅ **Good:**
```python
def get_minimum_value(value1, value2):
    """Return the smaller of two values."""
    if value1 < value2:
        return value1
    return value2

minimum = get_minimum_value(12, 5)
```

### Avoid Misleading Names

❌ **Bad:**
```python
accounts_list = []  # Not actually a list variable, it's a collection

get_account_by_id = get_accounts()  # Function name suggests single item, returns many
```

✅ **Good:**
```python
accounts = []

get_accounts_by_department = get_accounts(department='sales')
```

### Use Pronounceable Names

❌ **Bad:**
```python
ymdhms = "20230515093045"
genymdhms = "20230515093045"
```

✅ **Good:**
```python
timestamp = "2023-05-15T09:30:45Z"
generated_timestamp = "2023-05-15T09:30:45Z"
```

### Use Searchable Names

❌ **Bad:**
```python
for i in range(5):  # What does 5 mean?
    process(i)
```

✅ **Good:**
```python
MAX_RETRY_ATTEMPTS = 5

for attempt in range(MAX_RETRY_ATTEMPTS):
    process(attempt)
```

## 2. Functions

### Small Functions

A function should do one thing. If it's longer than 20 lines, it probably does multiple things.

❌ **Bad:**
```python
def process_order(order):  # Does validation, calculation, storage, logging
    # 80 lines of code
    pass
```

✅ **Good:**
```python
def process_order(order):
    """Orchestrate order processing."""
    validate_order(order)
    total = calculate_total(order)
    save_order(order, total)
    log_order_processed(order)

def validate_order(order):
    """Validate order structure. (5 lines)"""
    pass

def calculate_total(order):
    """Calculate order total. (5 lines)"""
    pass
```

### Functions Should Do One Thing

The name should describe exactly one purpose.

❌ **Bad:**
```python
def update_and_notify_user(user_id, new_data):
    # Multiple responsibilities
    update_database(user_id, new_data)
    send_email(user_id, new_data)
    log_change(user_id, new_data)
```

✅ **Good:**
```python
def update_user(user_id, new_data):
    """Update user data."""
    update_database(user_id, new_data)

# Separate function
def notify_user_of_change(user_id, new_data):
    """Send notification to user."""
    send_email(user_id, new_data)
    log_change(user_id, new_data)
```

### Keep Parameter Count Low

❌ **Bad:**
```python
def create_user(first_name, last_name, email, phone, address, city, state, zip_code, country):
    pass
```

✅ **Good:**
```python
class UserData:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.email = None
        self.phone = None
        self.address = None

def create_user(user_data):
    pass
```

### Use Descriptive Function Names

❌ **Bad:**
```python
def process(data):
    pass

def handle(request):
    pass

def execute(command):
    pass
```

✅ **Good:**
```python
def calculate_monthly_revenue(sales_data):
    pass

def validate_http_request(request):
    pass

def execute_database_migration(migration):
    pass
```

## 3. Comments

### Good Comments

✅ **Explain Why, Not What**
```python
# Users typically wait 30 seconds for response; requests after that timeout
# This 35-second threshold gives 5 seconds buffer
CONNECTION_TIMEOUT_SECONDS = 35
```

✅ **Clarify Complex Algorithms**
```python
def calculate_interest(principal, rate, years):
    """
    Calculate compound interest.
    
    Formula: A = P(1 + r/n)^(nt)
    Where: P = principal, r = annual rate, n = compounds per year, t = years
    """
    n = 12  # Monthly compounding
    return principal * ((1 + rate / n) ** (n * years))
```

✅ **Document Workarounds**
```python
# TODO: Replace with proper validation library once Cerberus supports nested schemas
if not validate_user_input(data):
    pass
```

### Bad Comments (Avoid)

❌ **Restate What the Code Already Says**
```python
# Add 1 to counter
counter += 1

# Check if age is greater than 18
if age > 18:
    pass
```

❌ **Leave TODO Comments That Never Get Done**
```python
# TODO: This is a hack, need to refactor
# FIXME: This will break when database changes
```

### Solution: Use Clear Code Instead

```python
# Instead of comment, use better naming:
retry_count = 0
retry_count += 1

is_adult = age > 18
if is_adult:
    pass
```

## 4. Error Handling

### Use Exceptions, Not Error Codes

❌ **Bad:**
```python
def find_user(user_id):
    user = db.get(user_id)
    if user is None:
        return -1  # -1 means error?
    return user
```

✅ **Good:**
```python
def find_user(user_id):
    user = db.get(user_id)
    if user is None:
        raise UserNotFoundError(f"User {user_id} not found")
    return user
```

### Handle Exceptions Specifically

❌ **Bad:**
```python
try:
    user = get_user(user_id)
except:  # Catches all exceptions!
    logger.error("Error")
    pass
```

✅ **Good:**
```python
try:
    user = get_user(user_id)
except UserNotFoundError:
    logger.error(f"User {user_id} not found")
    raise
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    raise
```

## 5. Formatting

### Be Consistent

Use your language's standard style guide:
- Python: PEP 8
- JavaScript: Google Style Guide
- Java: Google Style Guide

### Keep Lines Reasonable Length

Aim for 80-120 characters (easier to read).

### Group Related Code

```python
# Bad: Mixed concerns
user = User()
user.name = "Alice"
connection = connect_to_db()
user.email = "alice@example.com"
connection.save(user)

# Good: Group by concern
user = User()
user.name = "Alice"
user.email = "alice@example.com"

connection = connect_to_db()
connection.save(user)
```

## 6. SOLID Principles

### Single Responsibility Principle (SRP)

Each class/function should have one reason to change.

❌ **Bad:**
```python
class User:
    def save(self):
        # Saving logic
        pass
    
    def send_email(self):
        # Email logic
        pass
    
    def generate_report(self):
        # Reporting logic
        pass
```

✅ **Good:**
```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    def save(self, user):
        pass

class EmailService:
    def send_to_user(self, user):
        pass

class UserReporter:
    def generate_report(self, user):
        pass
```

### Open/Closed Principle (OCP)

Classes should be open for extension, closed for modification.

❌ **Bad:**
```python
def calculate_discount(user_type):
    if user_type == 'premium':
        return 0.20
    elif user_type == 'regular':
        return 0.05
    elif user_type == 'new':  # Need to modify function for each new type
        return 0.10
```

✅ **Good:**
```python
class DiscountCalculator:
    def calculate(self, user):
        raise NotImplementedError()

class PremiumDiscountCalculator(DiscountCalculator):
    def calculate(self, user):
        return 0.20

class RegularDiscountCalculator(DiscountCalculator):
    def calculate(self, user):
        return 0.05

# New type? Add new calculator, don't modify existing code
class NewUserDiscountCalculator(DiscountCalculator):
    def calculate(self, user):
        return 0.10
```

### Liskov Substitution Principle (LSP)

Subclasses must be substitutable for parent classes without breaking code.

### Interface Segregation Principle (ISP)

Clients should not be forced to depend on methods they don't use.

❌ **Bad:**
```python
class Animal:
    def fly(self):
        pass
    
    def swim(self):
        pass
    
    def run(self):
        pass

class Dog(Animal):
    def fly(self):
        raise NotImplementedError()  # Dog can't fly!
```

✅ **Good:**
```python
class Runnable:
    def run(self):
        pass

class Swimmable:
    def swim(self):
        pass

class Dog(Runnable, Swimmable):
    def run(self):
        pass
    
    def swim(self):
        pass
```

### Dependency Inversion Principle (DIP)

Depend on abstractions, not concrete implementations.

❌ **Bad:**
```python
class PaymentProcessor:
    def process(self, order):
        payment_gateway = PaypalGateway()  # Hard dependency
        payment_gateway.charge(order.total)
```

✅ **Good:**
```python
class PaymentProcessor:
    def __init__(self, payment_gateway):
        self.payment_gateway = payment_gateway  # Injected dependency
    
    def process(self, order):
        self.payment_gateway.charge(order.total)

# Can use any payment gateway
processor = PaymentProcessor(PaypalGateway())
processor = PaymentProcessor(StripeGateway())
```

## Summary Checklist

- [ ] Names reveal intent
- [ ] Functions are small (≤ 20 lines)
- [ ] Functions do one thing
- [ ] Exceptions used for errors (not error codes)
- [ ] Specific exceptions caught
- [ ] Comments explain why, not what
- [ ] Code formatted consistently
- [ ] SOLID principles followed
- [ ] No duplicate code (DRY)
- [ ] Tests comprehensive

**Following these principles makes code that's easier to understand, maintain, and extend.**
