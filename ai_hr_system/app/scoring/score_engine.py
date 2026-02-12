from typing import List, Dict
from app.scoring.schemas import ScoreBreakdown
from app.scoring.weight_config import get_weights
from app.answer_analysis.schemas import FullIntegrityReport
from app.interview_flow.schemas import SessionSummary
import re

class ScoreEngine:
    """
    Combines technical evaluation, integrity, and behavioral data.
    """

    def calculate_technical_scores(self, summary: SessionSummary, questions: List[Dict]) -> Dict[str, float]:
        """
        Simulate technical scoring by checking for technical keywords 
        and expected topics in answers.
        """
        q_map = {q["id"]: q for q in questions}
        
        technical_scores = []
        problem_solving_scores = []

        for answer in summary.answers:
            q_data = q_map.get(answer.question_id, {})
            expected = q_data.get("expected_topics", [])
            
            if not answer.answer_text or answer.is_timeout:
                technical_scores.append(0.0)
                continue

            # 1. Knowledge Score: Topic matching
            matches = 0
            for topic in expected:
                if re.search(r'\b' + re.escape(topic.lower()) + r'\b', answer.answer_text.lower()):
                    matches += 1
            
            # Base score from topics
            knowledge_base = (matches / len(expected)) * 100 if expected else 50
            
            # Depth bonus (longer answers with technical words)
            technical_keywords = ["implementation", "performance", "complexity", "architecture", "pattern", "logic"]
            depth_bonus = sum(5 for word in technical_keywords if word in answer.answer_text.lower())
            
            knowledge_final = min(100.0, knowledge_base + depth_bonus)
            technical_scores.append(knowledge_final)

            # 2. Problem Solving Score (heuristic for case questions)
            is_case = q_data.get("type") == "case"
            if is_case:
                # Better score if they mention "trade-offs", "strategy", "solution"
                ps_markers = ["trade-off", "alternative", "depends", "strategy", "handling", "solution", "scale"]
                ps_matches = sum(10 for m in ps_markers if m in answer.answer_text.lower())
                problem_solving_scores.append(min(100.0, knowledge_base + ps_matches))
            else:
                problem_solving_scores.append(knowledge_final * 0.8) # Non-cases don't show full PS

        avg_knowledge = sum(technical_scores) / len(technical_scores) if technical_scores else 0
        avg_ps = sum(problem_solving_scores) / len(problem_solving_scores) if problem_solving_scores else 0
        
        return {
            "knowledge": avg_knowledge,
            "problem_solving": avg_ps
        }

    def aggregate(self, 
                  summary: SessionSummary, 
                  integrity_report: FullIntegrityReport,
                  questions: List[Dict]) -> ScoreBreakdown:
        """
        Aggregate all data into component scores.
        """
        tech = self.calculate_technical_scores(summary, questions)
        
        # Mapping integrity report results back to components
        honesty = integrity_report.overall_honesty_score * 100
        
        # Time behavior score from integrity results
        time_scores = []
        for ans_rep in integrity_report.answer_reports:
            for res in ans_rep.analysis_results:
                if res.type == "time_behavior":
                    time_scores.append(res.score * 100)
        
        avg_time_score = sum(time_scores) / len(time_scores) if time_scores else 50

        return ScoreBreakdown(
            knowledge_score=round(tech["knowledge"], 2),
            honesty_score=round(honesty, 2),
            time_behavior_score=round(avg_time_score, 2),
            problem_solving_score=round(tech["problem_solving"], 2)
        )

    def calculate_final_weighted_score(self, breakdown: ScoreBreakdown, difficulty_mix: str) -> int:
        """
        Calculate the 0-100 final score using difficulty-based weights.
        """
        weights = get_weights(difficulty_mix)
        
        final = (
            breakdown.knowledge_score * weights["knowledge"] +
            breakdown.honesty_score * weights["honesty"] +
            breakdown.time_behavior_score * weights["time"] +
            breakdown.problem_solving_score * weights["problem_solving"]
        )
        
        return int(round(final))
