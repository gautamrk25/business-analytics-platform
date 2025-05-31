# Business Analysis Platform - Backend API Instructions for Claude Code

## CRITICAL: Backend API Implementation Only

## ⚠️ MANDATORY: Always Follow DEVELOPMENT_WORKFLOW.md

Before implementing ANY feature:
1. Read DEVELOPMENT_WORKFLOW.md for the exact sequence
2. Check PROJECT_STATUS.md for current task
3. Follow the workflow WITHOUT exception

**IMPORTANT**: This codebase is being transformed from a Streamlit application to a backend API that serves a React frontend. The frontend will be implemented separately. This codebase contains ONLY the backend API.

## Overview
This document provides essential context for implementing the Business Analysis Platform as a backend API service using FastAPI.

## Bash Commands
- `python -m venv venv`: Create virtual environment
- `source venv/bin/activate`: Activate virtual environment (macOS/Linux)
- `venv\Scripts\activate`: Activate virtual environment (Windows)
- `pip install -r requirements.txt`: Install dependencies
- `uvicorn main:app --reload`: Run the FastAPI application in development
- `uvicorn main:app --host 0.0.0.0 --port 8000`: Run in production
- `python -m pytest tests/`: Run all tests
- `python -m pytest tests/test_api/`: Run API tests
- `python -m pytest --cov=src --cov-report=html`: Run tests with coverage

## Core Files & API Structure
- `main.py`: FastAPI application entry point with API routes
- `src/api/`: API route definitions (blocks, data, analysis, templates)
  - `blocks.py`: Building block endpoints (currently using mock data)
  - `data.py`: Data management endpoints (placeholder)
  - `analysis.py`: Analysis endpoints (placeholder)
  - `templates.py`: Template endpoints (placeholder)
- `src/models/`: Database models and Pydantic schemas
  - `models.py`: SQLAlchemy ORM models
  - `schemas.py`: Pydantic request/response models
  - `database.py`: Database setup and session management
- `src/building_blocks/`: Analysis modules
  - `base.py`: Abstract base class for all building blocks
  - `registry.py`: Registry for managing building blocks
  - `data/data_validator.py`: Data validation building block
  - `data/smart_data_profiler.py`: Smart data profiling block
- `src/agents/`: AI agent implementations
  - `industry_detective.py`: Industry classification agent
  - `code_inspector.py`: Code error analysis agent
- `src/utils/`: Utility modules
  - `config.py`: ConfigManager for configuration management
  - `logger.py`: Centralized logging setup

## Code Style Guidelines
### IMPORTANT: Always follow these patterns
- Use type hints for ALL parameters and return values
- Include comprehensive docstrings with Args and Returns sections
- Handle exceptions with try/except blocks and log all errors
- Use abc.ABC and @abstractmethod for abstract base classes
- Return results as dictionaries matching format: `{success: bool, data: any, errors: []}`

### Python Conventions
- Follow PEP 8 style guide
- Use descriptive variable names (no single letters except for loop counters)
- Keep functions focused and under 20 lines when possible
- Use asyncio for asynchronous operations (always use await properly)

## Testing Instructions
### IMPORTANT: Test-Driven Development (TDD) Workflow
**YOU MUST follow this workflow for all new code:**
1. **Write tests FIRST** before implementing any functionality
2. **Run tests** to ensure they fail (Red phase)
3. **Implement code** to make tests pass (Green phase)
4. **Refactor** while keeping tests green
5. **Never proceed** without passing tests

**Refer to TDD_CHECKLIST.md for the complete workflow checklist**

### Running Tests
1. Activate virtual environment: `source venv/bin/activate`
2. Run all tests: `python -m pytest tests/ -v`
3. Run specific test: `python -m pytest tests/test_building_blocks.py -v`
4. Run with coverage: `python -m pytest tests/ --cov=src --cov-report=html`
5. Run tests continuously: `python -m pytest tests/ --watch`

### Writing Tests
- **Test Structure**: Place tests in `tests/` directory mirroring source structure
- **Naming Convention**: `test_<module_name>.py` for test files
- **Test Classes**: `TestClassName` for grouping related tests
- **Test Methods**: `test_<specific_behavior>` for individual tests

