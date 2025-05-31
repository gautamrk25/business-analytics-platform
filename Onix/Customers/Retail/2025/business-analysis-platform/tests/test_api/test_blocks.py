"""Tests for Building Blocks API router"""
import pytest
from uuid import uuid4
from datetime import datetime
from fastapi.testclient import TestClient

from main import app
from src.models.schemas import BlockExecutionRequest, BuildingBlockResponse


class TestBlocksAPI:
    """Test suite for Building Blocks API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    def test_list_blocks(self, client):
        """Test listing all available blocks"""
        response = client.get("/api/v1/blocks")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return standard response format
        assert "success" in data
        assert "data" in data
        assert "error" in data
        assert "metadata" in data
        
        assert data["success"] is True
        assert data["error"] is None
        assert isinstance(data["data"], list)
    
    def test_list_blocks_with_filters(self, client):
        """Test listing blocks with filters"""
        # Test with category filter
        response = client.get("/api/v1/blocks?category=data")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        # Test with active filter
        response = client.get("/api/v1/blocks?is_active=true")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_get_block_details(self, client):
        """Test getting details of a specific block"""
        block_id = "test_block"
        response = client.get(f"/api/v1/blocks/{block_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["error"] is None
        
        # Block details should match schema
        if data["data"]:  # If block exists
            block = data["data"]
            assert "id" in block
            assert "name" in block
            assert "description" in block
            assert "category" in block
            assert "version" in block
            assert "config_schema" in block
            assert "is_active" in block
    
    def test_get_nonexistent_block(self, client):
        """Test getting details of non-existent block"""
        block_id = "nonexistent_block"
        response = client.get(f"/api/v1/blocks/{block_id}")
        
        assert response.status_code == 404
        data = response.json()
        
        assert data["success"] is False
        assert data["error"] is not None
    
    def test_execute_block(self, client):
        """Test executing a building block"""
        block_id = "test_block"
        request_data = {
            "data": {"values": [1, 2, 3, 4, 5]},
            "config": {"threshold": 0.95}
        }
        
        response = client.post(
            f"/api/v1/blocks/{block_id}/execute",
            json=request_data
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["error"] is None
        assert "data" in data
        assert "metadata" in data
        
        # Metadata should include execution info
        metadata = data["metadata"]
        assert "timestamp" in metadata
        assert "execution_time" in metadata
        assert "block_version" in metadata
    
    def test_execute_nonexistent_block(self, client):
        """Test executing non-existent block"""
        block_id = "nonexistent_block"
        request_data = {"data": {}, "config": {}}
        
        response = client.post(
            f"/api/v1/blocks/{block_id}/execute",
            json=request_data
        )
        
        assert response.status_code == 404
        data = response.json()
        
        assert data["success"] is False
        assert data["error"] is not None
    
    def test_execute_block_validation_error(self, client):
        """Test executing block with invalid data"""
        block_id = "test_block"
        # Missing required 'data' field
        request_data = {"config": {}}
        
        response = client.post(
            f"/api/v1/blocks/{block_id}/execute",
            json=request_data
        )
        
        assert response.status_code == 422
        # FastAPI validation error response
    
    def test_execute_block_with_error(self, client):
        """Test executing block that returns an error"""
        block_id = "error_block"
        request_data = {"data": {"trigger_error": True}, "config": {}}
        
        response = client.post(
            f"/api/v1/blocks/{block_id}/execute",
            json=request_data
        )
        
        # Should still return 200 but with success=false in the response
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is False
        assert data["error"] is not None
        assert "Error executing block" in data["error"]
    
    def test_get_block_metrics(self, client):
        """Test getting metrics for a block"""
        block_id = "test_block"
        response = client.get(f"/api/v1/blocks/{block_id}/metrics")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "data" in data
        
        metrics = data["data"]
        if metrics:  # If metrics exist
            assert "execution_count" in metrics
            assert "success_rate" in metrics
            assert "average_execution_time" in metrics
            assert "last_execution" in metrics
    
    def test_get_metrics_nonexistent_block(self, client):
        """Test getting metrics for non-existent block"""
        block_id = "nonexistent_block"
        response = client.get(f"/api/v1/blocks/{block_id}/metrics")
        
        assert response.status_code == 404
        data = response.json()
        
        assert data["success"] is False
        assert data["error"] is not None
    
    def test_block_response_metadata(self, client):
        """Test that all responses include proper metadata"""
        # Test list endpoint
        response = client.get("/api/v1/blocks")
        data = response.json()
        
        metadata = data["metadata"]
        assert "timestamp" in metadata
        assert "request_id" in metadata
        assert "version" in metadata
        
        # Verify timestamp format
        timestamp = datetime.fromisoformat(metadata["timestamp"])
        assert isinstance(timestamp, datetime)
        
        # Verify version
        assert metadata["version"] == "1.0"
    
    def test_concurrent_block_execution(self, client):
        """Test executing multiple blocks concurrently"""
        import concurrent.futures
        
        block_id = "test_block"
        request_data = {"data": {"test": "concurrent"}, "config": {}}
        
        def execute_block():
            return client.post(
                f"/api/v1/blocks/{block_id}/execute",
                json=request_data
            )
        
        # Execute 5 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(execute_block) for _ in range(5)]
            results = [future.result() for future in futures]
        
        # All should succeed
        for response in results:
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
    
    def test_block_registry_integration(self, client):
        """Test that blocks are properly registered and discoverable"""
        # First, list all blocks
        response = client.get("/api/v1/blocks")
        all_blocks = response.json()["data"]
        
        if all_blocks:  # If any blocks are registered
            # Get details for each block
            for block_summary in all_blocks:
                block_id = block_summary["id"]
                detail_response = client.get(f"/api/v1/blocks/{block_id}")
                assert detail_response.status_code == 200
                
                block_detail = detail_response.json()["data"]
                assert block_detail["id"] == block_id