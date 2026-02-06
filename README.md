# 🚀 FreshMart Backend API

Complete FastAPI backend for FreshMart grocery e-commerce application.

## 📁 Project Structure

```
BackEnd/
├── app/
│   ├── __init__.py              # Package initializer
│   ├── main.py                  # FastAPI application
│   ├── database.py              # Database connection
│   ├── models.py                # SQLAlchemy models
│   ├── schemas.py               # Pydantic schemas
│   ├── config.py                # Configuration settings
│   ├── dependencies.py          # Reusable dependencies
│   │
│   ├── routers/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication
│   │   ├── addresses.py         # Address management
│   │   ├── products.py          # Product catalog
│   │   └── orders.py            # Order management
│   │
│   └── utils/                   # Helper functions
│       ├── __init__.py
│       └── security.py          # Password & JWT utilities
│
├── .env                         # Environment variables (create this!)
├── .env.example                 # Example environment file
├── requirements.txt             # Python dependencies
├── init_db.py                   # Database initialization
├── test_db.py                   # Test database connection
├── BACKEND_GUIDE.md             # Complete guide Part 1
├── BACKEND_GUIDE_PART2.md       # Complete guide Part 2
├── BACKEND_GUIDE_PART3.md       # Complete guide Part 3
└── LOCAL_POSTGRES_SETUP.md      # PostgreSQL setup guide
```

## 🚀 Quick Start

### 1. Create Database

```bash
createdb freshmart_db
```

### 2. Create `.env` File

Copy `.env.example` to `.env` and update with your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/freshmart_db
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Test Database Connection

```bash
python test_db.py
```

### 5. Initialize Database

```bash
python init_db.py
```

This creates all tables and adds sample data.

### 6. Start Server

```bash
uvicorn app.main:app --reload
```

### 7. Test API

Open: http://localhost:8000/docs

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info (requires auth)

### Addresses
- `GET /addresses/` - Get all user addresses (requires auth)
- `POST /addresses/` - Create new address (requires auth)
- `GET /addresses/{id}` - Get specific address (requires auth)
- `PUT /addresses/{id}` - Update address (requires auth)
- `DELETE /addresses/{id}` - Delete address (requires auth)
- `POST /addresses/{id}/set-default` - Set default address (requires auth)

### Products
- `GET /products/` - Get all products (with filters)
- `GET /products/{id}` - Get specific product
- `GET /products/category/{name}` - Get products by category

### Orders
- `POST /orders/` - Create new order (requires auth)
- `GET /orders/` - Get user orders (requires auth)
- `GET /orders/{id}` - Get specific order (requires auth)
- `POST /orders/{id}/cancel` - Cancel order (requires auth)

## 🧪 Test Credentials

After running `init_db.py`:

**Admin:**
- Username: `admin`
- Password: `admin123`

**Customer:**
- Username: `john_doe`
- Password: `password123`

## 📖 Documentation

Read the complete guides in order:

1. **LOCAL_POSTGRES_SETUP.md** - Database setup
2. **BACKEND_GUIDE.md** - Project structure & setup
3. **BACKEND_GUIDE_PART2.md** - API endpoints
4. **BACKEND_GUIDE_PART3.md** - Testing & deployment

## 🔧 Common Commands

```bash
# Start development server
uvicorn app.main:app --reload

# Start with custom host/port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Test database connection
python test_db.py

# Initialize/reset database
python init_db.py

# Install dependencies
pip install -r requirements.txt

# Check PostgreSQL status
pg_isready
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'app'"

Run from BackEnd directory:
```bash
cd BackEnd
uvicorn app.main:app --reload
```

### "Could not connect to database"

1. Check PostgreSQL is running: `pg_isready`
2. Verify DATABASE_URL in `.env`
3. Ensure database exists: `createdb freshmart_db`

### "SECRET_KEY not found"

Create `.env` file with SECRET_KEY (see `.env.example`)

## 📦 Database Models

- **User** - User accounts
- **UserAddress** - Delivery addresses
- **Category** - Product categories
- **Product** - Products catalog
- **Order** - Customer orders
- **OrderItem** - Items in orders

## 🔐 Security

- Passwords hashed with bcrypt
- JWT tokens for authentication
- Token expiry: 7 days (configurable)
- CORS configured for frontend origins

## 🚀 Deployment

See **BACKEND_GUIDE_PART3.md** for production deployment guide.

## 📝 License

MIT

## 🤝 Support

For detailed guides, see the BACKEND_GUIDE files in this directory.
