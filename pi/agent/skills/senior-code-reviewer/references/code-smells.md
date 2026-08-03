# Common Code Smells

Code smells are indicators that there might be deeper problems in the code. They're not bugs, but symptoms that the code might benefit from refactoring.

## High-Level Smells

### 1. Duplicated Code

**Smell:** The same code appears in multiple places.

**Problem:** Maintenance nightmare - fix a bug in one place, miss it elsewhere.

**Example:**
```python
# Function 1
def validate_email_1(email):
    if not email or '@' not in email or '.' not in email:
        return False
    return True

# Function 2
def validate_email_2(email):
    if not email or '@' not in email or '.' not in email:
        return False
    return True
```

**Solution:** Extract to shared function:
```python
def validate_email(email):
    """Validate email format."""
    if not email or '@' not in email or '.' not in email:
        raise ValueError(f"Invalid email: {email}")
    return True

# Use in both places
validate_email_1 = validate_email
validate_email_2 = validate_email
```

### 2. Long Methods/Functions

**Smell:** Methods/functions are more than 20 lines.

**Problem:** Hard to understand, test, and reuse.

**Example:**
```python
def process_order(order):  # 80 lines!
    # Validate
    if not order: raise ValueError()
    if not order.get('items'): raise ValueError()
    # ... 20 more lines
    
    # Calculate
    total = 0
    for item in order['items']:
        total += item['price'] * item['qty']
    # ... 15 more lines
    
    # Save
    db.save(order)
    # ... 30 more lines
```

**Solution:** Break into smaller functions:
```python
def process_order(order):
    """Main orchestration."""
    validate_order(order)
    total = calculate_total(order['items'])
    save_order(order, total)

def validate_order(order):
    """Validate order."""
    if not order: raise ValueError("Order required")
    if not order.get('items'): raise ValueError("Items required")

def calculate_total(items):
    """Calculate total."""
    return sum(item['price'] * item['qty'] for item in items)

def save_order(order, total):
    """Save order."""
    db.save(order, total)
```

### 3. Complex Conditional Logic

**Smell:** Many if/else branches or deeply nested conditions.

**Problem:** Hard to understand all paths; easy to miss edge cases.

**Example:**
```python
def get_discount(user_type, purchase_amount, is_holiday):
    if user_type == 'premium':
        if purchase_amount > 1000:
            if is_holiday:
                return 0.20
            else:
                return 0.15
        else:
            if is_holiday:
                return 0.10
            else:
                return 0.05
    elif user_type == 'regular':
        if purchase_amount > 500:
            return 0.05
        else:
            return 0.02
    else:
        return 0
```

**Solution:** Use lookup tables or guard clauses:
```python
def get_discount(user_type, purchase_amount, is_holiday):
    """Get discount based on user type and purchase."""
    discount_rules = {
        ('premium', True, True): 0.20,    # (user, high_amount, holiday)
        ('premium', True, False): 0.15,
        ('premium', False, True): 0.10,
        ('premium', False, False): 0.05,
        ('regular', True, False): 0.05,
        ('regular', False, False): 0.02,
    }
    
    high_amount = purchase_amount > (1000 if user_type == 'premium' else 500)
    key = (user_type, high_amount, is_holiday)
    return discount_rules.get(key, 0)
```

## Class-Level Smells

### 4. Feature Envy

**Smell:** A method uses more methods from another class than from its own.

**Problem:** The method belongs in the other class.

**Example:**
```python
class Order:
    def apply_discount(self, customer):
        # Using more Customer methods than Order methods!
        discount = customer.get_loyalty_years() * 0.05
        discount += customer.get_total_spent() * 0.01
        discount = min(discount, customer.get_max_discount())
        self.total *= (1 - discount)
```

**Solution:** Move logic to the class it belongs to:
```python
class Customer:
    def calculate_discount(self):
        discount = self.get_loyalty_years() * 0.05
        discount += self.get_total_spent() * 0.01
        discount = min(discount, self.get_max_discount())
        return discount

class Order:
    def apply_discount(self, customer):
        discount = customer.calculate_discount()
        self.total *= (1 - discount)
```

### 5. Inappropriate Intimacy

**Smell:** A class accesses internal data of another class.

**Problem:** Tight coupling; changes to one break the other.

**Example:**
```python
class PaymentProcessor:
    def process(self, customer):
        # Directly accessing private data!
        if customer._balance < 100:  # Should use public method
            raise ValueError("Insufficient funds")
```

**Solution:** Use public interfaces:
```python
class Customer:
    def has_sufficient_balance(self, amount):
        return self._balance >= amount

class PaymentProcessor:
    def process(self, customer):
        if not customer.has_sufficient_balance(100):
            raise ValueError("Insufficient funds")
```

### 6. Data Clumps

**Smell:** Multiple methods have similar groups of parameters.

**Problem:** Indicates missing abstraction.

**Example:**
```python
def create_user(first_name, last_name, email, phone):
    pass

def update_user(first_name, last_name, email, phone):
    pass

def validate_user(first_name, last_name, email, phone):
    pass
```

**Solution:** Create a class for the group:
```python
class User:
    def __init__(self, first_name, last_name, email, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
    
    def validate(self):
        pass

def create_user(user):
    user.validate()
    # ...

def update_user(user):
    user.validate()
    # ...
```

## Function-Level Smells

