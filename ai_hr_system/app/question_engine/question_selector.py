from app.question_engine.question_bank import QuestionBank
from app.question_engine.schemas import Question, QuestionType, DifficultyLevel, QuestionSet
from app.candidate_level.schemas import CandidateLevel, LevelDetectionResult
from typing import List
import random

class QuestionSelector:
    """
    Intelligently selects interview questions based on candidate skills and level.
    """
    
    def __init__(self):
        self.question_bank = QuestionBank()
        
        # Question distribution by level
        self.level_distribution = {
            CandidateLevel.JUNIOR: {
                "theory_ratio": 0.7,  # 70% theory
                "case_ratio": 0.3,    # 30% case
                "max_questions_per_skill": 1
            },
            CandidateLevel.MIDDLE: {
                "theory_ratio": 0.5,  # 50% theory
                "case_ratio": 0.5,    # 50% case
                "max_questions_per_skill": 2
            },
            CandidateLevel.SENIOR: {
                "theory_ratio": 0.3,  # 30% theory
                "case_ratio": 0.7,    # 70% case
                "max_questions_per_skill": 2
            }
        }
        
        # Difficulty mapping by level
        self.level_difficulty_map = {
            CandidateLevel.JUNIOR: DifficultyLevel.EASY,
            CandidateLevel.MIDDLE: DifficultyLevel.MEDIUM,
            CandidateLevel.SENIOR: DifficultyLevel.HARD
        }
    
    def select_questions(
        self, 
        level_result: LevelDetectionResult,
        max_total_questions: int = 5
    ) -> QuestionSet:
        """
        Select interview questions based on candidate level and skills.
        
        Rules:
        - Only select questions for skills the candidate has
        - Respect level-appropriate difficulty
        - Balance theory vs case questions
        - Limit questions per skill
        """
        candidate_level = level_result.level
        candidate_skills = [s.lower() for s in level_result.skills]
        
        distribution = self.level_distribution[candidate_level]
        base_difficulty = self.level_difficulty_map[candidate_level]
        
        selected_questions: List[Question] = []
        
        # Select questions for each skill
        for skill in candidate_skills:
            skill_questions = self._select_questions_for_skill(
                skill=skill,
                difficulty=base_difficulty,
                theory_ratio=distribution["theory_ratio"],
                max_questions=distribution["max_questions_per_skill"]
            )
            selected_questions.extend(skill_questions)
        
        # Limit total questions
        if len(selected_questions) > max_total_questions:
            selected_questions = selected_questions[:max_total_questions]
        
        return QuestionSet(
            candidate_name=level_result.candidate_name,
            candidate_level=str(candidate_level.value),
            questions=selected_questions,
            total_questions=len(selected_questions)
        )
    
    def _select_questions_for_skill(
        self,
        skill: str,
        difficulty: DifficultyLevel,
        theory_ratio: float,
        max_questions: int
    ) -> List[Question]:
        """
        Select questions for a specific skill.
        """
        # Get available questions for this skill and difficulty
        available_questions = self.question_bank.get_questions_by_skill_and_difficulty(
            skill, difficulty
        )
        
        if not available_questions:
            # No questions available for this skill/difficulty
            return []
        
        # Separate by type
        theory_questions = [q for q in available_questions if q.type == QuestionType.THEORY]
        case_questions = [q for q in available_questions if q.type == QuestionType.CASE]
        
        selected = []
        
        # Calculate how many of each type to select
        num_theory = int(max_questions * theory_ratio)
        num_case = max_questions - num_theory
        
        # Select theory questions
        if theory_questions and num_theory > 0:
            selected.extend(random.sample(
                theory_questions, 
                min(num_theory, len(theory_questions))
            ))
        
        # Select case questions
        if case_questions and num_case > 0:
            selected.extend(random.sample(
                case_questions,
                min(num_case, len(case_questions))
            ))
        
        return selected
