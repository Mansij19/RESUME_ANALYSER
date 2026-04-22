"""
Job Description Matcher Service
================================
Compares resume text with a job description using TF-IDF
cosine similarity and identifies missing skills.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.services.skill_extractor import SKILL_DATABASE


def match(resume_text, jd_text):
    """
    Calculate match score between resume and job description.

    Args:
        resume_text (str): The resume text.
        jd_text (str): The job description text.

    Returns:
        dict or None: {'score': float, 'missing_skills': list[str]}
    """
    if not jd_text or not jd_text.strip():
        return None

    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    match_score = round(similarity * 100, 1)

    resume_lower = resume_text.lower()
    jd_lower = jd_text.lower()
    missing_skills = []

    for category, skills in SKILL_DATABASE.items():
        for skill in skills:
            if skill in jd_lower and skill not in resume_lower:
                display = skill.upper() if len(skill) <= 3 else skill.title()
                missing_skills.append(display)

    return {
        "score": match_score,
        "missing_skills": missing_skills[:15]
    }
