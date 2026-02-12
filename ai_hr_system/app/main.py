from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from app.cv_intelligence.cv_analyzer import CVAnalyzer
from app.cv_intelligence.schemas import CVAnalysisResult
from app.summary_engine.ai_summarizer import AISummarizer
from app.summary_engine.top_candidates import TopCandidatesRanker
from app.summary_engine.schemas import CandidateSummary, TopCandidatesResponse
from app.candidate_level.level_detector import LevelDetector
from app.candidate_level.difficulty_mapper import DifficultyMapper
from app.candidate_level.schemas import LevelDetectionResult, InterviewPlan
from app.question_engine.question_selector import QuestionSelector
from app.question_engine.schemas import QuestionSet
from app.interview_flow.session_manager import SessionManager
from app.interview_flow.schemas import InterviewSession, QuestionProgress, SessionSummary
from app.answer_analysis.final_analyzer import FinalAnalyzer
from app.answer_analysis.schemas import FullIntegrityReport
from app.scoring.score_engine import ScoreEngine
from app.scoring.recommendation import RecommendationEngine
from app.scoring.confidence_level import ConfidenceAnalyzer
from app.scoring.schemas import FinalRecommendation
from typing import List
import uvicorn
import shutil
import os
import tempfile

app = FastAPI(title="AI HR System - Complete", version="6.0")

# Global Instances
analyzer = None
summarizer = None
ranker = None
level_detector = None
difficulty_mapper = None
question_selector = None
session_manager = None
integrity_analyzer = None
score_engine = None
recommendation_engine = None
confidence_analyzer = None

@app.on_event("startup")
async def startup_event():
    global analyzer, summarizer, ranker, level_detector, difficulty_mapper, question_selector, session_manager, integrity_analyzer, score_engine, recommendation_engine, confidence_analyzer
    analyzer = CVAnalyzer()
    summarizer = AISummarizer()
    ranker = TopCandidatesRanker()
    level_detector = LevelDetector()
    difficulty_mapper = DifficultyMapper()
    question_selector = QuestionSelector()
    session_manager = SessionManager()
    integrity_analyzer = FinalAnalyzer()
    score_engine = ScoreEngine()
    recommendation_engine = RecommendationEngine()
    confidence_analyzer = ConfidenceAnalyzer()

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

@app.post("/detect-level", response_model=LevelDetectionResult)
async def detect_candidate_level(
    candidate_name: str = Body(...),
    cv_result: CVAnalysisResult = Body(...)
):
    """
    Detect candidate seniority level (Junior/Middle/Senior).
    """
    if not level_detector:
        raise HTTPException(status_code=500, detail="Level detector not initialized")
    
    try:
        result = level_detector.detect_level(candidate_name, cv_result)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/interview-plan", response_model=InterviewPlan)
async def generate_interview_plan(
    level_result: LevelDetectionResult = Body(...)
):
    """
    Generate interview plan with difficulty-mapped questions based on candidate level.
    """
    if not difficulty_mapper:
        raise HTTPException(status_code=500, detail="Difficulty mapper not initialized")
    
    try:
        plan = difficulty_mapper.generate_interview_plan(level_result)
        return plan
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-questions", response_model=QuestionSet)
async def generate_interview_questions(
    level_result: LevelDetectionResult = Body(...),
    max_questions: int = Body(5)
):
    """
    Generate interview questions based on candidate level and skills.
    Only generates questions for skills the candidate has.
    """
    if not question_selector:
        raise HTTPException(status_code=500, detail="Question selector not initialized")
    
    try:
        question_set = question_selector.select_questions(
            level_result=level_result,
            max_total_questions=max_questions
        )
        return question_set
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/start-interview", response_model=InterviewSession)
async def start_interview(
    candidate_id: str = Body(...),
    candidate_name: str = Body(...),
    question_set: QuestionSet = Body(...)
):
    """
    Start a new interview session.
    Creates session and starts first question with timer.
    """
    if not session_manager:
        raise HTTPException(status_code=500, detail="Session manager not initialized")
    
    try:
        session = session_manager.create_session(
            candidate_id=candidate_id,
            candidate_name=candidate_name,
            question_set=question_set
        )
        return session
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/current-question/{session_id}", response_model=QuestionProgress)
async def get_current_question(session_id: str):
    """
    Get current question for active session.
    Includes time remaining.
    """
    if not session_manager:
        raise HTTPException(status_code=500, detail="Session manager not initialized")
    
    try:
        question = session_manager.get_current_question(session_id)
        if not question:
            raise HTTPException(status_code=404, detail="No active question")
        return question
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/submit-answer/{session_id}")
async def submit_answer(
    session_id: str,
    answer_text: str = Body(...)
):
    """
    Submit answer for current question.
    Automatically moves to next question or finishes session.
    """
    if not session_manager:
        raise HTTPException(status_code=500, detail="Session manager not initialized")
    
    try:
        answer = session_manager.submit_answer(
            session_id=session_id,
            answer_text=answer_text
        )
        return {
            "status": "success",
            "answer": answer,
            "message": "Answer submitted successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session-status/{session_id}", response_model=InterviewSession)
