# AI Resume Screening & Candidate Fit Assessment System

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.0%2B-646CFF.svg?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.0%2B-E92063.svg?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)

An end-to-end, full-stack Artificial Intelligence and Natural Language Processing (NLP) system designed to automate candidate resume parsing, job-role fit assessment against target Job Descriptions (JDs), skill gap analysis, and recruitment decision support.

This repository is organized as a **Monorepo** containing both the **React.js Frontend** and the **Python FastAPI REST Backend**.

---

## 📌 Problem Statement

In modern technical recruitment, talent acquisition teams receive hundreds of resumes for every job opening. Manual screening creates major operational bottlenecks:
1. **Time Inefficiency**: Recruiters spend hours scanning resumes for prerequisite keywords and experience.
2. **Keyword Mismatches**: Candidates often express skills using synonyms (e.g., `JS` vs `JavaScript`, `K8s` vs `Kubernetes`, `ML` vs `Machine Learning`), leading to false rejections by basic keyword filters.
3. **Lack of Explainability**: Traditional black-box filtering systems output opaque scores without explaining *why* a candidate was flagged or what specific competencies are missing.

This project solves these challenges with a dual-engine architecture: combining **boundary-safe entity extraction (160+ skill taxonomy)**, **NLP domain classification (99.5% accuracy)**, **TF-IDF contextual semantic similarity**, and **explainable hiring recommendations with tailored interview questions**.

---

## ✨ Key Features

- **Dual Resume Ingestion**: Upload PDF resumes via drag-and-drop or paste raw resume text.
- **Boundary-Safe Skill Extraction**: 160+ canonical technical skill taxonomy with regex word boundaries (`\b`) preventing substring collisions (`JavaScript` $\ne$ `Java`).
- **NLP Job Category Classifier**: 25-domain TF-IDF Logistic Regression classifier with **99.5% cross-validation accuracy**.
- **Multi-Factor Fit Scoring**: Weighted composite fit score:
  $$\text{Composite Score} = (0.50 \times \text{Skill Coverage}) + (0.30 \times \text{Semantic Overlap}) + (0.20 \times \text{Experience Alignment})$$
- **Skill Gap & Competency Badges**: Real-time breakdown into **Matched Skills** (Emerald), **Missing Required Skills** (Rose), and **Additional Strengths** (Cyan).
- **Explainable Decision Support**: Outputs human-interpretable hiring recommendations (`Hire`, `Review`, `Reject`) with confidence percentages and explicit rationales.
- **Tailored Technical Screening Questions**: Automatically generates interview screening questions addressing candidate-specific skill matches and identified gaps.
- **Candidate Optimization Tips**: Provides practical resume improvement tips for applicants.
- **Interactive REST API Documentation**: Live interactive OpenAPI Swagger and ReDoc documentation.

---

## 🛠️ Technology Stack

### 1. Frontend Technologies
- **Framework**: React.js 18 (Single Page Application)
- **Build Tool / Bundler**: Vite 5
- **Styling**: Vanilla CSS3 with Custom Design System (Glassmorphism, Dark Mode, KPI Cards, Responsive Grid)
- **API Client**: Native `fetch` with environment-driven base URL configuration (`VITE_API_BASE_URL`)

### 2. Backend Technologies
- **Framework**: Python FastAPI (Async ASGI framework)
- **Server**: Uvicorn (ASGI Web Server)
- **Validation & Schemas**: Pydantic v2
- **CORS Middleware**: Starlette CORS configured for cross-origin frontend communication
- **File Upload Handler**: `python-multipart`

