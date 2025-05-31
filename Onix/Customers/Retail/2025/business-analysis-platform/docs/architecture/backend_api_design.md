# Backend API Design for Business Analysis Platform

## Overview

This document defines the REST API interface for the Business Analysis Platform backend. The API is designed to be consumed by a React frontend application. All Streamlit code will be deprecated and removed.

## Architecture Changes

### Before (Current)
- Monolithic Python application with Streamlit UI
- Direct function calls between UI and business logic
- Session-based state management

### After (Target)
- Backend: Python REST API (FastAPI/Flask)
- Frontend: React application (separate repository)
- API-based communication
- Stateless requests with JWT authentication

## API Endpoints

### 1. Health Check
```
GET /api/v1/health
```
**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 2. Authentication
```
POST /api/v1/auth/login
```
**Request**:
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```
**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "123",
    "email": "user@example.com",
    "organization": "ACME Corp"
  }
}
```

### 3. Data Upload
```
POST /api/v1/data/upload
Content-Type: multipart/form-data
Authorization: Bearer {token}
```
**Request**:
- File: CSV or Excel file
- Form data: 
  - `dataset_name`: String
  - `description`: String (optional)

**Response**:
```json
{
  "dataset_id": "ds_123abc",
  "filename": "sales_data.csv",
  "columns": ["date", "sales", "inventory", "region"],
  "row_count": 1000,
  "upload_timestamp": "2024-01-15T10:30:00Z",
  "preview": [
    {"date": "2024-01-01", "sales": 5000, "inventory": 100, "region": "North"}
  ]
}
```

### 4. Get Sample Datasets
```
GET /api/v1/data/samples
Authorization: Bearer {token}
```
**Response**:
```json
{
  "sample_datasets": [
    {
      "id": "sample_retail",
      "name": "Retail Sales",
      "description": "Sample retail sales data",
      "columns": ["date", "sales", "inventory", "foot_traffic"],
      "row_count": 30,
      "industry": "retail"
    },
    {
      "id": "sample_marketing",
      "name": "Marketing Campaign",
      "description": "Sample marketing campaign data",
      "columns": ["campaign", "spend", "impressions", "clicks"],
      "row_count": 10,
      "industry": "marketing"
    }
  ]
}
```

### 5. Load Sample Dataset
```
POST /api/v1/data/load-sample
Authorization: Bearer {token}
```
**Request**:
```json
{
  "sample_id": "sample_retail"
}
```
**Response**: Same as data upload response

### 6. List Templates
```
GET /api/v1/templates
Authorization: Bearer {token}
```
**Query Parameters**:
- `department`: string (optional)
- `industry`: string (optional)

**Response**:
```json
{
  "templates": [
    {
      "id": "marketing_campaign_analyzer",
      "name": "Marketing Campaign Analyzer",
      "description": "Analyzes campaign performance and ROI",
      "department": "marketing",
      "industry_tags": ["all"],
      "required_columns": ["spend", "impressions", "clicks"],
      "sample_question": "How are our marketing campaigns performing?"
    }
  ]
}
```

### 7. Validate Template Compatibility
```
POST /api/v1/templates/validate
Authorization: Bearer {token}
```
**Request**:
```json
{
  "template_id": "marketing_campaign_analyzer",
  "dataset_id": "ds_123abc"
}
```
**Response**:
```json
{
  "compatible": true,
  "compatibility_score": 0.95,
  "missing_columns": [],
  "optional_columns_available": ["revenue"],
  "column_mappings": {
    "campaign_spend": "spend"
  }
}
```

