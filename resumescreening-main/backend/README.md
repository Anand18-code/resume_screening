# AI Resume Screening & Fit Assessment System - FastAPI Backend

High-performance RESTful API powering automated resume parsing, NLP domain classification, boundary-safe skill extraction, and multi-factor candidate job matching.

---

## 🛠️ Tech Stack & Architecture

- **Framework**: FastAPI (Async Python 3.10+)
- **Server**: Uvicorn (ASGI)
- **Validation**: Pydantic v2
- **ML & NLP**: Scikit-Learn, TF-IDF Vectorization, Logistic Regression, Joblib
- **Document Processing**: PDFPlumber, Regex Heuristics
- **Testing**: Python `unittest` & `TestClient`

---

## 🏗️ Structure

```
backend/
├── main.py                     # FastAPI application, CORS middleware & REST endpoints
├── requirements.txt            # Backend dependencies
├── models/                     # Serialized ML model pipelines (.pkl)
│   ├── category_model.pkl      # NLP Job Category Classifier (99.5% accuracy)
│   └── screening_model.pkl     # Candidate Fit Pipeline
├── schemas/                    # Pydantic request/response schemas
│   ├── __init__.py
│   └── resume.py
├── services/                   # Modular ML & business services
│   ├── __init__.py
│   ├── model_service.py        # Model loading singleton & domain prediction
│   ├── parser_service.py       # 160+ skill taxonomy extractor, experience & degree
│   ├── matcher_service.py      # Skill coverage, TF-IDF cosine similarity & composite fit
│   └── explainability_service.py # Recruiter reasoning, interview questions & tips
├── utils/                      # Reusable helper utilities
│   ├── __init__.py
│   ├── preprocessing.py        # Regex cleaning, PII removal, tech token preservation
│   └── pdf_extractor.py        # PDF document text extraction stream processor
├── uploads/                    # Temporary upload buffer
└── tests/                      # Automated unit & integration tests
    ├── __init__.py
    ├── test_api.py             # Integration tests for FastAPI endpoints
    └── test_services.py        # Unit tests for services and parsers
```

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the FastAPI Server
From the project root:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
Or from the `backend/` directory:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 3. API Documentation
- **Interactive Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Interactive Docs**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## 📡 REST Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Returns service status and ML model readiness |
| `GET` | `/api/sample-jds` | Returns sample Job Description presets |
| `POST` | `/api/extract-skills` | Extracts technical skills from input text |
| `POST` | `/api/extract-text` | Parses raw resume text into structured candidate profile |
| `POST` | `/api/predict-category` | Classifies candidate resume domain |
| `POST` | `/api/match-job` | Compares resume with JD (matched/missing skills, fit scores) |
| `POST` | `/api/screen-resume` | Unified JSON endpoint for end-to-end evaluation |
| `POST` | `/api/upload-resume` | Multipart PDF file upload + screening |

---

## 🧪 Running Backend Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```
*(All 21 automated unit and endpoint integration tests pass with 100% success).*
