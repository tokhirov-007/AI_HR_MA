from app.interview_flow.schemas import (
    InterviewSession,
    SessionStatus,
    QuestionProgress,
    Answer,
    SessionSummary
)
from app.interview_flow.timer import Timer
from app.interview_flow.answer_handler import AnswerHandler
from app.question_engine.schemas import QuestionSet
from datetime import datetime
from typing import Optional, Dict
import uuid

class SessionManager:
    """
    Manages interview sessions from start to finish.
    Orchestrates question flow, timing, and answer collection.
    """
    
    def __init__(self):
        # Store active sessions in memory
        # In production, this would be a database
        self.sessions: Dict[str, InterviewSession] = {}
        self.timers: Dict[str, Timer] = {}
        self.answer_handlers: Dict[str, AnswerHandler] = {}
    
    def create_session(
        self,
        candidate_id: str,
        candidate_name: str,
        question_set: QuestionSet
    ) -> InterviewSession:
        """
        Create a new interview session.
        
        Args:
            candidate_id: Unique candidate identifier
            candidate_name: Candidate name
            question_set: Set of questions from question engine
        
        Returns:
            InterviewSession object
        """
        session_id = str(uuid.uuid4())
        
        # Convert questions to dict format
        questions = [q.dict() for q in question_set.questions]
        
        # Create session
        session = InterviewSession(
            session_id=session_id,
            candidate_id=candidate_id,
            candidate_name=candidate_name,
            start_time=datetime.now(),
            status=SessionStatus.ACTIVE,
            total_questions=len(questions),
            current_question_index=0,
            questions=questions,
            answers=[],
            current_question=None
        )
        
        # Store session
        self.sessions[session_id] = session
        self.answer_handlers[session_id] = AnswerHandler()
        
        # Start first question
        self._start_next_question(session_id)
        
        return session
    
    def get_current_question(self, session_id: str) -> Optional[QuestionProgress]:
        """
        Get the current question for a session.
        
        Args:
            session_id: Session ID
        
        Returns:
            QuestionProgress or None
        """
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        if session.status != SessionStatus.ACTIVE:
            return None
        
        # Update time remaining
        if session.current_question and session_id in self.timers:
            timer = self.timers[session_id]
            session.current_question.time_remaining = timer.get_time_remaining()
        
        return session.current_question
    
    def submit_answer(
        self,
        session_id: str,
        answer_text: str
    ) -> Answer:
        """
        Submit answer for current question and move to next.
        
        Args:
            session_id: Session ID
            answer_text: Candidate's answer
        
        Returns:
            Answer object
        """
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        if session.status != SessionStatus.ACTIVE:
            raise ValueError(f"Session {session_id} is not active")
        
        if not session.current_question:
            raise ValueError("No active question")
        
        # Stop timer
        timer = self.timers.get(session_id)
        if not timer:
            raise ValueError("Timer not found")
        
        time_spent = timer.stop()
        is_timeout = timer.is_timeout()
        
        # Submit answer
        answer_handler = self.answer_handlers[session_id]
        answer = answer_handler.submit_answer(
            question_id=session.current_question.question_id,
            answer_text=answer_text,
            time_spent=time_spent,
            is_timeout=is_timeout
        )
        
        # Add to session
        session.answers.append(answer)
        
        # Move to next question
        session.current_question_index += 1
        
        if session.current_question_index >= session.total_questions:
            # Interview finished
            self._finish_session(session_id)
        else:
            # Start next question
            self._start_next_question(session_id)
        
        return answer
    
    def get_session_status(self, session_id: str) -> InterviewSession:
        """
        Get current session status.
        
        Args:
            session_id: Session ID
        
        Returns:
            InterviewSession object
        """
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Update current question time if active
        if session.status == SessionStatus.ACTIVE and session.current_question:
            timer = self.timers.get(session_id)
            if timer:
                session.current_question.time_remaining = timer.get_time_remaining()
        
        return session
    
    def get_session_summary(self, session_id: str) -> SessionSummary:
        """
        Get summary of completed session.
        
        Args:
            session_id: Session ID
        
        Returns:
            SessionSummary object
        """
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        answer_handler = self.answer_handlers.get(session_id)
        total_time = answer_handler.get_total_time_spent() if answer_handler else 0
        
        return SessionSummary(
            session_id=session.session_id,
            candidate_name=session.candidate_name,
            total_questions=session.total_questions,
            answered_questions=len(session.answers),
            total_time_spent=total_time,
            status=session.status,
            answers=session.answers
        )
    
    def _start_next_question(self, session_id: str):
        """Start the next question in the session"""
        session = self.sessions[session_id]
        
        if session.current_question_index >= len(session.questions):
            return
        
        # Get next question
        question_data = session.questions[session.current_question_index]
        
        # Create question progress
        question_progress = QuestionProgress(
            question_id=question_data["id"],
            question_text=question_data["question"],
            skill=question_data["skill"],
            difficulty=question_data["difficulty"],
            time_limit=Timer.get_time_limit(question_data["difficulty"]),
            started_at=datetime.now()
        )
        
        # Start timer
        timer = Timer(question_data["difficulty"])
        timer.start()
        self.timers[session_id] = timer
        
        # Update session
        session.current_question = question_progress
    
    def _finish_session(self, session_id: str):
        """Mark session as finished"""
        session = self.sessions[session_id]
        session.status = SessionStatus.FINISHED
        session.end_time = datetime.now()
        session.current_question = None
        
        # Clean up timer
        if session_id in self.timers:
            del self.timers[session_id]
