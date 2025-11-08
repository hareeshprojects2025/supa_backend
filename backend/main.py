"""
FastAPI Main Application
Mobile Attendance System Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import attendance_v1
from database import engine, Base
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Mobile Attendance System API",
    description="Backend for Android-based attendance tracking with Bluetooth",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for React frontend and Android app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(attendance_v1.router, prefix="/api/v1", tags=["Attendance V1"])

@app.get("/")
async def root():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {
        "status": "online",
        "message": "Mobile Attendance System API",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "api_version": "v1"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)