# Security Best Practices

Security is not an afterthought. Build it in from the start.

## Input Validation Principles

### Rule 1: Never Trust External Input

All input from outside your immediate system must be validated:
- User input (forms, APIs, files)
- Environment variables
- Configuration files
- Database values (from untrusted sources)
- Network data

### Rule 2: Validate Early

Validate input at the entry point, before processing.

❌ **Bad:**
```python
@app.post("/transfer")
def transfer_money(user_id, amount):
    # Validate too late!
    account = get_account(user_id)  # Wrong user_id causes issues first
    if amount <= 0:
        raise ValueError("Invalid amount")
```

✅ **Good:**
```python
@app.post("/transfer")
def transfer_money(user_id, amount):
    # Validate first
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user_id")
    if not isinstance(amount, float) or amount <= 0:
        raise ValueError("Invalid amount")
    if amount > 1000000:
        raise ValueError("Amount exceeds maximum transfer")
    
    account = get_account(user_id)
```

### Rule 3: Whitelist, Don't Blacklist

Whitelist (allow known good) is more secure than blacklist (block known bad).

❌ **Bad:**
```python
def is_safe_filename(filename):
    # Try to block bad chars - always misses something!
    bad_chars = ['<', '>', '|', '.', '..', '\\']
    for char in bad_chars:
        if char in filename:
            return False
    return True
```

✅ **Good:**
```python
import re

def is_safe_filename(filename):
    # Only allow known-good characters
    if not filename or len(filename) > 255:
        return False
    # Alphanumeric, hyphens, underscores, dots only
    return bool(re.match(r'^[a-zA-Z0-9._-]+$', filename))
```

## Common Vulnerabilities

### SQL Injection

❌ **Vulnerable:**
```python
user_id = request.args.get('id')
query = f"SELECT * FROM users WHERE id = {user_id}"
db.execute(query)
```

✅ **Safe:**
```python
user_id = request.args.get('id')
# Use parameterized query
query = "SELECT * FROM users WHERE id = ?"
db.execute(query, (user_id,))
```

### Command Injection

❌ **Vulnerable:**
```python
filename = request.args.get('file')
os.system(f"ls -la {filename}")  # filename can contain '; rm -rf /'
```

✅ **Safe:**
```python
filename = request.args.get('file')
# Use subprocess with list of args (no shell interpretation)
result = subprocess.run(['ls', '-la', filename], capture_output=True)
```

### Cross-Site Scripting (XSS)

❌ **Vulnerable:**
```python
@app.route('/greet/<name>')
def greet(name):
    return f"<h1>Hello {name}</h1>"  # If name = "<script>alert('xss')</script>"
```

✅ **Safe:**
```python
from markupsafe import escape

@app.route('/greet/<name>')
def greet(name):
    return f"<h1>Hello {escape(name)}</h1>"
```

### Path Traversal

❌ **Vulnerable:**
```python
filename = request.args.get('file')
content = open(f"uploads/{filename}").read()  # filename = "../../../etc/passwd"
```

✅ **Safe:**
```python
import os
from pathlib import Path

filename = request.args.get('file')

# Validate filename
if not filename or not os.path.isfile(filename):
    raise ValueError("Invalid file")

# Ensure file is in allowed directory
uploads_dir = Path('uploads').resolve()
file_path = (uploads_dir / filename).resolve()

if not str(file_path).startswith(str(uploads_dir)):
    raise ValueError("Path traversal attempt detected")

content = file_path.read_text()
```

## Data Protection

### 1. Encrypt Sensitive Data at Rest

```python
from cryptography.fernet import Fernet

# Generate key once, store securely
key = Fernet.generate_key()

cipher = Fernet(key)

# Encrypt passwords
encrypted_password = cipher.encrypt(password.encode())
db.save_password(user_id, encrypted_password)

# Decrypt when needed
password = cipher.decrypt(encrypted_password).decode()
```

### 2. Never Store Sensitive Data Unnecessarily

❌ **Bad:**
```python
def log_payment(user_id, card_number, amount):
    logger.info(f"Payment: user={user_id}, card={card_number}, amount={amount}")
```