### 7. Magic Numbers/Strings

**Smell:** Hard-coded values scattered throughout code.

**Problem:** Meaning unclear; difficult to change; error-prone.

**Example:**
```python
def calculate_price(quantity, unit_price):
    if quantity > 100:
        return quantity * unit_price * 0.85  # What's 0.85?
    elif quantity > 50:
        return quantity * unit_price * 0.90  # What's 0.90?
    else:
        return quantity * unit_price * 0.95  # What's 0.95?
```

**Solution:** Extract to named constants:
```python
# Define constants at module level
MIN_BULK_DISCOUNT_THRESHOLD = 100
MIN_DISCOUNT_THRESHOLD = 50

BULK_DISCOUNT_RATE = 0.85      # 15% off
MEDIUM_DISCOUNT_RATE = 0.90    # 10% off
SMALL_DISCOUNT_RATE = 0.95     # 5% off

def calculate_price(quantity, unit_price):
    """Calculate discounted price based on quantity."""
    if quantity > MIN_BULK_DISCOUNT_THRESHOLD:
        return quantity * unit_price * BULK_DISCOUNT_RATE
    elif quantity > MIN_DISCOUNT_THRESHOLD:
        return quantity * unit_price * MEDIUM_DISCOUNT_RATE
    else:
        return quantity * unit_price * SMALL_DISCOUNT_RATE
```

### 8. Long Parameter Lists

**Smell:** Functions have many parameters (more than 3-4).

**Problem:** Hard to call; easy to pass arguments in wrong order.

**Example:**
```python
def create_report(title, start_date, end_date, format, include_summary, 
                 include_charts, max_rows, sort_by, filter_by, theme, language):
    pass
```

**Solution:** Create configuration object:
```python
class ReportConfig:
    def __init__(self, title, start_date, end_date):
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        
        # Defaults
        self.format = 'pdf'
        self.include_summary = True
        self.include_charts = True
        self.max_rows = 1000
        # ...

def create_report(config):
    pass
```

### 9. Poorly Named Variables/Functions

**Smell:** Names don't clearly indicate purpose: `x`, `temp`, `data`, `process()`.

**Problem:** Code is unreadable; developers waste time figuring out what things are.

**Example:**
```python
def p(d):
    t = []
    for x in d:
        if x > 0:
            t.append(x * 2)
    return t
```

**Solution:** Use clear, descriptive names:
```python
def double_positive_numbers(numbers):
    """Double all positive numbers in a list."""
    doubled_numbers = []
    for number in numbers:
        if number > 0:
            doubled_numbers.append(number * 2)
    return doubled_numbers

# Or more Pythonic:
def double_positive_numbers(numbers):
    return [n * 2 for n in numbers if n > 0]
```

### 10. Comments Explaining Bad Code

**Smell:** Code requires extensive comments to understand.

**Problem:** The code is unclear; comments shouldn't compensate for bad code.

**Example:**
```python
def calc(p, q):
    # Loop through customers and find those with balance > 1000
    # Then multiply by 0.15 to get 15% discount
    # Add to list
    t = []
    for c in p:
        if c['bal'] > 1000:
            t.append(c['id'], c['bal'] * 0.15)
    return t
```

**Solution:** Make code self-explanatory:
```python
def find_high_value_customers_with_discounts(customers, high_value_threshold=1000, discount_rate=0.15):
    """
    Find customers with balance above threshold and calculate their discount.
    
    Args:
        customers: List of customer dictionaries
        high_value_threshold: Balance threshold for discount eligibility
        discount_rate: Discount rate to apply
        
    Returns:
        List of (customer_id, discount_amount) tuples
    """
    discounts = []
    for customer in customers:
        if customer['balance'] > high_value_threshold:
            discount = customer['balance'] * discount_rate
            discounts.append((customer['id'], discount))
    return discounts
```

## Module-Level Smells

### 11. Unused/Dead Code

**Smell:** Methods, classes, or imports that aren't used.

**Problem:** Clutters codebase; confuses maintainers; indicates incomplete refactoring.

**Solution:** Delete it. Use version control to recover if needed.

### 12. Shotgun Surgery

**Smell:** A single change requires modifications to multiple unrelated classes.

**Problem:** Classes are too tightly coupled; responsibility is spread.

**Solution:** Reorganize to group related changes together.

### 13. Parallel Inheritance Hierarchies

**Smell:** For every subclass of A, there's a parallel subclass of B.

**Problem:** Indicates missing abstraction or poor design.

**Solution:** Merge hierarchies or use composition instead of inheritance.

## Quick Reference Checklist

When code reviewing, watch for:

- [ ] Duplicated code blocks
- [ ] Methods/functions > 20 lines
- [ ] Nested if/else more than 3 levels deep
- [ ] Parameter lists with > 3-4 parameters
- [ ] Variables/functions with unclear names (x, temp, data, process)
- [ ] Magic numbers/strings without explanation
- [ ] Code requiring extensive comments to understand
- [ ] Similar patterns in different classes (data clumps)
- [ ] Methods accessing private data of other classes
- [ ] Long switch statements or if/else chains

**Fix these and your code will be much cleaner!**

## See Also

- [Refactoring Patterns](refactoring-patterns.md)
- [Clean Code Principles](clean-code-principles.md)
- [NASA Guidelines](nasa-guidelines.md)
