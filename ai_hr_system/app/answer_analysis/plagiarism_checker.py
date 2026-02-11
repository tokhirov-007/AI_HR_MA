import difflib
from typing import List
from app.answer_analysis.schemas import AnalysisResult, AnalysisType

class PlagiarismChecker:
    """
    Simple plagiarism checker to detect templated answers or repetitions.
    """
    
    # Common templated structures found on the web for dev interviews
    TEMPLATES = [
        "In this example, we use a dictionary to keep track of elements.",
        "As per my knowledge, this is the most efficient way to handle this.",
        "The first thing to consider is the time complexity of the operation.",
        "Typically, we would use a library like Redux for state management.",
        "Let's break down the problem into smaller components."
    ]

    def analyze(self, text: str, previous_answers: List[str] = None) -> AnalysisResult:
        flags = []
        plagiarism_prob = 0.0
        
        # 1. Check against templates
        for template in self.TEMPLATES:
            text_lower = text.lower()
            temp_lower = template.lower()
            
            # Direct substring match
            if temp_lower in text_lower:
                flags.append("known_template_detected")
                plagiarism_prob = max(plagiarism_prob, 0.9)
                continue
                
            # Fuzzy match for minor variations
            ratio = difflib.SequenceMatcher(None, temp_lower, text_lower).ratio()
            if ratio > 0.6:
                flags.append("possible_templated_phrasing")
                plagiarism_prob = max(plagiarism_prob, 0.5)

        # 2. Check for self-similarity (repetitive style between questions)
        if previous_answers:
            similarity_ratios = []
            for prev in previous_answers:
                if len(prev) > 20 and len(text) > 20:
                    sim = difflib.SequenceMatcher(None, prev.lower(), text.lower()).ratio()
                    similarity_ratios.append(sim)
            
            if similarity_ratios and max(similarity_ratios) > 0.7:
                flags.append("high_self_similarity")
                plagiarism_prob = max(plagiarism_prob, 0.4)

        return AnalysisResult(
            type=AnalysisType.PLAGIARISM,
            score=plagiarism_prob,
            probability=plagiarism_prob,
            flags=flags,
            details={
                "plagiarism_probability": plagiarism_prob,
                "found_matches": len(flags)
            }
        )
