from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from .database import engine, Base
from .routers import auth, addresses, products, orders

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="FreshMart API",
    description="Backend API for FreshMart Grocery Store",
    version="1.0.0"
)

# Get allowed origins from environment
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173,http://127.0.0.1:5500")
origins_list = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_list,
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
    """
    Detailed health check endpoint.
    Tests database connectivity and returns service status.
    """
    from sqlalchemy import text
    from .database import SessionLocal
    
    health_status = {
        "status": "healthy",
        "service": "FreshMart API",
        "version": "1.0.0",
        "database": "unknown"
    }
    
    # Test database connection
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        health_status["database"] = "connected"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["database"] = f"disconnected: {str(e)}"
    
    return health_status

@app.get("/ready")
async def readiness_check():
    """
    Readiness check for Kubernetes/Docker.
    Returns 200 if service is ready to accept traffic.
    """
    from sqlalchemy import text
    from .database import SessionLocal
    from fastapi import HTTPException
    
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service not ready: {str(e)}")


