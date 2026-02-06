# ⚡ Quick Start - 5 Minutes to Running Backend

Follow these steps in order. Don't skip any!

## ✅ Step-by-Step Checklist

### □ Step 1: Create Database (30 seconds)

```bash
createdb freshmart_db
```

**Expected output:** Nothing (silence means success!)

**If error:** PostgreSQL might not be running. Try:
```bash
pg_isready
# If not ready, start PostgreSQL
```

---

### □ Step 2: Create .env File (1 minute)

```bash
cd BackEnd
cp .env.example .env
```

Now edit `.env` file with your credentials:

```env
DATABASE_URL=postgresql://kzts669:ams123@localhost:5432/freshmart_db
SECRET_KEY=95e619802a9fec70b64c91a78d0539b212ee6feaf4508f6af5180bbdbdb30a6f
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:5500
```

**Note:** I used your existing PostgreSQL credentials (kzts669:ams123) from database.py

---

### □ Step 3: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

**Expected output:** Lots of "Successfully installed..." messages

**If error:** Make sure you have Python 3.8+ installed:
```bash
python --version
```

---

### □ Step 4: Test Database Connection (10 seconds)

```bash
python test_db.py
```

**Expected output:**
```
Testing connection to: postgresql://***@localhost:5432/freshmart_db
✅ Connected successfully!
PostgreSQL version: PostgreSQL 15.x...
```

**If error:** Check your DATABASE_URL in .env file

---

### □ Step 5: Initialize Database (30 seconds)

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

### □ Step 6: Start Server (5 seconds)

```bash
uvicorn app.main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Keep this terminal open!** The server is running.

---

### □ Step 7: Test API (30 seconds)

Open your browser: **http://localhost:8000/docs**

You should see **Swagger UI** with all your endpoints!

Try these:
1. Click on **POST /auth/login**
2. Click "Try it out"
3. Enter:
   ```json
   {
     "username": "john_doe",
     "password": "password123"
   }
   ```
4. Click "Execute"
5. You should get a token back!

---

## 🎉 Success!

If you got here, your backend is running! 

### What You Have Now:

✅ PostgreSQL database with tables
✅ Sample products, categories, and users
✅ FastAPI server running on port 8000
✅ All API endpoints working
✅ JWT authentication
✅ Swagger UI for testing

### Test Accounts:

**Customer Account:**
- Username: `john_doe`
- Password: `password123`

**Admin Account:**
- Username: `admin`
- Password: `admin123`

---

## 🔥 Common Issues & Fixes

### Issue: "createdb: command not found"

PostgreSQL not in PATH. Try:
```bash
/Library/PostgreSQL/15/bin/createdb freshmart_db
```

### Issue: "database already exists"

That's fine! Skip to Step 2.

### Issue: "ModuleNotFoundError: No module named 'app'"

Make sure you're in the BackEnd directory:
```bash
cd BackEnd
uvicorn app.main:app --reload
```

### Issue: "Could not connect to database"

1. Check PostgreSQL is running: `pg_isready`
2. Check your DATABASE_URL in .env
3. Make sure database exists: `psql -l | grep freshmart`

### Issue: "SECRET_KEY not found"

Make sure you created the .env file (Step 2)

---

## 📚 Next Steps

### Connect Frontend to Backend

Your frontend is already configured! Just make sure:
1. Backend is running on port 8000
2. Frontend uses `http://localhost:8000` as API_BASE_URL

### Test with Frontend

1. Start backend: `uvicorn app.main:app --reload`
2. Start frontend: `npm run dev` (in FrontEnd folder)
3. Open frontend in browser
4. Try logging in with john_doe / password123

### Explore API

Open http://localhost:8000/docs and try:
- Register a new user
- Login and get token
- Click "Authorize" and paste token
- Try creating an address
- Browse products
- Create an order

---

## 🚀 You're All Set!

Your backend is production-ready (after changing SECRET_KEY for production).

For more details, read:
- **README.md** - Overview
- **BACKEND_GUIDE.md** - Detailed explanations
- **BACKEND_GUIDE_PART2.md** - API endpoints
- **BACKEND_GUIDE_PART3.md** - Deployment

Happy coding! 🎉
