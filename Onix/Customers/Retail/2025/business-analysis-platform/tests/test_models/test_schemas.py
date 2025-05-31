"""Tests for Pydantic schemas"""
import pytest
from datetime import datetime
from uuid import uuid4
from pydantic import ValidationError

from src.models.schemas import (
    # User schemas
    UserBase, UserCreate, UserUpdate, UserInDB, UserResponse,
    
    # Dataset schemas
    DatasetBase, DatasetCreate, DatasetUpdate, DatasetInDB, DatasetResponse,
    
    # Building Block schemas
    BuildingBlockBase, BuildingBlockResponse, BlockExecutionRequest,
    
    # Analysis Job schemas
    AnalysisJobCreate, AnalysisJobUpdate, AnalysisJobResponse, JobResultResponse,
    
    # Common schemas
    StandardResponse, ErrorResponse, HealthResponse
)


class TestUserSchemas:
    """Test suite for User-related schemas"""
    
    def test_user_create_schema(self):
        """Test UserCreate schema validation"""
        # Valid data
        user_data = {
            "email": "test@example.com",
            "password": "StrongPassword123!"
        }
        user = UserCreate(**user_data)
        assert user.email == "test@example.com"
        assert user.password == "StrongPassword123!"
        
        # Invalid email
        with pytest.raises(ValidationError):
            UserCreate(email="invalid-email", password="password123")
        
        # Missing password
        with pytest.raises(ValidationError):
            UserCreate(email="test@example.com")
    
    def test_user_update_schema(self):
        """Test UserUpdate schema with optional fields"""
        # Update only email
        update = UserUpdate(email="new@example.com")
        assert update.email == "new@example.com"
        assert update.password is None
        
        # Update only password
        update = UserUpdate(password="NewPassword123!")
        assert update.password == "NewPassword123!"
        assert update.email is None
        
        # Update nothing (all fields optional)
        update = UserUpdate()
        assert update.email is None
        assert update.password is None
    
    def test_user_response_schema(self):
        """Test UserResponse schema"""
        user_data = {
            "id": str(uuid4()),
            "email": "test@example.com",
            "is_active": True,
            "is_superuser": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        user = UserResponse(**user_data)
        assert user.id == user_data["id"]
        assert user.email == "test@example.com"
        assert user.is_active is True
        assert user.is_superuser is False
        
        # Should not include password
        assert not hasattr(user, 'password')
        assert not hasattr(user, 'hashed_password')


class TestDatasetSchemas:
    """Test suite for Dataset-related schemas"""
    
    def test_dataset_create_schema(self):
        """Test DatasetCreate schema"""
        dataset_data = {
            "name": "Test Dataset",
            "description": "A test dataset",
            "file_path": "data/test.csv"
        }
        
        dataset = DatasetCreate(**dataset_data)
        assert dataset.name == "Test Dataset"
        assert dataset.description == "A test dataset"
        assert dataset.file_path == "data/test.csv"
        
        # Missing required field
        with pytest.raises(ValidationError):
            DatasetCreate(name="Test", description="Test")
    
    def test_dataset_response_schema(self):
        """Test DatasetResponse schema"""
        dataset_data = {
            "id": str(uuid4()),
            "name": "Test Dataset",
            "description": "A test dataset",
            "file_path": "data/test.csv",
            "file_size": 1024,
            "row_count": 100,
            "column_count": 5,
            "user_id": str(uuid4()),
            "meta_data": {"columns": ["col1", "col2"]},
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        dataset = DatasetResponse(**dataset_data)
        assert dataset.name == "Test Dataset"
        assert dataset.file_size == 1024
        assert dataset.meta_data["columns"][0] == "col1"


class TestBuildingBlockSchemas:
    """Test suite for Building Block-related schemas"""
    
    def test_building_block_response(self):
        """Test BuildingBlockResponse schema"""
        block_data = {
            "id": "data_validation",
            "name": "Data Validation",
            "description": "Validates data quality",
            "category": "data",
            "version": "1.0.0",
            "config_schema": {
                "type": "object",
                "properties": {
                    "threshold": {"type": "number"}
                }
            },
            "is_active": True
        }
        
        block = BuildingBlockResponse(**block_data)
        assert block.id == "data_validation"
        assert block.category == "data"
        assert block.config_schema["properties"]["threshold"]["type"] == "number"
    
    def test_block_execution_request(self):
        """Test BlockExecutionRequest schema"""
        request_data = {
            "data": {"values": [1, 2, 3]},
            "config": {"threshold": 0.95}
        }
        
        request = BlockExecutionRequest(**request_data)
        assert request.data["values"] == [1, 2, 3]
        assert request.config["threshold"] == 0.95
        
        # Empty config should be allowed
        request = BlockExecutionRequest(data={"test": "data"})
        assert request.config == {}


class TestAnalysisJobSchemas:
    """Test suite for Analysis Job-related schemas"""
    
    def test_analysis_job_create(self):
        """Test AnalysisJobCreate schema"""
        job_data = {
            "name": "Test Analysis",
            "description": "Test analysis job",
            "dataset_id": str(uuid4()),
            "config": {
                "blocks": ["data_validation", "statistical_analysis"],
                "parameters": {"threshold": 0.95}
            }
        }
        
        job = AnalysisJobCreate(**job_data)
        assert job.name == "Test Analysis"
        assert job.config["blocks"][0] == "data_validation"
        assert job.config["parameters"]["threshold"] == 0.95
    
    def test_analysis_job_response(self):
        """Test AnalysisJobResponse schema"""
        job_data = {
            "id": str(uuid4()),
            "name": "Test Analysis",
            "description": "Test analysis job",
            "status": "running",
            "user_id": str(uuid4()),
            "dataset_id": str(uuid4()),
            "config": {"blocks": ["test_block"]},
            "error_message": None,
            "started_at": datetime.utcnow(),
            "completed_at": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        job = AnalysisJobResponse(**job_data)
        assert job.status == "running"
        assert job.error_message is None
        assert job.completed_at is None
    
    def test_job_result_response(self):
        """Test JobResultResponse schema"""
        result_data = {
            "id": str(uuid4()),
            "job_id": str(uuid4()),
            "block_id": "test_block",
            "status": "success",
            "result_data": {"metrics": {"accuracy": 0.95}},
            "error_message": None,
            "execution_time": 1.5,
            "created_at": datetime.utcnow()
        }
        
        result = JobResultResponse(**result_data)
        assert result.status == "success"
        assert result.result_data["metrics"]["accuracy"] == 0.95
        assert result.execution_time == 1.5


class TestCommonSchemas:
    """Test suite for common schemas"""
    
    def test_standard_response(self):
        """Test StandardResponse schema"""
        response = StandardResponse(
            success=True,
            data={"result": "test"},
            errors=[]
        )
        
        assert response.success is True
        assert response.data["result"] == "test"
        assert response.errors == []
        
        # With errors
        response = StandardResponse(
            success=False,
            data=None,
            errors=["Error 1", "Error 2"]
        )
        
        assert response.success is False
        assert response.data is None
        assert len(response.errors) == 2
    
    def test_error_response(self):
        """Test ErrorResponse schema"""
        error = ErrorResponse(
            success=False,
            error={
                "code": "VALIDATION_ERROR",
                "message": "Invalid input data"
            }
        )
        
        assert error.success is False
        assert error.error["code"] == "VALIDATION_ERROR"
        assert error.error["message"] == "Invalid input data"
    
    def test_health_response(self):
        """Test HealthResponse schema"""
        health = HealthResponse(
            status="healthy",
            version="1.0.0",
            database="connected",
            timestamp=datetime.utcnow()
        )
        
        assert health.status == "healthy"
        assert health.version == "1.0.0"
        assert health.database == "connected"
        assert isinstance(health.timestamp, datetime)


class TestSchemaValidation:
    """Test schema validation rules"""
    
    def test_email_validation(self):
        """Test email field validation"""
        # Valid emails
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk"
        ]
        
        for email in valid_emails:
            user = UserCreate(email=email, password="Password123!")
            assert user.email == email
        
        # Invalid emails
        invalid_emails = [
            "invalid",
            "@example.com",
            "user@",
            "user..name@example.com"
        ]
        
        for email in invalid_emails:
            with pytest.raises(ValidationError):
                UserCreate(email=email, password="Password123!")
    
    def test_password_validation(self):
        """Test password strength validation"""
        # Valid passwords (if we implement password validation)
        valid_passwords = [
            "StrongP@ss123",
            "Complex!Pass456",
            "Secure#Password789"
        ]
        
        for password in valid_passwords:
            user = UserCreate(email="test@example.com", password=password)
            assert user.password == password
        
        # Note: Add password strength validation tests if implemented
    
    def test_json_field_validation(self):
        """Test JSON field validation"""
        # Valid JSON data
        job = AnalysisJobCreate(
            name="Test",
            dataset_id=str(uuid4()),
            config={"key": "value", "nested": {"data": 123}}
        )
        assert job.config["nested"]["data"] == 123
        
        # Should accept any JSON-serializable data
        job = AnalysisJobCreate(
            name="Test",
            dataset_id=str(uuid4()),
            config=[1, 2, 3]  # Lists are valid JSON
        )
        assert job.config == [1, 2, 3]
    
    def test_datetime_serialization(self):
        """Test datetime fields are properly serialized"""
        now = datetime.utcnow()
        
        response = AnalysisJobResponse(
            id=str(uuid4()),
            name="Test",
            status="completed",
            user_id=str(uuid4()),
            dataset_id=str(uuid4()),
            config={},
            created_at=now,
            updated_at=now,
            started_at=now,
            completed_at=now
        )
        
        # Should be able to convert to dict/JSON
        response_dict = response.model_dump()
        assert isinstance(response_dict["created_at"], datetime)
        
        # Should be able to serialize to JSON
        response_json = response.model_dump_json()
        assert isinstance(response_json, str)