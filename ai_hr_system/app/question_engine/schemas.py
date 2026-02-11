from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class QuestionType(str, Enum):
    """Type of interview question"""
    THEORY = "theory"
    CASE = "case"

class DifficultyLevel(str, Enum):
    """Question difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Question(BaseModel):
    """Individual interview question"""
    id: int
    skill: str
    difficulty: DifficultyLevel
    type: QuestionType
    question: str
    expected_topics: List[str] = []

class QuestionSet(BaseModel):
    """Complete set of interview questions for a candidate"""
    candidate_name: str
    candidate_level: str
    questions: List[Question]
    total_questions: int
