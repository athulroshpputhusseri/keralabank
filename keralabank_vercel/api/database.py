import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# For Vercel deployment, use tmp directory for SQLite
DATA_DIR = "tmp"
DATABASE_FILE = os.path.join(DATA_DIR, "bank.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Ensure tmp directory exists
os.makedirs(DATA_DIR, exist_ok=True)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass
