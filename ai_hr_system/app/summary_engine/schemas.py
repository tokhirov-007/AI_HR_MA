from typing import List, Dict, Optional
from pydantic import BaseModel

class CandidateSummary(BaseModel):
    """Summary of a single candidate"""
    candidate_name: Optional[str] = "Unknown"
    summary_hr: str
    summary_technical: str
    skills_detected: List[str]
    inferred_skills: List[str]
    experience_years: Optional[float] = None
    confidence: Dict[str, float] = {}
    total_score: float = 0.0

class TopCandidatesResponse(BaseModel):
    """Response containing ranked candidates"""
    candidates: List[CandidateSummary]
    total_candidates: int
