from pydantic_settings import BaseSettings
from typing import List
import os

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
        env_file_encoding = 'utf-8'
        case_sensitive = False
        # Don't fail if .env file doesn't exist
        extra = "ignore"

    @property
    def origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

# Try to load settings, provide helpful error message if it fails
try:
    settings = Settings()
except Exception as e:
    print("=" * 60)
    print("❌ ERROR: Missing required environment variables!")
    print("=" * 60)
    print("\nRequired variables:")
    print("  - DATABASE_URL")
    print("  - SECRET_KEY")
    print("\nPlease create a .env file with:")
    print("\nDATABASE_URL=postgresql://user:password@host:5432/dbname")
    print("SECRET_KEY=your-secret-key-here")
    print("\nOr set them as environment variables.")
    print("=" * 60)
    raise
