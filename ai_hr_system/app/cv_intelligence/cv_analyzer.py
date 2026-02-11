from app.cv_intelligence.parser import CVParser
from app.cv_intelligence.skill_extractor import SkillExtractor
from app.cv_intelligence.skill_mapper import SkillMapper
from app.cv_intelligence.schemas import CVAnalysisResult
from app.config import settings
import re

class CVAnalyzer:
    def __init__(self):
        print("Initializing CV Analyzer components...")
        self.parser = CVParser()
        self.extractor = SkillExtractor(model=settings.SPACY_MODEL)
        self.mapper = SkillMapper(model_name=settings.TRANSFORMER_MODEL)
        print("CV Analyzer ready.")

    def analyze(self, file_path: str) -> CVAnalysisResult:
        """
        Orchestrates the CV analysis process:
        1. Parse text from file
        2. Extract explicit skills and semantic candidates
        3. Map candidates to inferred skills
        4. Return structured result
        """
        # 1. Parse Text
        print(f"Parsing file: {file_path}")
        raw_text = self.parser.parse(file_path)
        
        # 2. Extract Skills
        print("Extracting skills...")
        extraction_result = self.extractor.extract(raw_text)
        explicit_skills = extraction_result["explicit"]
        candidates = extraction_result["candidates"]
        
        # 3. Map Skills (Semantic Understanding)
        print("Mapping semantic skills...")
        inferred_skills = self.mapper.map_skills(candidates)
        
        # 4. Construct Result
        return CVAnalysisResult(
            raw_text=raw_text, # Return full text as requested
            skills_detected=sorted(list(set(explicit_skills))),
            inferred_skills=sorted(list(set(inferred_skills))),
            experience_years=self._estimate_experience(raw_text),
            confidence={
                "parsing": 1.0 if raw_text else 0.0,
                "skill_extraction": 0.85 if explicit_skills else 0.1,
                "semantic_inference": 0.75 if inferred_skills else 0.0
            }
        )

    def _estimate_experience(self, text: str) -> float | None:
        # Simple heuristic to find years of experience
        # Looks for patterns like "5 years experience", "3+ years", etc.
        matches = re.findall(r'(\d+)\+?\s*(?:years?|yrs?)', text.lower())
        if matches:
            try:
                years = [int(m) for m in matches]
                return float(max(years)) if years else None
            except:
                return None
        return None
