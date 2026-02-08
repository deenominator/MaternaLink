"""
Retrieval-Augmented Generation Service
Ensures AI only uses retrieved facts, doesn't hallucinate
"""

from typing import Dict, Optional
from safety_checker import Stage, SafetyChecker

class RAGService:
    """RAG service for safe AI responses"""
    
    def __init__(self, safety_checker: SafetyChecker):
        self.safety_checker = safety_checker
        
    def generate_safe_response(self, query: str, stage: Stage) -> Dict:
        """
        Generate a safe response using RAG pattern
        1. Retrieve facts from trusted database
        2. Format response based ONLY on retrieved facts
        3. Add appropriate disclaimers
        """
        
        # Step 1: Retrieve facts (no AI yet)
        safety_response = self.safety_checker.check_safety(query, stage)
        
        # Step 2: If no match found, don't guess
        if not safety_response.get("matched", False):
            return {
                "answer": "I couldn't find verified information about this in our trusted medical databases.",
                "action": "Please consult your healthcare provider for personalized advice.",
                "confidence": "low",
                "sources": [],
                "disclaimer": "This information is not verified. Always consult a healthcare professional."
            }
        
        # Step 3: Format response based on retrieved facts
        entry = safety_response.get("entry", {})
        status = safety_response.get("safety_status", "unknown")
        explanation = safety_response.get("explanation", "")
        recommendation = safety_response.get("recommendation", "")
        
        # Step 4: Create safe response (NO AI HALLUCINATION)
        response_parts = []
        
        # Status indicator
        status_map = {
            "safe": "✅ **SAFE**",
            "limited": "⚠️ **LIMITED** use",
            "avoid": "🚫 **AVOID**",
            "consult_doctor": "👩‍⚕️ **CONSULT DOCTOR**",
            "unknown": "❓ **UNKNOWN**"
        }
        
        status_text = status_map.get(status, "❓ **UNKNOWN**")
        stage_text = self._stage_to_text(stage)
        
        response_parts.append(f"{status_text}: **{entry.get('name', 'Unknown')}** {stage_text}")
        
        # Add explanation
        response_parts.append(f"\n**Why?** {explanation}")
        
        # Add recommendation
        response_parts.append(f"\n**Recommendation:** {recommendation}")
        
        # Add details if available
        details = safety_response.get("details", {})
        if details.get("max_daily"):
            response_parts.append(f"\n**Maximum Daily:** {details['max_daily']}")
        
        if details.get("risks"):
            risks = ", ".join(details["risks"])
            response_parts.append(f"\n**Potential Risks:** {risks}")
        
        if details.get("benefits"):
            benefits = ", ".join(details["benefits"])
            response_parts.append(f"\n**Potential Benefits:** {benefits}")
        
        # Add sources (capped at 3)
        sources = safety_response.get("sources", [])
        if sources:
            response_parts.append("\n**Verified Sources:**")
            for source in sources[:3]:
                name = source.get('name', 'Medical Source')
                date = source.get('date', '')
                response_parts.append(f"- {name} ({date})")
        
        # Combine all parts
        full_response = "\n".join(response_parts)
        
        return {
            "answer": full_response,
            "action": recommendation,
            "confidence": "high" if safety_response.get("matched") else "low",
            "sources": sources,
            "safety_status": status,
            "verified_by": safety_response.get("verified_by"),
            "last_updated": safety_response.get("last_updated"),
            "query_id": safety_response.get("query_id")
        }
    
    def _stage_to_text(self, stage: Stage) -> str:
        """Convert stage enum to readable text"""
        stage_map = {
            Stage.PREGNANCY_FIRST_TRIMESTER: "during the first trimester of pregnancy",
            Stage.PREGNANCY_SECOND_TRIMESTER: "during the second trimester of pregnancy",
            Stage.PREGNANCY_THIRD_TRIMESTER: "during the third trimester of pregnancy",
            Stage.BREASTFEEDING: "while breastfeeding",
            Stage.INFANT: "for infants"
        }
        return stage_map.get(stage, "")