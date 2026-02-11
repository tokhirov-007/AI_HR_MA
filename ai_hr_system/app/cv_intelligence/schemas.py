from typing import List, Optional, Dict
from pydantic import BaseModel

class CVAnalysisResult(BaseModel):
    raw_text: str
    skills_detected: List[str]
    inferred_skills: List[str]
    experience_years: Optional[float] = None
    confidence: Dict[str, float] = {}
