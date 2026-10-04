# Phase 1 Task Board

## P0 — Setup

- [ ] Create GitHub repository
- [ ] Add Shubham and Nishtha as collaborators
- [ ] Confirm both can run backend
- [ ] Confirm both can run frontend
- [ ] Protect `main` from direct feature development

## Backend

### Shubham
- [x] FastAPI starter API
- [x] `/health`
- [x] `/api/analyze`
- [x] Initial scoring logic
- [ ] Review scoring weights after test resumes

### Nishtha
- [x] Starter PDF/DOCX parser included for reference
- [ ] Improve PDF/DOCX parser edge cases
- [ ] Add parser-specific error messages
- [ ] Add 3 test resumes locally and document results
- [ ] Add/extend unit tests
- [ ] Improve skill aliases and detection

## Frontend

### Shubham
- [x] Upload UI
- [x] API integration
- [x] Result cards
- [ ] Final responsive review

### Nishtha / Shared
- [ ] Add file drag-and-drop state
- [ ] Add missing-skills UI to role matches
- [ ] Add better loading state
- [ ] Check mobile layout

## Testing

- [ ] PDF with normal text layout
- [ ] DOCX resume
- [ ] Unsupported file
- [ ] Empty/scanned PDF
- [ ] File larger than 5 MB
- [ ] Resume with no LinkedIn
- [ ] Resume with limited skills

## Demo acceptance checklist

- [ ] Upload succeeds
- [ ] Score shown
- [ ] Skills shown
- [ ] Suggestions shown
- [ ] Role matches shown
- [ ] Errors are user-friendly
- [ ] README setup works on another machine
