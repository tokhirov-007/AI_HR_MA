import sys
import os
import time

# Add current dir to path
sys.path.append(os.getcwd())

from app.cv_intelligence.schemas import CVAnalysisResult
from app.candidate_level.level_detector import LevelDetector
from app.question_engine.question_selector import QuestionSelector
from app.interview_flow.session_manager import SessionManager

def test_interview_flow():
    print("Testing Interview Flow Module...")
    
    # Create test candidate
    cv_result = CVAnalysisResult(
        raw_text="Middle level developer...",
        skills_detected=["python", "javascript", "react"],
        inferred_skills=["Django"],
        experience_years=4.0,
        confidence={"python": 0.85, "javascript": 0.8}
    )
    
    # Detect level
    detector = LevelDetector()
    level_result = detector.detect_level("Test Candidate", cv_result)
    
    # Generate questions
    selector = QuestionSelector()
    question_set = selector.select_questions(level_result, max_total_questions=3)
    
    print(f"\n=== Test Setup ===")
    print(f"Candidate: {level_result.candidate_name}")
    print(f"Level: {level_result.level}")
    print(f"Questions: {question_set.total_questions}")
    
    # Create session
    manager = SessionManager()
    session = manager.create_session(
        candidate_id="test_001",
        candidate_name="Test Candidate",
        question_set=question_set
    )
    
    print(f"\n=== Test 1: Session Creation ===")
    print(f"Session ID: {session.session_id}")
    print(f"Status: {session.status}")
    print(f"Total Questions: {session.total_questions}")
    print(f"Current Question Index: {session.current_question_index}")
    
    # Validation
    assert session.status == "active", "Session should be active"
    assert session.total_questions == 3, "Should have 3 questions"
    assert session.current_question_index == 0, "Should start at question 0"
    assert session.current_question is not None, "Should have current question"
    
    print(f"\n=== Test 2: Question Flow ===")
    
    # Answer all questions
    for i in range(question_set.total_questions):
        # Get current question
        current_q = manager.get_current_question(session.session_id)
        
        print(f"\nQuestion {i+1}/{question_set.total_questions}:")
        print(f"  Skill: {current_q.skill}")
        print(f"  Difficulty: {current_q.difficulty}")
        print(f"  Time Limit: {current_q.time_limit}s")
        print(f"  Question: {current_q.question_text[:50]}...")
        
        # Simulate thinking time
        time.sleep(0.1)
        
        # Submit answer
        answer_text = f"This is my answer to question {current_q.question_id}"
        answer = manager.submit_answer(
            session_id=session.session_id,
            answer_text=answer_text
        )
        
        print(f"  Answer submitted: {answer.time_spent}s spent")
        print(f"  Timeout: {answer.is_timeout}")
        
        # Validation
        assert answer.question_id == current_q.question_id
        assert answer.answer_text == answer_text
        assert answer.time_spent >= 0
    
    print(f"\n=== Test 3: Session Completion ===")
    
    # Get final status
    final_session = manager.get_session_status(session.session_id)
    
    print(f"Final Status: {final_session.status}")
    print(f"Answered Questions: {len(final_session.answers)}")
    print(f"Current Question: {final_session.current_question}")
    
    # Validation
    assert final_session.status == "finished", "Session should be finished"
    assert len(final_session.answers) == 3, "Should have 3 answers"
    assert final_session.current_question is None, "Should have no current question"
    
    print(f"\n=== Test 4: Session Summary ===")
    
    # Get summary
    summary = manager.get_session_summary(session.session_id)
    
    print(f"Candidate: {summary.candidate_name}")
    print(f"Total Questions: {summary.total_questions}")
    print(f"Answered: {summary.answered_questions}")
    print(f"Total Time: {summary.total_time_spent}s")
    print(f"Status: {summary.status}")
    
    print(f"\nAnswers:")
    for i, ans in enumerate(summary.answers, 1):
        print(f"  {i}. Q{ans.question_id}: {ans.time_spent}s (timeout: {ans.is_timeout})")
    
    # Validation
    assert summary.total_questions == 3
    assert summary.answered_questions == 3
    assert summary.total_time_spent >= 0
    assert summary.status == "finished"
    
    print(f"\n=== Test 5: Timer Functionality ===")
    
    # Create new session to test timer
    session2 = manager.create_session(
        candidate_id="test_002",
        candidate_name="Timer Test",
        question_set=question_set
    )
    
    # Get current question
    q = manager.get_current_question(session2.session_id)
    initial_time = q.time_remaining
    
    print(f"Initial time remaining: {initial_time}s")
    
    # Wait at least 1 second to see the integer timer decrease
    time.sleep(1.2)
    
    # Check time again
    q2 = manager.get_current_question(session2.session_id)
    updated_time = q2.time_remaining
    
    print(f"After 1.2s: {updated_time}s remaining")
    
    # Validation
    assert updated_time < initial_time, f"Time should decrease. Initial: {initial_time}, Updated: {updated_time}"
    
    print("\n\n=== Validation ===")
    print("[SUCCESS] All tests passed!")
    print("- Session creation [OK]")
    print("- Question progression [OK]")
    print("- Answer submission [OK]")
    print("- Session completion [OK]")
    print("- Timer functionality [OK]")

if __name__ == "__main__":
    test_interview_flow()
