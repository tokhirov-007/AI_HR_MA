import re
from app.answer_analysis.schemas import AnalysisResult, AnalysisType

class StructureAnalyzer:
    """
    Analyzes the logical structure of an answer.
    Checks for explanations, code blocks, and reasoning.
    """

    def analyze(self, text: str) -> AnalysisResult:
        if not text:
            return AnalysisResult(type=AnalysisType.STRUCTURE, score=0.0)

        flags = []
        scores = []

        # 1. Code presence
        has_code = bool("```" in text or re.search(r"[{}();]", text))
        if has_code:
            flags.append("contains_code")
            scores.append(0.8) # Good for technical answers

        # 2. Logic steps (Check for Transition words like "First", "Then", "Result")
        logic_markers = ["first", "then", "second", "finally", "because", "therefore", "reason"]
        found_logic = sum(1 for word in logic_markers if word in text.lower())
        
        if found_logic >= 2:
            flags.append("logical_steps_detected")
            scores.append(1.0)
        else:
            flags.append("lack_of_explaining_steps")
            scores.append(0.3)

        # 3. Answer depth (length heuristic)
        word_count = len(text.split())
        if word_count > 100:
            flags.append("comprehensive_answer")
            scores.append(1.0)
        elif word_count < 15:
            flags.append("too_short_answer")
            scores.append(0.2)
        else:
            scores.append(0.7)

        # 4. "Vibe Coding" Detection (words but no code, or code but no words)
        if has_code and word_count < 10:
            flags.append("raw_code_no_explanation")
            scores.append(0.4)
        if not has_code and word_count > 80:
            flags.append("long_text_no_code") # Might be suspect for some tech questions
            scores.append(0.6)

        final_score = sum(scores) / len(scores) if scores else 0.5

        return AnalysisResult(
            type=AnalysisType.STRUCTURE,
            score=final_score,
            flags=flags,
            details={
                "word_count": word_count,
                "has_code": has_code,
                "logic_markers_found": found_logic
            }
        )
