from fastapi import FastAPI, UploadFile, File, HTTPException
from app.cv_intelligence.cv_analyzer import CVAnalyzer
from app.cv_intelligence.schemas import CVAnalysisResult
import uvicorn
import shutil
import os
import tempfile

app = FastAPI(title="AI HR System - CV Intelligence", version="1.0")

# Global Analyzer Instance
analyzer = None

@app.on_event("startup")
async def startup_event():
    global analyzer
    analyzer = CVAnalyzer()

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

if __name__ == "__main__":
    print("Starting AI HR System API...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
