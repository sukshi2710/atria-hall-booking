import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

is_vercel = os.getenv("VERCEL") is not None

if is_vercel:
    tmp_db_path = "/tmp/hall_booking.db"
    
    # Path to the bundled database in the repository
    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_db_path = os.path.abspath(os.path.join(base_dir, "..", "hall_booking.db"))
    
    # If the tmp database doesn't exist yet, copy the pre-existing one over
    if not os.path.exists(tmp_db_path) and os.path.exists(source_db_path):
        try:
            shutil.copyfile(source_db_path, tmp_db_path)
        except Exception as e:
            print(f"Error copying database: {e}")
            
    DATABASE_URL = f"sqlite:///{tmp_db_path}"
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hall_booking.db")

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
