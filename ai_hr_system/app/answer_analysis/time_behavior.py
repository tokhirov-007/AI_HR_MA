from app.answer_analysis.schemas import AnalysisResult, AnalysisType

class TimeBehaviorAnalyzer:
    """
    Analyzes response timing patterns.
    Detects suspiciously fast or uniform response times.
    """

    def analyze(self, time_spent: int, difficulty: str, text_length: int) -> AnalysisResult:
        """
        Analyze timing behavior.
        
        Args:
            time_spent: seconds
            difficulty: easy/medium/hard
            text_length: length of answer in characters
        """
        flags = []
        score = 1.0 # 1.0 is healthy, lower is suspicious
        
        # 1. Absolute speed check
        # Hard questions answered in < 30s are highly suspect
        if difficulty == "hard" and time_spent < 45:
            flags.append("too_fast_for_hard_question")
            score *= 0.4
        
        if difficulty == "medium" and time_spent < 20:
            flags.append("too_fast_for_medium_question")
            score *= 0.5
            
        if time_spent < 10:
            flags.append("suspiciously_short_time")
            score *= 0.3

        # 2. Reading/Typing speed correlation
        # Average typing speed is ~40-60 wpm (approx 3-4 chars per sec)
        # If someone "typed" a 1000 char answer in 5 seconds...
        if time_spent > 0:
            cps = text_length / time_spent
            if cps > 30: # > 30 characters per second is very likely copy-paste
                flags.append("impossible_typing_speed")
                score *= 0.3
            elif cps > 15:
                flags.append("extremely_high_typing_speed")
                score *= 0.6

        return AnalysisResult(
            type=AnalysisType.TIME_BEHAVIOR,
            score=score,
            flags=flags,
            details={
                "time_spent": time_spent,
                "difficulty": difficulty,
                "chars_per_second": round(text_length / time_spent, 1) if time_spent > 0 else 999
            }
        )