### 8. Analyze Data
```
POST /api/v1/analyze
Authorization: Bearer {token}
```
**Request**:
```json
{
  "dataset_id": "ds_123abc",
  "question": "What are the sales trends over time?",
  "template_id": "retail_sales_analyzer",  // optional
  "options": {
    "use_self_correction": true,
    "use_knowledge_base": true,
    "auto_suggest_templates": true
  }
}
```
**Response**:
```json
{
  "analysis_id": "an_456def",
  "status": "completed",
  "results": {
    "success": true,
    "insights": [
      "Sales show 15% growth trend over the period",
      "North region performs 25% better than average",
      "Inventory turnover is below industry benchmark"
    ],
    "recommendations": [
      "Monitor inventory levels to prevent stockouts",
      "Focus marketing efforts on peak sales periods"
    ],
    "industry": "retail",
    "analysis_type": "trend",
    "kpis": {
      "inventory_turnover": {
        "value": 5.2,
        "formatted": "5.2x",
        "status": "warning",
        "benchmark": "6.0x"
      }
    },
    "charts": [
      {
        "type": "line",
        "title": "Sales Trend",
        "data": {...}
      }
    ]
  },
  "execution_time": 2.5,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 9. Get Analysis History
```
GET /api/v1/analyses
Authorization: Bearer {token}
```
**Query Parameters**:
- `limit`: number (default: 10)
- `offset`: number (default: 0)
- `dataset_id`: string (optional)

**Response**:
```json
{
  "analyses": [
    {
      "analysis_id": "an_456def",
      "dataset_id": "ds_123abc",
      "question": "What are the sales trends?",
      "template_used": "retail_sales_analyzer",
      "status": "completed",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 25,
  "limit": 10,
  "offset": 0
}
```

### 10. Get Analysis Details
```
GET /api/v1/analyses/{analysis_id}
Authorization: Bearer {token}
```
**Response**: Same as analyze endpoint response

### 11. Export Analysis
```
GET /api/v1/analyses/{analysis_id}/export
Authorization: Bearer {token}
```
**Query Parameters**:
- `format`: "pdf" | "excel" | "json"

**Response**: File download

### 12. WebSocket for Real-time Updates
```
WS /api/v1/ws/analysis/{analysis_id}
Authorization: Bearer {token}
```
**Messages**:
```json
{
  "type": "progress",
  "step": "data_validation",
  "progress": 0.25,
  "message": "Validating data quality..."
}
```

## Error Responses

All errors follow this format:
```json
{
  "error": {
    "code": "INVALID_DATA",
    "message": "The uploaded file is not a valid CSV",
    "details": {
      "line": 5,
      "column": "sales",
      "reason": "Invalid numeric value"
    }
  },
  "request_id": "req_789ghi"
}
```

## Rate Limiting

- 100 requests per minute per user
- 10 concurrent analyses per organization
- 1GB max file upload size

## Implementation Notes

### Backend Framework
Use FastAPI for the backend because:
- Native async support
- Automatic API documentation
- Type validation
- WebSocket support

### Request/Response Models
```python
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AnalysisRequest(BaseModel):
    dataset_id: str
    question: str
    template_id: Optional[str] = None
    options: Optional[Dict[str, Any]] = None

class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    results: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
```

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Authentication Middleware
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # Verify JWT token
    return user_id
```

## Migration Plan

1. **Phase 1**: Create API endpoints alongside Streamlit
2. **Phase 2**: Test API with Postman/Insomnia
3. **Phase 3**: Build React frontend
4. **Phase 4**: Deprecate and remove Streamlit code

## Frontend Integration Guidelines

### React Service Layer
```javascript
class AnalysisService {
  async uploadData(file) {
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch('/api/v1/data/upload', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
      body: formData
    });
    return response.json();
  }

  async analyze(datasetId, question, templateId = null) {
    const response = await fetch('/api/v1/analyze', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        dataset_id: datasetId,
        question,
        template_id: templateId
      })
    });
    return response.json();
  }
}
```

### WebSocket Integration
```javascript
const ws = new WebSocket(`ws://localhost:8000/api/v1/ws/analysis/${analysisId}`);
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateProgress(data.progress, data.message);
};
```

## Security Considerations

1. **Authentication**: JWT tokens with refresh tokens
2. **Authorization**: Role-based access control
3. **Data Isolation**: Multi-tenant data separation
4. **Input Validation**: Strict input validation
5. **Rate Limiting**: Prevent abuse
6. **HTTPS**: Enforce TLS in production

This API design provides a clean separation between frontend and backend, enabling independent development and deployment of both components.