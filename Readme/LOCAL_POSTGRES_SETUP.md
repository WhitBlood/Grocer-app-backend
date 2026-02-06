# 🐘 Local PostgreSQL Setup for FreshMart

## ✅ You Already Have PostgreSQL - Great!

Since you have PostgreSQL installed locally, here's what you need to do:

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Create Database

Open your terminal and run:

```bash
# Connect to PostgreSQL
psql -U postgres

# Inside psql, create the database:
CREATE DATABASE freshmart_db;

# Verify it was created:
\l

# Exit psql:
\q
```

**Alternative (if you have a different PostgreSQL user):**
```bash
# If your PostgreSQL username is different (e.g., your system username)
psql -U your_username

# Then create database
CREATE DATABASE freshmart_db;
```

---

### Step 2: Create `.env` File

Create `BackEnd/.env` with your local PostgreSQL credentials:

```env
# Database Connection
# Format: postgresql://username:password@host:port/database_name
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/freshmart_db

# If you don't have a password set:
# DATABASE_URL=postgresql://postgres@localhost:5432/freshmart_db

# If your PostgreSQL user is different:
# DATABASE_URL=postgresql://your_username:your_password@localhost:5432/freshmart_db

# Security (change this!)
SECRET_KEY=your-super-secret-key-change-this-in-production-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# CORS (Frontend URLs)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:5500
```

---

### Step 3: Find Your PostgreSQL Credentials

**Don't know your PostgreSQL password?**

**Option A: Check if password is required**
```bash
psql -U postgres
# If it connects without asking for password, you don't need one!
```

**Option B: Reset PostgreSQL password (if needed)**
```bash
# macOS/Linux
sudo -u postgres psql
ALTER USER postgres PASSWORD 'newpassword';
\q

# Windows (run as Administrator in Command Prompt)
psql -U postgres
ALTER USER postgres PASSWORD 'newpassword';
\q
```

**Option C: Check your PostgreSQL config**
```bash
# Find your pg_hba.conf file
psql -U postgres -c "SHOW hba_file;"

# If it shows "trust" for local connections, no password needed
# Your DATABASE_URL would be: postgresql://postgres@localhost:5432/freshmart_db
```

---

### Step 4: Test Database Connection

Create a test file `BackEnd/test_db.py`:

```python
# BackEnd/test_db.py
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print(f"Testing connection to: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"✅ Connected successfully!")
        print(f"PostgreSQL version: {version}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check if PostgreSQL is running: pg_isready")
    print("2. Verify your DATABASE_URL in .env file")
    print("3. Check username and password")
    print("4. Make sure database 'freshmart_db' exists")
```

Run the test:
```bash
cd BackEnd
python test_db.py
```

---

## 🎯 Common PostgreSQL Connection Strings

Choose the one that matches your setup:

### 1. Default PostgreSQL (with password)
```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/freshmart_db
```

### 2. PostgreSQL without password (trust authentication)
```env
DATABASE_URL=postgresql://postgres@localhost:5432/freshmart_db
```

### 3. Custom PostgreSQL user
```env
DATABASE_URL=postgresql://myusername:mypassword@localhost:5432/freshmart_db
```

### 4. PostgreSQL on different port
```env
DATABASE_URL=postgresql://postgres:password@localhost:5433/freshmart_db
```

---

## 🔧 Troubleshooting

### Issue 1: "psql: command not found"

**macOS:**
```bash
# Add to PATH
echo 'export PATH="/Library/PostgreSQL/15/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Linux:**
```bash
sudo apt-get install postgresql-client
```

### Issue 2: "FATAL: database 'freshmart_db' does not exist"

```bash
# Create the database
createdb freshmart_db

# Or using psql:
psql -U postgres
CREATE DATABASE freshmart_db;
\q
```

### Issue 3: "FATAL: password authentication failed"

```bash
# Reset password
psql -U postgres
ALTER USER postgres PASSWORD 'newpassword';
\q

# Update .env with new password
```

### Issue 4: "could not connect to server"

```bash
# Check if PostgreSQL is running
pg_isready

# If not running, start it:
# macOS:
brew services start postgresql

# Linux:
sudo systemctl start postgresql

# Windows:
# Start PostgreSQL service from Services app
```

### Issue 5: "port 5432 already in use"

```bash
# Check what's using port 5432
lsof -i :5432

# Or check PostgreSQL status
pg_isready -p 5432
```

---

## ✅ Verify Everything Works

Once your `.env` is set up correctly:

```bash
cd BackEnd

# 1. Test database connection
python test_db.py

# 2. Initialize database with tables and sample data
python init_db.py

# 3. Start the FastAPI server
uvicorn app.main:app --reload

# 4. Open Swagger UI
# http://localhost:8000/docs
```

---

## 📊 Useful PostgreSQL Commands

```bash
# Connect to your database
psql -U postgres -d freshmart_db

# Inside psql:
\dt                          # List all tables
\d users                     # Describe users table
\d+ user_addresses          # Detailed info about table

SELECT * FROM users;         # View all users
SELECT * FROM user_addresses; # View all addresses
SELECT * FROM products;      # View all products

# Count records
SELECT COUNT(*) FROM users;

# Exit
\q
```

---

## 🎯 Quick Reference

### Your Setup Checklist:
- [x] PostgreSQL installed locally
- [ ] Database `freshmart_db` created
- [ ] `.env` file created with correct DATABASE_URL
- [ ] Connection tested with `test_db.py`
- [ ] Database initialized with `init_db.py`
- [ ] Server running with `uvicorn`

### Your DATABASE_URL Format:
```
postgresql://[username]:[password]@[host]:[port]/[database_name]
```

**Example for your local setup:**
```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/freshmart_db
```

---

## 🚀 Next Steps

1. **Create database**: `createdb freshmart_db`
2. **Create `.env`**: Copy the template above
3. **Test connection**: `python test_db.py`
4. **Initialize DB**: `python init_db.py`
5. **Start server**: `uvicorn app.main:app --reload`
6. **Test API**: Open http://localhost:8000/docs

You're all set! Your local PostgreSQL is perfect for development! 🎉
