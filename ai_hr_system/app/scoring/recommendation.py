from typing import List
from app.scoring.schemas import RecommendationLevel, ScoreBreakdown

class RecommendationEngine:
    """
    Generates human-readable HR recommendations based on scores and flags.
    """

    def get_recommendation(self, 
                           score: int, 
                           breakdown: ScoreBreakdown, 
                           flags: List[str]) -> tuple[RecommendationLevel, str]:
        """
        Determine recommendation level and descriptive reason.
        """
        
        # 🟢 Decision Matrix
        if score >= 85:
            if breakdown.honesty_score < 60:
                return RecommendationLevel.REVIEW, "Excellent technical knowledge, but significant integrity flags require human verification."
            return RecommendationLevel.STRONG_HIRE, "Exceptional candidate with strong technical depth and authentic communication."
            
        elif score >= 70:
            if breakdown.honesty_score < 50:
                return RecommendationLevel.REVIEW, "Good technical level, but low honesty score suggests potential AI usage or copy-pasting."
            return RecommendationLevel.HIRE, "Solid technical foundation. The candidate displays clear competence in the required skills."
            
        elif score >= 50:
            if "HIGH_RISK_OF_CHEATING" in flags:
                return RecommendationLevel.REJECT, "Candidate showed borderline performance and multiple serious integrity violations."
            return RecommendationLevel.REVIEW, "Average performance. May need additional training or a follow-up interview for clarification."
            
        else:
            reason = "Score is below the required threshold for this position."
            if breakdown.knowledge_score < 40:
                reason = "Insufficient technical knowledge demonstrated during the interview."
            return RecommendationLevel.REJECT, f"Does not meet current requirements. {reason}"

    def generate_comment(self, 
                         level: RecommendationLevel, 
                         breakdown: ScoreBreakdown, 
                         flags: List[str]) -> str:
        """
        Generate a qualitative HR comment.
        """
        comments = []
        
        # Technical part
        if breakdown.knowledge_score > 80:
            comments.append("Demonstrates mastery of core concepts.")
        elif breakdown.knowledge_score > 60:
            comments.append("Shows decent understanding of the stack.")
            
        # Integrity part
        if breakdown.honesty_score < 60:
            comments.append("Note: Answers show patterns consistent with AI assistance.")
        elif breakdown.honesty_score > 90:
            comments.append("Answers appear highly authentic and spontaneous.")
            
        # Behavioral part
        if breakdown.time_behavior_score < 50:
            comments.append("Responses given suspiciously fast for the complexity.")
            
        if not comments:
            comments.append("Standard performance across all metrics.")
            
        return " ".join(comments)
