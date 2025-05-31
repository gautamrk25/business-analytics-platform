"""Analysis API router"""
from fastapi import APIRouter

router = APIRouter()

# Placeholder endpoints
@router.get("/")
async def list_analyses():
    return {"analyses": []}
