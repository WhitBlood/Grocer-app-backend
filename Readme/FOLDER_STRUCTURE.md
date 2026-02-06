# 📁 Complete Backend Folder Structure

## Visual Directory Tree

```
BackEnd/
│
├── 📄 .env.example                    # Template for environment variables
├── 📄 .env                            # YOUR environment variables (create this!)
│
├── 📚 Documentation Files
│   ├── README.md                      # Quick start guide
│   ├── QUICK_START.md                 # 5-minute setup guide
│   ├── FILES_CREATED.md               # What was created
│   ├── FOLDER_STRUCTURE.md            # This file!
│   ├── BACKEND_GUIDE.md               # Complete guide Part 1
│   ├── BACKEND_GUIDE_PART2.md         # Complete guide Part 2
│   ├── BACKEND_GUIDE_PART3.md         # Complete guide Part 3
│   └── LOCAL_POSTGRES_SETUP.md        # PostgreSQL setup
│
├── 🔧 Setup Scripts
│   ├── requirements.txt               # Python dependencies
│   ├── test_db.py                     # Test database connection
│   └── init_db.py                     # Initialize database & seed data
│
└── 📦 app/                            # Main application package
    │
    ├── 📄 __init__.py                 # Makes 'app' a package
    ├── 📄 main.py                     # FastAPI application entry point
    ├── 📄 database.py                 # Database connection & session
    ├── 📄 models.py                   # SQLAlchemy database models
    ├── 📄 schemas.py                  # Pydantic request/response models
    ├── 📄 config.py                   # Configuration from .env
    ├── 📄 dependencies.py             # Reusable FastAPI dependencies
    │
    ├── 🌐 routers/                    # API endpoint routers
    │   ├── __init__.py                # Makes 'routers' a package
    │   ├── auth.py                    # Authentication endpoints
    │   ├── addresses.py               # Address management endpoints
    │   ├── products.py                # Product catalog endpoints
    │   └── orders.py                  # Order management endpoints
    │
    └── 🛠️ utils/                      # Utility functions
        ├── __init__.py                # Makes 'utils' a package
        └── security.py                # Password hashing & JWT tokens
```

## 📋 File Descriptions

### Root Level Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `.env` | Your secret credentials | Create from .env.example |
| `.env.example` | Template for .env | Copy to .env |
| `requirements.txt` | Python packages to install | `pip install -r requirements.txt` |
| `test_db.py` | Test database connection | Before init_db.py |
| `init_db.py` | Create tables & seed data | Once at setup |

### Documentation Files

| File | Content | Read When |
|------|---------|-----------|
| `README.md` | Quick overview | First! |
| `QUICK_START.md` | 5-minute setup | Starting setup |
| `FILES_CREATED.md` | What was created | Understanding structure |
| `FOLDER_STRUCTURE.md` | This file | Understanding layout |
| `BACKEND_GUIDE.md` | Detailed Part 1 | Learning FastAPI |
| `BACKEND_GUIDE_PART2.md` | API endpoints | Building endpoints |
| `BACKEND_GUIDE_PART3.md` | Testing & deploy | Going to production |
| `LOCAL_POSTGRES_SETUP.md` | Database setup | Database issues |

### app/ Directory

| File | Contains | Imports From |
|------|----------|--------------|
| `main.py` | FastAPI app, CORS, routers | database, routers |
| `database.py` | SQLAlchemy engine & session | config |
| `models.py` | Database table definitions | database |
| `schemas.py` | Request/response validation | - |
| `config.py` | Settings from .env | - |
| `dependencies.py` | Auth & DB dependencies | database, models, utils |

### app/routers/ Directory

