from app.services.analyzer import analyze_resume


def test_basic_resume_analysis():
    text = """
    Shubham Example
    shubham@example.com
    +91 9876543210
    linkedin.com/in/shubhamexample

    Professional Summary
    Python backend developer with 3 years of experience.

    Technical Skills
    Python, FastAPI, Django, REST API, PostgreSQL, Git, React

    Experience
    Developed REST APIs and optimized response time by 35%.
    Built automation used by 20 clients.

    Education
    Bachelor of Engineering

    Projects
    Resume Analyzer using Python and React.
    """
    result = analyze_resume(text)
    assert result["score"] > 50
    assert "Python" in result["skills"]
    assert result["contact"]["email"] == "shubham@example.com"
