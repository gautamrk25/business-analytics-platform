# Building Block System Design - Backend API Architecture (Version 3.0)
# Backend-First Implementation for React Frontend

## IMPORTANT: Backend API Implementation Guidelines

This codebase serves as a backend API for a React frontend. When implementing:

1. **NO Streamlit UI components - Backend API only**
2. **ALL functionality exposed through REST endpoints**
3. **Use FastAPI for the web framework**
4. **Implement WebSocket for real-time updates**
5. **JWT authentication for all protected endpoints**
6. **Follow RESTful naming conventions**
7. **Return JSON responses in standardized format**

## Quick Reference for Backend API Development

### FastAPI Endpoint Template:
```python
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List

router = APIRouter(prefix="/api/v1/blocks", tags=["building-blocks"])

@router.post("/{block_id}/execute")
async def execute_block(
    block_id: str,
    data: Dict[str, Any],
    config: Dict[str, Any] = {},
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Execute a building block via API"""
    try:
        block = registry.get_block(block_id)
        result = await block.execute(data, config)
        return {
            "success": True,
            "data": result,
            "metadata": {
                "block_id": block_id,
                "user_id": current_user.id,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## Executive Summary

This document outlines the design for transforming the Business Analysis Platform into a backend API service that powers a React frontend. The architecture focuses on RESTful endpoints, real-time WebSocket connections, and scalable microservice patterns.

## 1. API Architecture Overview

### 1.1 Core Architecture Principles

- **RESTful Design**: All functionality exposed via REST endpoints
- **Stateless**: No server-side session state
- **JWT Authentication**: Token-based security
- **WebSocket Support**: Real-time updates for long-running operations
- **CORS Enabled**: Cross-origin support for React frontend

### 1.2 Technology Stack

```yaml
backend:
  framework: FastAPI
  language: Python 3.8+
  database: PostgreSQL (production), SQLite (development)
  orm: SQLAlchemy
  cache: Redis (optional)
  queue: Celery (optional)
  
authentication:
  type: JWT
  library: python-jose
  
websocket:
  protocol: WebSocket
  library: FastAPI WebSocket
  
api_documentation:
  type: OpenAPI 3.0
  ui: Swagger UI
```

## 2. API Structure

### 2.1 Base API Configuration

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Business Analysis Platform API",
    version="1.0.0",
    description="Backend API for Business Analysis Platform"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(blocks_router, prefix="/api/v1/blocks")
app.include_router(workflows_router, prefix="/api/v1/workflows")
app.include_router(data_router, prefix="/api/v1/data")
app.include_router(analysis_router, prefix="/api/v1/analysis")
```

### 2.2 Building Block API Endpoints

```python
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, Any, List, Optional

blocks_router = APIRouter(tags=["building-blocks"])

@blocks_router.get("/")
async def list_blocks(
    category: Optional[str] = None,
    version: Optional[str] = None,
    current_user: User = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """List all available building blocks"""
    blocks = registry.list_blocks(category=category, version=version)
    return [block.to_dict() for block in blocks]

@blocks_router.get("/{block_id}")
async def get_block_details(
    block_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get detailed information about a specific block"""
    block = registry.get_block(block_id)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    
    return {
        "id": block.id,
        "name": block.name,
        "version": block.version,
        "category": block.category,
        "description": block.description,
        "input_schema": block.get_input_schema(),
        "output_schema": block.get_output_schema(),
        "metadata": block.metadata
    }

@blocks_router.post("/{block_id}/execute")
async def execute_block(
    block_id: str,
    request: BlockExecutionRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Execute a building block"""
    block = registry.get_block(block_id)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    
    # Create job for tracking
    job_id = create_job(block_id, request.data, current_user.id)
    
    # Execute in background
    background_tasks.add_task(
        execute_block_async,
        job_id,
        block,
        request.data,
        request.config
    )
    
    return {
        "job_id": job_id,
        "status": "started",
        "message": "Block execution started"
    }

@blocks_router.get("/{block_id}/metrics")
async def get_block_metrics(
    block_id: str,
    timeframe: str = "24h",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get performance metrics for a block"""
    return metrics_service.get_block_metrics(block_id, timeframe)
```

