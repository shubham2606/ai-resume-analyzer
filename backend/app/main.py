from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.services.parser import extract_resume_text
from app.services.analyzer import analyze_resume

app = FastAPI(
    title="AI Resume Analyzer POC",
    version="1.0.0",
    description="Phase 1 POC: resume parsing and rule-based analysis. LLM integration can be added in Phase 2.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@app.get("/")
def root():
    return {
        "message": "AI Resume Analyzer API is running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Please select a resume file.")

    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported in Phase 1.",
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File is larger than 5 MB.")

    try:
        text = extract_resume_text(content, extension)
    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Could not read this resume: {exc}",
        ) from exc

    if len(text.strip()) < 80:
        raise HTTPException(
            status_code=422,
            detail="Very little text was extracted. Please upload a text-based PDF/DOCX.",
        )

    result = analyze_resume(text)
    return {
        "filename": file.filename,
        "characters_extracted": len(text),
        **result,
    }
