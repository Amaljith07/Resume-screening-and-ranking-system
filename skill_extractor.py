import re
from skill_db import SKILLS

def extract_skills(text):
    """
    Extract skills from given text using rule-based NER
    """
    text = text.lower()
    found_skills = set()

    for category in SKILLS.values():
        for skill in category:
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, text):
                found_skills.add(skill)

    return found_skills


def skill_gap_analysis(resume_text, job_text):
    """
    Compare resume skills with job required skills
    """
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - resume_skills

    return list(matched_skills), list(missing_skills)
