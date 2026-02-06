# 🗄️ Database Setup - Copy & Paste Commands

## ✅ What You Need to Do

Your database already exists (`freshmart_db`), but you need to:
1. Create a `.env` file with your credentials
2. Install Python packages
3. Run the initialization script

That's it! 3 steps.

---

## 📋 Step-by-Step Commands

### Step 1: Create .env File (30 seconds)

Open terminal in `BackEnd` folder and run:

```bash
cd BackEnd
```

Create `.env` file with this content:

```bash
cat > .env << 'EOF'
DATABASE_URL=postgresql://kzts669:ams123@localhost:5432/freshmart_db
SECRET_KEY=95e619802a9fec70b64c91a78d0539b212ee6feaf4508f6af5180bbdbdb30a6f
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:5500
EOF
```

**✅ Done!** Your `.env` file is created with your existing PostgreSQL credentials.

---

### Step 2: Install Python Packages (1 minute)

Still in `BackEnd` folder, run:

```bash
pip install -r requirements.txt
```

**Expected output:** Lots of "Successfully installed..." messages

**If you see errors**, try:
```bash
pip3 install -r requirements.txt
```

---

### Step 3: Test Database Connection (10 seconds)

```bash
python test_db.py
```

**Expected output:**
```
Testing connection to: postgresql://***@localhost:5432/freshmart_db
✅ Connected successfully!
PostgreSQL version: PostgreSQL 15.x...
```

**If you see ❌ error:**
- Check if PostgreSQL is running: `pg_isready`
- If not running: `brew services start postgresql` (macOS)

---

### Step 4: Initialize Database (30 seconds)

This creates all tables and adds sample products:

```bash
python init_db.py
```

**Expected output:**
```
🚀 Initializing FreshMart Database...

Creating database tables...
✅ Tables created successfully!
Seeding database with sample data...
✅ Sample data added successfully!

📝 Test Credentials:
   Admin: username=admin, password=admin123
   Customer: username=john_doe, password=password123

✅ Database initialization complete!
```

---

### Step 5: Start Backend Server (5 seconds)

```bash
uvicorn app.main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

**✅ Backend is running!**

---

### Step 6: Test API (30 seconds)

Open browser: **http://localhost:8000/docs**

You should see Swagger UI with all endpoints!

Try logging in:
1. Click **POST /auth/login**
2. Click "Try it out"
3. Enter:
   ```json
   {
     "username": "john_doe",
     "password": "password123"
   }
   ```
4. Click "Execute"
5. You should get a token!

---

## 🎉 You're Done!

Your backend is fully running with:
- ✅ Database tables created
- ✅ Sample products loaded
- ✅ Test users created
- ✅ API server running
- ✅ All 16 endpoints working

---

## 🧪 Test Accounts

**Customer Account:**
- Username: `john_doe`
- Password: `password123`

**Admin Account:**
- Username: `admin`
- Password: `admin123`

---

## 📊 What's in Your Database Now?

After running `init_db.py`, you have:

**Users Table:**
- 2 users (admin and john_doe)

**Categories Table:**
- 8 categories (Fruits, Vegetables, Dairy, Meat, Seafood, Bakery, Grains, Beverages)

**Products Table:**
- 19 products with prices, images, ratings

**User Addresses Table:**
- 1 sample address for john_doe

**Orders & Order Items Tables:**
- Empty (ready for your orders)

---

## 🚀 Start Your Full Application

### Terminal 1 - Backend:
```bash
cd BackEnd
uvicorn app.main:app --reload
```

### Terminal 2 - Frontend:
```bash
cd FrontEnd
npm run dev
```

Then open: **http://localhost:5173**

---

## 🔍 Verify Database Tables

Want to see your tables? Run:

```bash
psql -U kzts669 -d freshmart_db
```

Inside psql:
```sql
-- List all tables
\dt

-- See users
SELECT id, username, email, role FROM users;

-- See products
SELECT id, name, price, category_id FROM products LIMIT 5;

-- See categories
SELECT * FROM categories;

-- Exit
\q
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pydantic_settings'"

```bash
pip install pydantic-settings
```

### Error: "Could not connect to database"

Check PostgreSQL is running:
```bash
pg_isready
```

If not running:
```bash
brew services start postgresql
```

### Error: "database 'freshmart_db' does not exist"

Your database exists! But if you need to recreate:
```bash
dropdb freshmart_db
createdb freshmart_db
python init_db.py
```

### Error: "SECRET_KEY not found"

Make sure you created `.env` file (Step 1)

---

## 📝 Summary - All Commands in Order

```bash
# 1. Go to BackEnd folder
cd BackEnd

# 2. Create .env file
cat > .env << 'EOF'
DATABASE_URL=postgresql://kzts669:ams123@localhost:5432/freshmart_db
SECRET_KEY=95e619802a9fec70b64c91a78d0539b212ee6feaf4508f6af5180bbdbdb30a6f
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:5500
EOF

# 3. Install packages
pip install -r requirements.txt

# 4. Test connection
python test_db.py

# 5. Initialize database
python init_db.py

# 6. Start server
uvicorn app.main:app --reload
```

**That's it!** Your full-fledged application is ready! 🎉