### 3. Machine Learning & Document Processing
- **NLP / ML Framework**: Scikit-Learn (`TfidfVectorizer`, `LogisticRegression`)
- **Model Persistence**: Joblib
- **Data Manipulation**: Pandas, NumPy
- **PDF Text Parsing**: PDFPlumber (stream-based text extraction)
- **Text Normalization**: Regex-based PII stripping (emails, phone numbers, URLs) with technical token preservation (`C++`, `C#`, `.NET`, `Node.js`)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (Vite)                    │
│   • Resume PDF Upload (multipart/form-data) OR Raw Text     │
│   • Target Job Description (Custom or 1-Click Preset)       │
└──────────────────────────────┬──────────────────────────────┘
                               │  HTTP REST API (JSON / FormData)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 FastAPI REST Backend (8000)                 │
│   • CORS Middleware enabled (Allow Origins: *)              │
│   • Pydantic Request Validation & Error Handling            │
└──────────────────────────────┬──────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
┌──────────────────────────────┐    ┌──────────────────────────────┐
│  Parser & Preprocessing      │    │  NLP ML Domain Classifier    │
│  • PDFPlumber text extractor │    │  • TF-IDF (1-2 N-grams)      │
│  • 160+ Skill Taxonomy       │    │  • Logistic Regression       │
│  • Section-aware experience  │    │  • 99.5% domain accuracy     │
│  • Education degree detector │    │  • Model: category_model.pkl │
└──────────────┬───────────────┘    └─────────────┬────────────────┘
               │                                  │
               └──────────────────┬───────────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────┐
│               Dual Matching & Explainable AI                │
│   • Skill Coverage & Gap Badges (Matched, Missing, Extra)   │
│   • TF-IDF Semantic Cosine Overlap                          │
│   • Composite Weighted Fit Score (50% / 30% / 20%)          │
│   • Recommendation Synthesis: Hire / Review / Reject        │
│   • Tailored Technical Interview Screening Questions        │
└──────────────────────────────┬──────────────────────────────┘
                               │  Structured JSON Response
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   React Result Dashboard                    │
│   • 4 KPI Cards (Score %, Coverage %, Decision, Domain)     │
│   • Fit Overview & Requirement Alignment Table              │
│   • Color-coded Badges (Matched, Missing, Extra)            │
│   • Explainable Decision Reasons & Interview Questions      │
│   • Extracted Candidate Attributes & Raw Text Inspector     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Folder Structure