### Test Requirements for Building Blocks
```python
# Example test structure for a new building block
class TestMyBuildingBlock:
    def test_initialization(self):
        """Test block can be initialized with required properties"""
        pass
    
    def test_execute_with_valid_data(self):
        """Test successful execution with valid input"""
        pass
    
    def test_execute_with_invalid_data(self):
        """Test proper error handling with invalid input"""
        pass
    
    def test_validate_input(self):
        """Test input validation catches all error cases"""
        pass
    
    def test_config_schema(self):
        """Test config schema is properly defined"""
        pass
```

### Test Coverage Requirements
- **Minimum 80% code coverage** for all new code
- **100% coverage** for critical paths (execute, validate_input)
- **Test all edge cases** and error conditions
- **Mock external dependencies** using pytest-mock

## Repository Etiquette
### Git Workflow
- Branch naming: `feature/description` or `fix/issue-description`
- Commit messages: Clear, concise, present tense (e.g., "Add data validation block")
- Always run tests before committing
- Create PR with descriptive title and testing checklist
- Never commit secrets or API keys

### File Structure
```
business-analysis-platform/
├── main.py                         # FastAPI application entry
├── config.yaml                     # Configuration
├── requirements.txt                # Dependencies
├── CLAUDE.md                       # This file
├── setup.py                        # Package setup
├── docker-compose.yml              # Docker orchestration
├── Dockerfile                      # Container definition
├── src/                           # Source code modules
│   ├── __init__.py
│   ├── api/                       # API routes
│   │   ├── __init__.py
│   │   ├── auth.py                # Authentication endpoints
│   │   ├── blocks.py              # Building block endpoints
│   │   ├── data.py                # Data management endpoints
│   │   ├── analysis.py            # Analysis endpoints
│   │   └── templates.py           # Template endpoints
│   ├── models/                    # Database models & schemas
│   │   ├── __init__.py
│   │   ├── database.py            # SQLAlchemy setup
│   │   ├── schemas.py             # Pydantic models
│   │   └── models.py              # ORM models
│   ├── services/                  # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py        # Authentication logic
│   │   ├── analysis_service.py    # Analysis orchestration
│   │   └── data_service.py        # Data management
│   ├── middleware/                # API middleware
│   │   ├── __init__.py
│   │   ├── auth.py                # JWT middleware
│   │   └── cors.py                # CORS configuration
│   ├── building_blocks/           # Building block implementations
│   │   ├── __init__.py
│   │   ├── base.py                # Abstract base classes
│   │   ├── data/                  # Data processing blocks
│   │   ├── analysis/              # Analysis blocks
│   │   └── reporting/             # Report generation blocks
│   ├── utils/                     # Utility functions
│   └── websocket/                 # WebSocket handlers
└── tests/                         # Test directory
    ├── __init__.py
    ├── conftest.py                # Pytest configuration
    ├── test_api/                  # API endpoint tests
    ├── test_services/             # Service layer tests
    ├── test_building_blocks/      # Building block tests
    └── fixtures/                  # Test data and fixtures
```

## Developer Environment Setup
### Prerequisites
- Python 3.9 or higher
- pip package manager
- Virtual environment support

### Initial Setup
1. Clone repository
2. Create virtual environment: `python -m venv venv`
3. Activate environment
4. Install dependencies: `pip install -r requirements.txt`
5. Run tests to verify setup

## Unexpected Behaviors & Warnings
- **Data Validation**: Auto-fix feature may modify input data - always log changes
- **Async Operations**: All building blocks must properly handle async/await
- **Large Datasets**: Performance may degrade with >10MB data files
- **Template Inheritance**: Child templates override parent configurations completely

## Implementation Rules - Backend API
### IMPORTANT: YOU MUST follow these patterns

1. **Remove ALL Streamlit Code**
   - No `import streamlit as st`
   - No UI components in Python
   - Convert all UI logic to API endpoints

