"""Building blocks API router"""
import time
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from src.models.schemas import (
    BlockExecutionRequest,
    BuildingBlockResponse,
    StandardResponse
)

router = APIRouter()

# Mock block registry until we implement the real one
MOCK_BLOCKS = {
    "test_block": {
        "id": "test_block",
        "name": "Test Block",
        "description": "A test building block",
        "category": "test",
        "version": "1.0.0",
        "config_schema": {
            "type": "object",
            "properties": {
                "threshold": {"type": "number", "default": 0.95}
            }
        },
        "is_active": True
    },
    "error_block": {
        "id": "error_block",
        "name": "Error Block",
        "description": "A block that triggers errors for testing",
        "category": "test",
        "version": "1.0.0",
        "config_schema": {},
        "is_active": True
    },
    "data_block": {
        "id": "data_block",
        "name": "Data Processing Block",
        "description": "Processes data",
        "category": "data",
        "version": "1.0.0",
        "config_schema": {},
        "is_active": True
    }
}

# Mock metrics storage
MOCK_METRICS = {}


def create_response(success: bool, data=None, error=None) -> Dict:
    """Create standardized API response"""
    return {
        "success": success,
        "data": data,
        "error": error,
        "metadata": {
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": str(uuid4()),
            "version": "1.0"
        }
    }


@router.get("/")
async def list_blocks(
    category: Optional[str] = Query(None, description="Filter by category"),
    is_active: Optional[bool] = Query(None, description="Filter by active status")
):
    """List all available building blocks"""
    blocks = list(MOCK_BLOCKS.values())
    
    # Apply filters
    if category:
        blocks = [b for b in blocks if b["category"] == category]
    
    if is_active is not None:
        blocks = [b for b in blocks if b["is_active"] == is_active]
    
    return create_response(success=True, data=blocks)


@router.get("/{block_id}")
async def get_block_details(block_id: str):
    """Get details of a specific building block"""
    if block_id not in MOCK_BLOCKS:
        return JSONResponse(
            status_code=404,
            content=create_response(
                success=False,
                error=f"Block '{block_id}' not found"
            )
        )
    
    block = MOCK_BLOCKS[block_id]
    return create_response(success=True, data=block)


@router.post("/{block_id}/execute")
async def execute_block(block_id: str, request: BlockExecutionRequest):
    """Execute a building block"""
    if block_id not in MOCK_BLOCKS:
        return JSONResponse(
            status_code=404,
            content=create_response(
                success=False,
                error=f"Block '{block_id}' not found"
            )
        )
    
    block = MOCK_BLOCKS[block_id]
    
    # Record start time
    start_time = time.time()
    
    try:
        # Mock execution logic
        if block_id == "error_block" and request.data.get("trigger_error"):
            raise Exception("Simulated error in block execution")
        
        # Simulate processing
        time.sleep(0.1)  # Simulate some work
        
        # Mock result
        result = {
            "processed_data": request.data,
            "config_applied": request.config,
            "block_info": {
                "id": block["id"],
                "name": block["name"],
                "version": block["version"]
            }
        }
        
        execution_time = time.time() - start_time
        
        # Update metrics
        if block_id not in MOCK_METRICS:
            MOCK_METRICS[block_id] = {
                "execution_count": 0,
                "success_count": 0,
                "error_count": 0,
                "total_execution_time": 0
            }
        
        MOCK_METRICS[block_id]["execution_count"] += 1
        MOCK_METRICS[block_id]["success_count"] += 1
        MOCK_METRICS[block_id]["total_execution_time"] += execution_time
        MOCK_METRICS[block_id]["last_execution"] = datetime.utcnow().isoformat()
        
        response = create_response(success=True, data=result)
        response["metadata"]["execution_time"] = execution_time
        response["metadata"]["block_version"] = block["version"]
        
        return response
        
    except Exception as e:
        execution_time = time.time() - start_time
        
        # Update error metrics
        if block_id in MOCK_METRICS:
            MOCK_METRICS[block_id]["error_count"] += 1
            MOCK_METRICS[block_id]["execution_count"] += 1
        
        response = create_response(
            success=False,
            error=f"Error executing block: {str(e)}"
        )
        response["metadata"]["execution_time"] = execution_time
        response["metadata"]["block_version"] = block["version"]
        
        return response


@router.get("/{block_id}/metrics")
async def get_block_metrics(block_id: str):
    """Get execution metrics for a building block"""
    if block_id not in MOCK_BLOCKS:
        return JSONResponse(
            status_code=404,
            content=create_response(
                success=False,
                error=f"Block '{block_id}' not found"
            )
        )
    
    metrics = MOCK_METRICS.get(block_id, {
        "execution_count": 0,
        "success_count": 0,
        "error_count": 0,
        "total_execution_time": 0,
        "last_execution": None
    })
    
    # Calculate success rate and average execution time
    if metrics["execution_count"] > 0:
        metrics["success_rate"] = metrics["success_count"] / metrics["execution_count"]
        metrics["average_execution_time"] = (
            metrics["total_execution_time"] / metrics["execution_count"]
        )
    else:
        metrics["success_rate"] = 0
        metrics["average_execution_time"] = 0
    
    return create_response(success=True, data=metrics)