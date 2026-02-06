# 🚀 FastAPI Backend Guide - Part 2: API Endpoints

## 🎯 Step 5: Create API Routers

### 5.1 Update `routers/auth.py` (Already exists, but let's improve it)

```python
# BackEnd/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserLogin, UserResponse, Token
from ..utils.security import hash_password, verify_password, create_access_token
from ..dependencies import DbSession, CurrentUser

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: DbSession):
    """
    Register a new user account.
    
    - Checks if username/email already exists
    - Hashes the password
    - Creates user in database
    """
    # Check if username exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        hashed_password=hash_password(user_data.password),
        role="customer",
        is_active=True,
        is_verified=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: DbSession):
    """
    Login with username and password.
    
    - Verifies credentials
    - Returns JWT token and user info
    """
    # Find user
    user = db.query(User).filter(User.username == credentials.username).first()
    
    # Verify user exists and password is correct
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.id, "username": user.username, "role": user.role}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: CurrentUser):
    """
    Get current logged-in user information.
    Requires authentication token.
    """
    return current_user
```

### 5.2 Create `routers/addresses.py`

```python
# BackEnd/app/routers/addresses.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from ..models import UserAddress
from ..schemas import AddressCreate, AddressUpdate, AddressResponse
from ..dependencies import DbSession, CurrentUser

router = APIRouter(prefix="/addresses", tags=["Addresses"])

@router.get("/", response_model=List[AddressResponse])
async def get_user_addresses(current_user: CurrentUser, db: DbSession):
    """
    Get all addresses for the current user.
    """
    addresses = db.query(UserAddress).filter(
        UserAddress.user_id == current_user.id
    ).order_by(UserAddress.is_default.desc(), UserAddress.created_at.desc()).all()
    
    return addresses


@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
async def create_address(address_data: AddressCreate, current_user: CurrentUser, db: DbSession):
    """
    Create a new address for the current user.
    
    - If is_default=True, removes default from other addresses
    """
    # If this is set as default, remove default from other addresses
    if address_data.is_default:
        db.query(UserAddress).filter(
            UserAddress.user_id == current_user.id
        ).update({"is_default": False})
    
    # Create new address
    new_address = UserAddress(
        user_id=current_user.id,
        **address_data.model_dump()
    )
    
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    
    return new_address


@router.get("/{address_id}", response_model=AddressResponse)
async def get_address(address_id: int, current_user: CurrentUser, db: DbSession):
    """
    Get a specific address by ID.
    Only returns if it belongs to the current user.
    """
    address = db.query(UserAddress).filter(
        UserAddress.id == address_id,
        UserAddress.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    
    return address


@router.put("/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: int,
    address_data: AddressUpdate,
    current_user: CurrentUser,
    db: DbSession
):
    """
    Update an existing address.
    Only updates if it belongs to the current user.
    """
    # Find address
    address = db.query(UserAddress).filter(
        UserAddress.id == address_id,
        UserAddress.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    
    # If setting as default, remove default from others
    if address_data.is_default:
        db.query(UserAddress).filter(
            UserAddress.user_id == current_user.id,
            UserAddress.id != address_id
        ).update({"is_default": False})
    
    # Update address fields
    update_data = address_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(address, field, value)
    
    db.commit()
    db.refresh(address)
    
    return address


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(address_id: int, current_user: CurrentUser, db: DbSession):
    """
    Delete an address.
    Only deletes if it belongs to the current user.
    """
    address = db.query(UserAddress).filter(
        UserAddress.id == address_id,
        UserAddress.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    
    db.delete(address)
    db.commit()
    
    return None


@router.post("/{address_id}/set-default", response_model=AddressResponse)
async def set_default_address(address_id: int, current_user: CurrentUser, db: DbSession):
    """
    Set an address as the default delivery address.
    """
    # Find address
    address = db.query(UserAddress).filter(
        UserAddress.id == address_id,
        UserAddress.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    
    # Remove default from all other addresses
    db.query(UserAddress).filter(
        UserAddress.user_id == current_user.id
    ).update({"is_default": False})
    
    # Set this as default
    address.is_default = True
    db.commit()
    db.refresh(address)
    
    return address
```

### 5.3 Create `routers/products.py`

