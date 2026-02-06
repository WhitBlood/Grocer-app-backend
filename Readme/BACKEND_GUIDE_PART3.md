# 🚀 FastAPI Backend Guide - Part 3: Database & Deployment

## 🗄️ Step 9: Database Setup & Seed Data

### 9.1 Create Database Initialization Script

Create `BackEnd/init_db.py`:

```python
# BackEnd/init_db.py
"""
Database initialization script.
Run this to create tables and add sample data.
"""
from app.database import engine, SessionLocal
from app.models import Base, User, Category, Product, UserAddress
from app.utils.security import hash_password

def init_database():
    """Create all tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

def seed_data():
    """Add sample data to database"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("⚠️  Database already has data. Skipping seed.")
            return
        
        print("Seeding database with sample data...")
        
        # Create admin user
        admin = User(
            username="admin",
            email="admin@freshmart.com",
            first_name="Admin",
            last_name="User",
            phone="9999999999",
            hashed_password=hash_password("admin123"),
            role="admin",
            is_active=True,
            is_verified=True
        )
        db.add(admin)
        
        # Create test customer
        customer = User(
            username="john_doe",
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            phone="9876543210",
            hashed_password=hash_password("password123"),
            role="customer",
            is_active=True,
            is_verified=True
        )
        db.add(customer)
        db.flush()  # Get user IDs
        
        # Add sample address for customer
        address = UserAddress(
            user_id=customer.id,
            label="Home",
            street="123 Main Street, Apartment 4B",
            city="Mumbai",
            state="Maharashtra",
            postal_code="400001",
            country="India",
            is_default=True,
            delivery_instructions="Ring the doorbell twice"
        )
        db.add(address)
        
        # Create categories
        categories_data = [
            {"name": "Fruits", "description": "Fresh fruits", "icon": "🍎"},
            {"name": "Vegetables", "description": "Fresh vegetables", "icon": "🥬"},
            {"name": "Dairy", "description": "Milk and dairy products", "icon": "🥛"},
            {"name": "Meat", "description": "Fresh meat", "icon": "🥩"},
            {"name": "Seafood", "description": "Fresh seafood", "icon": "🐟"},
            {"name": "Bakery", "description": "Bread and bakery items", "icon": "🍞"},
            {"name": "Grains", "description": "Rice, wheat, and grains", "icon": "🌾"},
            {"name": "Beverages", "description": "Drinks and beverages", "icon": "🥤"},
        ]
        
        categories = []
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.add(category)
            categories.append(category)
        
        db.flush()  # Get category IDs
        
        # Create sample products
        products_data = [
            # Fruits
            {"name": "Organic Apples", "description": "Fresh organic apples from local farms", "price": 120, "original_price": 150, "badge": "Organic", "category_id": categories[0].id, "stock": 100, "rating": 4.5, "reviews_count": 45, "image_url": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6"},
            {"name": "Fresh Bananas", "description": "Ripe yellow bananas", "price": 40, "original_price": 50, "badge": "Fresh", "category_id": categories[0].id, "stock": 150, "rating": 4.3, "reviews_count": 32},
            {"name": "Sweet Oranges", "description": "Juicy sweet oranges", "price": 80, "original_price": 100, "badge": "Premium", "category_id": categories[0].id, "stock": 80, "rating": 4.6, "reviews_count": 28},
            
            # Vegetables
            {"name": "Fresh Tomatoes", "description": "Farm fresh tomatoes", "price": 30, "original_price": 40, "badge": "Fresh", "category_id": categories[1].id, "stock": 200, "rating": 4.4, "reviews_count": 56},
            {"name": "Organic Spinach", "description": "Organic green spinach", "price": 25, "original_price": 35, "badge": "Organic", "category_id": categories[1].id, "stock": 120, "rating": 4.7, "reviews_count": 41},
            {"name": "Fresh Carrots", "description": "Crunchy fresh carrots", "price": 35, "original_price": 45, "badge": "Fresh", "category_id": categories[1].id, "stock": 150, "rating": 4.5, "reviews_count": 38},
            
            # Dairy
            {"name": "Fresh Milk", "description": "Full cream fresh milk 1L", "price": 60, "original_price": 70, "badge": "Fresh", "category_id": categories[2].id, "stock": 100, "rating": 4.8, "reviews_count": 89},
            {"name": "Greek Yogurt", "description": "Creamy Greek yogurt", "price": 80, "original_price": 100, "badge": "Premium", "category_id": categories[2].id, "stock": 60, "rating": 4.6, "reviews_count": 52},
            {"name": "Cheddar Cheese", "description": "Aged cheddar cheese", "price": 250, "original_price": 300, "badge": "Premium", "category_id": categories[2].id, "stock": 40, "rating": 4.7, "reviews_count": 34},
            
            # Meat
            {"name": "Chicken Breast", "description": "Fresh chicken breast 500g", "price": 180, "original_price": 220, "badge": "Fresh", "category_id": categories[3].id, "stock": 50, "rating": 4.5, "reviews_count": 67},
            {"name": "Lamb Chops", "description": "Premium lamb chops", "price": 450, "original_price": 550, "badge": "Premium", "category_id": categories[3].id, "stock": 30, "rating": 4.8, "reviews_count": 23},
            
            # Seafood
            {"name": "Fresh Salmon", "description": "Atlantic salmon fillet", "price": 600, "original_price": 750, "badge": "Premium", "category_id": categories[4].id, "stock": 25, "rating": 4.9, "reviews_count": 45},
            {"name": "Prawns", "description": "Large fresh prawns", "price": 400, "original_price": 500, "badge": "Fresh", "category_id": categories[4].id, "stock": 35, "rating": 4.7, "reviews_count": 38},
            
            # Bakery
            {"name": "Whole Wheat Bread", "description": "Fresh whole wheat bread", "price": 40, "original_price": 50, "badge": "Fresh", "category_id": categories[5].id, "stock": 80, "rating": 4.4, "reviews_count": 92},
            {"name": "Croissants", "description": "Butter croissants pack of 6", "price": 120, "original_price": 150, "badge": "Artisan", "category_id": categories[5].id, "stock": 40, "rating": 4.8, "reviews_count": 56},
            
            # Grains
            {"name": "Basmati Rice", "description": "Premium basmati rice 5kg", "price": 350, "original_price": 400, "badge": "Premium", "category_id": categories[6].id, "stock": 100, "rating": 4.6, "reviews_count": 78},
            {"name": "Quinoa", "description": "Organic quinoa 1kg", "price": 280, "original_price": 350, "badge": "Organic", "category_id": categories[6].id, "stock": 50, "rating": 4.7, "reviews_count": 34},
            
            # Beverages
            {"name": "Orange Juice", "description": "Fresh orange juice 1L", "price": 120, "original_price": 150, "badge": "Fresh", "category_id": categories[7].id, "stock": 70, "rating": 4.5, "reviews_count": 67},
            {"name": "Green Tea", "description": "Organic green tea 100g", "price": 200, "original_price": 250, "badge": "Organic", "category_id": categories[7].id, "stock": 90, "rating": 4.8, "reviews_count": 89},
        ]
        
        for prod_data in products_data:
            product = Product(**prod_data)
            db.add(product)
        
        db.commit()
        print("✅ Sample data added successfully!")
        print("\n📝 Test Credentials:")
        print("   Admin: username=admin, password=admin123")
        print("   Customer: username=john_doe, password=password123")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Initializing FreshMart Database...\n")
    init_database()
    seed_data()
    print("\n✅ Database initialization complete!")
```

