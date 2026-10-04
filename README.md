# ResumeLens AI — AI Resume Analyzer POC

A small two-developer collaboration project built as a practical Phase 1 proof of concept.

## What Phase 1 does

- Upload PDF or DOCX resume
- Extract resume text
- Detect email, phone, and LinkedIn URL
- Detect common technical skills
- Estimate experience when possible
- Check important resume sections
- Generate a deterministic resume score out of 100
- Provide improvement suggestions
- Show basic job-role matches
- Work without a paid AI/API key

Phase 2 can add an LLM for semantic resume feedback, job-description matching, bullet rewriting, and personalized suggestions.

## Tech stack

- Frontend: React + Vite
- Backend: Python + FastAPI
- Resume parsing: pypdf + python-docx
- API: REST
- Phase 1 analysis: Python rule engine
- Git/GitHub: collaboration and pull requests

## Project structure

```text
ai-resume-analyzer-poc/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── services/
│   │       ├── analyzer.py
│   │       └── parser.py
│   ├── tests/
│   │   └── test_analyzer.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── PROJECT_BRIEF.md
├── TASKS.md
└── README.md
```

# Run locally on Windows

## 1. Backend

Open CMD:

```cmd
cd ai-resume-analyzer-poc\backend
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Check:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

## 2. Frontend

Open another CMD:

```cmd
cd ai-resume-analyzer-poc\frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

## API

### `POST /api/analyze`

Form-data field:

```text
file = resume.pdf
```

Response includes:

- score
- contact
- skills
- estimated_experience
- detected sections
- score breakdown
- improvement suggestions
- job-role matches

## Git workflow for two developers

Create the repository once, then both developers work through feature branches.

```cmd
git checkout -b feature/resume-parser
```

or

```cmd
git checkout -b feature/frontend-results
```

Before starting new work:

```cmd
git checkout main
git pull origin main
```

Commit:

```cmd
git add .
git commit -m "Add resume parsing service"
git push origin feature/resume-parser
```

Then create a Pull Request on GitHub. The other developer reviews it before merging.

## Definition of done for Phase 1

- Backend starts without errors
- Frontend starts without errors
- PDF upload works
- DOCX upload works
- Invalid extensions show an error
- Resume analysis appears in the UI
- At least contact, skills, score, suggestions, and role matches are returned
- Code is merged through pull requests
- README is updated

## Phase 2 ideas

1. Add LLM provider abstraction
2. Job description upload/paste
3. Semantic JD-to-resume match score
4. AI rewrite suggestions for weak bullets
5. ATS keyword gap analysis
6. User accounts and analysis history
7. PostgreSQL database
8. Export analysis report as PDF
9. Deployment
