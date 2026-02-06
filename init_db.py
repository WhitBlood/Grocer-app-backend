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
