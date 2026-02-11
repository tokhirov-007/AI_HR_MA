import sys
import os

# Add current dir to path
sys.path.append(os.getcwd())

from app.cv_intelligence.schemas import CVAnalysisResult
from app.summary_engine.ai_summarizer import AISummarizer
from app.summary_engine.top_candidates import TopCandidatesRanker

def test_summary_engine():
    print("Testing Summary Engine...")
    
    # Create mock CV results for 3 candidates
    candidates_data = [
        {
            "candidate_name": "Ivan Petrov",
            "cv_result": CVAnalysisResult(
                raw_text="Experienced developer...",
                skills_detected=["python", "javascript", "react"],
                inferred_skills=["Vue", "Angular", "ES6+", "Django"],
                experience_years=5.0,
                confidence={"python": 0.9, "javascript": 0.85, "react": 0.8}
            )
        },
        {
            "candidate_name": "Maria Ivanova",
            "cv_result": CVAnalysisResult(
                raw_text="Full-stack engineer...",
                skills_detected=["python", "django", "postgresql", "docker"],
                inferred_skills=["Backend Development", "Database Design", "REST API"],
                experience_years=3.0,
                confidence={"python": 0.95, "django": 0.9}
            )
        },
        {
            "candidate_name": "Alex Smirnov",
            "cv_result": CVAnalysisResult(
                raw_text="Modern JS developer...",
                skills_detected=["javascript", "typescript", "react", "node.js"],
                inferred_skills=["Angular", "Vue", "ES6+", "Async/Await", "Frontend Development"],
                experience_years=7.0,
                confidence={"javascript": 0.92, "typescript": 0.88, "react": 0.9}
            )
        }
    ]
    
    # Test 1: Individual Summaries
    print("\n=== Test 1: Individual Summaries ===")
    summarizer = AISummarizer()
    
    for candidate in candidates_data:
        name = candidate["candidate_name"]
        cv_result = candidate["cv_result"]
        
        hr_summary = summarizer.generate_hr_summary(cv_result)
        tech_summary = summarizer.generate_technical_summary(cv_result)
        
        print(f"\n{name}:")
        print(f"  HR Summary: {hr_summary}")
        print(f"  Technical: {tech_summary}")
    
    # Test 2: Ranking
    print("\n\n=== Test 2: Candidate Ranking ===")
    ranker = TopCandidatesRanker()
    result = ranker.rank_candidates(candidates_data)
    
    print(f"Total Candidates: {result.total_candidates}")
    print("\nRanked List (Top to Bottom):")
    
    for i, candidate in enumerate(result.candidates, 1):
        print(f"\n{i}. {candidate.candidate_name} (Score: {candidate.total_score})")
        print(f"   Skills: {len(candidate.skills_detected + candidate.inferred_skills)}")
        print(f"   Experience: {candidate.experience_years} years")
        print(f"   HR Summary: {candidate.summary_hr}")
    
    # Validation
    print("\n\n=== Validation ===")
    assert result.total_candidates == 3, "Should have 3 candidates"
    assert result.candidates[0].total_score >= result.candidates[1].total_score, "Ranking should be descending"
    assert result.candidates[1].total_score >= result.candidates[2].total_score, "Ranking should be descending"
    
    print("[SUCCESS] All tests passed!")

if __name__ == "__main__":
    test_summary_engine()
