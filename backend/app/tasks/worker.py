# backend/app/tasks/worker.py
from celery import Celery
from ..config import settings
import os
from ..services.parser import extract_text_from_pdf
from ..services.scoring import tfidf_cosine_score
from ..database import SessionLocal
from .. import models

celery = Celery("worker", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@celery.task
def parse_and_score(resume_path: str, job_description: str, user_id: int):
    text = extract_text_from_pdf(resume_path)
    score = tfidf_cosine_score(text, job_description)
    db = SessionLocal()
    try:
        resume = models.Resume(filename=os.path.basename(resume_path), text=text, ats_score=score, owner_id=user_id)
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return {"resume_id": resume.id, "score": score}
    finally:
        db.close()