async def get_session_status(session_id: str):
    """
    Get current status of interview session.
    """
    if not session_manager:
        raise HTTPException(status_code=500, detail="Session manager not initialized")
    
    try:
        session = session_manager.get_session_status(session_id)
        return session
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session-summary/{session_id}", response_model=SessionSummary)
async def get_session_summary(session_id: str):
    """
    Get summary of completed interview session.
    """
    if not session_manager:
        raise HTTPException(status_code=500, detail="Session manager not initialized")
    
    try:
        summary = session_manager.get_session_summary(session_id)
        return summary
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-integrity/{session_id}", response_model=FullIntegrityReport)
async def analyze_integrity(session_id: str):
    """
    Analyze the integrity and honesty of a completed interview session.
    Detects AI usage, plagiarism, and suspicious timing.
    """
    if not session_manager or not integrity_analyzer:
        raise HTTPException(status_code=500, detail="Analyzers not initialized")
    
    try:
        # 1. Get session summary
        summary = session_manager.get_session_summary(session_id)
        
        # 2. Get the session to access question data (difficulty, etc.)
        session = session_manager.get_session_status(session_id)
        
        # 3. Perform analysis
        report = integrity_analyzer.analyze_session(summary, session.questions)
        return report
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-recommendation/{session_id}", response_model=FinalRecommendation)
async def generate_recommendation(session_id: str):
    """
    Generate the absolute final HR recommendation.
    Aggregates technical score, integrity flags, and behavior.
    """
    if not all([session_manager, integrity_analyzer, score_engine, recommendation_engine, confidence_analyzer]):
        raise HTTPException(status_code=500, detail="Engines not initialized")
    
    try:
        # 1. Get session summary and technical data
        summary = session_manager.get_session_summary(session_id)
        session = session_manager.get_session_status(session_id)
        
        # 2. Get integrity report (Step 6)
        integrity_report = integrity_analyzer.analyze_session(summary, session.questions)
        
        # 3. Calculate Score Breakdown
        breakdown = score_engine.aggregate(summary, integrity_report, session.questions)
        
        # 4. Calculate Final Weighted Score
        # Assume a mix based on overall session (heuristic)
        difficulty_mix = "medium" # Default
        if all(q["difficulty"] == "hard" for q in session.questions):
            difficulty_mix = "hard"
        elif all(q["difficulty"] == "easy" for q in session.questions):
            difficulty_mix = "easy"
            
        final_score = score_engine.calculate_final_weighted_score(breakdown, difficulty_mix)
        
        # 5. Get HR Recommendation & Decision
        decision, reason = recommendation_engine.get_recommendation(
            final_score, breakdown, integrity_report.global_flags
        )
        hr_comment = recommendation_engine.generate_comment(
            decision, breakdown, integrity_report.global_flags
        )
        
        # 6. Calculate Confidence
        ans_lengths = [len(a.answer_text) for a in summary.answers]
        confidence = confidence_analyzer.calculate(
            summary.total_questions,
            summary.answered_questions,
            ans_lengths,
            integrity_report.suspicious_answers_count
        )
        
        return FinalRecommendation(
            session_id=session_id,
            candidate_name=summary.candidate_name,
            final_score=final_score,
            decision=decision, # Pydantic model with str, Enum should handle this, but let's be sure
            confidence=confidence,
            hr_comment=hr_comment,
            score_breakdown=breakdown,
            flags=integrity_report.global_flags + [reason],
            metadata={
                "difficulty_mix": difficulty_mix,
                "integrity_summary": integrity_report.recommendation
            }
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting AI HR System API...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
