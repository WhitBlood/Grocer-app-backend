"""
Script to drop and recreate all database tables.
Run this when your models change and you need to reset the database.
"""
from app.database import engine, Base
from app.models import User, UserAddress, Category, Product, Order, OrderItem

def recreate_tables():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database tables recreated successfully!")

if __name__ == "__main__":
    recreate_tables()
