from typing import List, Dict
import statistics
from app.answer_analysis.schemas import (
    AnalysisResult,
    AnalysisType,
    AnswerIntegrityReport,
    FullIntegrityReport
)
from app.answer_analysis.ai_detector import AIDetector
from app.answer_analysis.structure_analyzer import StructureAnalyzer
from app.answer_analysis.time_behavior import TimeBehaviorAnalyzer
from app.answer_analysis.plagiarism_checker import PlagiarismChecker
from app.interview_flow.schemas import SessionSummary, Answer

class FinalAnalyzer:
    """
    Orchestrator for candidate answer integrity analysis.
    Aggregates results from multiple specialized analyzers.
    """

    def __init__(self):
        self.ai_detector = AIDetector()
        self.structure_analyzer = StructureAnalyzer()
        self.time_analyzer = TimeBehaviorAnalyzer()
        self.plagiarism_checker = PlagiarismChecker()

    def analyze_session(self, session_summary: SessionSummary, questions_data: List[Dict]) -> FullIntegrityReport:
        """
        Analyze all answers in a session for integrity and honesty.
        """
        answer_reports = []
        previous_texts = []
        
        # Maps question_id to difficulty for easier lookup
        question_map = {q["id"]: q for q in questions_data}

        for answer in session_summary.answers:
            q_data = question_map.get(answer.question_id, {"difficulty": "medium"})
            
            # 1. Run individual analyzers
            ai_res = self.ai_detector.analyze(answer.answer_text)
            struct_res = self.structure_analyzer.analyze(answer.answer_text)
            time_res = self.time_analyzer.analyze(
                time_spent=answer.time_spent,
                difficulty=q_data["difficulty"],
                text_length=len(answer.answer_text)
            )
            plag_res = self.plagiarism_checker.analyze(
                answer.answer_text, 
                previous_answers=previous_texts
            )
            
            previous_texts.append(answer.answer_text)
            
            # 2. Calculate Answer Honesty Score (Weighted)
            # Higher is better (more honest)
            # AI Probability and Plagiarism lower the score
            # Time and Structure influence it as indicators
            
            # Penalty factors (invert probability for honesty score)
            ai_penalty = 1.0 - ai_res.score
            plag_penalty = 1.0 - plag_res.score
            
            # Weighted average for honesty
            # 40% AI Probability, 30% Plagiarism, 20% Timing, 10% Structure validity
            honesty_score = (
                (ai_penalty * 0.4) + 
                (plag_penalty * 0.3) + 
                (time_res.score * 0.2) + 
                (struct_res.score * 0.1)
            )
            
            # 3. Create individual report
            all_results = [ai_res, struct_res, time_res, plag_res]
            all_flags = []
            for r in all_results:
                all_flags.extend(r.flags)
                
            is_suspicious = honesty_score < 0.6 or ai_res.score > 0.7 or plag_res.score > 0.7
            
            # Generate summary text
            if is_suspicious:
                summary = "Suspicious activity detected: " + ", ".join(list(set(all_flags))[:3])
            else:
                summary = "Answer looks authentic and manually written."

            report = AnswerIntegrityReport(
                question_id=answer.question_id,
                honesty_score=round(honesty_score, 2),
                is_suspicious=is_suspicious,
                ai_probability=ai_res.score,
                analysis_results=all_results,
                summary=summary
            )
            answer_reports.append(report)

        # 4. Final Aggregation
        overall_honesty = statistics.mean([r.honesty_score for r in answer_reports]) if answer_reports else 1.0
        suspicious_count = sum(1 for r in answer_reports if r.is_suspicious)
        
        # Global Flags
        global_flags = []
        if overall_honesty < 0.5:
            global_flags.append("HIGH_RISK_OF_CHEATING")
        if suspicious_count > len(answer_reports) / 2:
            global_flags.append("SYSTEMIC_AI_USAGE_LIKELY")

        # Recommendation
        if overall_honesty > 0.8:
            rec = "Highly Trustworthy: The candidate answered naturally and manually."
        elif overall_honesty > 0.6:
            rec = "Mostly Honest: Some flags detected, but likely minor assistance or fast typing."
        elif overall_honesty > 0.4:
            rec = "Suspect: Significant indicators of AI assistance or automated tools."
        else:
            rec = "Risk: Strong probability of systemic cheating. Human review recommended."

        return FullIntegrityReport(
            session_id=session_summary.session_id,
            candidate_name=session_summary.candidate_name,
            overall_honesty_score=round(overall_honesty, 2),
            suspicious_answers_count=suspicious_count,
            global_flags=global_flags,
            answer_reports=answer_reports,
            recommendation=rec
        )
