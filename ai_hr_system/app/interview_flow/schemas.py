from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class SessionStatus(str, Enum):
    """Interview session status"""
    ACTIVE = "active"
    FINISHED = "finished"
    TIMEOUT = "timeout"

class Answer(BaseModel):
    """Candidate answer to a question"""
    question_id: int
    answer_text: str
    time_spent: int  # seconds
    submitted_at: datetime
    is_timeout: bool = False

class QuestionProgress(BaseModel):
    """Current question state in the interview"""
    question_id: int
    question_text: str
    skill: str
    difficulty: str
    time_limit: int  # seconds
    time_remaining: Optional[int] = None
    started_at: datetime

class InterviewSession(BaseModel):
    """Complete interview session"""
    session_id: str
    candidate_id: str
    candidate_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: SessionStatus
    total_questions: int
    current_question_index: int
    questions: List[Dict]  # List of questions from QuestionSet
    answers: List[Answer] = []
    current_question: Optional[QuestionProgress] = None

class SessionSummary(BaseModel):
    """Summary of completed interview session"""
    session_id: str
    candidate_name: str
    total_questions: int
    answered_questions: int
    total_time_spent: int  # seconds
    status: SessionStatus
    answers: List[Answer]