```python
# BackEnd/app/routers/products.py
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import Product, Category
from ..schemas import ProductResponse
from ..dependencies import DbSession

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductResponse])
async def get_products(
    db: DbSession,
    category: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """
    Get all products with optional filtering.
    
    - category: Filter by category name
    - search: Search in product name/description
    - skip: Number of products to skip (pagination)
    - limit: Maximum number of products to return
    """
    query = db.query(Product).filter(Product.is_active == True)
    
    # Filter by category
    if category:
        cat = db.query(Category).filter(Category.name == category).first()
        if cat:
            query = query.filter(Product.category_id == cat.id)
    
    # Search in name and description
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Product.name.ilike(search_term)) | 
            (Product.description.ilike(search_term))
        )
    
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: DbSession):
    """
    Get a specific product by ID.
    """
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_active == True
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product


@router.get("/category/{category_name}", response_model=List[ProductResponse])
async def get_products_by_category(category_name: str, db: DbSession):
    """
    Get all products in a specific category.
    """
    category = db.query(Category).filter(Category.name == category_name).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    products = db.query(Product).filter(
        Product.category_id == category.id,
        Product.is_active == True
    ).all()
    
    return products
```

### 5.4 Create `routers/orders.py`

```python
# BackEnd/app/routers/orders.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from ..models import Order, OrderItem, Product
from ..schemas import OrderCreate, OrderResponse
from ..dependencies import DbSession, CurrentUser

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, current_user: CurrentUser, db: DbSession):
    """
    Create a new order.
    
    - Validates products exist and have stock
    - Calculates totals
    - Creates order and order items
    """
    # Calculate totals
    subtotal = 0
    order_items_data = []
    
    for item in order_data.items:
        # Get product
        product = db.query(Product).filter(Product.id == item.product_id).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.product_id} not found"
            )
        
        if not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product {product.name} is not available"
            )
        
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for {product.name}"
            )
        
        item_subtotal = float(product.price) * item.quantity
        subtotal += item_subtotal
        
        order_items_data.append({
            "product_id": product.id,
            "product_name": product.name,
            "product_price": float(product.price),
            "quantity": item.quantity,
            "subtotal": item_subtotal
        })
    
    # Calculate fees
    delivery_fee = 0 if subtotal > 500 else 49
    tax = round(subtotal * 0.05, 2)
    total = subtotal + delivery_fee + tax
    
    # Create order
    new_order = Order(
        user_id=current_user.id,
        delivery_street=order_data.delivery_street,
        delivery_city=order_data.delivery_city,
        delivery_state=order_data.delivery_state,
        delivery_postal_code=order_data.delivery_postal_code,
        delivery_country=order_data.delivery_country,
        delivery_instructions=order_data.delivery_instructions,
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        tax=tax,
        total=total,
        payment_method=order_data.payment_method,
        status="pending",
        payment_status="pending"
    )
    
    db.add(new_order)
    db.flush()  # Get order ID without committing
    
    # Create order items
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=new_order.id,
            **item_data
        )
        db.add(order_item)
        
        # Update product stock
        product = db.query(Product).filter(Product.id == item_data["product_id"]).first()
        product.stock -= item_data["quantity"]
    
    db.commit()
    db.refresh(new_order)
    
    return new_order


@router.get("/", response_model=List[OrderResponse])
async def get_user_orders(current_user: CurrentUser, db: DbSession):
    """
    Get all orders for the current user.
    """
    orders = db.query(Order).filter(
        Order.user_id == current_user.id
    ).order_by(Order.created_at.desc()).all()
    
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, current_user: CurrentUser, db: DbSession):
    """
    Get a specific order by ID.
    Only returns if it belongs to the current user.
    """
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order


@router.post("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(order_id: int, current_user: CurrentUser, db: DbSession):
    """
    Cancel an order.
    Only works if order is still pending.
    """
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only cancel pending orders"
        )
    
    order.status = "cancelled"
    
    # Restore product stock
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock += item.quantity
    
    db.commit()
    db.refresh(order)
    
    return order
```

---

## 🎯 Step 6: Main Application

### 6.1 Update `main.py`

```python
# BackEnd/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .config import settings
from .routers import auth, addresses, products, orders

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="FreshMart API",
    description="Backend API for FreshMart Grocery Store",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(addresses.router)
app.include_router(products.router)
app.include_router(orders.router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "FreshMart API is running!",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected"
    }
```

---

## 🚀 Step 7: Run the Application

### 7.1 Start the server

```bash
cd BackEnd
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7.2 Test the API

Open browser: http://localhost:8000/docs

You'll see **Swagger UI** with all your endpoints!

---

## 📚 Step 8: Testing with Examples

### Example 1: Register a User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "9876543210",
    "password": "SecurePass123!"
  }'
```

### Example 2: Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123!"
  }'
```

Save the `access_token` from response!

### Example 3: Create Address (with token)

```bash
curl -X POST "http://localhost:8000/addresses/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "label": "Home",
    "street": "123 Main St",
    "city": "Mumbai",
    "state": "Maharashtra",
    "postal_code": "400001",
    "country": "India",
    "is_default": true
  }'
```

---

**Continue to Part 3 for Database Setup & Seed Data?** 👉
