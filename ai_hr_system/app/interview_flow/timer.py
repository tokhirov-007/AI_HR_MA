from datetime import datetime, timedelta
from typing import Optional

class Timer:
    """
    Timer for tracking time limits on interview questions.
    """
    
    # Time limits by difficulty (in seconds)
    TIME_LIMITS = {
        "easy": 300,    # 5 minutes
        "medium": 600,  # 10 minutes
        "hard": 900     # 15 minutes
    }
    
    def __init__(self, difficulty: str):
        """
        Initialize timer with difficulty-based time limit.
        
        Args:
            difficulty: Question difficulty (easy/medium/hard)
        """
        self.difficulty = difficulty.lower()
        self.time_limit = self.TIME_LIMITS.get(self.difficulty, 600)  # Default 10 min
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
    
    def start(self):
        """Start the timer"""
        self.start_time = datetime.now()
        self.end_time = None
    
    def stop(self) -> int:
        """
        Stop the timer and return time spent.
        
        Returns:
            Time spent in seconds
        """
        if not self.start_time:
            return 0
        
        self.end_time = datetime.now()
        return self.get_time_spent()
    
    def get_time_spent(self) -> int:
        """
        Get time spent so far.
        
        Returns:
            Time spent in seconds
        """
        if not self.start_time:
            return 0
        
        end = self.end_time or datetime.now()
        delta = end - self.start_time
        return int(delta.total_seconds())
    
    def get_time_remaining(self) -> int:
        """
        Get time remaining.
        
        Returns:
            Time remaining in seconds (0 if timeout)
        """
        if not self.start_time:
            return self.time_limit
        
        time_spent = self.get_time_spent()
        remaining = self.time_limit - time_spent
        return max(0, remaining)
    
    def is_timeout(self) -> bool:
        """
        Check if time limit has been exceeded.
        
        Returns:
            True if timeout, False otherwise
        """
        return self.get_time_remaining() == 0
    
    @staticmethod
    def get_time_limit(difficulty: str) -> int:
        """
        Get time limit for a difficulty level.
        
        Args:
            difficulty: Question difficulty
        
        Returns:
            Time limit in seconds
        """
        return Timer.TIME_LIMITS.get(difficulty.lower(), 600)