2. **FastAPI Structure**
   ```python
   from fastapi import FastAPI, APIRouter, Depends, HTTPException
   from fastapi.middleware.cors import CORSMiddleware
   
   app = FastAPI(title="Business Analysis Platform API")
   
   # CORS for React frontend
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. **Standard API Response Format**
   ```python
   {
       "success": true,
       "data": {...},
       "error": null,
       "metadata": {
           "timestamp": "2024-01-01T00:00:00Z",
           "request_id": "uuid",
           "version": "1.0"
       }
   }
   ```

4. **Building Block API Access**
   ```python
   @router.post("/blocks/{block_id}/execute")
   async def execute_block(
       block_id: str,
       request: BlockExecutionRequest
   ):
       block = registry.get_block(block_id)
       result = await block.execute(request.data, request.config)
       return {"success": True, "data": result}
   ```

6. **WebSocket for Real-time Updates**
   ```python
   @app.websocket("/ws/{job_id}")
   async def websocket_endpoint(websocket: WebSocket, job_id: str):
       await manager.connect(websocket, job_id)
       # Send real-time analysis updates
   ```

7. **Error Handling**
   ```python
   from fastapi.responses import JSONResponse
   
   @app.exception_handler(BusinessException)
   async def business_exception_handler(request: Request, exc: BusinessException):
       return JSONResponse(
           status_code=exc.status_code,
           content={
               "success": False,
               "error": {
                   "code": exc.error_code,
                   "message": exc.detail
               }
           }
       )
   ```

8. **Database Models with SQLAlchemy**
   ```python
   from sqlalchemy import Column, String, DateTime
   from sqlalchemy.ext.declarative import declarative_base
   
   Base = declarative_base()
   
   class User(Base):
       __tablename__ = "users"
       id = Column(String, primary_key=True)
       email = Column(String, unique=True)
       created_at = Column(DateTime)
   ```

9. **API Documentation**
   - All endpoints must have OpenAPI documentation
   - Use Pydantic models for request/response validation
   - Include examples in docstrings

10. **Testing API Endpoints**
    ```python
    from fastapi.testclient import TestClient
    
    def test_execute_block():
        response = client.post(
            "/api/v1/blocks/test_block/execute",
            json={"data": {"test": "data"}}
        )
        assert response.status_code == 200
    ```

## Building Block Architecture - API Integration
### Core Principles
- Each block inherits from abstract BuildingBlock class
- Blocks validate input data before processing
- All blocks accessible via REST API endpoints
- Execution results follow standardized JSON format
- Registry exposes blocks through API discovery endpoint

### API Endpoints for Building Blocks
```python
# List all available blocks
GET /api/v1/blocks

# Get block details and schema
GET /api/v1/blocks/{block_id}

# Execute a block
POST /api/v1/blocks/{block_id}/execute
{
    "data": {...},
    "config": {...}
}