### 2.3 Workflow API Endpoints

```python
workflows_router = APIRouter(tags=["workflows"])

@workflows_router.post("/")
async def create_workflow(
    workflow: WorkflowCreate,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Create a new workflow"""
    workflow_id = workflow_service.create_workflow(
        name=workflow.name,
        steps=workflow.steps,
        user_id=current_user.id
    )
    
    return {
        "workflow_id": workflow_id,
        "status": "created",
        "message": "Workflow created successfully"
    }

@workflows_router.post("/{workflow_id}/execute")
async def execute_workflow(
    workflow_id: str,
    data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Execute a workflow"""
    job_id = workflow_service.start_workflow_execution(
        workflow_id,
        data,
        current_user.id
    )
    
    background_tasks.add_task(
        execute_workflow_async,
        job_id,
        workflow_id,
        data
    )
    
    return {
        "job_id": job_id,
        "workflow_id": workflow_id,
        "status": "started"
    }

@workflows_router.get("/{workflow_id}/status")
async def get_workflow_status(
    workflow_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get workflow execution status"""
    status = workflow_service.get_workflow_status(workflow_id)
    return status
```

### 2.4 WebSocket for Real-time Updates

```python
from fastapi import WebSocket
from typing import Dict, Any
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, client_id: str):
        del self.active_connections[client_id]
    
    async def send_update(self, client_id: str, message: Dict[str, Any]):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    await manager.connect(websocket, job_id)
    try:
        while True:
            # Send job updates
            status = job_service.get_job_status(job_id)
            await manager.send_update(job_id, status)
            
            # Wait for next update or client disconnect
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(job_id)
```

## 3. Data Management API

### 3.1 Data Upload Endpoints

```python
data_router = APIRouter(tags=["data"])

@data_router.post("/upload")
async def upload_file(
    file: UploadFile,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Upload a data file"""
    # Validate file type
    if not file.filename.endswith(('.csv', '.xlsx', '.json')):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format"
        )
    
    # Save file and create dataset
    dataset_id = await data_service.save_uploaded_file(
        file,
        current_user.id
    )
    
    # Start profiling in background
    background_tasks.add_task(
        profile_dataset,
        dataset_id
    )
    
    return {
        "dataset_id": dataset_id,
        "filename": file.filename,
        "status": "uploaded",
        "message": "File uploaded successfully"
    }

@data_router.get("/{dataset_id}")
async def get_dataset_info(
    dataset_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get dataset information"""
    dataset = data_service.get_dataset(dataset_id, current_user.id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return dataset.to_dict()

@data_router.get("/{dataset_id}/preview")
async def preview_dataset(
    dataset_id: str,
    rows: int = 10,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Preview dataset contents"""
    preview = data_service.get_preview(dataset_id, rows, current_user.id)
    return {"preview": preview}
```

### 3.2 Analysis API Endpoints

```python
analysis_router = APIRouter(tags=["analysis"])

@analysis_router.post("/")
async def create_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Start a new analysis"""
    # Validate dataset access
    dataset = data_service.get_dataset(request.dataset_id, current_user.id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Create analysis job
    job_id = analysis_service.create_analysis_job(
        dataset_id=request.dataset_id,
        question=request.question,
        template_id=request.template_id,
        user_id=current_user.id
    )
    
    # Start analysis in background
    background_tasks.add_task(
        run_analysis,
        job_id,
        request
    )
    
    return {
        "job_id": job_id,
        "status": "started",
        "websocket_url": f"/ws/{job_id}"
    }

@analysis_router.get("/{job_id}/status")
async def get_analysis_status(
    job_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get analysis job status"""
    status = analysis_service.get_job_status(job_id, current_user.id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return status

@analysis_router.get("/{job_id}/results")
async def get_analysis_results(
    job_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get analysis results"""
    results = analysis_service.get_results(job_id, current_user.id)
    if not results:
        raise HTTPException(status_code=404, detail="Results not found")
    
    return results
```

