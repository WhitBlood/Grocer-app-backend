# 🚀 Complete FastAPI Backend Guide for Beginners

## 📚 What You'll Learn

By the end of this guide, you'll have a fully functional FastAPI backend with:
- User authentication (register/login)
- Address management
- Product management
- Order management
- Database integration with PostgreSQL

Don't worry - I'll explain everything step by step! 💪

---

## 📁 Project Structure

```
BackEnd/
├── app/
│   ├── __init__.py                 # Makes 'app' a Python package
│   ├── main.py                     # Main FastAPI application
│   ├── database.py                 # Database connection setup
│   ├── models.py                   # Database table definitions (SQLAlchemy models)
│   ├── schemas.py                  # Pydantic models (request/response validation)
│   ├── dependencies.py             # Reusable dependencies (auth, DB session)
│   ├── config.py                   # Configuration (database URL, secrets)
│   │
│   ├── routers/                    # API endpoints organized by feature
│   │   ├── __init__.py
│   │   ├── auth.py                 # Login, Register, Logout
│   │   ├── addresses.py            # Address CRUD operations
│   │   ├── products.py             # Product listing, details
│   │   ├── orders.py               # Order creation, history
│   │   └── users.py                # User profile management
│   │
│   └── utils/                      # Helper functions
│       ├── __init__.py
│       ├── security.py             # Password hashing, JWT tokens
│       └── validators.py           # Custom validation functions
│
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (secrets)
└── README.md                      # Documentation
```

---

## 🛠️ Step 1: Setup & Installation

### 1.1 Install Python Dependencies

Create `requirements.txt`:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic[email]==2.5.0
python-dotenv==1.0.0
```

Install:
```bash
cd BackEnd
pip install -r requirements.txt
```

### 1.2 Setup PostgreSQL Database

**Option A: Local PostgreSQL**
```bash
# Install PostgreSQL (macOS)
brew install postgresql
brew services start postgresql

# Create database
createdb freshmart_db
```

**Option B: Docker PostgreSQL**
```bash
docker run --name freshmart-postgres \
  -e POSTGRES_PASSWORD=yourpassword \
  -e POSTGRES_DB=freshmart_db \
  -p 5432:5432 \
  -d postgres:15
```

### 1.3 Create `.env` File

Create `BackEnd/.env`:
```env
# Database
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/freshmart_db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# CORS (Frontend URLs)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:5500
```

---

## 📝 Step 2: Database Setup

### 2.1 Create `config.py`

```python
# BackEnd/app/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"
    
    @property
    def origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

settings = Settings()
```

### 2.2 Create `database.py`

```python
# BackEnd/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    echo=True  # Log SQL queries (disable in production)
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    """
    Creates a new database session for each request.
    Automatically closes the session when done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 2.3 Create `models.py` (Database Tables)

```python
# BackEnd/app/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

class User(Base):
    """User account table"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String(20), default="customer")  # customer, admin
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    addresses = relationship("UserAddress", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user")


class UserAddress(Base):
    """User delivery addresses table"""
    __tablename__ = "user_addresses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    label = Column(String(50), nullable=False)  # Home, Work, Other
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), default="India")
    is_default = Column(Boolean, default=False)
    delivery_instructions = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    user = relationship("User", back_populates="addresses")


class Category(Base):
    """Product categories table"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)  # Emoji or icon class
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    products = relationship("Product", back_populates="category")


class Product(Base):
    """Products table"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    original_price = Column(Numeric(10, 2), nullable=True)
    image_url = Column(String(500), nullable=True)
    badge = Column(String(50), nullable=True)  # Organic, Premium, Fresh
    rating = Column(Numeric(3, 2), default=0.0)
    reviews_count = Column(Integer, default=0)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")


class Order(Base):
    """Orders table"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Delivery address (snapshot at order time)
    delivery_street = Column(String(255), nullable=False)
    delivery_city = Column(String(100), nullable=False)
    delivery_state = Column(String(100), nullable=False)
    delivery_postal_code = Column(String(20), nullable=False)
    delivery_country = Column(String(100), nullable=False)
    delivery_instructions = Column(Text, nullable=True)
    
    # Order details
    subtotal = Column(Numeric(10, 2), nullable=False)
    delivery_fee = Column(Numeric(10, 2), default=0)
    tax = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(10, 2), nullable=False)
    
    # Status
    status = Column(String(50), default="pending")  # pending, confirmed, shipped, delivered, cancelled
    payment_method = Column(String(50), nullable=True)  # card, cash, upi
    payment_status = Column(String(50), default="pending")  # pending, paid, failed
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    """Order items table (products in an order)"""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    # Product snapshot at order time
    product_name = Column(String(200), nullable=False)
    product_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
```

---

## 🔐 Step 3: Security & Authentication

### 3.1 Create `utils/security.py`

```python
# BackEnd/app/utils/security.py
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from ..config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plain password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
```

### 3.2 Create `dependencies.py`

```python
# BackEnd/app/dependencies.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .utils.security import decode_access_token

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Type aliases for cleaner code
DbSession = Annotated[Session, Depends(get_db)]
TokenStr = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(token: TokenStr, db: DbSession) -> User:
    """
    Get the current authenticated user from JWT token.
    Raises 401 if token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decode token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    # Get user ID from token
    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user

# Type alias for current user dependency
CurrentUser = Annotated[User, Depends(get_current_user)]
```

---

## 📋 Step 4: Request/Response Schemas

### 4.1 Create `schemas.py`

```python
# BackEnd/app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ============= USER SCHEMAS =============

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# ============= ADDRESS SCHEMAS =============

class AddressBase(BaseModel):
    label: str = Field(..., max_length=50)
    street: str = Field(..., max_length=255)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    postal_code: str = Field(..., max_length=20)
    country: str = Field(default="India", max_length=100)
    is_default: bool = False
    delivery_instructions: Optional[str] = None

class AddressCreate(AddressBase):
    pass

class AddressUpdate(BaseModel):
    label: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    is_default: Optional[bool] = None
    delivery_instructions: Optional[str] = None

class AddressResponse(AddressBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ============= PRODUCT SCHEMAS =============

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    image_url: Optional[str] = None
    badge: Optional[str] = None
    category_id: int

class ProductResponse(ProductBase):
    id: int
    rating: float
    reviews_count: int
    stock: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============= ORDER SCHEMAS =============

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    delivery_street: str
    delivery_city: str
    delivery_state: str
    delivery_postal_code: str
    delivery_country: str = "India"
    delivery_instructions: Optional[str] = None
    payment_method: str = "card"

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_price: float
    quantity: int
    subtotal: float
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    delivery_street: str
    delivery_city: str
    delivery_state: str
    delivery_postal_code: str
    delivery_country: str
    subtotal: float
    delivery_fee: float
    tax: float
    total: float
    status: str
    payment_method: str
    payment_status: str
    created_at: datetime
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True
```

---

## 🎯 Step 5: API Routers (Endpoints)

I'll create the complete routers in the next message. This is getting long!

**Continue to Part 2?** 👉
