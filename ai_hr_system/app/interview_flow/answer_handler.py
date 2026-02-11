from app.interview_flow.schemas import Answer
from datetime import datetime
from typing import List

class AnswerHandler:
    """
    Handles answer submission and storage.
    No evaluation or scoring - just storage.
    """
    
    def __init__(self):
        self.answers: List[Answer] = []
    
    def submit_answer(
        self,
        question_id: int,
        answer_text: str,
        time_spent: int,
        is_timeout: bool = False
    ) -> Answer:
        """
        Submit and store an answer.
        
        Args:
            question_id: ID of the question
            answer_text: Candidate's answer
            time_spent: Time spent in seconds
            is_timeout: Whether answer was submitted due to timeout
        
        Returns:
            Answer object
        """
        # Validate answer
        if not answer_text or not answer_text.strip():
            raise ValueError("Answer cannot be empty")
        
        # Create answer
        answer = Answer(
            question_id=question_id,
            answer_text=answer_text.strip(),
            time_spent=time_spent,
            submitted_at=datetime.now(),
            is_timeout=is_timeout
        )
        
        # Store answer
        self.answers.append(answer)
        
        return answer
    
    def get_answers(self) -> List[Answer]:
        """
        Get all submitted answers.
        
        Returns:
            List of answers
        """
        return self.answers
    
    def get_answer_by_question_id(self, question_id: int) -> Answer:
        """
        Get answer for a specific question.
        
        Args:
            question_id: Question ID
        
        Returns:
            Answer or None if not found
        """
        for answer in self.answers:
            if answer.question_id == question_id:
                return answer
        return None
    
    def get_total_time_spent(self) -> int:
        """
        Get total time spent on all questions.
        
        Returns:
            Total time in seconds
        """
        return sum(answer.time_spent for answer in self.answers)
