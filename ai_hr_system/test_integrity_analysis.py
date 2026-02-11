import sys
import os
from datetime import datetime

# Add current dir to path
sys.path.append(os.getcwd())

from app.answer_analysis.final_analyzer import FinalAnalyzer
from app.interview_flow.schemas import SessionSummary, Answer

def test_answer_analysis():
    print("Testing Answer Analysis Module (Integrity Checks)...")
    
    analyzer = FinalAnalyzer()
    
    # ---------------------------------------------------------
    # Scenario 1: The "Honest" Candidate
    # Simple answers, manual typing speed, logical structure
    # ---------------------------------------------------------
    honest_summary = SessionSummary(
        session_id="honest_001",
        candidate_name="Honest John",
        total_questions=2,
        answered_questions=2,
        total_time_spent=300,
        status="finished",
        answers=[
            Answer(
                question_id=1,
                answer_text="I think decorators in Python are just wrappers around functions. They allow you to add functionality. First, you define the wrapper, then you return it.",
                time_spent=120, # 2 minutes
                submitted_at=datetime.now(),
                is_timeout=False
            ),
            Answer(
                question_id=2,
                answer_text="React hooks are for managing state. For example, useState lets you keep data between renders. It's better than class components for many reasons.",
                time_spent=180, # 3 minutes
                submitted_at=datetime.now(),
                is_timeout=False
            )
        ]
    )
    
    q_data = [
        {"id": 1, "difficulty": "medium", "skill": "python"},
        {"id": 2, "difficulty": "medium", "skill": "react"}
    ]
    
    print("\n--- Testing Honest Candidate ---")
    report1 = analyzer.analyze_session(honest_summary, q_data)
    print(f"Overall Honesty Score: {report1.overall_honesty_score}")
    print(f"Global Flags: {report1.global_flags}")
    print(f"Recommendation: {report1.recommendation}")
    
    assert report1.overall_honesty_score > 0.7
    assert "HIGH_RISK_OF_CHEATING" not in report1.global_flags

    # ---------------------------------------------------------
    # Scenario 2: The "AI" Candidate
    # Perfect structure, high markers, extremely fast speed
    # ---------------------------------------------------------
    ai_summary = SessionSummary(
        session_id="ai_001",
        candidate_name="Bot Bob",
        total_questions=1,
        answered_questions=1,
        total_time_spent=10,
        status="finished",
        answers=[
            Answer(
                question_id=3,
                answer_text="""From a technical perspective, it's important to note that microservices architecture offers several key advantages:
1. Scalability: You can scale individual components independently.
2. Fault Isolation: A failure in one service does not bring down the entire system.
Furthermore, it is worth mentioning that deployment becomes more complex.""",
                time_spent=5, # Only 5 seconds for a long perfect answer
                submitted_at=datetime.now(),
                is_timeout=False
            )
        ]
    )
    
    q_data_ai = [{"id": 3, "difficulty": "hard", "skill": "architecture"}]
    
    print("\n--- Testing AI Candidate ---")
    report2 = analyzer.analyze_session(ai_summary, q_data_ai)
    print(f"Overall Honesty Score: {report2.overall_honesty_score}")
    print(f"Suspicious Count: {report2.suspicious_answers_count}")
    print(f"Individual Report Summary: {report2.answer_reports[0].summary}")
    
    # Check flags in the first answer
    ans_report = report2.answer_reports[0]
    ai_flags = [res.flags for res in ans_report.analysis_results if res.type == "ai_detection"][0]
    time_flags = [res.flags for res in ans_report.analysis_results if res.type == "time_behavior"][0]
    
    print(f"AI Detection Flags: {ai_flags}")
    print(f"Time Behavior Flags: {time_flags}")
    
    assert report2.overall_honesty_score < 0.5
    assert ans_report.is_suspicious is True
    assert "suspiciously_short_time" in time_flags or "too_fast_for_hard_question" in time_flags

    # ---------------------------------------------------------
    # Scenario 3: The "Copy-Paster"
    # Using known templates
    # ---------------------------------------------------------
    plag_summary = SessionSummary(
        session_id="plag_001",
        candidate_name="Copy Cat",
        total_questions=1,
        answered_questions=1,
        total_time_spent=60,
        status="finished",
        answers=[
            Answer(
                question_id=4,
                answer_text="In this example, we use a dictionary to keep track of elements. As per my knowledge, this is the most efficient way to handle this.",
                time_spent=60,
                submitted_at=datetime.now(),
                is_timeout=False
            )
        ]
    )
    
    print("\n--- Testing Plagiarism ---")
    report3 = analyzer.analyze_session(plag_summary, [{"id": 4, "difficulty": "easy"}])
    print(f"Overall Honesty Score: {report3.overall_honesty_score}")
    
    ans_report_plag = report3.answer_reports[0]
    plag_flags = [res.flags for res in ans_report_plag.analysis_results if res.type == "plagiarism"][0]
    print(f"Plagiarism Flags: {plag_flags}")
    
    assert "known_template_detected" in plag_flags

    print("\n\n=== Validation ===")
    print("[SUCCESS] All integrity analysis tests passed!")

if __name__ == "__main__":
    test_answer_analysis()
