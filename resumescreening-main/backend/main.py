"""FastAPI Backend for AI Resume Screening & Candidate Fit Assessment System.

Provides RESTful endpoints for:
1. PDF resume upload and text extraction.
2. Boundary-safe technical skill extraction.
3. NLP job category & domain classification.
4. Multi-factor Job Description matching and gap analysis.
5. Actionable hiring recommendation synthesis with explainability insights.
"""

import os
import sys
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add project root to sys.path so modules resolve cleanly
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from backend.schemas.resume import (
    HealthResponse,
    SkillExtractionRequest,
    SkillExtractionResponse,
    TextExtractRequest,
    TextExtractResponse,
    CandidateProfileSchema,
    CategoryPredictionRequest,
    CategoryPredictionResponse,
    JobMatchRequest,
    JobMatchResponse,
    ScreeningRequest,
    ScreeningResponse,
    HiringDecisionSchema,
    ExplainabilitySchema,
    SampleJDsResponse,
)
from backend.services.model_service import model_service
from backend.services.parser_service import (
    extract_skills,
    parse_resume_full,
)
from backend.services.matcher_service import (
    match_resume_to_job,
    synthesize_hiring_decision,
)
from backend.services.explainability_service import explain_prediction
from backend.utils.pdf_extractor import extract_text_from_pdf_bytes
from backend.utils.preprocessing import clean_text


# Initialize FastAPI application
app = FastAPI(
    title="AI Resume Screening & Fit Assessment API",
    description=(
        "Production-grade RESTful API providing automated resume parsing, NLP job domain classification, "
        "Job Description skill matching, gap analysis, and explainable hiring recommendations."
    ),
    version="2.5.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------
# CORS Configuration for Frontend Connectivity
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all frontend origins (Streamlit, React, Vue, Next.js)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Sample Job Description Presets
# ---------------------------------------------------------
SAMPLE_JDS = {
    "Data Scientist / ML Engineer": (
        "We are seeking a Data Scientist with 3+ years of experience in Python, SQL, and Machine Learning. "
        "Hands-on expertise in Deep Learning, PyTorch, TensorFlow, Pandas, Scikit-Learn, and Docker. "
        "Experience with Tableau, Power BI, and AWS cloud deployments is preferred. Bachelor's or Master's degree in Computer Science or related field."
    ),
    "Full Stack Web Developer": (
        "Looking for a Full Stack Developer with 2+ years of experience proficient in JavaScript, TypeScript, React, Next.js, and Node.js. "
        "Strong skills in HTML5, CSS3, Tailwind CSS, REST API development, PostgreSQL, MongoDB, and Git. "
        "Familiarity with Docker and AWS is a plus. Bachelor's degree required."
    ),
    "Cloud / DevOps Engineer": (
        "Seeking a DevOps Engineer with 3+ years of experience in Linux, Docker, Kubernetes, Terraform, CI/CD pipelines, "
        "and AWS or Azure cloud infrastructure. Proficient in Python, Bash scripting, Networking, and Git."
    ),
    "Cybersecurity Specialist": (
        "Hiring a Cybersecurity Analyst with 2+ years of experience in Networking, Linux, Penetration Testing, "
        "SIEM, Python scripting, Ethical Hacking, and Information Security best practices."
    ),
    "Java Backend Developer": (
        "Seeking a Senior Java Developer with 4+ years of experience in Java, Spring Boot, Microservices, REST APIs, "
        "SQL, PostgreSQL, Docker, Redis, and Git. Experience with AWS and CI/CD pipelines is a plus."
    )
}


# ---------------------------------------------------------
# Health Check Endpoint
# ---------------------------------------------------------
@app.get(
    "/health",
    response_model=HealthResponse,
    summary="System Health & Model Readiness",
    tags=["System"],
)
@app.get(
    "/",
    response_model=HealthResponse,
    summary="Root Health Check",
    tags=["System"],
)
async def health_check():
    """Returns the operational status of the API and whether ML models are loaded."""
    return HealthResponse(
        status="healthy",
        app_name="AI Resume Screening & JD Fit API",
        version="2.5.0",
        category_model_loaded=model_service.category_model_loaded,
        models_path=model_service.models_directory,
    )


# ---------------------------------------------------------
# Sample Job Description Presets Endpoint
# ---------------------------------------------------------
@app.get(
    "/api/sample-jds",
    response_model=SampleJDsResponse,
    summary="Get Sample Job Description Presets",
    tags=["Presets"],
)
async def get_sample_jds():
    """Returns pre-configured job description templates for quick testing."""
    return SampleJDsResponse(presets=SAMPLE_JDS)


# ---------------------------------------------------------
# Skill Extraction Endpoint
# ---------------------------------------------------------
@app.post(
    "/api/extract-skills",
    response_model=SkillExtractionResponse,
    summary="Extract Technical Skills",
    tags=["Entity Extraction"],
)
async def api_extract_skills(payload: SkillExtractionRequest):
    """Extracts technical skills using boundary-safe regex patterns and 160+ taxonomy."""
    if not payload.text or not payload.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input text cannot be empty."
        )
    skills = extract_skills(payload.text)
    return SkillExtractionResponse(
        total_skills_found=len(skills),
        skills=skills
    )


