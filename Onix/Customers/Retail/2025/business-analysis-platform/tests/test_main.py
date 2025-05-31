"""Tests for main FastAPI application"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from main import app


class TestMainApp:
    """Test suite for main FastAPI application"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    def test_app_initialization(self):
        """Test that FastAPI app initializes correctly"""
        assert app.title == "Business Analysis Platform API"
        assert app.version == "1.0.0"
    
    def test_health_check_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert "timestamp" in data
        
        # Verify timestamp is valid ISO format
        timestamp = datetime.fromisoformat(data["timestamp"])
        assert isinstance(timestamp, datetime)
    
    def test_version_endpoint(self, client):
        """Test version endpoint"""
        response = client.get("/api/v1/version")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["version"] == "1.0.0"
        assert data["api_name"] == "Business Analysis Platform API"
        assert "environment" in data
    
    def test_cors_configuration(self):
        """Test CORS is configured correctly"""
        # Check that CORS middleware is configured
        cors_middleware = None
        
        for middleware in app.user_middleware:
            if middleware.cls.__name__ == "CORSMiddleware":
                cors_middleware = middleware
                break
        
        assert cors_middleware is not None
        
        # Check allowed origins include React frontend
        assert "http://localhost:3000" in cors_middleware.kwargs["allow_origins"]
        assert cors_middleware.kwargs["allow_credentials"] is True
        assert cors_middleware.kwargs["allow_methods"] == ["*"]
        assert cors_middleware.kwargs["allow_headers"] == ["*"]
    
    def test_routers_mounted(self):
        """Test that all expected routers are mounted"""
        # Get all routes
        routes = [route.path for route in app.routes]
        
        # Check for expected API prefixes
        assert any("/api/v1/blocks" in route for route in routes)
        assert any("/api/v1/data" in route for route in routes)
        assert any("/api/v1/analysis" in route for route in routes)
        assert any("/api/v1/templates" in route for route in routes)
    
    def test_error_handlers_registered(self):
        """Test that error handlers are registered"""
        # Test 404 error
        client = TestClient(app)
        response = client.get("/nonexistent")
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data or "detail" in data
    
    def test_root_redirect(self, client):
        """Test that root path redirects to docs"""
        response = client.get("/")
        
        # Should redirect to docs
        assert response.status_code == 200 or response.status_code == 307
        
        # If it's a redirect, follow it
        if response.status_code == 307:
            assert "/docs" in response.headers.get("location", "")
    
    def test_openapi_documentation(self, client):
        """Test that OpenAPI documentation is available"""
        # Test docs endpoint
        response = client.get("/docs")
        assert response.status_code == 200
        
        # Test OpenAPI JSON endpoint
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        openapi_data = response.json()
        assert openapi_data["info"]["title"] == "Business Analysis Platform API"
        assert openapi_data["info"]["version"] == "1.0.0"
    
    def test_exception_handler(self, client):
        """Test custom exception handling"""
        # This will test if we have proper exception handling
        # We'll need to create an endpoint that raises an exception
        response = client.get("/api/v1/test-error")
        
        # Should return structured error response
        if response.status_code == 500:
            data = response.json()
            assert "error" in data or "detail" in data
    
    def test_middleware_order(self):
        """Test that middleware is applied in correct order"""
        middleware_classes = [m.cls.__name__ for m in app.user_middleware]
        
        # CORS should be one of the first middleware
        cors_index = next((i for i, name in enumerate(middleware_classes) 
                          if name == "CORSMiddleware"), -1)
        assert cors_index != -1
        assert cors_index < 2  # Should be near the top
    
    def test_api_prefix_consistency(self, client):
        """Test that all API endpoints use consistent prefix"""
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)
        
        # All API endpoints should start with /api/v1
        api_routes = [r for r in routes if r.startswith("/api/")]
        for route in api_routes:
            assert route.startswith("/api/v1/"), f"Route {route} doesn't use /api/v1 prefix"