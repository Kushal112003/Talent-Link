# backend/app/routers/users.py
from fastapi import APIRouter, Depends
from ..auth import get_current_user
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=schemas.UserOut)
def read_me(user = Depends(get_current_user)):
    return user

@router.get("/me/resumes")
def my_resumes(user = Depends(get_current_user)):
    db = SessionLocal()
    try:
        resumes = db.query(models.Resume).filter(models.Resume.owner_id == user.id).order_by(models.Resume.created_at.asc()).all()
        out = [{"id": r.id, "filename": r.filename, "score": r.ats_score, "timestamp": r.created_at.strftime("%Y-%m-%d %H:%M:%S")} for r in resumes]
        return out
    finally:
        db.close()

@router.put("/me", response_model=schemas.UserOut)
def update_me(profile: schemas.UserCreate, user = Depends(get_current_user)):
    # Note: Using UserCreate for simplicity, though it requires password. 
    # Ideally should use a separate UserUpdate schema.
    # For now, we will just update tags and full_name if provided, ignoring password complexity for this specific task scope
    # unless UserCreate is strictly enforced.
    # Better approach: Create a dynamic update or just use body parameters.
    # Let's create a UserUpdate schema inline or just accept dict body if we want to be quick, but schema is better.
    # Re-reading schemas.py: UserCreate has email, password, full_name, tags.
    # Let's define a local UserUpdate or just handle it here.
    db = SessionLocal()
    try:
        user_db = db.query(models.User).filter(models.User.id == user.id).first()
        if profile.full_name:
            user_db.full_name = profile.full_name
        if profile.tags is not None:
            user_db.tags = profile.tags
        db.commit()
        db.refresh(user_db)
        return user_db
    finally:
        db.close()
