##Om Namah Shivayah##
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app.models import Admin
from app.auth import get_password_hash
from app.routers import bookings, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="College Hall Booking API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bookings.router)
app.include_router(admin.router)

@app.on_event("startup")
def create_initial_admin():
    db = SessionLocal()
    if not db.query(Admin).first():
        default_admin = Admin(
            username="admin",
            password_hash=get_password_hash("admin123"), # Change for production!
            email="admin@college.edu"
        )
        db.add(default_admin)
        db.commit()
    db.close()

@app.get("/")
def health_check():
    return {"status": "running", "system": "Seminar & Placement Hall Booking Portal"}