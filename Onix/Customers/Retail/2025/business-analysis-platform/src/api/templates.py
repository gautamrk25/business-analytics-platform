"""Templates API router"""
from fastapi import APIRouter

router = APIRouter()

# Placeholder endpoints
@router.get("/")
async def list_templates():
    return {"templates": []}
