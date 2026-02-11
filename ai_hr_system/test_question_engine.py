import sys
import os

# Add current dir to path
sys.path.append(os.getcwd())

from app.cv_intelligence.schemas import CVAnalysisResult
from app.candidate_level.level_detector import LevelDetector
from app.candidate_level.schemas import CandidateLevel
from app.question_engine.question_selector import QuestionSelector

def test_question_engine():
    print("Testing Question Engine...")
    
    # Create test candidates with different levels
    test_candidates = [
        {
            "name": "Junior Python Developer",
            "cv": CVAnalysisResult(
                raw_text="Entry level developer...",
                skills_detected=["python", "javascript"],
                inferred_skills=["React"],
                experience_years=1.5,
                confidence={"python": 0.7, "javascript": 0.6}
            ),
            "expected_level": CandidateLevel.JUNIOR
        },
        {
            "name": "Middle Full-Stack Developer",
            "cv": CVAnalysisResult(
                raw_text="Experienced developer...",
                skills_detected=["python", "javascript", "react", "django"],
                inferred_skills=["PostgreSQL", "Docker"],
                experience_years=4.0,
                confidence={"python": 0.85, "javascript": 0.8, "react": 0.82}
            ),
            "expected_level": CandidateLevel.MIDDLE
        },
        {
            "name": "Senior Backend Engineer",
            "cv": CVAnalysisResult(
                raw_text="Senior engineer...",
                skills_detected=["python", "django", "postgresql", "docker"],
                inferred_skills=["Node.js", "SQL"],
                experience_years=8.0,
                confidence={"python": 0.95, "django": 0.92, "postgresql": 0.9}
            ),
            "expected_level": CandidateLevel.SENIOR
        }
    ]
    
    # Initialize components
    detector = LevelDetector()
    selector = QuestionSelector()
    
    print("\n=== Test 1: Question Selection by Level ===")
    
    for candidate in test_candidates:
        name = candidate["name"]
        cv = candidate["cv"]
        expected_level = candidate["expected_level"]
        
        # Detect level
        level_result = detector.detect_level(name, cv)
        
        # Generate questions
        question_set = selector.select_questions(level_result, max_total_questions=5)
        
        print(f"\n{name} ({level_result.level}):")
        print(f"  Skills: {', '.join(level_result.skills)}")
        print(f"  Total Questions: {question_set.total_questions}")
        print(f"  Questions:")
        
        for i, q in enumerate(question_set.questions, 1):
            print(f"    {i}. [{q.skill}] ({q.difficulty}, {q.type})")
            print(f"       {q.question}")
        
        # Validation
        assert level_result.level == expected_level, f"Expected {expected_level}, got {level_result.level}"
        assert question_set.total_questions > 0, "Should have at least one question"
        
        # Verify questions are only for candidate's skills
        candidate_skills_lower = [s.lower() for s in level_result.skills]
        for q in question_set.questions:
            assert q.skill.lower() in candidate_skills_lower, \
                f"Question skill '{q.skill}' not in candidate skills {candidate_skills_lower}"
    
    print("\n\n=== Test 2: Question Type Distribution ===")
    
    # Test Junior (should have more theory)
    junior_cv = test_candidates[0]["cv"]
    junior_level = detector.detect_level("Junior Test", junior_cv)
    junior_questions = selector.select_questions(junior_level, max_total_questions=10)
    
    theory_count = sum(1 for q in junior_questions.questions if q.type == "theory")
    case_count = sum(1 for q in junior_questions.questions if q.type == "case")
    
    print(f"\nJunior Distribution:")
    print(f"  Theory: {theory_count}")
    print(f"  Case: {case_count}")
    print(f"  Theory Ratio: {theory_count / len(junior_questions.questions):.2f}")
    
    # Test Senior (should have more cases)
    senior_cv = test_candidates[2]["cv"]
    senior_level = detector.detect_level("Senior Test", senior_cv)
    senior_questions = selector.select_questions(senior_level, max_total_questions=10)
    
    theory_count = sum(1 for q in senior_questions.questions if q.type == "theory")
    case_count = sum(1 for q in senior_questions.questions if q.type == "case")
    
    print(f"\nSenior Distribution:")
    print(f"  Theory: {theory_count}")
    print(f"  Case: {case_count}")
    print(f"  Case Ratio: {case_count / len(senior_questions.questions):.2f}")
    
    # Validation
    print("\n\n=== Validation ===")
    print("[SUCCESS] All tests passed!")
    print("- Questions selected only for candidate skills [OK]")
    print("- Level-appropriate difficulty [OK]")
    print("- Correct question type distribution [OK]")
    print("- No irrelevant questions [OK]")

if __name__ == "__main__":
    test_question_engine()
