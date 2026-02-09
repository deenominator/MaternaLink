import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import logging
import asyncio
from typing import Optional, List  # ADDED List
from open_source_vision import OpenSourceVision
open_source_vision = OpenSourceVision()

# Import local modules
from config import config
from image_validator import ImageValidator
from gemini_vision_handler import GeminiHandler  # Make sure filename matches
from safety_formatter import SafetyFormatter

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="MaternaLink Injury Lens AI",
    description="AI-powered image analysis for minor injuries (non-diagnostic)",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
try:
    image_validator = ImageValidator()
    gemini_handler = None

    @app.on_event("startup")
    async def startup_event():
       global gemini_handler
       gemini_handler = GeminiHandler()

    safety_formatter = SafetyFormatter()
    logger.info("All services initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize services: {e}")
    raise

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "MaternaLink Injury Lens AI",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "POST /analyze",
            "health": "GET /health"
        },
        "disclaimer": "This is a non-diagnostic support tool only."
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "injury_lens_ai",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/analyze")
async def analyze_injury(
    image: UploadFile = File(..., description="Image of injury/rash"),
    injury_type: Optional[str] = Query(
        "skin_issue", 
        description="Type of injury: skin_issue, cut, bruise, burn, insect_bite"
    )
):
    """
    Analyze an injury/rash image and provide non-diagnostic guidance
    
    - **image**: Upload image file (JPG, PNG, BMP, GIF up to 5MB)
    - **injury_type**: Optional type of injury for context
    """
    logger.info(f"Received analysis request for {injury_type}")
    
    try:
        # 1. Validate and process image
        logger.info("Validating image...")
        image_bytes, pil_image = await image_validator.validate_image(image)
        
        # Get image metadata
        image_info = ImageValidator.get_image_metadata(pil_image)
        
        # 2. Analyze with Gemini
        logger.info("Analyzing with Gemini Vision API...")
        raw_analysis = await asyncio.to_thread(
          open_source_vision.analyze_image,
          pil_image,
          injury_type
        )

        # 3. Prepare metadata
        metadata = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "image_info": {
                "filename": image.filename,
                "content_type": image.content_type,
                "size_bytes": len(image_bytes),
                "dimensions": image_info["size"],
                "format": image_info["format"]
            },
            "injury_type": injury_type
        }
        
        # 4. Apply safety formatting
        logger.info("Applying safety formatting...")
        response = safety_formatter.format_response(
            raw_analysis, 
            metadata, 
            injury_type
        )
        
        logger.info("Analysis completed successfully")
        return response
        
    except HTTPException as he:
        logger.error(f"HTTP error in analysis: {he.detail}")
        raise he
    except Exception as e:
        logger.error(f"Unexpected error in analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@app.post("/analyze-batch")
async def analyze_batch_injuries(
    images: List[UploadFile] = File(..., description="Multiple injury images"),  # CHANGED to List
    injury_type: Optional[str] = Query("skin_issue")
):
    """
    Analyze multiple injury images (for future use)
    """
    # Note: This is a placeholder for future batch processing
    return {
        "status": "batch_processing_not_implemented",
        "message": "Batch processing will be available in future versions",
        "suggestion": "Please submit images one at a time for now"
    }

if __name__ == "__main__":
    logger.info(f"Starting Injury Lens AI Service on {config.HOST}:{config.PORT}")
    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT,
        log_level="info"
    )