| File | Endpoints | Requires Auth |
|------|-----------|---------------|
| `auth.py` | /auth/register, /auth/login, /auth/me | Only /me |
| `addresses.py` | /addresses/* (CRUD) | Yes |
| `products.py` | /products/* (read-only) | No |
| `orders.py` | /orders/* (CRUD) | Yes |

### app/utils/ Directory

| File | Functions | Used By |
|------|-----------|---------|
| `security.py` | hash_password, verify_password, create_access_token, decode_access_token | auth.py, dependencies.py |

## 🔄 How Files Connect

```
main.py
  ├─→ database.py (get DB connection)
  ├─→ routers/auth.py
  ├─→ routers/addresses.py
  ├─→ routers/products.py
  └─→ routers/orders.py

routers/auth.py
  ├─→ database.py (get_db)
  ├─→ models.py (User)
  ├─→ schemas.py (UserCreate, UserLogin, Token)
  └─→ utils/security.py (hash_password, verify_password, create_access_token)

routers/addresses.py
  ├─→ models.py (UserAddress)
  ├─→ schemas.py (AddressCreate, AddressUpdate, AddressResponse)
  └─→ dependencies.py (CurrentUser, DbSession)

routers/products.py
  ├─→ models.py (Product, Category)
  ├─→ schemas.py (ProductResponse)
  └─→ dependencies.py (DbSession)

routers/orders.py
  ├─→ models.py (Order, OrderItem, Product)
  ├─→ schemas.py (OrderCreate, OrderResponse)
  └─→ dependencies.py (CurrentUser, DbSession)

dependencies.py
  ├─→ database.py (get_db)
  ├─→ models.py (User)
  └─→ utils/security.py (decode_access_token)

config.py
  └─→ .env file (reads environment variables)

database.py
  └─→ config.py (gets DATABASE_URL)
```

## 🎯 Import Patterns

### Relative Imports (within app/)

```python
# In app/routers/auth.py
from ..database import get_db          # Go up one level
from ..models import User              # Go up one level
from ..schemas import UserCreate       # Go up one level
from ..utils.security import hash_password  # Go up, then into utils
from ..dependencies import CurrentUser # Go up one level
```

### Absolute Imports (from root)

```python
# In init_db.py (root level)
from app.database import engine, SessionLocal
from app.models import Base, User, Product
from app.utils.security import hash_password
```

## 📊 Database Models Relationships

```
User (users table)
  ├─→ has many UserAddress (user_addresses table)
  └─→ has many Order (orders table)

UserAddress (user_addresses table)
  └─→ belongs to User

Category (categories table)
  └─→ has many Product (products table)

Product (products table)
  ├─→ belongs to Category
  └─→ has many OrderItem (order_items table)

Order (orders table)
  ├─→ belongs to User
  └─→ has many OrderItem (order_items table)

OrderItem (order_items table)
  ├─→ belongs to Order
  └─→ belongs to Product
```

## 🚀 Execution Flow

### 1. Server Startup

```
1. Load .env file (config.py)
2. Create database engine (database.py)
3. Create FastAPI app (main.py)
4. Add CORS middleware (main.py)
5. Include routers (main.py)
6. Start uvicorn server
```

### 2. API Request (with auth)

```
1. Request arrives at endpoint (e.g., POST /addresses/)
2. FastAPI calls dependencies:
   - get_db() → provides database session
   - get_current_user() → validates JWT token
3. Router function executes
4. Database operations performed
5. Response returned (validated by Pydantic schema)
6. Database session closed
```

### 3. Authentication Flow

```
1. User sends POST /auth/login with username/password
2. auth.py finds user in database
3. verify_password() checks password hash
4. create_access_token() generates JWT
5. Token returned to user
6. User includes token in future requests
7. get_current_user() validates token
8. User object provided to endpoint
```

## 📝 File Sizes (Approximate)

| File | Lines | Purpose |
|------|-------|---------|
| main.py | ~60 | App setup |
| database.py | ~30 | DB connection |
| models.py | ~150 | 6 database models |
| schemas.py | ~140 | Request/response models |
| config.py | ~25 | Settings |
| dependencies.py | ~45 | Auth dependency |
| routers/auth.py | ~90 | 3 endpoints |
| routers/addresses.py | ~160 | 6 endpoints |
| routers/products.py | ~80 | 3 endpoints |
| routers/orders.py | ~170 | 4 endpoints |
| utils/security.py | ~40 | 4 functions |
| init_db.py | ~180 | Database seeding |

**Total:** ~1,170 lines of Python code

## 🎓 Learning Path

If you're new to FastAPI, read files in this order:

1. **main.py** - See how FastAPI app is created
2. **database.py** - Understand database connection
3. **models.py** - Learn SQLAlchemy models
4. **schemas.py** - Learn Pydantic validation
5. **utils/security.py** - Understand password & JWT
6. **dependencies.py** - Learn FastAPI dependencies
7. **routers/auth.py** - Simple authentication
8. **routers/addresses.py** - CRUD operations
9. **routers/products.py** - Read-only endpoints
10. **routers/orders.py** - Complex business logic

## 🔍 Quick File Finder

**Need to...**
- Change database URL? → `.env`
- Add new endpoint? → `app/routers/`
- Add new table? → `app/models.py`
- Change request validation? → `app/schemas.py`
- Modify JWT settings? → `app/config.py` and `.env`
- Add utility function? → `app/utils/`
- Change CORS settings? → `app/main.py`
- Add sample data? → `init_db.py`

## ✅ Checklist: Files You Need to Create

- [ ] `.env` (copy from .env.example)

That's it! Everything else is already created.

## 🎉 Summary

You have a **complete, production-ready FastAPI backend** with:
- ✅ 16 API endpoints
- ✅ JWT authentication
- ✅ 6 database models
- ✅ Request/response validation
- ✅ CORS configuration
- ✅ Database seeding
- ✅ Complete documentation

All organized in a clean, professional structure! 🚀
