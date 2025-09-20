"""
Music generation endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
import structlog
from datetime import datetime

from app.models.music import MusicGeneration, MusicStatus, MusicParameters
from app.models.drawing import Drawing
from app.services.music_service import MusicService
from app.services.ai_service import AIService

logger = structlog.get_logger()
router = APIRouter()

# Initialize services
music_service = MusicService()
ai_service = AIService()

@router.post("/generate", response_model=MusicGeneration)
async def generate_music(
    background_tasks: BackgroundTasks,
    drawing_id: str,
    provider: str = "suno",
    user_id: Optional[str] = None
):
    """
    Generate music from a drawing
    """
    try:
        # Get drawing
        drawing = await Drawing.get(drawing_id)
        if not drawing:
            raise HTTPException(status_code=404, detail="Drawing not found")
        
        if drawing.status != "completed":
            raise HTTPException(status_code=400, detail="Drawing analysis not completed")
        
        # Generate music prompt from visual analysis
        if not drawing.visual_analysis:
            raise HTTPException(status_code=400, detail="Drawing analysis not available")
        
        # Convert visual analysis to dict for AI service
        analysis_dict = drawing.visual_analysis.dict()
        prompt = await ai_service.generate_music_prompt(analysis_dict)
        
        # Create music parameters
        musical_suggestions = analysis_dict.get("musical_suggestions", {})
        parameters = MusicParameters(
            tempo=120,  # Default, will be updated by AI
            key=musical_suggestions.get("key_suggestion", "C major"),
            scale="major",
            genre=musical_suggestions.get("genre", "contemporary"),
            mood=analysis_dict.get("mood", {}).get("primary", "neutral"),
            instruments=musical_suggestions.get("instrumentation", ["piano"]),
            duration=45,
            dynamics="mezzo-forte",
            rhythm_pattern="regular"
        )
        
        # Create music generation record
        music_gen = MusicGeneration(
            drawing_id=drawing_id,
            user_id=user_id,
            parameters=parameters,
            prompt=prompt,
            provider=provider,
            status=MusicStatus.PENDING
        )
        
        await music_gen.insert()
        
        # Start background generation
        background_tasks.add_task(generate_music_task, music_gen.id, prompt, parameters, provider)
        
        logger.info(f"Music generation started: {music_gen.id}")
        return music_gen
        
    except Exception as e:
        logger.error(f"Error starting music generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{music_id}", response_model=MusicGeneration)
async def get_music(music_id: str):
    """
    Get music generation by ID
    """
    music_gen = await MusicGeneration.get(music_id)
    if not music_gen:
        raise HTTPException(status_code=404, detail="Music generation not found")
    return music_gen

@router.get("/", response_model=List[MusicGeneration])
async def list_music_generations(
    user_id: Optional[str] = None,
    drawing_id: Optional[str] = None,
    status: Optional[MusicStatus] = None,
    limit: int = 20,
    offset: int = 0
):
    """
    List music generations with optional filters
    """
    query = {}
    if user_id:
        query["user_id"] = user_id
    if drawing_id:
        query["drawing_id"] = drawing_id
    if status:
        query["status"] = status
    
    music_gens = await MusicGeneration.find(query).skip(offset).limit(limit).to_list()
    return music_gens

@router.get("/providers/available")
async def get_available_providers():
    """
    Get list of available music generation providers
    """
    providers = await music_service.get_available_providers()
    return {"providers": providers}

@router.post("/{music_id}/play")
async def record_play(music_id: str):
    """
    Record a play event for analytics
    """
    music_gen = await MusicGeneration.get(music_id)
    if not music_gen:
        raise HTTPException(status_code=404, detail="Music generation not found")
    
    music_gen.play_count += 1
    await music_gen.save()
    
    return {"message": "Play recorded"}

@router.post("/{music_id}/rate")
async def rate_music(music_id: str, rating: float):
    """
    Rate a music generation
    """
    if not 0.0 <= rating <= 5.0:
        raise HTTPException(status_code=400, detail="Rating must be between 0.0 and 5.0")
    
    music_gen = await MusicGeneration.get(music_id)
    if not music_gen:
        raise HTTPException(status_code=404, detail="Music generation not found")
    
    music_gen.rating = rating
    await music_gen.save()
    
    return {"message": "Rating saved"}

async def generate_music_task(music_id: str, prompt: str, parameters: MusicParameters, provider: str):
    """
    Background task to generate music
    """
    try:
        music_gen = await MusicGeneration.get(music_id)
        if not music_gen:
            logger.error(f"Music generation not found: {music_id}")
            return
        
        # Update status
        music_gen.status = MusicStatus.GENERATING
        await music_gen.save()
        
        # Generate music
        result = await music_service.generate_music(prompt, parameters, provider)
        
        if result.get("success"):
            music_gen.audio_url = result.get("audio_url")
            music_gen.audio_duration = result.get("duration")
            music_gen.status = MusicStatus.COMPLETED
            music_gen.generated_at = datetime.utcnow()
            music_gen.generation_time = 1.0  # Placeholder
        else:
            music_gen.status = MusicStatus.FAILED
            music_gen.error_message = result.get("error", "Unknown error")
        
        await music_gen.save()
        
        logger.info(f"Music generation completed: {music_id}")
        
    except Exception as e:
        logger.error(f"Error generating music {music_id}: {e}")
        
        # Update with error
        music_gen = await MusicGeneration.get(music_id)
        if music_gen:
            music_gen.status = MusicStatus.FAILED
            music_gen.error_message = str(e)
            await music_gen.save()
