"""
Core safety checking service - No FastAPI, just pure logic
This is what the AI team needs to implement
"""

import json
import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import uuid
from enum import Enum

# Enums (same as before)
class Stage(str, Enum):
    PREGNANCY_FIRST_TRIMESTER = "pregnancy_first_trimester"
    PREGNANCY_SECOND_TRIMESTER = "pregnancy_second_trimester"
    PREGNANCY_THIRD_TRIMESTER = "pregnancy_third_trimester"
    BREASTFEEDING = "breastfeeding"
    INFANT = "infant"

class SafetyStatus(str, Enum):
    SAFE = "safe"
    LIMITED = "limited"
    AVOID = "avoid"
    CONSULT_DOCTOR = "consult_doctor"
    UNKNOWN = "unknown"

class SafetyEntry:
    """Model for a safety entry in the database"""
    def __init__(self, data: Dict):
        self.id = data.get("id", "")
        self.name = data.get("name", "")
        self.aliases = data.get("aliases", [])
        self.category = data.get("category", "")
        self.description = data.get("description", "")
        self.safety_info = self._parse_safety_info(data.get("safety_info", {}))
        self.sources = data.get("sources", [])
        self.last_updated = data.get("last_updated", "")
        self.verified_by = data.get("verified_by", "CDC/NHS/WHO")
    
    def _parse_safety_info(self, safety_info: Dict) -> Dict[Stage, Dict]:
        """Convert string keys to Stage enum"""
        parsed = {}
        for stage_str, info in safety_info.items():
            try:
                stage = Stage(stage_str)
                parsed[stage] = info
            except ValueError:
                continue
        return parsed
    
    def get_safety_for_stage(self, stage: Stage) -> Dict:
        """Get safety info for specific stage"""
        return self.safety_info.get(stage, {
            "status": SafetyStatus.UNKNOWN,
            "explanation": "No specific information available for this stage",
            "recommendation": "Consult your healthcare provider"
        })
    
    def matches_query(self, query: str) -> bool:
        """Check if query matches this entry (name or aliases)"""
        query_lower = query.lower()
        if self.name.lower() in query_lower:
            return True
        for alias in self.aliases:
            if alias.lower() in query_lower:
                return True
        return False

class SafetyChecker:
    """Core safety checking logic - Pure Python, no web framework"""
    
    def __init__(self, database_path: str = "safety_db.json"):
        self.database_path = database_path
        self.entries = self._load_database()
        
    def _load_database(self) -> List[SafetyEntry]:
        """Load safety database from JSON file"""
        try:
            with open(self.database_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            entries = []
            for entry_data in data.get('entries', []):
                entries.append(SafetyEntry(entry_data))
            
            print(f"✅ Loaded {len(entries)} safety entries from {self.database_path}")
            return entries
        except FileNotFoundError:
            print(f"❌ Database file not found: {self.database_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing database: {e}")
            return []
    
    def check_safety(self, query: str, stage: Stage) -> Dict:
        """
        Main safety check function
        Returns structured safety information
        
        Args:
            query: User's question (e.g., "Can I have coffee?")
            stage: Pregnancy/breastfeeding stage
            
        Returns:
            Dictionary with safety information
        """
        query_id = str(uuid.uuid4())
        normalized_query = self._normalize_query(query)
        
        # Find matching entries
        matching_entries = self._find_matching_entries(normalized_query)
        
        if not matching_entries:
            return self._get_no_match_response(query, stage, query_id)
        
        # Get safety info for best match
        best_match = matching_entries[0]
        safety_info = best_match.get_safety_for_stage(stage)
        
        response = {
            "query_id": query_id,
            "query": query,
            "stage": stage.value,
            "matched": True,
            "entry": {
                "id": best_match.id,
                "name": best_match.name,
                "category": best_match.category
            },
            "safety_status": safety_info.get("status", SafetyStatus.UNKNOWN),
            "explanation": safety_info.get("explanation", "No information available"),
            "recommendation": safety_info.get("recommendation", "Consult your healthcare provider"),
            "details": {
                "max_daily": safety_info.get("max_daily"),
                "risks": safety_info.get("risks", []),
                "benefits": safety_info.get("benefits", []),
                "notes": safety_info.get("notes")
            },
            "sources": best_match.sources,
            "last_updated": best_match.last_updated,
            "verified_by": best_match.verified_by,
            "timestamp": datetime.now().isoformat()
        }
        
        return response
    
    def _find_matching_entries(self, query: str) -> List[SafetyEntry]:
        """Find entries that match the query"""
        matches = []
        
        # Exact matches
        for entry in self.entries:
            if entry.matches_query(query):
                matches.append(entry)
        
        # Partial matches if no exact matches
        if not matches:
            query_words = set(query.lower().split())
            for entry in self.entries:
                entry_words = set(entry.name.lower().split())
                if query_words.intersection(entry_words):
                    matches.append(entry)
        
        return matches
    
    def _normalize_query(self, query: str) -> str:
        """Normalize the query for better matching"""
        normalized = query.lower()
        
        # Remove common prefixes
        prefixes = ["can i have ", "is ", "can i take ", "is it safe to have ", "is it safe to take "]
        for prefix in prefixes:
            if normalized.startswith(prefix):
                normalized = normalized[len(prefix):]
        
        # Clean up
        normalized = normalized.replace('?', '').strip()
        
        return normalized
    
    def _get_no_match_response(self, query: str, stage: Stage, query_id: str) -> Dict:
        """Generate response when no match is found"""
        return {
            "query_id": query_id,
            "query": query,
            "stage": stage.value,
            "matched": False,
            "safety_status": SafetyStatus.UNKNOWN.value,
            "explanation": "No verified information found in our database",
            "recommendation": "Please consult your healthcare provider",
            "sources": [],
            "timestamp": datetime.now().isoformat()
        }
    
    def search(self, term: str, limit: int = 10) -> List[Dict]:
        """Search the database for entries"""
        results = []
        term_lower = term.lower()
        
        for entry in self.entries:
            if (term_lower in entry.name.lower() or 
                any(term_lower in alias.lower() for alias in entry.aliases)):
                results.append({
                    "id": entry.id,
                    "name": entry.name,
                    "category": entry.category,
                    "description": entry.description
                })
                if len(results) >= limit:
                    break
        
        return results
    
    def get_stats(self) -> Dict:
        """Get statistics about the database"""
        categories = list(set(entry.category for entry in self.entries))
        
        return {
            "total_entries": len(self.entries),
            "categories": categories,
            "database_last_updated": max([entry.last_updated for entry in self.entries]) if self.entries else None
        }