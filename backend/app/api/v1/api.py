"""
API v1 router
"""

from fastapi import APIRouter
from app.api.v1.endpoints import drawings, music, users, analytics

api_router = APIRouter()

api_router.include_router(drawings.router, prefix="/drawings", tags=["drawings"])
api_router.include_router(music.router, prefix="/music", tags=["music"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
