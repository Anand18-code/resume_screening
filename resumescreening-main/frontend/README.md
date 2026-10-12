# AI Resume Screening & JD Fit System - Frontend Client

Modern React.js Single Page Application built with Vite for candidate resume screening, skill gap visualization, and hiring fit assessment.

---

## 🎨 Features

- **Dual Input Modes**: PDF resume drag-and-drop upload and raw resume text pasting.
- **Job Description Presets**: 1-click preset templates (*Data Scientist, Full Stack Developer, DevOps, Cybersecurity, Java Backend*).
- **Executive Metric Cards**: Dynamic overall match score %, skill coverage %, recommendation category, and NLP domain classification.
- **Competency Badges**: Color-coded badges for Matched (Emerald), Missing (Rose), and Additional Skills (Cyan).
- **Recruiter Insights & Questions**: Tailored technical screening interview questions generated from candidate skill gaps.
- **Candidate Profile Metadata**: Formatted table of experience, education, certifications, and project counts.
- **Zero-Dependency Standalone Mode**: Includes `standalone.html` to run in any browser with zero npm installs.

---

## 🏗️ Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx              # App header with live backend status indicator
│   │   ├── ResumeInput.jsx         # PDF dropzone & text mode toggle
│   │   ├── JobDescriptionInput.jsx # JD input with sample preset chips
│   │   ├── MetricCards.jsx         # 4 KPI cards (Score, Coverage, Rec, Domain)
│   │   ├── OverviewTab.jsx         # Fit progress bar, status & alignment table
│   │   ├── SkillAnalysis.jsx       # Matched, Missing & Extra skill badges
│   │   ├── InsightsTab.jsx         # Recruiter reasons, interview questions & tips
│   │   └── CandidateProfileTab.jsx # Extracted entity table & raw text viewer
│   ├── pages/
│   │   └── Dashboard.jsx           # Primary screening dashboard workspace
│   ├── services/
│   │   └── api.js                  # REST API client consuming FastAPI backend
│   ├── App.jsx                     # Application entrypoint
│   ├── main.jsx                    # React DOM root mount
│   └── index.css                   # Custom CSS Design System
├── public/
│   └── favicon.svg                 # Brand icon
├── package.json                    # Project dependencies (React 18, Vite)
├── vite.config.js                  # Vite configuration & backend proxy
├── index.html                      # HTML5 root template
├── standalone.html                 # 0-dependency browser client
├── .env                            # Environment variables (VITE_API_BASE_URL)
└── .env.example                    # Template environment file
```

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Backend API URL
Create or edit `.env`:
```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### 3. Launch Development Server
```bash
npm run dev
```
Open your browser at **[http://localhost:3000](http://localhost:3000)** (or Vite's active port).

---

## 💡 Standalone Browser Execution (0 Dependencies)

If Node.js / npm is not installed, simply open `standalone.html` directly in your browser or run:
```bash
python -m http.server 3000 --directory frontend
```
Navigate to [http://127.0.0.1:3000/standalone.html](http://127.0.0.1:3000/standalone.html) with your FastAPI backend running on port 8000.