```
AI-Resume-Screening/
│
├── frontend/                         # React.js (Vite) Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx            # App header with live backend status indicator
│   │   │   ├── ResumeInput.jsx       # Drag & drop PDF upload & text paste toggle
│   │   │   ├── JobDescriptionInput.jsx # JD input with 1-click sample presets
│   │   │   ├── MetricCards.jsx       # 4 KPI cards (Score %, Coverage %, Rec, Domain)
│   │   │   ├── OverviewTab.jsx       # Score gauge, decision rationale & criteria table
│   │   │   ├── SkillAnalysis.jsx     # Matched (green), Missing (red), Extra (blue) badges
│   │   │   ├── InsightsTab.jsx       # Tailored interview questions & resume tips
│   │   │   └── CandidateProfileTab.jsx # Extracted entity table & raw text inspector
│   │   ├── pages/
│   │   │   └── Dashboard.jsx         # Primary screening workspace & state manager
│   │   ├── services/
│   │   │   └── api.js                # REST API client connecting to FastAPI backend
│   │   ├── App.jsx                   # React root component
│   │   ├── main.jsx                  # React DOM mounting
│   │   └── index.css                 # Custom CSS Design System (Glassmorphism, Badges)
│   ├── public/
│   │   └── favicon.svg               # Brand icon
│   ├── package.json                  # Frontend npm dependencies (React 18, Vite)
│   ├── vite.config.js                # Vite build & backend proxy config
│   ├── index.html                    # Single Page Application entry template
│   ├── standalone.html               # 0-dependency browser client (open directly in browser)
│   ├── .env                          # Environment config (VITE_API_BASE_URL)
│   ├── .env.example                  # Environment template
│   └── README.md                     # Frontend documentation & usage guide
│
├── backend/                          # Python FastAPI REST Backend
│   ├── main.py                       # FastAPI app, CORS middleware & REST endpoints
│   ├── requirements.txt              # Backend dependencies (FastAPI, Pydantic, Scikit-Learn)
│   ├── models/                       # ML model binaries (.pkl)
│   │   ├── category_model.pkl        # NLP Domain Classifier (99.5% accuracy)
│   │   └── screening_model.pkl       # Candidate Fit Recommendation pipeline
│   ├── schemas/                      # Pydantic request & response DTOs
│   │   ├── __init__.py
│   │   └── resume.py
│   ├── services/                     # Modular ML & business services
│   │   ├── __init__.py
│   │   ├── model_service.py          # Model loading singleton & domain inference
│   │   ├── parser_service.py         # 160+ skill taxonomy extractor, experience & degree
│   │   ├── matcher_service.py        # Skill coverage, TF-IDF cosine similarity & composite fit
│   │   └── explainability_service.py # Recruiter reasoning, interview questions & tips
│   ├── utils/                        # Helper utilities
│   │   ├── __init__.py
│   │   ├── preprocessing.py          # Regex cleaning, PII removal, tech token preservation
│   │   └── pdf_extractor.py          # PDF document text extraction stream processor
│   ├── uploads/                      # Temporary upload buffer
│   │   └── .gitkeep
│   ├── tests/                        # Automated unit & integration tests (24 passing tests)
│   │   ├── __init__.py
│   │   ├── test_api.py               # Endpoint & CORS integration tests
│   │   └── test_services.py          # Unit tests for services and parsers
│   └── README.md                     # Backend documentation & API specification
│
├── data/                             # Benchmark datasets
│   ├── UpdatedResumeDataSet.csv
│   └── AI_Resume_Screening.csv
│
├── README.md                         # Master documentation (this file)
├── .gitignore                        # Multi-stack gitignore (Python, Node, OS)
└── .env.example                      # Root environment configuration template
```

---

## ⚙️ How It Works