## 4. Authentication & Authorization

### 4.1 JWT Authentication

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def create_access_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = {
        "sub": user_id,
        "exp": expire
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = user_service.get_user(user_id)
    if user is None:
        raise credentials_exception
    
    return user
```

### 4.2 Role-Based Access Control

```python
from enum import Enum
from functools import wraps

class Role(Enum):
    USER = "user"
    ADMIN = "admin"
    ANALYST = "analyst"

def require_role(role: Role):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if current_user.role != role.value:
                raise HTTPException(
                    status_code=403,
                    detail="Insufficient permissions"
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

@blocks_router.post("/")
@require_role(Role.ADMIN)
async def create_block(
    block: BlockCreate,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Create a new building block (admin only)"""
    # Implementation
    pass
```

## 5. Error Handling

### 5.1 Standardized Error Response

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class BusinessException(Exception):
    def __init__(self, status_code: int, detail: str, error_code: str):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code

@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.detail,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred",
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    )
```

## 6. Database Models

### 6.1 SQLAlchemy Models

```python
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    datasets = relationship("Dataset", back_populates="user")
    analyses = relationship("Analysis", back_populates="user")

class Dataset(Base):
    __tablename__ = "datasets"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="datasets")

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    dataset_id = Column(String, ForeignKey("datasets.id"))
    question = Column(String)
    status = Column(String, default="pending")
    results = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    user = relationship("User", back_populates="analyses")
    dataset = relationship("Dataset")
```

## 7. Deployment Configuration

### 7.1 Docker Configuration

```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 7.2 Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db/dbname
      - JWT_SECRET=${JWT_SECRET}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./uploads:/app/uploads
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:6
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

## 8. Testing

### 8.1 API Testing

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_block():
    response = client.post(
        "/api/v1/blocks/",
        json={
            "name": "test_block",
            "category": "analysis",
            "version": "1.0"
        },
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["success"] == True

def test_execute_block():
    response = client.post(
        "/api/v1/blocks/test_block/execute",
        json={
            "data": {"test": "data"},
            "config": {}
        },
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert "job_id" in response.json()
```

## 9. Performance Optimization

### 9.1 Caching Strategy

```python
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expiration=3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Check cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            redis_client.setex(
                cache_key,
                expiration,
                json.dumps(result)
            )
            
            return result
        return wrapper
    return decorator

@cache_result(expiration=3600)
async def get_expensive_analysis(dataset_id: str):
    # Expensive operation
    pass
```

### 9.2 Database Query Optimization

```python
from sqlalchemy.orm import selectinload

# Eager loading relationships
def get_user_with_datasets(user_id: str):
    return db.query(User)\
        .options(selectinload(User.datasets))\
        .filter(User.id == user_id)\
        .first()

# Pagination
def get_analyses_paginated(user_id: str, page: int = 1, size: int = 10):
    return db.query(Analysis)\
        .filter(Analysis.user_id == user_id)\
        .offset((page - 1) * size)\
        .limit(size)\
        .all()
```

## 10. Monitoring & Logging

### 10.1 Structured Logging

```python
import logging
from pythonjsonlogger import jsonlogger

# Configure JSON logging
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Log API requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        "api_request",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time": process_time,
            "client_host": request.client.host
        }
    )
    
    return response
```

## 11. Best Practices Summary

### 11.1 API Design Principles
- Use consistent naming conventions
- Return standardized response formats
- Implement proper error handling
- Use async/await for all I/O operations
- Document all endpoints with OpenAPI

### 11.2 Security Practices
- Always validate input data
- Use JWT for authentication
- Implement rate limiting
- Sanitize error messages
- Use HTTPS in production

### 11.3 Performance Guidelines
- Cache expensive operations
- Use database indexes
- Implement pagination
- Optimize database queries
- Use background tasks for long operations

This backend API design provides a robust foundation for serving the React frontend while maintaining scalability, security, and performance.