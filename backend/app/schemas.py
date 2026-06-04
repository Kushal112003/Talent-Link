# backend/app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str]
    tags: Optional[str] = ""
    role: str = "candidate"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    tags: Optional[str]
    role: str

    class Config:
        orm_mode = True

class ResumeOut(BaseModel):
    id: int
    filename: str
    ats_score: float
    created_at: datetime.datetime

    class Config:
        orm_mode = True
