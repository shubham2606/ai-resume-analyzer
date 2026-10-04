import re
from collections import OrderedDict

SKILLS = [
    "Python", "FastAPI", "Django", "Flask", "JavaScript", "TypeScript",
    "React", "Node.js", "Express", "HTML", "CSS", "Bootstrap", "Tailwind",
    "SQL", "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis",
    "REST API", "GraphQL", "Git", "GitHub", "Docker", "Kubernetes",
    "AWS", "Azure", "GCP", "Linux", "Pandas", "NumPy", "Scikit-learn",
    "TensorFlow", "PyTorch", "Machine Learning", "NLP", "LLM",
    "Frappe", "ERPNext", "Selenium", "BeautifulSoup",
]

SKILL_PATTERNS = {
    "Node.js": r"\bnode(?:\.js|js)?\b",
    "REST API": r"\brest(?:ful)?\s+api(?:s)?\b|\brest\b",
    "GitHub": r"\bgithub\b",
    "Git": r"\bgit\b",
    "Scikit-learn": r"\bscikit[- ]learn\b|\bsklearn\b",
    "Machine Learning": r"\bmachine learning\b",
    "NLP": r"\bnlp\b|\bnatural language processing\b",
    "LLM": r"\bllm(?:s)?\b|\blarge language model(?:s)?\b",
}

ACTION_VERBS = [
    "built", "developed", "designed", "implemented", "created", "improved",
    "optimized", "automated", "integrated", "deployed", "led", "managed",
    "reduced", "increased", "delivered", "engineered",
]

SECTION_PATTERNS = OrderedDict([
    ("summary", r"\b(summary|profile|objective|professional summary)\b"),
    ("skills", r"\b(skills|technical skills|technologies|tech stack)\b"),
    ("experience", r"\b(experience|work experience|employment|professional experience)\b"),
    ("education", r"\b(education|academic|qualification|qualifications)\b"),
    ("projects", r"\b(projects|project experience|personal projects)\b"),
])

ROLE_REQUIREMENTS = OrderedDict([
    ("Python Backend Developer", ["Python", "FastAPI", "Django", "REST API", "SQL", "PostgreSQL", "Git"]),
    ("Full Stack Developer", ["Python", "JavaScript", "React", "REST API", "SQL", "Git"]),
    ("Data Analyst", ["Python", "SQL", "Pandas", "NumPy", "Excel"]),
    ("Machine Learning Engineer", ["Python", "Machine Learning", "Scikit-learn", "Pandas", "NumPy"]),
    ("ERPNext / Frappe Developer", ["Python", "Frappe", "ERPNext", "JavaScript", "SQL"]),
])

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?\d{1,3}[-\s]?)?(?:\d[-\s]?){9,12}(?!\d)")
LINKEDIN_RE = re.compile(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?", re.I)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_contact(text: str) -> dict:
    email_match = EMAIL_RE.search(text)
    phone_match = PHONE_RE.search(text)
    linkedin_match = LINKEDIN_RE.search(text)
    return {
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0).strip() if phone_match else None,
        "linkedin": linkedin_match.group(0) if linkedin_match else None,
    }


def extract_skills(text: str) -> list[str]:
    lowered = text.lower()
    found = []

    for skill in SKILLS:
        pattern = SKILL_PATTERNS.get(skill)
        if pattern:
            matched = re.search(pattern, lowered, re.I)
        else:
            matched = re.search(rf"(?<!\w){re.escape(skill.lower())}(?!\w)", lowered)

        if matched and skill not in found:
            found.append(skill)

    return found


def detect_sections(text: str) -> dict:
    return {
        section: bool(re.search(pattern, text, re.I))
        for section, pattern in SECTION_PATTERNS.items()
    }


def estimate_experience(text: str) -> str:
    explicit = re.findall(
        r"\b(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?experience\b",
        text,
        re.I,
    )
    if explicit:
        years = max(float(value) for value in explicit)
        if years.is_integer():
            years = int(years)
        return f"{years} years (mentioned in resume)"

    # Simple fallback: detect year ranges such as 2021 - 2024 / 2021 - Present.
    ranges = re.findall(
        r"\b((?:19|20)\d{2})\s*(?:-|–|—|to)\s*((?:19|20)\d{2}|present|current)\b",
        text,
        re.I,
    )
    durations = []
    from datetime import datetime
    current_year = datetime.now().year

    for start, end in ranges:
        start_year = int(start)
        end_year = current_year if end.lower() in {"present", "current"} else int(end)
        if 0 <= end_year - start_year <= 50:
            durations.append(end_year - start_year)

    if durations:
        approx = max(durations)
        return f"Approximately {approx}+ years based on detected date ranges"

    return "Not confidently detected"


