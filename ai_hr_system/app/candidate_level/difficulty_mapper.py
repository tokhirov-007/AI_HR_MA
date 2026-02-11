from app.candidate_level.schemas import (
    CandidateLevel, 
    DifficultyLevel, 
    SkillDifficulty, 
    InterviewPlan,
    LevelDetectionResult
)
from typing import List
import random

class DifficultyMapper:
    """
    Maps candidate level to appropriate question difficulty for each skill.
    """
    
    def __init__(self):
        # Level to difficulty mapping
        self.level_difficulty_map = {
            CandidateLevel.JUNIOR: DifficultyLevel.EASY,
            CandidateLevel.MIDDLE: DifficultyLevel.MEDIUM,
            CandidateLevel.SENIOR: DifficultyLevel.HARD
        }
        
        # Maximum questions per interview
        self.max_questions = 5
    
    def generate_interview_plan(
        self, 
        level_result: LevelDetectionResult
    ) -> InterviewPlan:
        """
        Generate interview plan with difficulty-mapped questions.
        
        Args:
            level_result: Result from LevelDetector
        
        Returns:
            InterviewPlan with skills and difficulty assignments
        """
        candidate_level = level_result.level
        skills = level_result.skills
        
        # Get base difficulty for this level
        base_difficulty = self.level_difficulty_map[candidate_level]
        
        # Select top skills (limit to max_questions)
        selected_skills = self._select_top_skills(skills)
        
        # Create interview plan
        interview_items = []
        for skill in selected_skills:
            # Assign difficulty (could be customized per skill)
            difficulty = self._assign_difficulty(skill, candidate_level)
            
            # Generate simulated case ID
            case_id = self._generate_case_id(skill, difficulty)
            
            interview_items.append(
                SkillDifficulty(
                    skill=skill,
                    difficulty=difficulty,
                    case_id=case_id
                )
            )
        
        return InterviewPlan(
            candidate_name=level_result.candidate_name,
            candidate_level=candidate_level,
            interview_plan=interview_items,
            total_questions=len(interview_items)
        )
    
    def _select_top_skills(self, skills: List[str]) -> List[str]:
        """
        Select top skills for interview (limit to max_questions).
        Prioritizes diverse skills.
        """
        if len(skills) <= self.max_questions:
            return skills
        
        # Simple selection: take first N skills
        # In production, could prioritize based on job requirements
        return skills[:self.max_questions]
    
    def _assign_difficulty(
        self, 
        skill: str, 
        level: CandidateLevel
    ) -> DifficultyLevel:
        """
        Assign difficulty for a specific skill based on candidate level.
        
        Could be customized to:
        - Make core skills harder
        - Make secondary skills easier
        - Adjust based on confidence scores
        """
        # For now, use base difficulty from level
        return self.level_difficulty_map[level]
    
    def _generate_case_id(self, skill: str, difficulty: DifficultyLevel) -> int:
        """
        Generate simulated case ID.
        In production, this would query a question database.
        """
        # Simulate case IDs based on skill hash and difficulty
        skill_hash = hash(skill.lower()) % 100
        difficulty_offset = {
            DifficultyLevel.EASY: 0,
            DifficultyLevel.MEDIUM: 100,
            DifficultyLevel.HARD: 200
        }[difficulty]
        
        return skill_hash + difficulty_offset
