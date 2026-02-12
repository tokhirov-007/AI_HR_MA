from typing import List
from app.scoring.schemas import ConfidenceLevel

class ConfidenceAnalyzer:
    """
    Determines how reliable the interview data is.
    """

    def calculate(self, 
                  total_questions: int, 
                  answered_questions: int, 
                  answer_lengths: List[int],
                  suspicious_count: int) -> ConfidenceLevel:
        """
        Calculates confidence in the result.
        """
        if total_questions == 0:
            return ConfidenceLevel.LOW
            
        rate = answered_questions / total_questions
        
        # Factors that lower confidence:
        # 1. Very few questions
        # 2. Many skipped questions
        # 3. Very short answers
        # 4. High suspicious activity (integrity issues make the technical score less reliable)
        
        points = 100
        
        # Question count penalty
        if total_questions < 3:
            points -= 40
        elif total_questions < 5:
            points -= 20
            
        # Completion rate penalty
        if rate < 0.5:
            points -= 50
        elif rate < 0.8:
            points -= 20
            
        # Answer depth penalty
        avg_len = sum(answer_lengths) / len(answer_lengths) if answer_lengths else 0
        if avg_len < 20:
            points -= 30
            
        # Suspicion penalty
        if suspicious_count > 0:
            points -= (suspicious_count * 15)

        if points >= 80:
            return ConfidenceLevel.HIGH
        elif points >= 50:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
