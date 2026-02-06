"""
Test database connection script.
Run this to verify your DATABASE_URL is correct.
"""
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in .env file!")
    print("\nPlease create a .env file with:")
    print("DATABASE_URL=postgresql://username:password@localhost:5432/freshmart_db")
    exit(1)

print(f"Testing connection to: {DATABASE_URL.replace(DATABASE_URL.split('@')[0].split('//')[1], '***')}")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"✅ Connected successfully!")
        print(f"PostgreSQL version: {version[:50]}...")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check if PostgreSQL is running: pg_isready")
    print("2. Verify your DATABASE_URL in .env file")
    print("3. Check username and password")
    print("4. Make sure database 'freshmart_db' exists: createdb freshmart_db")
