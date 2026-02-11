from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from enum import Enum

class AnalysisType(str, Enum):
    AI_DETECTION = "ai_detection"
    STRUCTURE = "structure"
    TIME_BEHAVIOR = "time_behavior"
    PLAGIARISM = "plagiarism"

class AnalysisResult(BaseModel):
    """Result from a single analysis module"""
    type: AnalysisType
    score: float  # 0.0 to 1.0
    probability: Optional[float] = None
    flags: List[str] = []
    details: Dict[str, Any] = {}

class AnswerIntegrityReport(BaseModel):
    """Integrity report for a single answer"""
    question_id: int
    honesty_score: float  # Weighted average
    is_suspicious: bool
    ai_probability: float
    analysis_results: List[AnalysisResult]
    summary: str

class FullIntegrityReport(BaseModel):
    """Complete integrity report for an interview session"""
    session_id: str
    candidate_name: str
    overall_honesty_score: float
    suspicious_answers_count: int
    global_flags: List[str]
    answer_reports: List[AnswerIntegrityReport]
    recommendation: str
