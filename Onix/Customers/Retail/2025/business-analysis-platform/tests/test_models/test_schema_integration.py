"""Integration tests for Pydantic schemas with FastAPI compatibility"""
import json
from datetime import datetime
from typing import Dict
from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.models.schemas import (
    UserCreate, UserResponse, DatasetCreate, DatasetResponse,
    AnalysisJobCreate, AnalysisJobResponse, StandardResponse,
    ErrorResponse, BlockExecutionRequest
)


class TestSchemaIntegration:
    """Test schema integration and FastAPI compatibility"""
    
    def test_json_serialization(self):
        """Test that schemas can be serialized to JSON"""
        # User response
        user = UserResponse(
            id=str(uuid4()),
            email="test@example.com",
            is_active=True,
            is_superuser=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Should be able to convert to JSON
        user_json = user.model_dump_json()
        assert isinstance(user_json, str)
        
        # Should be able to parse back
        user_data = json.loads(user_json)
        assert user_data["email"] == "test@example.com"
    
    def test_api_response_format(self):
        """Test standard API response format"""
        # Success response
        data = {"user_id": str(uuid4()), "name": "Test User"}
        response = StandardResponse(
            success=True,
            data=data,
            errors=[]
        )
        
        response_dict = response.model_dump()
        assert response_dict["success"] is True
        assert response_dict["data"]["name"] == "Test User"
        assert response_dict["errors"] == []
        
        # Error response
        error_response = ErrorResponse(
            success=False,
            error={
                "code": "VALIDATION_ERROR",
                "message": "Invalid input"
            }
        )
        
        error_dict = error_response.model_dump()
        assert error_dict["success"] is False
        assert error_dict["error"]["code"] == "VALIDATION_ERROR"
    
    def test_nested_schema_validation(self):
        """Test validation of nested schemas"""
        # Create a complex nested structure
        job_data = {
            "name": "Complex Analysis",
            "description": "Test analysis with nested config",
            "dataset_id": str(uuid4()),
            "config": {
                "blocks": ["block1", "block2"],
                "parameters": {
                    "threshold": 0.95,
                    "iterations": 100,
                    "nested": {
                        "deep": {
                            "value": "test"
                        }
                    }
                }
            }
        }
        
        job = AnalysisJobCreate(**job_data)
        assert job.config["parameters"]["nested"]["deep"]["value"] == "test"
    
    def test_schema_aliases(self):
        """Test that schemas work with field aliases"""
        # Dataset with meta_data (which might be aliased in API)
        dataset = DatasetResponse(
            id=str(uuid4()),
            name="Test Dataset",
            file_path="data/test.csv",
            user_id=str(uuid4()),
            meta_data={"columns": ["col1", "col2"]},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Convert to dict with aliases
        dataset_dict = dataset.model_dump()
        assert "meta_data" in dataset_dict
        assert dataset_dict["meta_data"]["columns"][0] == "col1"
    
    def test_optional_fields_handling(self):
        """Test handling of optional fields"""
        # Create with minimal required fields
        dataset = DatasetCreate(
            name="Minimal Dataset",
            file_path="data/minimal.csv"
            # description is optional
        )
        
        assert dataset.name == "Minimal Dataset"
        assert dataset.description is None
        
        # Update with only some fields
        job_update = {
            "status": "running"
            # name and description are optional
        }
        
        # This should work without the optional fields
        from src.models.schemas import AnalysisJobUpdate
        update = AnalysisJobUpdate(**job_update)
        assert update.status == "running"
        assert update.name is None
    
    def test_validation_error_messages(self):
        """Test that validation errors provide useful messages"""
        # Invalid email
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(email="invalid-email", password="password123")
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("email" in str(error) for error in errors)
        
        # Missing required field
        with pytest.raises(ValidationError) as exc_info:
            DatasetCreate(name="Test")  # missing file_path
        
        errors = exc_info.value.errors()
        assert any("file_path" in str(error) for error in errors)
    
    def test_datetime_timezone_handling(self):
        """Test datetime handling with timezones"""
        now = datetime.utcnow()
        
        user = UserResponse(
            id=str(uuid4()),
            email="test@example.com",
            is_active=True,
            is_superuser=False,
            created_at=now,
            updated_at=now
        )
        
        # Serialize to JSON and back
        user_json = user.model_dump_json()
        user_data = json.loads(user_json)
        
        # Parse back to schema
        user_parsed = UserResponse(**user_data)
        
        # Datetimes should be preserved
        assert isinstance(user_parsed.created_at, datetime)
    
    def test_uuid_handling(self):
        """Test UUID field handling"""
        # UUIDs as strings
        user_id = str(uuid4())
        dataset_id = str(uuid4())
        
        job = AnalysisJobResponse(
            id=str(uuid4()),
            name="Test Job",
            status="pending",
            user_id=user_id,
            dataset_id=dataset_id,
            config={},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Should handle UUID strings properly
        assert job.user_id == user_id
        assert job.dataset_id == dataset_id
        
        # Should serialize properly
        job_dict = job.model_dump()
        assert isinstance(job_dict["user_id"], str)
    
    def test_request_payload_validation(self):
        """Test request payload validation for API endpoints"""
        # Valid block execution request
        request = BlockExecutionRequest(
            data={"input": [1, 2, 3]},
            config={"threshold": 0.95}
        )
        
        assert request.data["input"] == [1, 2, 3]
        assert request.config["threshold"] == 0.95
        
        # Request with only required fields
        minimal_request = BlockExecutionRequest(
            data={"test": "data"}
            # config is optional with default empty dict
        )
        
        assert minimal_request.data["test"] == "data"
        assert minimal_request.config == {}
    
    def test_response_metadata(self):
        """Test that response schemas include proper metadata"""
        # Job response with all metadata
        job = AnalysisJobResponse(
            id=str(uuid4()),
            name="Test Analysis",
            status="completed",
            user_id=str(uuid4()),
            dataset_id=str(uuid4()),
            config={"blocks": ["test"]},
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # All fields should be present
        job_dict = job.model_dump()
        assert "started_at" in job_dict
        assert "completed_at" in job_dict
        assert "created_at" in job_dict
        assert "updated_at" in job_dict