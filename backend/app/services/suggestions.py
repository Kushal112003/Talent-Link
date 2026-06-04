# backend/app/services/suggestions.py
def generate_suggestions(resume_text: str, job_description: str):
    suggestions = []
    if not resume_text or len(resume_text) < 400:
        suggestions.append("Add more detail about projects, responsibilities and metrics.")
    if "team" not in resume_text.lower():
        suggestions.append("Mention teamwork / collaboration experiences.")
    jd_tokens = set(job_description.lower().split())
    resume_tokens = set(resume_text.lower().split())
    common_skills = ["python", "machine", "learning", "sql", "aws", "docker", "fastapi", "java", "spring", "react"]
    missing = [w for w in common_skills if (w in jd_tokens and w not in resume_tokens)]
    if missing:
        suggestions.append(f"Include relevant keywords: {', '.join(missing)}.")
    suggestions.append("Use action verbs (Implemented, Designed, Improved) and quantify results.")
    return suggestions
