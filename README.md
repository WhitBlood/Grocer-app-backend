# FreshMart - Premium Grocery E-commerce Platform

A modern, full-stack e-commerce platform for premium grocery delivery built with React and FastAPI.

## Features

- 🛒 **Shopping Cart**: Add, remove, and manage items
- 🔍 **Search & Filter**: Find products by name, category
- 🌙 **Dark Mode**: Toggle between light and dark themes
- 📱 **Responsive Design**: Works on all devices
- 🎨 **Modern UI**: Beautiful animations and transitions
- 💳 **Checkout Process**: Complete order management
- 📦 **Product Categories**: Organized product browsing
- 👤 **User Authentication**: Registration, login, profile management
- 📊 **Admin Dashboard**: Product and order management
- 🚚 **Order Tracking**: Real-time delivery updates

## Tech Stack

### Frontend
- React 18 with Hooks
- Tailwind CSS for styling
- Vite for build tooling
- React Router for navigation
- Context API for state management

### Backend
- FastAPI (Python)
- PostgreSQL (Primary Database)
- Redis (Caching & Sessions)
- JWT Authentication
- Pydantic for data validation
- SQLAlchemy ORM
- Alembic for migrations

## Backend API Routes & Database Schema

### 🗄️ Database Tables Required

#### Users Table
```sql
users:
- id (Primary Key)
- email (Unique)
- password_hash
- first_name
- last_name
- phone
- is_active
- is_verified
- role (customer/admin)
- created_at
- updated_at
```

#### Products Table
```sql
products:
- id (Primary Key)
- name
- description
- price
- original_price
- category_id (Foreign Key)
- stock_quantity
- sku
- images (JSON array)
- rating
- review_count
- is_active
- created_at
- updated_at
```

#### Categories Table
```sql
categories:
- id (Primary Key)
- name
- description
- icon
- color_gradient
- is_active
- created_at
```

#### Orders Table
```sql
orders:
- id (Primary Key)
- user_id (Foreign Key)
- status (pending/confirmed/processing/shipped/delivered/cancelled)
- total_amount
- subtotal
- tax_amount
- delivery_fee
- delivery_address (JSON)
- payment_method
- payment_status
- created_at
- updated_at
```

#### Order Items Table
```sql
order_items:
- id (Primary Key)
- order_id (Foreign Key)
- product_id (Foreign Key)
- quantity
- unit_price
- total_price
```

#### User Addresses Table
```sql
user_addresses:
- id (Primary Key)
- user_id (Foreign Key)
- address_line1
- address_line2
- city
- state
- pincode
- is_default
- created_at
```

#### Reviews Table
```sql
reviews:
- id (Primary Key)
- user_id (Foreign Key)
- product_id (Foreign Key)
- rating (1-5)
- comment
- created_at
```

### 🛣️ FastAPI Routes to Implement

#### Authentication Routes (`/auth`)
```python
POST   /auth/register          # User registration
POST   /auth/login             # User login
POST   /auth/logout            # User logout
POST   /auth/refresh           # Refresh JWT token
POST   /auth/forgot-password   # Password reset request
POST   /auth/reset-password    # Password reset confirmation
GET    /auth/verify-email      # Email verification
```

#### User Routes (`/users`)
```python
GET    /users/me               # Get current user profile
PUT    /users/me               # Update user profile
GET    /users/me/addresses     # Get user addresses
POST   /users/me/addresses     # Add new address
PUT    /users/me/addresses/{id} # Update address
DELETE /users/me/addresses/{id} # Delete address
GET    /users/me/orders        # Get user order history
```

#### Product Routes (`/products`)
```python
GET    /products               # Get all products (with pagination, filters)
GET    /products/{id}          # Get single product details
GET    /products/search        # Search products
GET    /products/category/{category_id} # Get products by category
GET    /products/{id}/reviews  # Get product reviews
POST   /products/{id}/reviews  # Add product review (authenticated)
```

#### Category Routes (`/categories`)
```python
GET    /categories             # Get all categories
GET    /categories/{id}        # Get category details
GET    /categories/{id}/products # Get products in category
```

#### Cart Routes (`/cart`)
```python
GET    /cart                   # Get user's cart
POST   /cart/items             # Add item to cart
PUT    /cart/items/{id}        # Update cart item quantity
DELETE /cart/items/{id}        # Remove item from cart
DELETE /cart                   # Clear entire cart
```

#### Order Routes (`/orders`)
```python
POST   /orders                 # Create new order
GET    /orders                 # Get user's orders
GET    /orders/{id}            # Get specific order details
PUT    /orders/{id}/cancel     # Cancel order
GET    /orders/{id}/track      # Track order status
```

#### Admin Routes (`/admin`)
```python
# Product Management
GET    /admin/products         # Get all products (admin view)
POST   /admin/products         # Create new product
PUT    /admin/products/{id}    # Update product
DELETE /admin/products/{id}    # Delete product
POST   /admin/products/{id}/images # Upload product images

# Order Management
GET    /admin/orders           # Get all orders
PUT    /admin/orders/{id}/status # Update order status
GET    /admin/dashboard        # Get dashboard statistics

# User Management
GET    /admin/users            # Get all users
PUT    /admin/users/{id}/status # Activate/deactivate user

# Category Management
GET    /admin/categories       # Get all categories
POST   /admin/categories       # Create category
PUT    /admin/categories/{id}  # Update category
DELETE /admin/categories/{id}  # Delete category
```

#### Utility Routes
```python
GET    /health                 # Health check
POST   /upload                 # File upload endpoint
GET    /stats                  # Public statistics
```

### 🔧 Additional Backend Requirements

#### Environment Variables
```env
DATABASE_URL=postgresql://user:password@localhost/freshmart
REDIS_URL=redis://localhost:6379
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880  # 5MB
```

#### Key Features to Implement
- **JWT Authentication** with refresh tokens
- **Password hashing** using bcrypt
- **Email verification** for new users
- **File upload** for product images
- **Pagination** for product listings
- **Search functionality** with filters
- **Rate limiting** for API endpoints
- **Input validation** using Pydantic models
- **Error handling** with proper HTTP status codes
- **Database migrations** using Alembic
- **Redis caching** for frequently accessed data
- **Background tasks** for email sending
- **API documentation** with Swagger/OpenAPI

#### Recommended FastAPI Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API route handlers
│   ├── services/            # Business logic
│   ├── utils/               # Utility functions
│   └── dependencies.py     # Dependency injection
├── alembic/                 # Database migrations
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables
```

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL 13+
- Redis 6+

### Frontend Installation

1. Clone the repository
```bash
git clone <repository-url>
cd freshmart
```

2. Install frontend dependencies
```bash
cd FrontEnd
npm install
```

3. Start development server
```bash
npm run dev
```

4. Open http://localhost:3000 in your browser

### Backend Setup (To be implemented)

1. Create virtual environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Setup database
```bash
createdb freshmart
alembic upgrade head
```

4. Start FastAPI server
```bash
uvicorn app.main:app --reload
```

## Project Structure

```
FrontEnd/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/         # Page components
│   ├── context/       # React Context providers
│   ├── data/          # Static data and utilities
│   └── main.jsx       # App entry point
├── public/            # Static assets
└── package.json       # Dependencies and scripts

backend/               # FastAPI backend (to be created)
├── app/
│   ├── models/        # Database models
│   ├── routers/       # API routes
│   ├── schemas/       # Pydantic schemas
│   └── services/      # Business logic
└── requirements.txt   # Python dependencies
```

## Available Scripts

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

### Backend (Planned)
- `uvicorn app.main:app --reload` - Start development server
- `alembic upgrade head` - Run database migrations
- `pytest` - Run tests

## Docker Setup

### Build and run with Docker Compose
```bash
cd FrontEnd
docker-compose up --build
```

### Access the application
- Frontend: http://localhost:3000
- Health check: http://localhost:3000/health

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
