# backend/app/services/scoring.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def tfidf_cosine_score(resume_text: str, job_description: str) -> float:
    if not resume_text or not job_description:
        return 0.0
    docs = [resume_text, job_description]
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
    tfidf = vectorizer.fit_transform(docs)
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(float(score * 100), 2)
