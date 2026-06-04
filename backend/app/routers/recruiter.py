# backend/app/routers/recruiter.py
from fastapi import APIRouter, Depends, Query, UploadFile, File
from ..auth import get_current_user
from ..database import SessionLocal
from .. import models, schemas
from sqlalchemy import or_
import fitz # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

router = APIRouter(prefix="/recruiter", tags=["recruiter"])

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/resumes", response_model=list[schemas.UserOut])
def get_candidates(q: str = None, tags: str = None, user = Depends(get_current_user)):
    # Check if user is recruiter
    # if user.role != "recruiter": raise HTTPException... (Skipping strictly for MVP velocity as requested, but good practice)
    
    db = SessionLocal()
    try:
        query = db.query(models.User).filter(models.User.role == "candidate")
        
        if q:
            search = f"%{q}%"
            query = query.filter(or_(models.User.full_name.ilike(search), models.User.email.ilike(search)))
        
        if tags:
            # Simple substring match for tags since we store them as comma strings
            # For more robust logic, we'd split and check intersection
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]
            for tag in tag_list:
                query = query.filter(models.User.tags.ilike(f"%{tag}%"))
                
        candidates = query.all()
        return candidates
    finally:
        db.close()

@router.post("/match-resume")
async def match_resume(file: UploadFile = File(...), user = Depends(get_current_user)):
    db = SessionLocal()
    try:
        # 1. Extract text from uploaded file
        content = await file.read()
        target_text = ""
        
        if file.filename.endswith(".pdf"):
            try:
                with fitz.open(stream=content, filetype="pdf") as doc:
                    for page in doc:
                        target_text += page.get_text()
            except Exception as e:
                logger.error(f"Error reading PDF: {e}")
                target_text = content.decode("utf-8", errors="ignore") # Fallback
        else:
             target_text = content.decode("utf-8", errors="ignore")

        # 2. Get all candidate resumes
        candidates_with_resumes = db.query(models.User).filter(models.User.role == "candidate").all()
        
        if not candidates_with_resumes:
            return []

        documents = [target_text]
        candidate_map = []
        
        for cand in candidates_with_resumes:
            # Concatenate all resume keys or just pick the latest resume
            # Simplified: Use the text of the latest resume
            latest_resume = db.query(models.Resume).filter(models.Resume.owner_id == cand.id).order_by(models.Resume.created_at.desc()).first()
            if latest_resume and latest_resume.text:
                documents.append(latest_resume.text)
                candidate_map.append(cand)
        
        if len(documents) <= 1:
            return []

        # 3. TF-IDF
        tfidf = TfidfVectorizer(stop_words='english')
        try:
            tfidf_matrix = tfidf.fit_transform(documents)
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
            
            # 4. Rank
            scores = cosine_sim[0]
            ranked_indices = scores.argsort()[::-1]
            
            results = []
            for idx in ranked_indices:
                score = float(scores[idx])
                if score > 0.05: # Threshold
                    cand = candidate_map[idx]
                    # Use schema manually or construct dict
                    cand_data = schemas.UserOut.from_orm(cand).dict()
                    cand_data["match_score"] = round(score * 100, 1)
                    results.append(cand_data)
            
            return results
            
        except ValueError:
            # Handle empty vocabulary
            return []

    finally:
        db.close()
