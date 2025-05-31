# AI Agents Implementation Plan for Business Analysis Platform

## Overview
This document outlines the implementation of the AI agent system for the Business Analysis Platform backend API. These agents work together to provide intelligent business analysis with industry-specific insights.

## Agent Architecture

### 1. Industry Detective Agent 🕵️
**Location**: `src/agents/industry_detective.py`
**Purpose**: Automatically detects business type from data patterns

```python
class IndustryDetective:
    """Detects industry type based on data columns and question context"""
    
    def detect_industry(self, question: str, data_columns: List[str]) -> Dict[str, Any]:
        """Returns industry type with confidence score"""
        # Analyzes column names and question keywords
        # Returns: {
        #   "industry": "retail",
        #   "confidence": 0.85,
        #   "indicators": ["sales", "inventory", "customer_satisfaction"]
        # }
```

**API Endpoint**: `POST /api/v1/analysis/detect-industry`

### 2. Execution Manager Agent ⚡
**Location**: `src/agents/execution_manager.py`
**Purpose**: Manages analysis execution with timeouts and progress tracking

```python
class ExecutionManager:
    """Manages analysis tasks with progress tracking and timeouts"""
    
    async def execute_with_progress(self, task: Callable, timeout: int = 300) -> Dict[str, Any]:
        """Executes task with real-time progress updates via WebSocket"""
        # Tracks progress and sends updates
        # Implements timeout handling
        # Returns execution results or timeout error
```

**WebSocket**: `WS /ws/analysis/{job_id}`

### 3. Code Inspector Agent 🔍
**Location**: `src/agents/code_inspector.py`
**Purpose**: Analyzes errors and suggests corrections

```python
class CodeInspector:
    """Analyzes errors and suggests fixes based on history"""
    
    def analyze_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Returns error analysis with fix suggestions"""
        # Categorizes error type
        # Searches history for similar errors
        # Suggests fixes based on past solutions
```

### 4. Business Analysis Agent 🧠
**Location**: `src/agents/business_analysis.py`
**Purpose**: Core analysis engine with industry-specific insights

```python
class BusinessAnalysisAgent:
    """Performs business analysis with self-correction"""
    
    async def analyze_with_retry(self, data: pd.DataFrame, question: str, industry: str) -> Dict[str, Any]:
        """Analyzes data with automatic retry on failure"""
        # Applies industry-specific analysis
        # Implements self-correction on errors
        # Generates insights and recommendations
```

**API Endpoint**: `POST /api/v1/analysis/analyze`

### 5. Memory Keeper Agent 📚
**Location**: `src/agents/memory_keeper.py`
**Purpose**: Tracks analysis history and patterns

```python
class MemoryKeeper:
    """Stores and retrieves analysis history"""
    
    def store_analysis(self, analysis: Dict[str, Any]) -> None:
        """Stores analysis results with metadata"""
        
    def get_similar_analyses(self, question: str) -> List[Dict[str, Any]]:
        """Retrieves similar past analyses"""
```

### 6. Orchestrator Agent 🎼
**Location**: `src/agents/orchestrator.py`
**Purpose**: Coordinates all agents for seamless analysis

```python
class AnalysisOrchestrator:
    """Orchestrates the entire analysis workflow"""
    
    async def orchestrate_analysis(self, data: pd.DataFrame, question: str) -> Dict[str, Any]:
        """Coordinates all agents to complete analysis"""
        # 1. Industry detection
        # 2. Analysis execution with progress
        # 3. Error handling and retry
        # 4. Memory storage
        # 5. Results compilation
```

**API Endpoint**: `POST /api/v1/analysis/orchestrate`

## API Implementation Plan

### 1. Question Interface API
```python
# src/api/questions.py

@router.get("/categories")
async def get_question_categories():
    """Returns available question categories"""
    return {
        "categories": [
            {
                "id": "trend_analysis",
                "name": "Trend Analysis",
                "examples": ["What are my sales trends?", "Show revenue growth"]
            },
            {
                "id": "comparative",
                "name": "Comparative Analysis",
                "examples": ["Compare Q1 vs Q2", "Regional performance comparison"]
            },
            {
                "id": "correlation",
                "name": "Correlation Analysis",
                "examples": ["What drives customer satisfaction?", "Revenue correlation factors"]
            }
        ]
    }

@router.post("/suggest")
async def suggest_questions(data_info: DataInfo):
    """Suggests relevant questions based on data"""
    # Uses Industry Detective to determine business type
    # Returns industry-specific question suggestions
```

