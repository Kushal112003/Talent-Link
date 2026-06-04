# backend/app/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True, nullable=False)
    full_name = Column(String(256))
    hashed_password = Column(String(256), nullable=False)
    role = Column(String(50), default="candidate")  # candidate, recruiter, admin
    tags = Column(String(1024), default="")  # Comma separated tags
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    resumes = relationship("Resume", back_populates="owner")

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(512))
    text = Column(Text)
    ats_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="resumes")
