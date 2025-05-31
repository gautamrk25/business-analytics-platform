"""SQLAlchemy database models"""
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    Column, String, DateTime, Boolean, Integer, Float, 
    ForeignKey, JSON, UniqueConstraint, Text
)
from sqlalchemy.orm import relationship

from src.models.database import Base


class User(Base):
    """User model for authentication and ownership"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    datasets = relationship("Dataset", back_populates="user", cascade="all, delete-orphan")
    jobs = relationship("AnalysisJob", back_populates="user", cascade="all, delete-orphan")


class Dataset(Base):
    """Dataset model for uploaded data files"""
    __tablename__ = "datasets"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=True)
    row_count = Column(Integer, nullable=True)
    column_count = Column(Integer, nullable=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    meta_data = Column(JSON, default=dict)  # Renamed from metadata to avoid SQLAlchemy reserved word
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="datasets")
    jobs = relationship("AnalysisJob", back_populates="dataset", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='_user_dataset_name_uc'),
    )


class BuildingBlock(Base):
    """Building block registry model"""
    __tablename__ = "building_blocks"
    
    id = Column(String, primary_key=True)  # Unique identifier
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)  # data, analysis, visualization, etc.
    version = Column(String, nullable=False)
    config_schema = Column(JSON, default=dict)  # JSON Schema for configuration
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    results = relationship("JobResult", back_populates="block")


class AnalysisJob(Base):
    """Analysis job model for tracking analysis workflows"""
    __tablename__ = "analysis_jobs"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="pending")  # pending, running, completed, failed
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    dataset_id = Column(String, ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    config = Column(JSON, default=dict)  # Job configuration
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="jobs")
    dataset = relationship("Dataset", back_populates="jobs")
    results = relationship("JobResult", back_populates="job", cascade="all, delete-orphan")


class JobResult(Base):
    """Results from individual building blocks within a job"""
    __tablename__ = "job_results"
    
    id = Column(String, primary_key=True)
    job_id = Column(String, ForeignKey("analysis_jobs.id", ondelete="CASCADE"), nullable=False)
    block_id = Column(String, ForeignKey("building_blocks.id"), nullable=False)
    status = Column(String, nullable=False)  # success, failed, skipped
    result_data = Column(JSON, default=dict)  # Actual results
    error_message = Column(Text, nullable=True)
    execution_time = Column(Float, nullable=True)  # Time in seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job = relationship("AnalysisJob", back_populates="results")
    block = relationship("BuildingBlock", back_populates="results")