# backend/app/routers/resumes.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from ..auth import get_current_user
from ..config import settings
import os
from ..tasks.worker import parse_and_score
from ..services.parser import extract_text_from_pdf
from ..services.scoring import tfidf_cosine_score
from ..services.suggestions import generate_suggestions
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/resumes", tags=["resumes"])

@router.post("/upload_sync", response_model=dict)
async def upload_resume_sync(file: UploadFile = File(...), job_description: str = Form(""), user = Depends(get_current_user)):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    text = extract_text_from_pdf(file_path)
    score = tfidf_cosine_score(text, job_description)
    suggestions = generate_suggestions(text, job_description)
    db = SessionLocal()
    try:
        resume = models.Resume(filename=file.filename, text=text, ats_score=score, owner_id=user.id)
        db.add(resume)
        db.commit()
        db.refresh(resume)
    finally:
        db.close()
    return {"resume_id": resume.id, "score": score, "suggestions": suggestions}

@router.post("/upload_async", response_model=dict)
async def upload_resume_async(file: UploadFile = File(...), job_description: str = Form(""), user = Depends(get_current_user)):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    # schedule background task
    task = parse_and_score.delay(file_path, job_description, user.id)
    return {"task_id": task.id}