### 2. Real-time Progress Tracking
```python
# src/websocket/progress.py

@app.websocket("/ws/analysis/{job_id}")
async def analysis_progress(websocket: WebSocket, job_id: str):
    """WebSocket for real-time progress updates"""
    await manager.connect(websocket, job_id)
    
    while True:
        progress = await get_job_progress(job_id)
        await websocket.send_json({
            "type": "progress",
            "data": {
                "percent": progress.percent,
                "stage": progress.current_stage,
                "message": progress.message
            }
        })
```

### 3. Results Dashboard API
```python
# src/api/results.py

@router.get("/results/{job_id}")
async def get_analysis_results(job_id: str):
    """Returns comprehensive analysis results"""
    return {
        "dashboard": {
            "key_metrics": [...],
            "charts": [...],
            "summary": "..."
        },
        "insights": [
            {"finding": "...", "confidence": 0.92, "impact": "high"}
        ],
        "recommendations": [
            {"action": "...", "priority": "high", "expected_impact": "..."}
        ],
        "industry_context": {
            "benchmarks": {...},
            "trends": {...}
        },
        "details": {
            "full_analysis": "...",
            "methodology": "..."
        }
    }

@router.post("/export/{format}")
async def export_results(job_id: str, format: str):
    """Exports results in various formats"""
    # Supports: PDF, Excel, PowerPoint, Jupyter
```

## Implementation Sequence

### Phase 1: Core Agents (Week 1)
1. ✅ ConfigManager (already done)
2. 🔄 Industry Detective Agent
3. 🔄 Execution Manager Agent
4. 🔄 Code Inspector Agent

### Phase 2: Analysis Agents (Week 2)
5. 🔄 Business Analysis Agent
6. 🔄 Memory Keeper Agent
7. 🔄 Orchestrator Agent

### Phase 3: API Integration (Week 3)
8. 🔄 Question Interface API
9. 🔄 WebSocket Progress Tracking
10. 🔄 Results Dashboard API

### Phase 4: Frontend Integration (Week 4)
11. 🔄 React components for agent visualization
12. 🔄 Real-time progress display
13. 🔄 Interactive dashboard

## Testing Strategy

### Unit Tests
```python
# tests/test_agents/test_industry_detective.py
def test_detect_retail_industry():
    detective = IndustryDetective()
    result = detective.detect_industry(
        question="What are my sales trends?",
        data_columns=["date", "sales", "inventory", "region"]
    )
    assert result["industry"] == "retail"
    assert result["confidence"] > 0.8
```

### Integration Tests
```python
# tests/test_integration/test_agent_orchestration.py
async def test_full_analysis_workflow():
    orchestrator = AnalysisOrchestrator()
    result = await orchestrator.orchestrate_analysis(
        data=sample_retail_data,
        question="What drives my sales?"
    )
    assert "insights" in result
    assert "recommendations" in result
```

## Configuration
```yaml
# config.yaml
agents:
  industry_detective:
    confidence_threshold: 0.7
    industry_patterns:
      retail: ["sales", "inventory", "customer"]
      saas: ["subscription", "churn", "mrr"]
      
  execution_manager:
    default_timeout: 300
    progress_update_interval: 1.0
    
  business_analysis:
    max_retries: 3
    self_correction_enabled: true
```

## Success Metrics
- Industry detection accuracy > 85%
- Analysis completion rate > 95%
- Self-correction success rate > 80%
- Average analysis time < 30 seconds
- User satisfaction score > 4.5/5

## Next Steps
1. Implement Industry Detective Agent with tests
2. Create WebSocket infrastructure for progress tracking
3. Design API contracts for all endpoints
4. Build agent coordination logic
5. Integrate with existing building blocks