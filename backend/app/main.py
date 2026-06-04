# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from .routers import auth_routes, resumes, users, recruiter

# create DB tables - dev only
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# CORS - allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_routes.router)
app.include_router(users.router)
app.include_router(resumes.router)
app.include_router(recruiter.router)

@app.get("/")
def root():
    return {"status": "ok", "project": settings.PROJECT_NAME}
