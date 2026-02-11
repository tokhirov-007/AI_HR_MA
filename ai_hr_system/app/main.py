from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from app.cv_intelligence.cv_analyzer import CVAnalyzer
from app.cv_intelligence.schemas import CVAnalysisResult
from app.summary_engine.ai_summarizer import AISummarizer
from app.summary_engine.top_candidates import TopCandidatesRanker
from app.summary_engine.schemas import CandidateSummary, TopCandidatesResponse
from typing import List
import uvicorn
import shutil
import os
import tempfile

app = FastAPI(title="AI HR System - CV Intelligence + Summary", version="2.0")

# Global Instances
analyzer = None
summarizer = None
ranker = None

@app.on_event("startup")
async def startup_event():
    global analyzer, summarizer, ranker
    analyzer = CVAnalyzer()
    summarizer = AISummarizer()
    ranker = TopCandidatesRanker()

@app.post("/analyze", response_model=CVAnalysisResult)
async def analyze_cv(file: UploadFile = File(...)):
    """
    Endpoint to analyze a CV file (PDF or DOCX).
    """
    if not analyzer:
        raise HTTPException(status_code=500, detail="Analyzer not initialized")
        
    # Validate file extension
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ['.pdf', '.docx']:
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload .pdf or .docx")

    # Save to temp file to process
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    
    try:
        result = analyzer.analyze(tmp_path)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

@app.post("/summarize", response_model=CandidateSummary)
async def summarize_candidate(
    candidate_name: str = Body(...),
    cv_result: CVAnalysisResult = Body(...)
):
    """
    Generate HR-friendly and technical summary for a candidate.
    """
    if not summarizer:
        raise HTTPException(status_code=500, detail="Summarizer not initialized")
    
    try:
        hr_summary = summarizer.generate_hr_summary(cv_result)
        tech_summary = summarizer.generate_technical_summary(cv_result)
        
        # Calculate score
        from app.summary_engine.top_candidates import TopCandidatesRanker
        temp_ranker = TopCandidatesRanker()
        score = temp_ranker._calculate_score(cv_result)
        
        return CandidateSummary(
            candidate_name=candidate_name,
            summary_hr=hr_summary,
            summary_technical=tech_summary,
            skills_detected=cv_result.skills_detected,
            inferred_skills=cv_result.inferred_skills,
            experience_years=cv_result.experience_years,
            confidence=cv_result.confidence,
            total_score=score
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/top-candidates", response_model=TopCandidatesResponse)
async def rank_candidates(
    candidates: List[dict] = Body(...)
):
    """
    Rank multiple candidates and return sorted list.
    
    Expected input format:
    [
        {
            "candidate_name": "Ivan Ivanov",
            "cv_result": { ... CVAnalysisResult ... }
        },
        ...
    ]
    """
    if not ranker:
        raise HTTPException(status_code=500, detail="Ranker not initialized")
    
    try:
        result = ranker.rank_candidates(candidates)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting AI HR System API...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
