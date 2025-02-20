from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from resume_parser import extract_skills

def calculate_skill_match_score(resume_skills, job_skills):
    """Calculate skill match score between resume and job description."""
    if not job_skills:
        return 0
    
    matches = sum(1 for skill in resume_skills if skill in job_skills)
    return matches / len(job_skills)

def rank_resumes(resumes, job_description):
    """Rank resumes based on similarity to job description."""
    job_skills = extract_skills(job_description)
    documents = [job_description] + [resume['text'] for resume in resumes]
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    cos_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    
    ranked_candidates = []
    for idx, resume in enumerate(resumes):
        resume_skills = extract_skills(resume['text'])
        content_score = cos_similarities[0][idx]
        skill_score = calculate_skill_match_score(resume_skills, job_skills)
        overall_score = (0.5 * content_score) + (0.5 * skill_score)
        
        ranked_candidates.append({
            'filename': resume['filename'],
            'email': resume['email'],
            'score': overall_score,
            'skills': resume_skills
        })
    ranked_candidates.sort(key=lambda x: x['score'], reverse=True)
    
    return ranked_candidates