# Get block execution metrics
GET /api/v1/blocks/{block_id}/metrics
```

### Creating New Building Blocks - Backend API Workflow
1. **Create API test first**: `tests/test_api/test_blocks/<block_name>_api.py`
2. **Write API endpoint tests** for the new block
3. **Create block test**: `tests/test_building_blocks/test_<block_name>.py`
4. **Create building block** in `src/building_blocks/<category>/<block_name>.py`
5. **Register block** in the API registry
6. **Implement API endpoint** in `src/api/blocks.py`
7. **Test via API**: Ensure block works through REST interface
8. **Update OpenAPI docs** with block schema and examples
9. **Add to API documentation**

### Example API Test
```python
def test_new_block_api(client):
    response = client.post(
        "/api/v1/blocks/new_block/execute",
        json={
            "data": {"input": "test"},
            "config": {}
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] == True
```

## Working with Templates
- Templates are pre-configured analysis workflows
- Stored in JSON format with metadata
- Support inheritance for common patterns
- Must include name, description, and validation rules

## Performance Considerations
- Use caching for repeated operations
- Batch process data when possible
- Implement timeout handling for long operations
- Monitor memory usage with large datasets

## Debug & Troubleshooting
### Common Issues
- Import errors: Check virtual environment activation
- Async errors: Ensure proper await usage
- Config errors: Verify YAML syntax in config.yaml
- Template errors: Validate JSON format

### Debugging Tools
- Use logger for detailed output
- Enable debug mode in config.yaml
- Check execution_metadata in results
- Review workflow_summary for step details

## Quick Reference
### Common API Patterns
```python
# FastAPI endpoint pattern
@router.post("/endpoint")
async def endpoint_handler(
    request: RequestModel
) -> ResponseModel:
    try:
        result = await service.process(request)
        return ResponseModel(success=True, data=result)
    except BusinessException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

# Building block API result
return {
    "success": True,
    "data": processed_data,
    "errors": [],
    "metadata": {
        "execution_time": time_elapsed,
        "block_version": "1.0",
        "timestamp": datetime.utcnow().isoformat()
    }
}

# WebSocket update pattern
async def send_progress_update(websocket: WebSocket, progress: float):
    await websocket.send_json({
        "type": "progress",
        "data": {
            "progress": progress,
            "message": f"Processing: {progress:.0%} complete"
        }
    })

# Basic route pattern
@router.get("/status")
async def get_status():
    return {"status": "active", "version": "1.0.0"}
```

## API Endpoints to Implement

### Health Check (`/api/v1`)
- `GET /health` - API health status
- `GET /version` - API version information

### Data Management (`/api/v1/data`)
- `POST /upload` - Upload CSV/Excel file
- `GET /{dataset_id}` - Get dataset info
- `GET /{dataset_id}/preview` - Preview data
- `DELETE /{dataset_id}` - Delete dataset

### Building Blocks (`/api/v1/blocks`)
- `GET /` - List all blocks
- `GET /{block_id}` - Get block details
- `POST /{block_id}/execute` - Execute block
- `GET /{block_id}/metrics` - Get metrics

### Analysis (`/api/v1/analysis`)
- `POST /` - Start analysis
- `GET /{job_id}` - Get job status
- `GET /{job_id}/results` - Get results
- `DELETE /{job_id}` - Cancel job

### Templates (`/api/v1/templates`)
- `GET /` - List templates
- `GET /{template_id}` - Get template
- `POST /` - Create template
- `PUT /{template_id}` - Update template
- `DELETE /{template_id}` - Delete template

### WebSocket Endpoints
- `/ws/{job_id}` - Real-time job updates
- `/ws/notifications` - System notifications

## AI Agent Implementation Patterns

### Agent Structure Pattern
```python
class IndustryDetective:
    def __init__(self):
        self.patterns = {
            "retail": ["sales", "inventory", "customer"],
            "saas": ["subscription", "churn", "mrr"],
        }
    
    async def detect_industry(self, columns: List[str], question: str) -> Dict[str, Any]:
        """Detect industry with confidence score"""
        # Pattern matching logic
        return {"industry": "retail", "confidence": 0.92}
```

### Error Recovery Pattern
```python
class CodeInspector:
    async def analyze_error(self, error: Exception, context: Dict) -> Dict[str, Any]:
        """Analyze error and suggest fix"""
        if "column not found" in str(error):
            # Fuzzy match to find similar column
            suggestion = self.find_similar_column(error.column, context.columns)
            return {"fix": f"use '{suggestion}' instead"}
```

### Orchestration Pattern
```python
class AnalysisOrchestrator:
    async def orchestrate_analysis(self, data: pd.DataFrame, question: str):
        # 1. Detect industry
        industry = await self.industry_detective.detect(data.columns, question)
        
        # 2. Execute with progress
        async with self.execution_manager.track_progress() as progress:
            result = await self.business_agent.analyze(data, question, industry)
            
        # 3. Handle errors
        if result.get("error"):
            fix = await self.code_inspector.analyze_error(result["error"])
            result = await self.retry_with_fix(fix)
            
        # 4. Store in memory
        await self.memory_keeper.store(question, result)
        
        return result
```

## Additional Resources
- Backend API Design: `backend_api_design.md`
- API Implementation Guide: `building_block_system_design_backend_api.md`
- AI Agents Architecture: `AI_AGENTS_IMPLEMENTATION.md`