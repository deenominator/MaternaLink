import io
from PIL import Image, UnidentifiedImageError
from fastapi import HTTPException
from typing import Tuple
import imghdr

from config import config

class ImageValidator:
    @staticmethod
    async def validate_image(file) -> Tuple[bytes, Image.Image]:
        """
        Validate and process uploaded image
        Returns: (image_bytes, PIL_image)
        """
        # Read file content
        contents = await file.read()
        file_size = len(contents)
        
        # Check file size
        if file_size > config.MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Image too large. Maximum size is {config.MAX_IMAGE_SIZE_MB}MB"
            )
        
        # Check file extension
        filename = file.filename.lower()
        if not any(filename.endswith(ext) for ext in config.ALLOWED_EXTENSIONS):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(config.ALLOWED_EXTENSIONS)}"
            )
        
        # Validate it's actually an image
        try:
            image = Image.open(io.BytesIO(contents))
            image.verify()  # Verify it's a valid image
        except (UnidentifiedImageError, Exception) as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image file: {str(e)}"
            )
        
        # Re-open image after verify
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if needed
        if image.mode not in ['RGB', 'L']:
            image = image.convert('RGB')
        
        # Optional: Resize if too large (for performance)
        max_dimension = 1024
        width, height = image.size
        if max(width, height) > max_dimension:
            ratio = max_dimension / max(width, height)
            new_size = (int(width * ratio), int(height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        return contents, image
    
    @staticmethod
    def get_image_metadata(image: Image.Image) -> dict:
        """Extract basic image metadata"""
        return {
            "size": image.size,
            "mode": image.mode,
            "format": image.format if hasattr(image, 'format') else "Unknown"
        }