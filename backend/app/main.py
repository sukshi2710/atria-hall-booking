##Om Namah Shivayah##
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import engine, Base, SessionLocal
from app.models import Admin
from app.auth import get_password_hash
from app.routers import bookings, admin

# Initialize database schema
Base.metadata.create_all(bind=engine)

app = FastAPI(title="College Hall Booking API", version="1.0.0")

# Enable CORS for cross-origin frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints
app.include_router(bookings.router)
app.include_router(admin.router)

# Resolve path to the frontend folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../frontend"))

# Mount frontend assets if directory exists
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/", include_in_schema=False)
    def serve_home():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

    @app.get("/admin", include_in_schema=False)
    def serve_admin():
        return FileResponse(os.path.join(FRONTEND_DIR, "admin.html"))

    # Explicit route for direct file requests (CSS, JS, Images)
    @app.get("/{filename}", include_in_schema=False)
    def serve_static_file(filename: str):
        file_path = os.path.join(FRONTEND_DIR, filename)
        if os.path.exists(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.on_event("startup")
def create_or_update_admin():
    db = SessionLocal()
    try:
        target_username = "admin"
        # REPLACE THIS with your desired new plain password:
        target_password = "Atria@2026"

        admin_record = db.query(Admin).filter(Admin.username == target_username).first()

        if not admin_record:
            # Create the record if it does not exist yet
            new_admin = Admin(
                username=target_username,
                password_hash=get_password_hash(target_password),
                email="admin@college.edu"
            )
            db.add(new_admin)
            db.commit()
            print("[AUTH] Default admin created successfully.")
        else:
            # Overwrite password hash with the new password
            admin_record.password_hash = get_password_hash(target_password)
            db.commit()
            print("[AUTH] Admin password synchronized successfully.")
    except Exception as e:
        print(f"[AUTH ERROR] Failed to configure admin credentials: {e}")
    finally:
        db.close()

@app.get("/api/health", tags=["System"])
def health_check():
    return {"status": "running", "system": "Seminar & Placement Hall Booking Portal"}
