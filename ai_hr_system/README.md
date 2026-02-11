# CV Intelligence Module

This module provides an AI-powered CV analysis system that extracts skills and interprets semantic meaning from resumes (PDF/DOCX).

## Features
- **File Support**: PDF and DOCX.
- **Skill Extraction**: Identifies explicit skills using NLP (Spacy) and Pattern Matching.
- **Semantic Understanding**: Maps abstract concepts (e.g., "Modern Frontend") to concrete skills (e.g., "React", "Vue") using Sentence Transformers (Embeddings).

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download Models**:
   The application will automatically download the necessary models (`en_core_web_sm` and `sentence-transformers/all-MiniLM-L6-v2`) on the first run. 
   
   *Note: If automatic download fails, install Spacy model manually:*
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

### Start the API
Run the application from the `ai_hr_system` directory:
```bash
python -m app.main
```
The server will start at `http://0.0.0.0:8000`.

### Analyze a CV
You can use `curl` or the Swagger UI at `http://localhost:8000/docs`.

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/resume.pdf'
```

**Example Response:**
```json
{
  "raw_text": "Experienced in Modern JavaScript...",
  "skills_detected": ["JavaScript"],
  "inferred_skills": ["React", "Vue", "ES6+", "Async/Await"],
  "experience_years": 5.0,
  "confidence": {
    "parsing": 1.0,
    "skill_extraction": 0.85,
    "semantic_inference": 0.75
  }
}
```