# ---------------------------------------------------------
# Text Extraction & Full Profile Parsing Endpoint
# ---------------------------------------------------------
@app.post(
    "/api/extract-text",
    response_model=TextExtractResponse,
    summary="Parse Resume Text into Structured Profile",
    tags=["Entity Extraction"],
)
async def api_extract_text(payload: TextExtractRequest):
    """Parses raw resume text into structured fields (skills, experience, education, certifications)."""
    if not payload.text or not payload.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text cannot be empty."
        )
    profile_dict = parse_resume_full(payload.text)
    return TextExtractResponse(
        raw_text=payload.text,
        cleaned_text=profile_dict["clean_text"],
        profile=CandidateProfileSchema(**profile_dict)
    )


# ---------------------------------------------------------
# Job Category Prediction Endpoint
# ---------------------------------------------------------
@app.post(
    "/api/predict-category",
    response_model=CategoryPredictionResponse,
    summary="Predict Job Domain Category",
    tags=["Machine Learning"],
)
async def api_predict_category(payload: CategoryPredictionRequest):
    """Classifies candidate resume text into a job domain (e.g. Data Science, Java Developer)."""
    if not payload.text or not payload.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text cannot be empty for category prediction."
        )
    cat, method, conf = model_service.predict_category(payload.text)
    return CategoryPredictionResponse(
        predicted_category=cat,
        method=method,
        confidence=conf
    )


# ---------------------------------------------------------
# Job Description Matching Endpoint
# ---------------------------------------------------------
@app.post(
    "/api/match-job",
    response_model=JobMatchResponse,
    summary="Match Resume Against Job Description",
    tags=["Matching Engine"],
)
async def api_match_job(payload: JobMatchRequest):
    """Evaluates candidate fit against JD (skills, semantics, experience, education)."""
    if not payload.resume_text or not payload.resume_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text cannot be empty."
        )
    match_result = match_resume_to_job(payload.resume_text, payload.job_description or "")
    return JobMatchResponse(**match_result)


# ---------------------------------------------------------
# Unified Screening Endpoint (Raw Text or JSON Payload)
# ---------------------------------------------------------
@app.post(
    "/api/screen-resume",
    response_model=ScreeningResponse,
    summary="End-to-End Resume Screening (JSON Payload)",
    tags=["Screening Engine"],
)
async def api_screen_resume(payload: ScreeningRequest):
    """Performs full end-to-end evaluation for raw resume text + optional Job Description."""
    if not payload.resume_text or not payload.resume_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text cannot be empty."
        )

    # 1. Profile Extraction
    profile = parse_resume_full(payload.resume_text)

    # 2. NLP Category Prediction
    predicted_cat, _, _ = model_service.predict_category(profile["clean_text"])

    # 3. Dual Matching Engine
    jd_text = payload.job_description or ""
    match_result = match_resume_to_job(payload.resume_text, jd_text)

    # 4. Hiring Recommendation Synthesis
    has_jd = bool(jd_text.strip())
    decision_data = synthesize_hiring_decision(
        match_result=match_result,
        has_job_description=has_jd
    )

    # 5. Explainability & Insights
    explanation = explain_prediction(match_result=match_result)

    return ScreeningResponse(
        document_name=payload.filename or "Candidate Resume",
        predicted_category=predicted_cat,
        profile=CandidateProfileSchema(**profile),
        match_result=JobMatchResponse(**match_result),
        hiring_decision=HiringDecisionSchema(**decision_data),
        explainability=ExplainabilitySchema(**explanation)
    )


# ---------------------------------------------------------
# PDF Resume Upload & Screening Endpoint (Multipart/Form-Data)
# ---------------------------------------------------------
@app.post(
    "/api/upload-resume",
    response_model=ScreeningResponse,
    summary="Upload PDF Resume & Screen Against JD",
    tags=["Screening Engine"],
)
async def api_upload_resume(
    file: UploadFile = File(..., description="PDF Resume file to upload"),
    job_description: Optional[str] = Form("", description="Target Job Description text")
):
    """Accepts a PDF resume file upload and screens it against the provided Job Description."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF resume files (.pdf) are supported."
        )

    try:
        content_bytes = await file.read()
        resume_text = extract_text_from_pdf_bytes(content_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to parse PDF resume: {str(e)}"
        )

    # Re-use the screening logic
    profile = parse_resume_full(resume_text)
    predicted_cat, _, _ = model_service.predict_category(profile["clean_text"])
    
    jd_text = job_description or ""
    match_result = match_resume_to_job(resume_text, jd_text)
    has_jd = bool(jd_text.strip())
    
    decision_data = synthesize_hiring_decision(
        match_result=match_result,
        has_job_description=has_jd
    )
    explanation = explain_prediction(match_result=match_result)

    return ScreeningResponse(
        document_name=file.filename,
        predicted_category=predicted_cat,
        profile=CandidateProfileSchema(**profile),
        match_result=JobMatchResponse(**match_result),
        hiring_decision=HiringDecisionSchema(**decision_data),
        explainability=ExplainabilitySchema(**explanation)
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
