"""Pydantic schemas for request/response validation"""
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic.types import constr


# Common schemas
class StandardResponse(BaseModel):
    """Standard API response format"""
    success: bool
    data: Any
    errors: List[str] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    """Error response format"""
    success: bool = False
    error: Dict[str, str]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    database: str
    timestamp: datetime


# User schemas
class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    """User schema with database fields"""
    id: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):
    """User response schema (no password)"""
    id: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Dataset schemas
class DatasetBase(BaseModel):
    """Base dataset schema"""
    name: str
    description: Optional[str] = None


class DatasetCreate(DatasetBase):
    """Schema for creating a dataset"""
    file_path: str


class DatasetUpdate(BaseModel):
    """Schema for updating a dataset"""
    name: Optional[str] = None
    description: Optional[str] = None


class DatasetInDB(DatasetBase):
    """Dataset schema with database fields"""
    id: str
    file_path: str
    file_size: Optional[int] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    user_id: str
    meta_data: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class DatasetResponse(DatasetInDB):
    """Dataset response schema"""
    pass


# Building Block schemas
class BuildingBlockBase(BaseModel):
    """Base building block schema"""
    name: str
    description: Optional[str] = None
    category: str
    version: str


class BuildingBlockResponse(BaseModel):
    """Building block response schema"""
    id: str
    name: str
    description: Optional[str] = None
    category: str
    version: str
    config_schema: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)


class BlockExecutionRequest(BaseModel):
    """Request schema for executing a building block"""
    data: Dict[str, Any]
    config: Dict[str, Any] = Field(default_factory=dict)


# Analysis Job schemas
class AnalysisJobCreate(BaseModel):
    """Schema for creating an analysis job"""
    name: str
    description: Optional[str] = None
    dataset_id: str
    config: Union[Dict[str, Any], List[Any]]


class AnalysisJobUpdate(BaseModel):
    """Schema for updating an analysis job"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class AnalysisJobResponse(BaseModel):
    """Analysis job response schema"""
    id: str
    name: str
    description: Optional[str] = None
    status: str
    user_id: str
    dataset_id: str
    config: Union[Dict[str, Any], List[Any]]
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class JobResultResponse(BaseModel):
    """Job result response schema"""
    id: str
    job_id: str
    block_id: str
    status: str
    result_data: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)