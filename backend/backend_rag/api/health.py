from fastapi import APIRouter
from typing import Dict

router = APIRouter()


@router.get("/status")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint to verify the service is running
    """
    return {"status": "healthy"}