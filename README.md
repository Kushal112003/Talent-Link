# TalentLink — AI Resume Screening & Candidate Ranking System

## Overview
TalentLink is a full-stack app:
- Backend: FastAPI, PostgreSQL, Redis + Celery for background tasks, TF-IDF scoring (scikit-learn), PyMuPDF resume parsing.
- Frontend: Next.js (pages), minimalistic professional UI (components included).

## Quick start (local, docker)
1. Copy repository and files exactly as provided.
2. Create `.env` from `.env.example` and update secrets if needed.
3. From repo root:
   ```bash
   docker-compose up --build
   ```

## Manual Setup (Local Dev)

### Backend
1. Navigate to `backend`:
   ```bash
   cd backend
   ```
2. Create virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install pydantic-settings # Ensure this is installed
   ```
3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend
1. Navigate to `frontend`:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

