import sys
import os
from datetime import datetime

# Add current dir to path
sys.path.append(os.getcwd())

from app.scoring.score_engine import ScoreEngine
from app.scoring.recommendation import RecommendationEngine
from app.scoring.confidence_level import ConfidenceAnalyzer
from app.scoring.schemas import FinalRecommendation
from app.interview_flow.schemas import SessionSummary, Answer
from app.answer_analysis.schemas import FullIntegrityReport

def test_serialization():
    print("Testing FinalRecommendation Serialization...")
    
    score_engine = ScoreEngine()
    rec_engine = RecommendationEngine()
    conf_analyzer = ConfidenceAnalyzer()
    
    summary = SessionSummary(
        session_id="test",
        candidate_name="test",
        total_questions=1,
        answered_questions=1,
        total_time_spent=100,
        status="finished",
        answers=[
            Answer(
                question_id=1,
                answer_text="Code implementation performance",
                time_spent=100,
                submitted_at=datetime.now(),
                is_timeout=False
            )
        ]
    )
    
    integrity = FullIntegrityReport(
        session_id="test",
        candidate_name="test",
        overall_honesty_score=0.9,
        suspicious_answers_count=0,
        global_flags=[],
        answer_reports=[],
        recommendation="Trustworthy"
    )
    
    questions = [{"id": 1, "difficulty": "medium", "expected_topics": ["code"]}]
    
    breakdown = score_engine.aggregate(summary, integrity, questions)
    final_score = score_engine.calculate_final_weighted_score(breakdown, "medium")
    decision, reason = rec_engine.get_recommendation(final_score, breakdown, [])
    hr_comment = rec_engine.generate_comment(decision, breakdown, [])
    
    confidence = conf_analyzer.calculate(1, 1, [100], 0)
    
    result = FinalRecommendation(
        session_id="test",
        candidate_name="test",
        final_score=final_score,
        decision=decision,
        confidence=confidence,
        hr_comment=hr_comment,
        score_breakdown=breakdown,
        flags=["flag1"],
        metadata={"key": "val"}
    )
    
    print("Object created successfully.")
    print(result.model_dump_json())
    print("Serialization successful.")

if __name__ == "__main__":
    test_serialization()
