from app.cv_intelligence.schemas import CVAnalysisResult
from app.summary_engine.schemas import CandidateSummary, TopCandidatesResponse
from app.summary_engine.ai_summarizer import AISummarizer
from typing import List

class TopCandidatesRanker:
    """
    Ranks candidates based on skills, experience, and confidence scores.
    """
    
    def __init__(self):
        self.summarizer = AISummarizer()
    
    def rank_candidates(self, candidates: List[dict]) -> TopCandidatesResponse:
        """
        Rank candidates and return sorted list.
        
        Args:
            candidates: List of dicts with 'name' and 'cv_result' (CVAnalysisResult)
        
        Returns:
            TopCandidatesResponse with ranked candidates
        """
        summaries = []
        
        for candidate in candidates:
            name = candidate.get("candidate_name", "Unknown")
            cv_result: CVAnalysisResult = candidate.get("cv_result")
            
            if not cv_result:
                continue
            
            # Generate summaries
            hr_summary = self.summarizer.generate_hr_summary(cv_result)
            tech_summary = self.summarizer.generate_technical_summary(cv_result)
            
            # Calculate score
            score = self._calculate_score(cv_result)
            
            summary = CandidateSummary(
                candidate_name=name,
                summary_hr=hr_summary,
                summary_technical=tech_summary,
                skills_detected=cv_result.skills_detected,
                inferred_skills=cv_result.inferred_skills,
                experience_years=cv_result.experience_years,
                confidence=cv_result.confidence,
                total_score=score
            )
            
            summaries.append(summary)
        
        # Sort by score (descending)
        summaries.sort(key=lambda x: x.total_score, reverse=True)
        
        return TopCandidatesResponse(
            candidates=summaries,
            total_candidates=len(summaries)
        )
    
    def _calculate_score(self, cv_result: CVAnalysisResult) -> float:
        """
        Calculate candidate score based on:
        - Number of skills (detected + inferred)
        - Years of experience
        - Average confidence
        - Skill diversity
        """
        score = 0.0
        
        # 1. Skills count (max 40 points)
        total_skills = len(set(cv_result.skills_detected + cv_result.inferred_skills))
        score += min(total_skills * 2, 40)
        
        # 2. Experience (max 30 points)
        years = cv_result.experience_years or 0
        score += min(years * 5, 30)
        
        # 3. Average confidence (max 20 points)
        if cv_result.confidence:
            avg_confidence = sum(cv_result.confidence.values()) / len(cv_result.confidence)
            score += avg_confidence * 20
        
        # 4. Skill diversity bonus (max 10 points)
        diversity_score = self._calculate_diversity(cv_result.skills_detected + cv_result.inferred_skills)
        score += diversity_score * 10
        
        return round(score, 2)
    
    def _calculate_diversity(self, skills: List[str]) -> float:
        """
        Calculate skill diversity (frontend + backend + devops + ai/ml).
        Returns 0.0 to 1.0
        """
        skills_lower = [s.lower() for s in skills]
        
        categories = {
            "frontend": ["react", "vue", "angular", "html", "css", "javascript", "typescript"],
            "backend": ["node.js", "python", "django", "flask", "fastapi", "java", "go"],
            "devops": ["docker", "kubernetes", "aws", "azure", "gcp", "ci/cd"],
            "ai_ml": ["machine learning", "tensorflow", "pytorch", "nlp"]
        }
        
        categories_covered = 0
        for category_skills in categories.values():
            if any(skill in skills_lower for skill in category_skills):
                categories_covered += 1
        
        return categories_covered / len(categories)
