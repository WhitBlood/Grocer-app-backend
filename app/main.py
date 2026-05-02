from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .config import settings
from .database import engine, Base
from .routers import auth, addresses, products, orders

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
logger.info("Creating database tables if they don't exist...")
Base.metadata.create_all(bind=engine)
logger.info("✅ Database tables ready")

# Create FastAPI app with dynamic configuration
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs" if not settings.is_production else None,  # Disable docs in production
    redoc_url="/redoc" if not settings.is_production else None,
)

logger.info(f"Starting {settings.API_TITLE} v{settings.API_VERSION}")
logger.info(f"Environment: {settings.ENVIRONMENT}")
logger.info(f"CORS Origins: {settings.origins_list}")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,  # Use configured origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(auth.router)
app.include_router(addresses.router)
app.include_router(products.router)
app.include_router(orders.router)

logger.info("✅ All routers registered")


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("🚀 Application startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("👋 Application shutting down")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": f"{settings.API_TITLE} is running!",
        "version": settings.API_VERSION,
        "status": "healthy",
        "environment": settings.ENVIRONMENT
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
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
        "database": "unknown"
    }
    
    # Test database connection
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        health_status["database"] = "connected"
        logger.debug("Health check: database connection successful")
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["database"] = f"disconnected: {str(e)}"
        logger.error(f"Health check: database connection failed - {e}")
    
    return health_status


@app.get("/ready")
async def readiness_check():
    """
    Readiness check for Kubernetes/Docker/ECS.
    Returns 200 if service is ready to accept traffic.
    """
    from sqlalchemy import text
    from .database import SessionLocal
    from fastapi import HTTPException
    
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "ready", "environment": settings.ENVIRONMENT}
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service not ready: {str(e)}")