### 1. How the Frontend Works
1. The user selects either **PDF Upload** (drag-and-drop file) or **Paste Text Mode**.
2. The user enters a Job Description or selects a pre-configured 1-click template (*Data Scientist*, *Full Stack Web Developer*, *DevOps Engineer*, etc.).
3. When the user clicks **Analyze Resume & JD Match**, [frontend/src/services/api.js](file:///c:/Users/ADITYA%20PRTAP%20SINGH/OneDrive/Desktop/resumescreening-main%20-%20Copy/resumescreening-main/frontend/src/services/api.js) sends a `multipart/form-data` request (`/api/upload-resume`) or JSON request (`/api/screen-resume`) to the FastAPI backend.
4. While waiting, the frontend displays an interactive loading spinner.
5. Upon receiving the structured JSON response, React updates state and renders the 4 KPI cards and interactive tabs without reloading the page.

### 2. How the Backend Works
1. **Document Ingestion & Text Extraction**: When a PDF is uploaded, `backend.utils.pdf_extractor` extracts all readable text pages using `pdfplumber`.
2. **Text Normalization**: `backend.utils.preprocessing` strips PII (emails, phone numbers, URLs) while safeguarding programming tokens (`C++`, `C#`, `.NET`, `Node.js`).
3. **Entity & Skill Extraction**: `backend.services.parser_service` scans the text against a 160+ skill taxonomy using word boundary regex, estimates professional experience years (filtering out college degree durations), and detects degrees.
4. **NLP Domain Classification**: `backend.services.model_service` runs the TF-IDF vectorizer and trained Logistic Regression pipeline on the normalized text to predict the candidate's domain category.
5. **Dual Matching & Scoring**: `backend.services.matcher_service` calculates the exact intersection of required JD skills vs candidate skills, computes TF-IDF N-gram cosine similarity, and checks experience requirements.
6. **Explainability Synthesis**: `backend.services.explainability_service` compiles decision reasons, generates custom screening questions targeting candidate skill gaps, and returns a unified Pydantic response.

---

## 📡 REST API Endpoints

| HTTP Method | Endpoint | Description | Request Body / Form | Response Model |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/health` | System health check and model readiness status | None | `HealthResponse` |
| `GET` | `/api/sample-jds` | Returns pre-configured Job Description templates | None | `SampleJDsResponse` |
| `POST` | `/api/extract-skills` | Extracts boundary-safe technical skills from input text | `{"text": "..."}` | `SkillExtractionResponse` |
| `POST` | `/api/extract-text` | Parses resume text into structured profile | `{"text": "..."}` | `TextExtractResponse` |
| `POST` | `/api/predict-category` | Classifies resume domain using NLP model | `{"text": "..."}` | `CategoryPredictionResponse` |
| `POST` | `/api/match-job` | Evaluates candidate fit against JD | `{"resume_text": "...", "job_description": "..."}` | `JobMatchResponse` |
| `POST` | `/api/screen-resume` | Unified JSON endpoint for end-to-end evaluation | `{"resume_text": "...", "job_description": "..."}` | `ScreeningResponse` |
| `POST` | `/api/upload-resume` | Multipart PDF resume upload + screening against JD | `file: UploadFile` + `job_description: str` | `ScreeningResponse` |

---

## 💻 Installation & Setup Guide

### 1. Prerequisites
- Python 3.10 or higher
- Node.js 18+ and npm (for React Vite development)
- Git

---

### 2. Backend Setup

```bash
# 1. Clone repository
git clone https://github.com/your-username/AI-Resume-Screening.git
cd AI-Resume-Screening

# 2. Create and activate a Python virtual environment
# Windows:
python -m venv venv
venv\Scripts\activate
# Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# 3. Install backend dependencies
pip install -r backend/requirements.txt
```

---

### 3. Frontend Setup

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install npm packages
npm install
```

---

## 🔐 Environment Variables

Create `.env` in the `frontend/` directory (or copy from `.env.example`):

```env
# Frontend Configuration (.env)
VITE_API_BASE_URL=http://127.0.0.1:8000
```

---

## 🚀 Running the Complete Project

### Step 1: Launch FastAPI Backend Server (Terminal 1)
```bash
# From project root:
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
- Interactive Swagger Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health Check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### Step 2: Launch React Frontend (Terminal 2)
```bash
# From frontend directory:
cd frontend
npm run dev
```
- Open browser at: **[http://localhost:3000](http://localhost:3000)** (or Vite's active port).

> **💡 Zero-Setup Browser Mode**: You can also double-click [frontend/standalone.html](file:///c:/Users/ADITYA%20PRTAP%20SINGH/OneDrive/Desktop/resumescreening-main%20-%20Copy/resumescreening-main/frontend/standalone.html) or run `python -m http.server 3000 --directory frontend` to launch the React frontend directly in any browser with zero npm installs!

---

## 📊 Example API Workflow

### Request (`POST /api/screen-resume`):
```json
{
  "resume_text": "Senior Python Developer with 4 years of experience building scalable backend APIs using FastAPI, Docker, PostgreSQL, and Git. Bachelor of Technology in Computer Science.",
  "job_description": "Seeking a Senior Backend Engineer with 3+ years of experience in Python, FastAPI, Docker, and Kubernetes.",
  "filename": "senior_developer_resume.txt"
}
```

### Response (`200 OK`):
```json
{
  "document_name": "senior_developer_resume.txt",
  "predicted_category": "Python Developer",
  "profile": {
    "skills": ["docker", "fastapi", "git", "postgresql", "python"],
    "skills_str": "docker, fastapi, git, postgresql, python",
    "experience_years": 4,
    "education": "B.Tech",
    "certification": "None",
    "projects_count": 1,
    "clean_text": "senior python developer with 4 years of experience..."
  },
  "match_result": {
    "composite_score": 80.7,
    "skill_score": 75.0,
    "semantic_score": 62.4,
    "matched_skills": ["docker", "fastapi", "python"],
    "missing_skills": ["kubernetes"],
    "extra_skills": ["git", "postgresql"],
    "grade": "Strong Match",
    "total_required_skills": 4,
    "total_matched_skills": 3,
    "candidate_experience": 4,
    "required_experience": 3,
    "experience_status": "Exceeded",
    "experience_score": 100.0,
    "candidate_education": "B.Tech",
    "required_education": null,
    "education_status": "Candidate: B.Tech"
  },
  "hiring_decision": {
    "decision": "Hire (Recommended for Interview)",
    "category": "Hire",
    "confidence": 85.0,
    "reason": "High alignment (80.7%) with required competencies (docker, fastapi, python), matching experience and education criteria."
  },
  "explainability": {
    "summary_reasons": [
      "✅ Strong Skill Alignment (75.0%): Candidate possesses 3 core competencies required in the JD (docker, fastapi, python).",
      "✅ Experience Criteria Met: Candidate has 4 years of experience (JD required minimum 3 years)."
    ],
    "interview_questions": [
      "Can you explain your familiarity or hands-on experience with Kubernetes, or an equivalent tool you have used in production?",
      "Walk us through a challenging project where you leveraged Docker to deliver measurable business impact.",
      "How do you approach learning and rapidly mastering new frameworks or architectures required for a new role?"
    ],
    "improvement_tips": [
      "Highlight practical project experience with missing core skills: kubernetes."
    ],
    "feature_contributions": [
      { "feature": "Skill Match Coverage", "impact": "75.0%", "type": "Positive" },
      { "feature": "Contextual Semantic Similarity", "impact": "62.4%", "type": "Positive" },
      { "feature": "Experience Qualification", "impact": "4 yrs", "type": "Positive" }
    ]
  }
}
```

---

## 🧪 Automated Testing

The backend includes a comprehensive automated test suite testing preprocessing, parsing heuristics, NLP category inferences, decision synthesis, and FastAPI endpoints:

```bash
# Run all automated tests
python -m unittest discover -s backend/tests -p "test_*.py"
```

```
........................
----------------------------------------------------------------------
Ran 24 tests in 0.182s

OK
```

---

## 🖼️ Application Preview

*(Add screenshots of your application dashboard here before presentation)*

| Candidate Input & Presets | KPI Overview & Skill Gap Analysis |
| :---: | :---: |
| `[ Screenshot 1: Resume Upload & JD Selection ]` | `[ Screenshot 2: Match Score & Recommendation ]` |

| Explainable AI Insights | Extracted Profile & Inspector |
| :---: | :---: |
| `[ Screenshot 3: Auto-Generated Interview Questions ]` | `[ Screenshot 4: Parsed Candidate Metadata ]` |

---

## 🔮 Future Improvements

1. **OCR Support for Scanned PDFs**: Integrate `pytesseract` or PaddleOCR to parse image-only scanned resumes.
2. **Transformer-Based Dense Embeddings**: Integrate Sentence-Transformers (`all-MiniLM-L6-v2`) for deeper semantic embeddings.
3. **Batch Screening & Recruiter Leaderboard**: Support uploading a ZIP file containing multiple resumes to rank all applicants against a single Job Description.
4. **Exportable PDF Screening Reports**: Generate one-click downloadable candidate screening summary reports for hiring managers.

---

## ⚖️ Ethical AI & Recruitment Disclaimer

> **⚠️ Disclaimer**: This system is designed strictly as an **assistive, decision-support tool** to aid recruiters in ranking candidate competencies and accelerating initial screening. It is **not** an automated hiring replacement. Final recruitment evaluations, interview decisions, and employment selections should always be conducted by authorized human hiring teams in compliance with fair hiring regulations and ethical AI employment guidelines.