def calculate_score(text: str, skills: list[str], contact: dict, sections: dict) -> tuple[int, list[dict]]:
    score = 0
    breakdown = []

    contact_points = 0
    contact_points += 4 if contact["email"] else 0
    contact_points += 3 if contact["phone"] else 0
    contact_points += 3 if contact["linkedin"] else 0
    score += contact_points
    breakdown.append({"name": "Contact details", "score": contact_points, "max": 10})

    section_points = round(sum(sections.values()) / len(sections) * 25)
    score += section_points
    breakdown.append({"name": "Important sections", "score": section_points, "max": 25})

    skill_points = min(20, len(skills) * 2)
    score += skill_points
    breakdown.append({"name": "Relevant skills", "score": skill_points, "max": 20})

    quantified = re.findall(r"\b\d+(?:\.\d+)?\s*(?:%|x|k|m|hours?|days?|users?|clients?|projects?)\b", text, re.I)
    impact_points = min(15, len(quantified) * 3)
    score += impact_points
    breakdown.append({"name": "Quantified impact", "score": impact_points, "max": 15})

    verb_count = sum(1 for verb in ACTION_VERBS if re.search(rf"\b{verb}\b", text, re.I))
    verb_points = min(10, verb_count * 2)
    score += verb_points
    breakdown.append({"name": "Action-oriented writing", "score": verb_points, "max": 10})

    words = text.split()
    word_count = len(words)
    if 250 <= word_count <= 900:
        length_points = 10
    elif 150 <= word_count < 250 or 900 < word_count <= 1200:
        length_points = 7
    else:
        length_points = 4
    score += length_points
    breakdown.append({"name": "Resume length", "score": length_points, "max": 10})

    readability_points = 10 if len(_normalize(text)) > 500 else 5
    score += readability_points
    breakdown.append({"name": "Readable extracted content", "score": readability_points, "max": 10})

    return min(100, score), breakdown


def build_suggestions(text: str, skills: list[str], contact: dict, sections: dict) -> list[str]:
    suggestions = []

    if not contact["linkedin"]:
        suggestions.append("Add a LinkedIn profile URL near your contact information.")
    if not sections["summary"]:
        suggestions.append("Add a concise professional summary tailored to the role you are targeting.")
    if not sections["skills"]:
        suggestions.append("Add a clearly labeled Technical Skills section for ATS readability.")
    if not sections["projects"]:
        suggestions.append("Add 2–3 relevant projects with your role, technologies, and measurable outcomes.")
    if len(skills) < 6:
        suggestions.append("Include more role-relevant technical skills that you genuinely use.")

    quantified = re.findall(r"\b\d+(?:\.\d+)?\s*(?:%|x|k|m|hours?|days?|users?|clients?|projects?)\b", text, re.I)
    if len(quantified) < 2:
        suggestions.append("Quantify achievements, for example: reduced API response time by 30%.")

    verb_count = sum(1 for verb in ACTION_VERBS if re.search(rf"\b{verb}\b", text, re.I))
    if verb_count < 4:
        suggestions.append("Start more experience bullets with strong action verbs such as Built, Developed, Automated, or Optimized.")

    if not suggestions:
        suggestions.append("The resume has a strong basic structure. Next, tailor keywords and achievements for each target job description.")

    return suggestions[:6]


def match_roles(skills: list[str]) -> list[dict]:
    skill_set = {skill.lower() for skill in skills}
    results = []

    for role, required in ROLE_REQUIREMENTS.items():
        matched = [skill for skill in required if skill.lower() in skill_set]
        missing = [skill for skill in required if skill.lower() not in skill_set]
        percent = round((len(matched) / len(required)) * 100)
        results.append({
            "role": role,
            "match_percent": percent,
            "matched_skills": matched,
            "missing_skills": missing[:4],
        })

    return sorted(results, key=lambda item: item["match_percent"], reverse=True)[:4]


def analyze_resume(text: str) -> dict:
    clean_text = _normalize(text)
    contact = extract_contact(clean_text)
    skills = extract_skills(clean_text)
    sections = detect_sections(text)
    score, breakdown = calculate_score(clean_text, skills, contact, sections)

    return {
        "score": score,
        "contact": contact,
        "skills": skills,
        "estimated_experience": estimate_experience(clean_text),
        "sections": sections,
        "score_breakdown": breakdown,
        "suggestions": build_suggestions(clean_text, skills, contact, sections),
        "job_matches": match_roles(skills),
        "note": "Phase 1 uses deterministic rules. Phase 2 can add an LLM for deeper semantic suggestions and job-description matching.",
    }
