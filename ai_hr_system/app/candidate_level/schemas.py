from typing import List, Dict, Optional
from pydantic import BaseModel
from enum import Enum

class CandidateLevel(str, Enum):
    """Candidate seniority levels"""
    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"

class DifficultyLevel(str, Enum):
    """Question difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class LevelDetectionResult(BaseModel):
    """Result of level detection"""
    candidate_name: str
    level: CandidateLevel
    confidence_overall: float
    skills: List[str]
    experience_years: Optional[float] = None
    level_score: float = 0.0

class SkillDifficulty(BaseModel):
    """Difficulty assignment for a single skill"""
    skill: str
    difficulty: DifficultyLevel
    case_id: int  # Simulated case ID

class InterviewPlan(BaseModel):
    """Complete interview plan with difficulty-mapped questions"""
    candidate_name: str
    candidate_level: CandidateLevel
    interview_plan: List[SkillDifficulty]
    total_questions: int
