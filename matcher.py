from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from skill_extractor import extract_skills

model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_similarity(resume_text, job_text):
    """
    Computes semantic similarity using SBERT
    """
    embeddings = model.encode([resume_text, job_text])

    similarity = cosine_similarity(
        [embeddings[0]], [embeddings[1]]
    )[0][0]

    return round(float(similarity), 3)


def match_resume_job(resume_text, job_text):
    """
    Wrapper function used by UI
    """
    return compute_similarity(resume_text, job_text)


def skill_gap_analysis(resume_text, job_text):
    """
    Extract matched and missing skills
    """
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - resume_skills

    return list(matched_skills), list(missing_skills)

