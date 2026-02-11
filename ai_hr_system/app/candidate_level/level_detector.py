from app.cv_intelligence.schemas import CVAnalysisResult
from app.summary_engine.schemas import CandidateSummary
from app.candidate_level.schemas import CandidateLevel, LevelDetectionResult
from typing import Optional

class LevelDetector:
    """
    Determines candidate seniority level based on CV analysis and summary.
    
    Levels:
    - Junior: 0-3 years, limited skills, basic confidence
    - Middle: 3-5 years, diverse skills, good confidence
    - Senior: 5+ years, extensive skills, high confidence
    """
    
    def __init__(self):
        # Scoring weights
        self.weights = {
            "experience": 0.40,  # 40% weight
            "skills_count": 0.30,  # 30% weight
            "confidence": 0.20,  # 20% weight
            "diversity": 0.10   # 10% weight
        }
        
        # Level thresholds (0-100 scale)
        # Adjusted for more realistic classification
        self.thresholds = {
            CandidateLevel.JUNIOR: (0, 45),
            CandidateLevel.MIDDLE: (45, 75),
            CandidateLevel.SENIOR: (75, 100)
        }
    
    def detect_level(
        self, 
        candidate_name: str,
        cv_result: CVAnalysisResult,
        summary: Optional[CandidateSummary] = None
    ) -> LevelDetectionResult:
        """
        Detect candidate level from CV analysis and optional summary.
        """
        # Calculate component scores
        experience_score = self._score_experience(cv_result.experience_years or 0)
        skills_score = self._score_skills(cv_result.skills_detected + cv_result.inferred_skills)
        confidence_score = self._score_confidence(cv_result.confidence)
        diversity_score = self._score_diversity(cv_result.skills_detected + cv_result.inferred_skills)
        
        # Weighted total score (0-100)
        total_score = (
            experience_score * self.weights["experience"] +
            skills_score * self.weights["skills_count"] +
            confidence_score * self.weights["confidence"] +
            diversity_score * self.weights["diversity"]
        ) * 100
        
        # Determine level
        level = self._score_to_level(total_score)
        
        # Calculate confidence (how close to threshold boundaries)
        confidence = self._calculate_confidence(total_score, level)
        
        all_skills = list(set(cv_result.skills_detected + cv_result.inferred_skills))
        
        return LevelDetectionResult(
            candidate_name=candidate_name,
            level=level,
            confidence_overall=round(confidence, 2),
            skills=all_skills,
            experience_years=cv_result.experience_years,
            level_score=round(total_score, 2)
        )
    
    def _score_experience(self, years: float) -> float:
        """Score experience (0-1 scale)"""
        if years <= 1:
            return 0.1
        elif years <= 3:
            return 0.3
        elif years <= 5:
            return 0.6
        elif years <= 7:
            return 0.8
        else:
            return 1.0
    
    def _score_skills(self, skills: list) -> float:
        """Score based on number of skills (0-1 scale)"""
        skill_count = len(set(skills))
        if skill_count <= 3:
            return 0.2
        elif skill_count <= 6:
            return 0.5
        elif skill_count <= 10:
            return 0.8
        else:
            return 1.0
    
    def _score_confidence(self, confidence_dict: dict) -> float:
        """Score based on average confidence (0-1 scale)"""
        if not confidence_dict:
            return 0.5  # Default
        
        avg_confidence = sum(confidence_dict.values()) / len(confidence_dict)
        return avg_confidence
    
    def _score_diversity(self, skills: list) -> float:
        """Score based on skill diversity (0-1 scale)"""
        skills_lower = [s.lower() for s in skills]
        
        categories = {
            "frontend": ["react", "vue", "angular", "html", "css", "javascript", "typescript"],
            "backend": ["node.js", "python", "django", "flask", "java", "go", "php"],
            "database": ["sql", "postgresql", "mysql", "mongodb", "redis"],
            "devops": ["docker", "kubernetes", "aws", "azure", "ci/cd"]
        }
        
        categories_covered = 0
        for category_skills in categories.values():
            if any(skill in skills_lower for skill in category_skills):
                categories_covered += 1
        
        return categories_covered / len(categories)
    
    def _score_to_level(self, score: float) -> CandidateLevel:
        """Convert score to level"""
        for level, (min_score, max_score) in self.thresholds.items():
            if min_score <= score < max_score:
                return level
        
        # If score >= 100, return Senior
        return CandidateLevel.SENIOR
    
    def _calculate_confidence(self, score: float, level: CandidateLevel) -> float:
        """
        Calculate confidence based on distance from threshold boundaries.
        Higher confidence when far from boundaries.
        """
        min_score, max_score = self.thresholds[level]
        range_size = max_score - min_score
        
        # Distance from nearest boundary
        distance_from_min = score - min_score
        distance_from_max = max_score - score
        min_distance = min(distance_from_min, distance_from_max)
        
        # Normalize to 0-1
        confidence = min_distance / (range_size / 2)
        
        return min(confidence, 1.0)
