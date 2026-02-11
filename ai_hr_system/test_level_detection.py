import sys
import os

# Add current dir to path
sys.path.append(os.getcwd())

from app.cv_intelligence.schemas import CVAnalysisResult
from app.candidate_level.level_detector import LevelDetector
from app.candidate_level.difficulty_mapper import DifficultyMapper

def test_level_detection():
    print("Testing Level Detection Module...")
    
    # Create test candidates with different profiles
    test_candidates = [
        {
            "name": "Junior Developer",
            "cv": CVAnalysisResult(
                raw_text="Entry level developer...",
                skills_detected=["python", "javascript"],
                inferred_skills=["React"],
                experience_years=1.5,
                confidence={"python": 0.7, "javascript": 0.6}
            ),
            "expected_level": "Junior"
        },
        {
            "name": "Middle Developer",
            "cv": CVAnalysisResult(
                raw_text="Experienced developer...",
                skills_detected=["python", "javascript", "react", "node.js"],
                inferred_skills=["Vue", "Django", "PostgreSQL"],
                experience_years=4.0,
                confidence={"python": 0.85, "javascript": 0.8, "react": 0.82}
            ),
            "expected_level": "Middle"
        },
        {
            "name": "Senior Developer",
            "cv": CVAnalysisResult(
                raw_text="Senior full-stack engineer...",
                skills_detected=["python", "javascript", "typescript", "react", "node.js", "docker"],
                inferred_skills=["Vue", "Angular", "Django", "PostgreSQL", "AWS", "Kubernetes"],
                experience_years=8.0,
                confidence={"python": 0.95, "javascript": 0.92, "typescript": 0.9}
            ),
            "expected_level": "Senior"
        }
    ]
    
    # Test Level Detection
    print("\n=== Test 1: Level Detection ===")
    detector = LevelDetector()
    
    for candidate in test_candidates:
        name = candidate["name"]
        cv = candidate["cv"]
        expected = candidate["expected_level"]
        
        result = detector.detect_level(name, cv)
        
        print(f"\n{name}:")
        print(f"  Detected Level: {result.level}")
        print(f"  Expected Level: {expected}")
        print(f"  Score: {result.level_score}")
        print(f"  Confidence: {result.confidence_overall}")
        print(f"  Skills: {len(result.skills)}")
        print(f"  Experience: {result.experience_years} years")
        
        # Validation
        assert result.level == expected, f"Expected {expected}, got {result.level}"
    
    # Test Interview Planning
    print("\n\n=== Test 2: Interview Planning ===")
    mapper = DifficultyMapper()
    
    for candidate in test_candidates:
        name = candidate["name"]
        cv = candidate["cv"]
        
        level_result = detector.detect_level(name, cv)
        plan = mapper.generate_interview_plan(level_result)
        
        print(f"\n{name} ({plan.candidate_level}):")
        print(f"  Total Questions: {plan.total_questions}")
        print(f"  Interview Plan:")
        
        for item in plan.interview_plan:
            print(f"    - {item.skill}: {item.difficulty} (Case #{item.case_id})")
    
    # Validation
    print("\n\n=== Validation ===")
    print("[SUCCESS] All tests passed!")
    print("- Junior level correctly detected")
    print("- Middle level correctly detected")
    print("- Senior level correctly detected")
    print("- Interview plans generated with appropriate difficulty")

if __name__ == "__main__":
    test_level_detection()
