"""Pydantic schemas and Data Transfer Objects for the AI Resume Screening API."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Health Schema
# ---------------------------------------------------------
class HealthResponse(BaseModel):
    status: str = Field(..., example="healthy")
    app_name: str = Field(..., example="AI Resume Screening & JD Fit API")
    version: str = Field(..., example="2.5.0")
    category_model_loaded: bool = Field(..., example=True)
    models_path: str = Field(..., example="/backend/models")


# ---------------------------------------------------------
# Skill Extraction Schemas
# ---------------------------------------------------------
class SkillExtractionRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Raw text of resume or job description to extract skills from.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "Senior Machine Learning Engineer with 4 years in Python, PyTorch, Docker, and AWS."
            }
        }
    }


class SkillExtractionResponse(BaseModel):
    total_skills_found: int = Field(..., example=4)
    skills: List[str] = Field(..., example=["aws", "docker", "machine learning", "python", "pytorch"])


# ---------------------------------------------------------
# Candidate Profile & Parsing Schemas
# ---------------------------------------------------------
class CandidateProfileSchema(BaseModel):
    skills: List[str] = Field(default_factory=list, example=["python", "sql", "machine learning"])
    skills_str: str = Field("", example="python, sql, machine learning")
    experience_years: int = Field(0, example=3)
    education: str = Field("B.Tech", example="B.Tech")
    certification: str = Field("None", example="AWS Certified")
    projects_count: int = Field(1, example=3)
    clean_text: str = Field("", description="Cleaned, normalized resume text.")


class TextExtractRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Raw text of the resume.")


class TextExtractResponse(BaseModel):
    raw_text: str
    cleaned_text: str
    profile: CandidateProfileSchema


# ---------------------------------------------------------
# Category Prediction Schemas
# ---------------------------------------------------------
class CategoryPredictionRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Resume text to classify.")


class CategoryPredictionResponse(BaseModel):
    predicted_category: str = Field(..., example="Data Science")
    method: str = Field(..., example="NLP LogisticRegression Model")
    confidence: Optional[float] = Field(None, example=98.5)


# ---------------------------------------------------------
# Job Matching Schemas
# ---------------------------------------------------------
class JobMatchRequest(BaseModel):
    resume_text: str = Field(..., min_length=1, description="Resume text or candidate profile.")
    job_description: str = Field(..., description="Target Job Description requirements.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "resume_text": "Data Scientist with experience in Python, SQL, Machine Learning, Docker, 4 years exp.",
                "job_description": "Seeking a Data Scientist with 3+ years experience proficient in Python, SQL, Machine Learning, and Tableau."
            }
        }
    }


class JobMatchResponse(BaseModel):
    composite_score: float = Field(..., example=82.0, description="Overall weighted fit score (0-100%).")
    skill_score: float = Field(..., example=75.0, description="Percentage of required JD skills present in resume.")
    semantic_score: float = Field(..., example=68.5, description="TF-IDF cosine contextual similarity percentage.")
    matched_skills: List[str] = Field(..., example=["data science", "machine learning", "python", "sql"])
    missing_skills: List[str] = Field(..., example=["tableau"])
    extra_skills: List[str] = Field(..., example=["docker"])
    grade: str = Field(..., example="Strong Match")
    total_required_skills: int = Field(..., example=4)
    total_matched_skills: int = Field(..., example=3)
    candidate_experience: int = Field(..., example=4)
    required_experience: Optional[int] = Field(None, example=3)
    experience_status: str = Field(..., example="Exceeded")
    experience_score: float = Field(..., example=100.0)
    candidate_education: str = Field(..., example="B.Tech")
    required_education: Optional[str] = Field(None, example="Bachelor's")
    education_status: str = Field(..., example="Candidate: B.Tech")


# ---------------------------------------------------------
# Explainability & Insights Schemas
# ---------------------------------------------------------
class FeatureImpactSchema(BaseModel):
    feature: str = Field(..., example="Skill Match Coverage")
    impact: str = Field(..., example="75.0%")
    type: str = Field(..., example="Positive")


class ExplainabilitySchema(BaseModel):
    summary_reasons: List[str] = Field(default_factory=list)
    interview_questions: List[str] = Field(default_factory=list)
    improvement_tips: List[str] = Field(default_factory=list)
    feature_contributions: List[FeatureImpactSchema] = Field(default_factory=list)


# ---------------------------------------------------------
# Unified End-to-End Screening Schemas
# ---------------------------------------------------------
class ScreeningRequest(BaseModel):
    resume_text: str = Field(..., min_length=1, description="Raw text of candidate's resume.")
    job_description: Optional[str] = Field("", description="Target Job Description. If blank, general assessment is performed.")
    filename: Optional[str] = Field("resume.txt", description="Optional filename identifier.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "resume_text": "Senior Python Developer with 4 years experience in FastAPI, PostgreSQL, Docker, and AWS.",
                "job_description": "Looking for a Backend Developer with 3+ years experience in Python, FastAPI, Docker, and Kubernetes.",
                "filename": "candidate_resume.txt"
            }
        }
    }


class HiringDecisionSchema(BaseModel):
    decision: str = Field(..., example="Hire (Recommended for Interview)")
    category: str = Field(..., example="Hire")
    confidence: float = Field(..., example=88.5)
    reason: str = Field(..., example="High alignment (88.5%) with required competencies.")


class ScreeningResponse(BaseModel):
    document_name: str = Field(..., example="candidate_resume.pdf")
    predicted_category: str = Field(..., example="Python Developer")
    profile: CandidateProfileSchema
    match_result: JobMatchResponse
    hiring_decision: HiringDecisionSchema
    explainability: ExplainabilitySchema


# ---------------------------------------------------------
# Presets Schemas
# ---------------------------------------------------------
class SampleJDItem(BaseModel):
    title: str
    description: str


class SampleJDsResponse(BaseModel):
    presets: Dict[str, str]