✅ **Good:**
```python
def log_payment(user_id, card_last_four, amount):
    logger.info(f"Payment: user={user_id}, card_ending={card_last_four}, amount={amount}")
```

### 3. Use Environment Variables for Secrets

❌ **Bad:**
```python
API_KEY = "secret-key-12345"  # In source code!
DATABASE_PASSWORD = "prod_password_123"  # Hardcoded!
```

✅ **Good:**
```python
import os

API_KEY = os.environ.get('API_KEY')
DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')

if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```

### 4. Hash Passwords

❌ **Bad:**
```python
password_field = password  # Plain text! Never do this!
```

✅ **Good:**
```python
import bcrypt

# Store
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
db.save_password(user_id, hashed)

# Verify
if bcrypt.checkpw(password.encode(), stored_hash):
    user_authenticated = True
```

## Error Handling Security

### Don't Leak Information in Errors

❌ **Bad:**
```python
try:
    user = db.get_user(user_id)
except Exception as e:
    return Response(f"Database error: {e}")  # Reveals database structure!
```

✅ **Good:**
```python
try:
    user = db.get_user(user_id)
except DatabaseError as e:
    logger.error(f"Database error retrieving user {user_id}: {e}")
    return Response("User not found", status=404)  # Generic message
```

## Authentication & Authorization

### 1. Validate Authentication on Every Request

```python
@app.before_request
def check_auth():
    token = request.headers.get('Authorization')
    if not token:
        return Response("Unauthorized", status=401)
    
    if not verify_token(token):
        return Response("Invalid token", status=401)
    
    request.user = get_user_from_token(token)
```

### 2. Enforce Authorization

```python
@app.route('/user/<user_id>')
def get_user(user_id):
    # Check that requester has permission
    if request.user.id != user_id and not request.user.is_admin:
        return Response("Forbidden", status=403)
    
    return get_user_data(user_id)
```

### 3. Use HTTPS Always

- Never transmit sensitive data over HTTP
- Use secure cookies (HttpOnly, Secure, SameSite)

```python
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

## Dependency Security

### 1. Keep Dependencies Updated

```bash
# Check for known vulnerabilities
pip-audit

# Update to latest secure versions
pip install --upgrade <package>
```

### 2. Use Integrity Verification

```bash
# Pin exact versions
pip install Flask==2.3.1

# Or use requirements.txt with hashes
Flask==2.3.1 --hash=sha256:...
```

## Configuration Security

### 1. Separate Configuration by Environment

```python
import os

class Config:
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = "sqlite:///dev.db"

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = os.environ['DATABASE_URL']
    SECRET_KEY = os.environ['SECRET_KEY']

config = os.environ.get('ENV', 'development').lower()
app.config.from_object(f'config.{config.title()}Config')
```

### 2. Don't Expose Sensitive Configuration

❌ **Bad:**
```python
DEBUG = True  # In production!
SQLALCHEMY_ECHO = True  # Logs all SQL queries
```

✅ **Good:**
```python
DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
SQLALCHEMY_ECHO = os.environ.get('SQL_DEBUG', 'false').lower() == 'true'
```

## Security Checklist

- [ ] All inputs are validated and sanitized
- [ ] Parameterized queries used (no string concatenation)
- [ ] No hardcoded secrets or credentials
- [ ] Sensitive data encrypted at rest
- [ ] Passwords hashed with bcrypt/argon2
- [ ] Error messages don't leak information
- [ ] HTTPS/TLS used for all communication
- [ ] Authentication enforced on every request
- [ ] Authorization checked before returning sensitive data
- [ ] Dependencies checked for known vulnerabilities
- [ ] Sensitive data not logged
- [ ] Rate limiting in place for APIs
- [ ] CORS properly configured
- [ ] CSRF tokens implemented (if needed)
- [ ] Security headers set (CSP, X-Frame-Options, etc.)

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [CWE (Common Weakness Enumeration)](https://cwe.mitre.org/)
- [NASA Coding Guidelines](nasa-guidelines.md)
