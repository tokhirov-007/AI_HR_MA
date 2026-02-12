import sys
import os
from datetime import datetime

# Add current dir to path
sys.path.append(os.getcwd())

from app.scoring.score_engine import ScoreEngine
from app.scoring.recommendation import RecommendationEngine
from app.scoring.confidence_level import ConfidenceAnalyzer
from app.interview_flow.schemas import SessionSummary, Answer
from app.answer_analysis.schemas import FullIntegrityReport, AnswerIntegrityReport, AnalysisResult, AnalysisType

def test_final_scoring():
    print("Testing Final Scoring & Recommendation Module...")
    
    score_engine = ScoreEngine()
    rec_engine = RecommendationEngine()
    conf_analyzer = ConfidenceAnalyzer()
    
    # ---------------------------------------------------------
    # Scenario: The Rockstar Senior (High Skills, High Honesty)
    # ---------------------------------------------------------
    summary = SessionSummary(
        session_id="expert_001",
        candidate_name="Senior Dev",
        total_questions=2,
        answered_questions=2,
        total_time_spent=600,
        status="finished",
        answers=[
            Answer(
                question_id=1,
                answer_text="Implementation of microservices architecture requires careful orchestration. We use Kubernetes for deployment and focus on resilience through circuit breakers.",
                time_spent=300,
                submitted_at=datetime.now(),
                is_timeout=False
            ),
            Answer(
                question_id=2,
                answer_text="Performance optimization in Python involves profiling. Memory complexity can be managed with generators and efficient data structures like slots.",
                time_spent=300,
                submitted_at=datetime.now(),
                is_timeout=False
            )
        ]
    )
    
    q_data = [
        {"id": 1, "difficulty": "hard", "type": "technical", "expected_topics": ["microservices", "kubernetes", "resilience"]},
        {"id": 2, "difficulty": "hard", "type": "technical", "expected_topics": ["performance", "complexity", "generators"]}
    ]
    
    # Mock Integrity Report for Honest Senior
    integrity = FullIntegrityReport(
        session_id="expert_001",
        candidate_name="Senior Dev",
        overall_honesty_score=0.95,
        suspicious_answers_count=0,
        global_flags=[],
        answer_reports=[],
        recommendation="Trustworthy"
    )
    
    print("\n--- Testing Rockstar Senior ---")
    breakdown = score_engine.aggregate(summary, integrity, q_data)
    final_score = score_engine.calculate_final_weighted_score(breakdown, "hard")
    decision, reason = rec_engine.get_recommendation(final_score, breakdown, [])
    
    print(f"Knowledge Score: {breakdown.knowledge_score}")
    print(f"Honesty Score: {breakdown.honesty_score}")
    print(f"Final Weighted Score: {final_score}")
    print(f"Decision: {decision}")
    
    assert final_score > 80
    assert decision == "Strong Hire"

    # ---------------------------------------------------------
    # Scenario: The Suspect Pro (High Skills, Low Honesty)
    # ---------------------------------------------------------
    integrity_low = FullIntegrityReport(
        session_id="suspect_001",
        candidate_name="Smart Cheater",
        overall_honesty_score=0.3,
        suspicious_answers_count=2,
        global_flags=["HIGH_RISK_OF_CHEATING"],
        answer_reports=[],
        recommendation="Suspect"
    )
    
    print("\n--- Testing Suspect Expert ---")
    breakdown_suspect = score_engine.aggregate(summary, integrity_low, q_data)
    final_score_suspect = score_engine.calculate_final_weighted_score(breakdown_suspect, "hard")
    decision_suspect, reason_suspect = rec_engine.get_recommendation(final_score_suspect, breakdown_suspect, ["HIGH_RISK_OF_CHEATING"])
    
    print(f"Final Weighted Score: {final_score_suspect}")
    print(f"Decision: {decision_suspect}")
    print(f"Reason: {reason_suspect}")
    
    # Even if knowledge is 100, low honesty and high risk flags should lead to Review or Reject
    assert decision_suspect in ["Review", "Reject"]

    print("\n\n=== Validation ===")
    print("[SUCCESS] All scoring and recommendation tests passed!")

if __name__ == "__main__":
    test_final_scoring()