### 9.2 Run the initialization script

```bash
cd BackEnd
python init_db.py
```

---

## 🧪 Step 10: Testing Your API

### 10.1 Using Swagger UI (Easiest!)

1. Start your server:
```bash
uvicorn app.main:app --reload
```

2. Open browser: http://localhost:8000/docs

3. Try these endpoints:
   - POST `/auth/register` - Create account
   - POST `/auth/login` - Get token
   - Click "Authorize" button, paste token
   - GET `/addresses/` - Get your addresses
   - POST `/addresses/` - Create address
   - GET `/products/` - Get all products

### 10.2 Using curl

```bash
# 1. Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "phone": "1234567890",
    "password": "password123"
  }'

# 2. Login (save the token!)
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'

# 3. Get products (no auth needed)
curl http://localhost:8000/products/

# 4. Create address (needs token)
curl -X POST http://localhost:8000/addresses/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "label": "Home",
    "street": "123 Test St",
    "city": "Mumbai",
    "state": "Maharashtra",
    "postal_code": "400001",
    "country": "India",
    "is_default": true
  }'
```

---

## 🔗 Step 11: Connect Frontend to Backend

### 11.1 Update Frontend API URLs

In your React app, create `src/config.js`:

```javascript
// FrontEnd/src/config.js
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  // Auth
  register: `${API_BASE_URL}/auth/register`,
  login: `${API_BASE_URL}/auth/login`,
  me: `${API_BASE_URL}/auth/me`,
  
  // Addresses
  addresses: `${API_BASE_URL}/addresses`,
  
  // Products
  products: `${API_BASE_URL}/products`,
  
  // Orders
  orders: `${API_BASE_URL}/orders`,
};
```

### 11.2 Create API Helper

