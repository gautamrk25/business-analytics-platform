"""Tests for SQLAlchemy models"""
import pytest
from datetime import datetime
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.models import User, Dataset, AnalysisJob, BuildingBlock, JobResult
from src.models.database import Base


class TestModels:
    """Test suite for all database models"""
    
    @pytest.fixture
    def db_session(self):
        """Create an in-memory SQLite database for testing"""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        
        yield session
        
        session.close()
        Base.metadata.drop_all(engine)
    
    def test_user_model(self, db_session):
        """Test User model creation and attributes"""
        user = User(
            id=str(uuid4()),
            email="test@example.com",
            hashed_password="hashedpassword123",
            is_active=True,
            is_superuser=False
        )
        
        db_session.add(user)
        db_session.commit()
        
        # Query the user back
        queried_user = db_session.query(User).filter_by(email="test@example.com").first()
        
        assert queried_user is not None
        assert queried_user.email == "test@example.com"
        assert queried_user.is_active is True
        assert queried_user.is_superuser is False
        assert isinstance(queried_user.created_at, datetime)
        assert isinstance(queried_user.updated_at, datetime)
    
    def test_dataset_model(self, db_session):
        """Test Dataset model creation and relationships"""
        # Create a user first
        user = User(
            id=str(uuid4()),
            email="test@example.com",
            hashed_password="hashedpassword123"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create a dataset
        dataset = Dataset(
            id=str(uuid4()),
            name="Test Dataset",
            description="A test dataset",
            file_path="data/test.csv",
            file_size=1024,
            row_count=100,
            column_count=5,
            user_id=user.id,
            meta_data={"columns": ["col1", "col2", "col3", "col4", "col5"]}
        )
        
        db_session.add(dataset)
        db_session.commit()
        
        # Query the dataset back
        queried_dataset = db_session.query(Dataset).filter_by(name="Test Dataset").first()
        
        assert queried_dataset is not None
        assert queried_dataset.name == "Test Dataset"
        assert queried_dataset.file_size == 1024
        assert queried_dataset.user_id == user.id
        assert queried_dataset.user.email == "test@example.com"
        assert queried_dataset.meta_data["columns"][0] == "col1"
    
    def test_building_block_model(self, db_session):
        """Test BuildingBlock model"""
        block = BuildingBlock(
            id="data_validation_block",
            name="Data Validation Block",
            description="Validates data quality",
            category="data",
            version="1.0.0",
            config_schema={
                "type": "object",
                "properties": {
                    "threshold": {"type": "number"}
                }
            },
            is_active=True
        )
        
        db_session.add(block)
        db_session.commit()
        
        # Query the block back
        queried_block = db_session.query(BuildingBlock).filter_by(id="data_validation_block").first()
        
        assert queried_block is not None
        assert queried_block.name == "Data Validation Block"
        assert queried_block.category == "data"
        assert queried_block.version == "1.0.0"
        assert queried_block.is_active is True
        assert queried_block.config_schema["properties"]["threshold"]["type"] == "number"
    
    def test_analysis_job_model(self, db_session):
        """Test AnalysisJob model and relationships"""
        # Create dependencies
        user = User(
            id=str(uuid4()),
            email="test@example.com", 
            hashed_password="hashedpassword123"
        )
        
        dataset = Dataset(
            id=str(uuid4()),
            name="Test Dataset",
            file_path="data/test.csv",
            user_id=user.id
        )
        
        db_session.add_all([user, dataset])
        db_session.commit()
        
        # Create analysis job
        job = AnalysisJob(
            id=str(uuid4()),
            name="Test Analysis",
            description="Test analysis job",
            status="pending",
            user_id=user.id,
            dataset_id=dataset.id,
            config={
                "blocks": ["data_validation", "statistical_analysis"],
                "parameters": {"threshold": 0.95}
            }
        )
        
        db_session.add(job)
        db_session.commit()
        
        # Query the job back
        queried_job = db_session.query(AnalysisJob).filter_by(name="Test Analysis").first()
        
        assert queried_job is not None
        assert queried_job.status == "pending"
        assert queried_job.user.email == "test@example.com"
        assert queried_job.dataset.name == "Test Dataset"
        assert queried_job.config["blocks"][0] == "data_validation"
        assert queried_job.started_at is None
        assert queried_job.completed_at is None
    
    def test_job_result_model(self, db_session):
        """Test JobResult model"""
        # Create dependencies
        user = User(
            id=str(uuid4()),
            email="test@example.com",
            hashed_password="hashedpassword123"
        )
        
        dataset = Dataset(
            id=str(uuid4()),
            name="Test Dataset", 
            file_path="data/test.csv",
            user_id=user.id
        )
        
        job = AnalysisJob(
            id=str(uuid4()),
            name="Test Analysis",
            status="running",
            user_id=user.id,
            dataset_id=dataset.id
        )
        
        block = BuildingBlock(
            id="test_block",
            name="Test Block",
            category="test",
            version="1.0.0"
        )
        
        db_session.add_all([user, dataset, job, block])
        db_session.commit()
        
        # Create job result
        result = JobResult(
            id=str(uuid4()),
            job_id=job.id,
            block_id=block.id,
            status="success",
            result_data={
                "metrics": {"accuracy": 0.95},
                "charts": ["chart1.png", "chart2.png"]
            },
            error_message=None,
            execution_time=1.5
        )
        
        db_session.add(result)
        db_session.commit()
        
        # Query the result back
        queried_result = db_session.query(JobResult).filter_by(job_id=job.id).first()
        
        assert queried_result is not None
        assert queried_result.status == "success"
        assert queried_result.execution_time == 1.5
        assert queried_result.result_data["metrics"]["accuracy"] == 0.95
        assert queried_result.job.name == "Test Analysis"
        assert queried_result.block.name == "Test Block"
    
    def test_model_relationships(self, db_session):
        """Test relationships between models"""
        # Create a user
        user = User(
            id=str(uuid4()),
            email="test@example.com",
            hashed_password="hashedpassword123"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create multiple datasets for the user
        dataset1 = Dataset(
            id=str(uuid4()),
            name="Dataset 1",
            file_path="data/test1.csv",
            user_id=user.id
        )
        
        dataset2 = Dataset(
            id=str(uuid4()),
            name="Dataset 2", 
            file_path="data/test2.csv",
            user_id=user.id
        )
        
        db_session.add_all([dataset1, dataset2])
        db_session.commit()
        
        # Create analysis jobs
        job1 = AnalysisJob(
            id=str(uuid4()),
            name="Analysis 1",
            status="completed",
            user_id=user.id,
            dataset_id=dataset1.id
        )
        
        job2 = AnalysisJob(
            id=str(uuid4()),
            name="Analysis 2",
            status="pending",
            user_id=user.id,
            dataset_id=dataset2.id
        )
        
        db_session.add_all([job1, job2])
        db_session.commit()
        
        # Test relationships
        queried_user = db_session.query(User).filter_by(email="test@example.com").first()
        
        # User should have 2 datasets
        assert len(queried_user.datasets) == 2
        assert queried_user.datasets[0].name in ["Dataset 1", "Dataset 2"]
        
        # User should have 2 jobs
        assert len(queried_user.jobs) == 2
        assert queried_user.jobs[0].name in ["Analysis 1", "Analysis 2"]
        
        # Dataset should reference back to user
        assert dataset1.user.email == "test@example.com"
        
        # Job should reference both user and dataset
        assert job1.user.email == "test@example.com"
        assert job1.dataset.name == "Dataset 1"
    
    def test_model_constraints(self, db_session):
        """Test model constraints and validations"""
        # Test unique email constraint
        user1 = User(
            id=str(uuid4()),
            email="unique@example.com",
            hashed_password="password123"
        )
        db_session.add(user1)
        db_session.commit()
        
        # Try to create another user with same email
        user2 = User(
            id=str(uuid4()),
            email="unique@example.com",
            hashed_password="password456"
        )
        db_session.add(user2)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()
        
        db_session.rollback()
        
        # Test dataset name uniqueness per user
        dataset1 = Dataset(
            id=str(uuid4()),
            name="My Dataset",
            file_path="data/test1.csv",
            user_id=user1.id
        )
        db_session.add(dataset1)
        db_session.commit()
        
        # Same name, same user - should fail
        dataset2 = Dataset(
            id=str(uuid4()),
            name="My Dataset",
            file_path="data/test2.csv",
            user_id=user1.id
        )
        db_session.add(dataset2)
        
        with pytest.raises(Exception):
            db_session.commit()
        
        db_session.rollback()
        
        # Same name, different user - should succeed
        user3 = User(
            id=str(uuid4()),
            email="other@example.com",
            hashed_password="password789"
        )
        db_session.add(user3)
        db_session.commit()
        
        dataset3 = Dataset(
            id=str(uuid4()),
            name="My Dataset",
            file_path="data/test3.csv",
            user_id=user3.id
        )
        db_session.add(dataset3)
        db_session.commit()  # Should succeed
    
    def test_cascade_delete(self, db_session):
        """Test cascade delete behavior"""
        # Create user with related data
        user = User(
            id=str(uuid4()),
            email="cascade@example.com",
            hashed_password="password123"
        )
        
        dataset = Dataset(
            id=str(uuid4()),
            name="Cascade Dataset",
            file_path="data/cascade.csv",
            user_id=user.id
        )
        
        job = AnalysisJob(
            id=str(uuid4()),
            name="Cascade Job",
            status="completed",
            user_id=user.id,
            dataset_id=dataset.id
        )
        
        db_session.add_all([user, dataset, job])
        db_session.commit()
        
        # Delete the user
        db_session.delete(user)
        db_session.commit()
        
        # Related data should be deleted
        assert db_session.query(Dataset).filter_by(id=dataset.id).first() is None
        assert db_session.query(AnalysisJob).filter_by(id=job.id).first() is None