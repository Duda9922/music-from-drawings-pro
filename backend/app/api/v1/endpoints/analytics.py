"""
Analytics endpoints
"""

from fastapi import APIRouter
from typing import Dict, Any
import structlog
from datetime import datetime, timedelta

from app.models.drawing import Drawing
from app.models.music import MusicGeneration
from app.models.user import User

logger = structlog.get_logger()
router = APIRouter()

@router.get("/stats")
async def get_analytics_stats():
    """
    Get analytics statistics
    """
    try:
        # Count total drawings
        total_drawings = await Drawing.count()
        
        # Count completed drawings
        completed_drawings = await Drawing.find(Drawing.status == "completed").count()
        
        # Count total music generations
        total_music = await MusicGeneration.count()
        
        # Count completed music generations
        completed_music = await MusicGeneration.find(MusicGeneration.status == "completed").count()
        
        # Count total users
        total_users = await User.count()
        
        # Count active users (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        active_users = await User.find(User.last_login >= thirty_days_ago).count()
        
        # Get average rating
        music_with_ratings = await MusicGeneration.find(MusicGeneration.rating != None).to_list()
        avg_rating = 0.0
        if music_with_ratings:
            avg_rating = sum(m.rating for m in music_with_ratings) / len(music_with_ratings)
        
        # Get total play count
        total_plays = sum(m.play_count for m in await MusicGeneration.find().to_list())
        
        return {
            "drawings": {
                "total": total_drawings,
                "completed": completed_drawings,
                "completion_rate": completed_drawings / total_drawings if total_drawings > 0 else 0
            },
            "music": {
                "total": total_music,
                "completed": completed_music,
                "completion_rate": completed_music / total_music if total_music > 0 else 0,
                "average_rating": avg_rating,
                "total_plays": total_plays
            },
            "users": {
                "total": total_users,
                "active": active_users
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        return {
            "error": "Failed to get analytics",
            "drawings": {"total": 0, "completed": 0, "completion_rate": 0},
            "music": {"total": 0, "completed": 0, "completion_rate": 0, "average_rating": 0, "total_plays": 0},
            "users": {"total": 0, "active": 0}
        }

@router.get("/trends")
async def get_trends(days: int = 7):
    """
    Get trends over time
    """
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get drawings created in time range
        drawings = await Drawing.find(
            Drawing.created_at >= start_date,
            Drawing.created_at <= end_date
        ).to_list()
        
        # Get music generations created in time range
        music_gens = await MusicGeneration.find(
            MusicGeneration.created_at >= start_date,
            MusicGeneration.created_at <= end_date
        ).to_list()
        
        # Group by day
        daily_stats = {}
        for i in range(days):
            date = (start_date + timedelta(days=i)).date()
            daily_stats[date.isoformat()] = {
                "drawings": 0,
                "music_generations": 0,
                "plays": 0
            }
        
        # Count drawings by day
        for drawing in drawings:
            date = drawing.created_at.date().isoformat()
            if date in daily_stats:
                daily_stats[date]["drawings"] += 1
        
        # Count music generations by day
        for music_gen in music_gens:
            date = music_gen.created_at.date().isoformat()
            if date in daily_stats:
                daily_stats[date]["music_generations"] += 1
                daily_stats[date]["plays"] += music_gen.play_count
        
        return {
            "period_days": days,
            "daily_stats": daily_stats
        }
        
    except Exception as e:
        logger.error(f"Error getting trends: {e}")
        return {"error": "Failed to get trends"}
