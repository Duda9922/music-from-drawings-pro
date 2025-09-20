"""
Drawing endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, UploadFile, File
from typing import List, Optional
import structlog
from PIL import Image
import io
import hashlib
from datetime import datetime

from app.models.drawing import Drawing, DrawingStatus, VisualAnalysis
from app.services.ai_service import AIService
from app.core.database import get_database

logger = structlog.get_logger()
router = APIRouter()

# Initialize services
ai_service = AIService()

@router.post("/upload", response_model=Drawing)
async def upload_drawing(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: Optional[str] = None,
    description: Optional[str] = None,
    user_id: Optional[str] = None
):
    """
    Upload and analyze a drawing
    """
    try:
        # Validate file
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Generate image hash
        image_hash = hashlib.md5(image_data).hexdigest()
        
        # Check if drawing already exists
        existing_drawing = await Drawing.find_one(Drawing.image_hash == image_hash)
        if existing_drawing:
            return existing_drawing
        
        # Create drawing document
        drawing = Drawing(
            user_id=user_id,
            title=title or f"Drawing {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
            description=description,
            image_url=f"uploads/{image_hash}.{file.filename.split('.')[-1]}",
            image_hash=image_hash,
            width=image.width,
            height=image.height,
            status=DrawingStatus.PENDING
        )
        
        # Save to database
        await drawing.insert()
        
        # Start background analysis
        background_tasks.add_task(analyze_drawing_task, drawing.id, image)
        
        logger.info(f"Drawing uploaded: {drawing.id}")
        return drawing
        
    except Exception as e:
        logger.error(f"Error uploading drawing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{drawing_id}", response_model=Drawing)
async def get_drawing(drawing_id: str):
    """
    Get drawing by ID
    """
    drawing = await Drawing.get(drawing_id)
    if not drawing:
        raise HTTPException(status_code=404, detail="Drawing not found")
    return drawing

@router.get("/", response_model=List[Drawing])
async def list_drawings(
    user_id: Optional[str] = None,
    status: Optional[DrawingStatus] = None,
    limit: int = 20,
    offset: int = 0
):
    """
    List drawings with optional filters
    """
    query = {}
    if user_id:
        query["user_id"] = user_id
    if status:
        query["status"] = status
    
    drawings = await Drawing.find(query).skip(offset).limit(limit).to_list()
    return drawings

@router.post("/{drawing_id}/analyze")
async def trigger_analysis(drawing_id: str, background_tasks: BackgroundTasks):
    """
    Manually trigger drawing analysis
    """
    drawing = await Drawing.get(drawing_id)
    if not drawing:
        raise HTTPException(status_code=404, detail="Drawing not found")
    
    if drawing.status == DrawingStatus.PROCESSING:
        raise HTTPException(status_code=400, detail="Analysis already in progress")
    
    # Update status
    drawing.status = DrawingStatus.PENDING
    await drawing.save()
    
    # Start background analysis
    background_tasks.add_task(analyze_drawing_task, drawing_id, None)
    
    return {"message": "Analysis started"}

async def analyze_drawing_task(drawing_id: str, image: Optional[Image.Image] = None):
    """
    Background task to analyze drawing
    """
    try:
        drawing = await Drawing.get(drawing_id)
        if not drawing:
            logger.error(f"Drawing not found: {drawing_id}")
            return
        
        # Update status
        drawing.status = DrawingStatus.PROCESSING
        await drawing.save()
        
        # Load image if not provided
        if not image:
            # In production, load from storage
            # For now, use a placeholder
            image = Image.new('RGB', (400, 300), color='white')
        
        # Analyze with AI
        analysis_data = await ai_service.analyze_drawing(image)
        
        # Create visual analysis object
        visual_analysis = VisualAnalysis(**analysis_data)
        
        # Update drawing
        drawing.visual_analysis = visual_analysis
        drawing.status = DrawingStatus.COMPLETED
        drawing.processed_at = datetime.utcnow()
        drawing.processing_time = 1.0  # Placeholder
        await drawing.save()
        
        logger.info(f"Drawing analysis completed: {drawing_id}")
        
    except Exception as e:
        logger.error(f"Error analyzing drawing {drawing_id}: {e}")
        
        # Update drawing with error
        drawing = await Drawing.get(drawing_id)
        if drawing:
            drawing.status = DrawingStatus.FAILED
            drawing.error_message = str(e)
            await drawing.save()
