# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

engine_args = {"pool_pre_ping": True}
if "sqlite" in settings.DATABASE_URL:
    engine_args = {"connect_args": {"check_same_thread": False}}

engine = create_engine(settings.DATABASE_URL, **engine_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
