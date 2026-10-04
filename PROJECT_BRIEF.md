# AI Resume Analyzer — Collaboration Brief

## Project goal

Build a practical AI-powered web application that helps a user understand the quality of a resume and identify how well the profile fits different job roles.

The project is intentionally divided into small phases so both developers can learn, contribute, review each other's work, and keep the first deliverable manageable.

## Phase 1 — POC

Phase 1 does not require a paid AI API.

### User flow

1. User opens the web application.
2. User uploads a PDF or DOCX resume.
3. Backend extracts resume text.
4. Backend identifies contact information and technical skills.
5. A rule engine calculates a resume score.
6. The system suggests practical improvements.
7. The system shows possible matching job roles.
8. Results are displayed in the React frontend.

## Architecture

```text
React Frontend
      |
      | multipart/form-data
      v
FastAPI REST API
      |
      +--> Resume Parser
      |      +-- PDF -> pypdf
      |      +-- DOCX -> python-docx
      |
      +--> Resume Analyzer
             +-- Contact extraction
             +-- Skill extraction
             +-- Section detection
             +-- Score calculation
             +-- Improvement rules
             +-- Role matching
```

## Responsibilities

### Shubham

- Overall architecture and repository setup
- FastAPI project structure
- API contract and integration
- Resume scoring design
- Code review and final integration
- Phase 2 LLM integration design

### Nishtha

Suggested first ownership area:

- Resume parsing service for PDF/DOCX
- Validation and error handling
- Skill extraction improvements
- Backend test cases
- Documentation for parser behavior

Because Nishtha is learning React, she can also pick one small frontend issue after the backend parser is complete.

### Shared

- GitHub pull-request review
- Testing different resume formats
- Deciding scoring improvements
- Weekly feature selection
- README/documentation
- Demo preparation

## Suggested 1-week POC milestone

Day 1:
- Repository setup
- Branch workflow
- Backend/frontend start successfully

Day 2:
- PDF and DOCX parsing

Day 3:
- Contact and skill extraction

Day 4:
- Resume scoring and suggestions

Day 5:
- React results UI and API integration

Day 6:
- Testing and bug fixes

Day 7:
- Demo, README cleanup, and Phase 2 discussion

This is a learning milestone rather than a hard deadline.

## Phase 2

- LLM integration
- Job description matching
- ATS keyword gap analysis
- AI-generated resume suggestions
- Better experience/project extraction

## Phase 3

- Authentication
- PostgreSQL
- Saved analyses
- PDF reports
- Deployment
