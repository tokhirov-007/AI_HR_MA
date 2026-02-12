import re
from typing import List
from app.answer_analysis.schemas import AnalysisResult, AnalysisType

class AIDetector:
    """
    Heuristic-based detector of AI-generated content patterns.
    Analyzes style, structure, and markers common in LLM outputs.
    """
    
    # Common markers often found in AI-generated technical answers
    AI_MARKERS = [
        r"it's important to note",
        r"in terms of",
        r"from a technical perspective",
        r"to summarize",
        r"furthermore",
        r"moreover",
        r"additionally",
        r"typically",
        r"in many cases",
        r"key features include",
        r"one should consider",
        r"it is worth mentioning",
        r"best practices suggest"
    ]

    def analyze(self, text: str) -> AnalysisResult:
        """
        Analyze text for AI indicators.
        """
        if not text:
            return AnalysisResult(type=AnalysisType.AI_DETECTION, score=0.0, flags=["empty_text"])

        # 1. Check for specific AI markers (linguistic patterns)
        marker_count = 0
        found_markers = []
        for marker in self.AI_MARKERS:
            if re.search(marker, text.lower()):
                marker_count += 1
                found_markers.append(marker)
        
        # 2. Analyze structure (AI often uses perfect bullet points/numbered lists)
        structure_score = 0.0
        flags = []
        
        # Check for list patterns (1. , - )
        list_patterns = len(re.findall(r"^\d+\.\s", text, re.MULTILINE))
        bullet_patterns = len(re.findall(r"^[-*•]\s", text, re.MULTILINE))
        
        if list_patterns > 1:
            flags.append("perfect_numbered_list")
            structure_score += 0.2
        if bullet_patterns > 1:
            flags.append("perfect_bullet_points")
            structure_score += 0.2
            
        # 3. Text complexity/consistency (AI often uses very balanced sentence lengths)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        
        if len(sentences) > 3:
            lengths = [len(s.split()) for s in sentences]
            avg_len = sum(lengths) / len(sentences)
            v_len = sum((x - avg_len) ** 2 for x in lengths) / len(sentences)
            
            # AI tends to have more uniform sentence lengths (lower variance)
            if v_len < 10:
                flags.append("uniform_sentence_lengths")
                structure_score += 0.3

        # 4. Perfect grammar indicator (very basic heuristic)
        # In manual responses, people often miss capitalization or periods.
        if text[0].isupper() and text.strip().endswith('.') and bool(re.search(r'[A-Z]', text)):
            # If everything is perfectly capitalized and punctuated
            structure_score += 0.1

        # Calculate final probability
        # This is a heuristic simulation of AI detection
        ai_probability = min(0.95, (marker_count * 0.15) + structure_score)
        
        if marker_count > 3:
            flags.append("high_marker_density")
            
        return AnalysisResult(
            type=AnalysisType.AI_DETECTION,
            score=ai_probability,
            probability=ai_probability,
            flags=flags,
            details={
                "marker_count": marker_count,
                "found_markers": found_markers[:5],
                "sentence_variance": round(v_len, 2) if 'v_len' in locals() else 0
            }
        )
