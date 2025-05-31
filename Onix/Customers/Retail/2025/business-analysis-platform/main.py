"""Main FastAPI application for Business Analysis Platform API"""
from datetime import datetime

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# Import routers
from src.api import blocks, data, analysis, templates

# Create FastAPI app
app = FastAPI(
    title="Business Analysis Platform API",
    version="1.0.0",
    description="Backend API for Business Analysis Platform",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create API v1 router
api_v1_router = APIRouter(prefix="/api/v1")


# Health check endpoint
@api_v1_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


# Version endpoint
@api_v1_router.get("/version")
async def get_version():
    """Get API version information"""
    return {
        "version": "1.0.0",
        "api_name": "Business Analysis Platform API",
        "environment": "development"  # This should come from config in production
    }


# Root redirect to docs
@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to API documentation"""
    return RedirectResponse(url="/docs")


# Include routers
api_v1_router.include_router(blocks.router, prefix="/blocks", tags=["blocks"])
api_v1_router.include_router(data.router, prefix="/data", tags=["data"])
api_v1_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_v1_router.include_router(templates.router, prefix="/templates", tags=["templates"])

# Mount API v1 router
app.include_router(api_v1_router)


# Error handlers
from fastapi.responses import JSONResponse

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={"error": "Not found", "detail": str(exc)}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors"""
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


# Test error endpoint (for testing error handling)
@api_v1_router.get("/test-error", include_in_schema=False)
async def test_error():
    """Test endpoint that raises an error"""
    raise Exception("Test error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)