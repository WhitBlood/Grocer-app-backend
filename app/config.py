
from pydantic_settings import BaseSettings
from typing import List, Optional
import os
import boto3
import json
from botocore.exceptions import ClientError
import logging
from dotenv import load_dotenv

# Load environment variables from .env file FIRST
load_dotenv()

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def get_aws_secret(secret_name: str, region_name: Optional[str] = None) -> dict:
    """
    Fetch a secret from AWS Secrets Manager.
    
    Args:
        secret_name: Name of the secret in AWS Secrets Manager
        region_name: AWS region (defaults to AWS_REGION env var or us-east-1)
    
    Returns:
        Dictionary containing the secret values
    
    Raises:
        ClientError: If unable to fetch the secret
    """
    if region_name is None:
        region_name = os.getenv("AWS_REGION", "us-east-1")
    
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    try:
        logger.info(f"Fetching secret '{secret_name}' from AWS Secrets Manager in region {region_name}")
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        logger.info(f"Successfully fetched secret '{secret_name}'")
        return json.loads(secret)
    except ClientError as e:
        error_code = e.response['Error']['Code']
        logger.error(f"Failed to fetch secret '{secret_name}': {error_code} - {e}")
        raise


def build_database_url(secret: dict) -> str:
    """
    Build a PostgreSQL connection URL from secret components.
    
    Args:
        secret: Dictionary containing database credentials
    
    Returns:
        PostgreSQL connection URL string
    """
    # Try to build from individual components
    host = secret.get("host")
    username = secret.get("username")
    password = secret.get("password")
    dbname = secret.get("dbname")
    port = secret.get("port", 5432)
    
    if all([host, username, password, dbname]):
        url = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
        logger.info(f"Built database URL from components: postgresql://{username}:***@{host}:{port}/{dbname}")
        return url
    
    # Fallback to DATABASE_URL if present
    if "DATABASE_URL" in secret:
        logger.info("Using DATABASE_URL from secret")
        return secret["DATABASE_URL"]
    
    raise ValueError("Secret must contain either (host, username, password, dbname) or DATABASE_URL")


# Determine deployment mode
USE_AWS_SECRETS = os.getenv("USE_AWS_SECRETS", "false").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

logger.info(f"Starting application in {ENVIRONMENT} mode")
logger.info(f"USE_AWS_SECRETS: {USE_AWS_SECRETS}")

# Load configuration based on deployment mode
if USE_AWS_SECRETS:
    logger.info("Loading configuration from AWS Secrets Manager")
    try:
        secret_name = os.getenv("AWS_SECRET_NAME", "rds-db-password")
        aws_secret = get_aws_secret(secret_name)
        DATABASE_URL = build_database_url(aws_secret)
        SECRET_KEY = aws_secret.get("SECRET_KEY")
        
        if not SECRET_KEY:
            raise ValueError("SECRET_KEY not found in AWS secret")
            
    except Exception as e:
        logger.error(f"Failed to load AWS secrets: {e}")
        raise RuntimeError(f"AWS Secrets Manager configuration failed: {e}")
else:
    logger.info("Loading configuration from environment variables")
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is required when USE_AWS_SECRETS=false")
    if not SECRET_KEY:
        logger.warning("SECRET_KEY not set, using default (NOT SECURE FOR PRODUCTION)")
        SECRET_KEY = "dev-secret-key-change-in-production"

class Settings(BaseSettings):
    """Application settings with support for both local and AWS deployments."""
    
    # Database
    DATABASE_URL: str = DATABASE_URL
    
    # Security
    SECRET_KEY: str = SECRET_KEY
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))  # 7 days default
    
    # CORS
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
    
    # Application
    ENVIRONMENT: str = ENVIRONMENT
    API_TITLE: str = os.getenv("API_TITLE", "FreshMart API")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    API_DESCRIPTION: str = os.getenv("API_DESCRIPTION", "Backend API for FreshMart Grocery Store")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    SQL_ECHO: bool = os.getenv("SQL_ECHO", "true").lower() == "true"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = False
        extra = "ignore"

    @property
    def origins_list(self) -> List[str]:
        """Parse ALLOWED_ORIGINS into a list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT.lower() == "development"


# Initialize settings
try:
    settings = Settings()
    logger.info("✅ Settings loaded successfully")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configured'}")
    logger.info(f"CORS Origins: {settings.origins_list}")
except Exception as e:
    logger.error(f"❌ Failed to load settings: {e}")
    if USE_AWS_SECRETS:
        logger.error("Check that AWS Secrets Manager is properly configured:")
        logger.error(f"  - Secret name: {os.getenv('AWS_SECRET_NAME', 'rds-db-password')}")
        logger.error(f"  - Region: {os.getenv('AWS_REGION', 'us-east-1')}")
        logger.error("  - IAM permissions for secretsmanager:GetSecretValue")
    else:
        logger.error("For local development, ensure .env file exists with:")
        logger.error("  - DATABASE_URL")
        logger.error("  - SECRET_KEY")
    raise
