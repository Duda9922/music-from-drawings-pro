"""
User endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
import structlog

from app.models.user import User

logger = structlog.get_logger()
router = APIRouter()

@router.get("/", response_model=List[User])
async def list_users(limit: int = 20, offset: int = 0):
    """
    List users (admin only)
    """
    users = await User.find().skip(offset).limit(limit).to_list()
    return users

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    """
    Get user by ID
    """
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
