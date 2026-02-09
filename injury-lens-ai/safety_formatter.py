import re
from typing import Dict, Any, Optional

from config import config

class SafetyFormatter:
    @staticmethod
    def add_safety_disclaimers(analysis: str) -> str:
        """Add mandatory medical disclaimers"""
        disclaimer = f"\n\n{config.MEDICAL_DISCLAIMER}"
        
        # Check for emergency keywords
        analysis_lower = analysis.lower()
        emergency_keywords = config.DANGEROUS_KEYWORDS
        if any(keyword in analysis_lower for keyword in emergency_keywords):
            disclaimer += f"\n\n{config.EMERGENCY_PROMPT}"
        
        # Add general guidance footer
        disclaimer += "\n\n📋 **General Guidelines:**\n"
        disclaimer += "• Monitor for changes over next 24-48 hours\n"
        disclaimer += "• Seek professional help if symptoms worsen\n"
        disclaimer += "• Keep the area clean and protected\n"
        disclaimer += "• When in doubt, consult a healthcare provider\n"
        
        return analysis + disclaimer
    
    @staticmethod
    def filter_dangerous_content(text: str) -> str:
        """Remove or flag potentially dangerous suggestions"""
        # Phrases to remove or replace
        dangerous_phrases = {
            r"you should (take|use|apply)": "consider",
            r"prescribe you": "suggest for",
            r"diagnosis is": "appears to be",
            r"definitely|certainly|guarantee": "may be",
            r"take (aspirin|ibuprofen|antibiotics)": "consult doctor about pain relief",
            r"apply (steroid|antibiotic) cream": "consider appropriate topical treatment"
        }
        
        safe_text = text
        for pattern, replacement in dangerous_phrases.items():
            safe_text = re.sub(pattern, replacement, safe_text, flags=re.IGNORECASE)
        
        return safe_text
    
    @staticmethod
    def check_emergency_level(analysis: str) -> Dict[str, bool]:
        """Determine if emergency response is suggested"""
        analysis_lower = analysis.lower()
        
        emergency_flags = {
            "is_emergency": False,
            "needs_urgent_care": False,
            "recommend_doctor": False
        }
        
        # Emergency indicators
        emergency_indicators = [
            "emergency room", "call 911", "immediate medical", 
            "life-threatening", "severe pain", "unable to breathe",
            "anaphylaxis", "choking", "unconscious"
        ]
        
        # Urgent care indicators
        urgent_indicators = [
            "see a doctor today", "urgent care", "within hours",
            "worsening quickly", "fever with rash", "severe swelling"
        ]
        
        # Doctor recommendation indicators
        doctor_indicators = [
            "see your doctor", "consult a physician", "medical attention",
            "professional evaluation", "healthcare provider"
        ]
        
        if any(indicator in analysis_lower for indicator in emergency_indicators):
            emergency_flags["is_emergency"] = True
            emergency_flags["needs_urgent_care"] = True
        
        elif any(indicator in analysis_lower for indicator in urgent_indicators):
            emergency_flags["needs_urgent_care"] = True
            emergency_flags["recommend_doctor"] = True
        
        elif any(indicator in analysis_lower for indicator in doctor_indicators):
            emergency_flags["recommend_doctor"] = True
        
        return emergency_flags
    
    @staticmethod
    def format_response(
        analysis: str, 
        metadata: Dict[str, Any],
        injury_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Format final response with all safety measures"""
        # Set default injury_type
        if injury_type is None:
            injury_type = metadata.get("injury_type", "skin_issue")
        
        # Filter dangerous content
        safe_analysis = SafetyFormatter.filter_dangerous_content(analysis)
        
        # Add disclaimers
        final_analysis = SafetyFormatter.add_safety_disclaimers(safe_analysis)
        
        # Check emergency level
        emergency_flags = SafetyFormatter.check_emergency_level(analysis)
        
        # Format response
        response = {
            "status": "success",
            "service": "MaternaLink Injury Lens",
            "version": "1.0.0",
            "analysis": final_analysis,
            "emergency_flags": emergency_flags,
            "metadata": {
                "injury_type": injury_type,
                "timestamp": metadata.get("timestamp"),
                "image_info": metadata.get("image_info", {})
            },
            "next_steps": [
                "Monitor the area for changes",
                "Keep clean and dry",
                "Contact healthcare provider if concerned",
                "Watch for signs of infection"
            ],
            "disclaimer": "This service provides general information only, not medical advice."
        }
        
        return response