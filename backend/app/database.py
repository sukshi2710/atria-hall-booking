import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Detect if running in Vercel/serverless or local environment
is_vercel = os.getenv("VERCEL") is not None

if is_vercel:
    DATABASE_URL = "sqlite:////tmp/hall_booking.db"
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hall_booking.db")

# SQLite requires check_same_thread=False in FastAPI
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
