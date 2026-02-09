import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

class Config:
    # API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = "models/gemini-1.5-flash"

    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = 8002
    
    # Image Configuration
    MAX_IMAGE_SIZE_MB = 5
    MAX_IMAGE_SIZE = MAX_IMAGE_SIZE_MB * 1024 * 1024
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}
    ALLOWED_MIME_TYPES = {
        "image/jpeg", "image/jpg", "image/png", 
        "image/bmp", "image/gif"
    }
    
    # Safety Configuration
    MEDICAL_DISCLAIMER = "⚠️ IMPORTANT: This is not a medical diagnosis. Always consult a healthcare professional for medical concerns."
    EMERGENCY_PROMPT = "🚨 If this appears severe or you're concerned, seek immediate medical attention."
    
    # Dangerous keywords for safety checking
    DANGEROUS_KEYWORDS = [
        "emergency", "urgent", "911", "ambulance", "hospital immediately",
        "anaphylaxis", "difficulty breathing", "choking", "unconscious",
        "severe bleeding", "broken bone", "fracture", "third degree burn",
        "chemical burn", "poison", "overdose", "seizure", "stroke"
    ]
    
    # Prompt templates
    ANALYSIS_PROMPT = """Analyze this image of a potential skin issue or minor injury.

IMPORTANT RULES:
1. DO NOT provide a medical diagnosis
2. DO NOT suggest specific medications or treatments
3. DO NOT use medical jargon without explanation
4. Focus on observable characteristics only

Please provide:

A. VISUAL DESCRIPTION (what can be seen):
- Color and pattern
- Size and location
- Texture or appearance

B. GENERAL GUIDANCE (non-medical):
- Basic first aid if appropriate
- When to consider professional help
- General care suggestions

C. SAFETY NOTES:
- Any concerning characteristics to watch for
- General precautions

Keep response clear, simple, and actionable."""

config = Config()