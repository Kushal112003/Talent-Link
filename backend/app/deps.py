# backend/app/deps.py
from fastapi import Depends, HTTPException, status
from .auth import get_current_user
from sqlalchemy.orm import Session
from .database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def require_role(role: str):
    def inner(user = Depends(get_current_user)):
        if user.role != role and user.role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
    return inner
