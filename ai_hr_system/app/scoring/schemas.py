from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from enum import Enum

class RecommendationLevel(str, Enum):
    STRONG_HIRE = "Strong Hire"
    HIRE = "Hire"
    REVIEW = "Review"
    REJECT = "Reject"

class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ScoreBreakdown(BaseModel):
    """Breakdown of different score components"""
    knowledge_score: float        # 0-100
    honesty_score: float          # 0-100
    time_behavior_score: float    # 0-100
    problem_solving_score: float  # 0-100

class FinalRecommendation(BaseModel):
    """The absolute final result for HR"""
    session_id: str
    candidate_name: str
    final_score: int              # 0-100
    decision: RecommendationLevel
    confidence: ConfidenceLevel
    hr_comment: str
    score_breakdown: ScoreBreakdown
    flags: List[str]
    metadata: Dict[str, Any] = {}