```javascript
// FrontEnd/src/utils/api.js
import { API_ENDPOINTS } from '../config';

// Get auth token
const getToken = () => localStorage.getItem('freshmart_token');

// Generic API call function
export const apiCall = async (url, options = {}) => {
  const token = getToken();
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const response = await fetch(url, {
    ...options,
    headers,
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'API request failed');
  }
  
  return response.json();
};

// Auth API
export const authAPI = {
  register: (data) => apiCall(API_ENDPOINTS.register, {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  login: (data) => apiCall(API_ENDPOINTS.login, {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  getMe: () => apiCall(API_ENDPOINTS.me),
};

// Address API
export const addressAPI = {
  getAll: () => apiCall(API_ENDPOINTS.addresses),
  
  create: (data) => apiCall(API_ENDPOINTS.addresses, {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  update: (id, data) => apiCall(`${API_ENDPOINTS.addresses}/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  
  delete: (id) => apiCall(`${API_ENDPOINTS.addresses}/${id}`, {
    method: 'DELETE',
  }),
  
  setDefault: (id) => apiCall(`${API_ENDPOINTS.addresses}/${id}/set-default`, {
    method: 'POST',
  }),
};

// Product API
export const productAPI = {
  getAll: (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return apiCall(`${API_ENDPOINTS.products}?${queryString}`);
  },
  
  getById: (id) => apiCall(`${API_ENDPOINTS.products}/${id}`),
};

// Order API
export const orderAPI = {
  create: (data) => apiCall(API_ENDPOINTS.orders, {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  getAll: () => apiCall(API_ENDPOINTS.orders),
  
  getById: (id) => apiCall(`${API_ENDPOINTS.orders}/${id}`),
  
  cancel: (id) => apiCall(`${API_ENDPOINTS.orders}/${id}/cancel`, {
    method: 'POST',
  }),
};
```

### 11.3 Use in Components

```javascript
// Example: Update Login.jsx
import { authAPI } from '../utils/api';

const handleSubmit = async (e) => {
  e.preventDefault();
  setIsLoading(true);
  setError('');

  try {
    const response = await authAPI.login({
      username: formData.username,
      password: formData.password
    });
    
    // Save token and user
    localStorage.setItem('freshmart_token', response.access_token);
    localStorage.setItem('freshmart_user', JSON.stringify(response.user));
    
    navigate('/');
  } catch (err) {
    setError(err.message);
  } finally {
    setIsLoading(false);
  }
};
```

---

## 📊 Step 12: Database Management

### 12.1 View Database

```bash
# Connect to PostgreSQL
psql -U postgres -d freshmart_db

# Useful commands:
\dt                    # List all tables
\d users              # Describe users table
SELECT * FROM users;  # View all users
\q                    # Quit
```

### 12.2 Reset Database

```bash
# Drop and recreate database
dropdb freshmart_db
createdb freshmart_db
python init_db.py
```

---

## 🚀 Step 13: Deployment (Production)

### 13.1 Update for Production

1. **Change SECRET_KEY** in `.env`
2. **Disable SQL echo** in `database.py`
3. **Update CORS origins** in `.env`
4. **Use production database**

### 13.2 Deploy to Render/Railway/Heroku

```bash
# Install gunicorn
pip install gunicorn

# Create Procfile
echo "web: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT" > Procfile

# Push to Git and deploy!
```

---

## 📚 Quick Reference

### Common Commands

```bash
# Start server
uvicorn app.main:app --reload

# Initialize database
python init_db.py

# Install dependencies
pip install -r requirements.txt

# Create migration (if using Alembic)
alembic revision --autogenerate -m "message"
alembic upgrade head
```

### API Endpoints Summary

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register user | No |
| POST | `/auth/login` | Login | No |
| GET | `/auth/me` | Get current user | Yes |
| GET | `/addresses/` | Get all addresses | Yes |
| POST | `/addresses/` | Create address | Yes |
| PUT | `/addresses/{id}` | Update address | Yes |
| DELETE | `/addresses/{id}` | Delete address | Yes |
| GET | `/products/` | Get all products | No |
| GET | `/products/{id}` | Get product | No |
| POST | `/orders/` | Create order | Yes |
| GET | `/orders/` | Get user orders | Yes |

---

## 🎉 You Did It!

You now have a complete FastAPI backend with:
- ✅ User authentication
- ✅ Address management
- ✅ Product catalog
- ✅ Order system
- ✅ Database integration
- ✅ API documentation

**Next Steps:**
1. Test all endpoints in Swagger UI
2. Connect your frontend
3. Add more features (reviews, wishlist, etc.)
4. Deploy to production

**Need Help?**
- FastAPI Docs: https://fastapi.tiangolo.com
- SQLAlchemy Docs: https://docs.sqlalchemy.org
- PostgreSQL Docs: https://www.postgresql.org/docs

You're not a "dumb ass bastard" - you're a developer learning FastAPI! 🚀💪
