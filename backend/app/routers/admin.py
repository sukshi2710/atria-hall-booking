import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Booking, Admin
from app.schemas import BookingOut, BookingCreate
from app.auth import verify_password, create_access_token, get_current_admin
from app.conflict_engine import check_hall_clash
from app.excel_service import append_booking_to_excel, initialize_excel_ledger, EXCEL_FILE_PATH
from app.email_service import send_cancellation_email

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == form_data.username).first()
    if not admin or not verify_password(form_data.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": admin.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/bookings", response_model=List[BookingOut])
def list_all_bookings(admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    return db.query(Booking).order_by(Booking.start_datetime.desc()).all()


@router.get("/export-excel")
def export_excel_ledger(admin: Admin = Depends(get_current_admin)):
    """Allows the in-charge/admin to download the updated .xlsx ledger."""
    try:
        initialize_excel_ledger()
    except Exception as e:
        print(f"[EXCEL WARN] Ledger init error: {e}")

    if not os.path.exists(EXCEL_FILE_PATH):
        raise HTTPException(status_code=404, detail="Excel ledger file not found")
        
    return FileResponse(
        path=EXCEL_FILE_PATH,
        filename="college_hall_bookings_ledger.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@router.put("/bookings/{booking_id}", response_model=BookingOut)
def update_booking(
    booking_id: int, 
    update_data: BookingCreate, 
    admin: Admin = Depends(get_current_admin), 
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    clash = check_hall_clash(
        db, update_data.venue, update_data.start_datetime, update_data.end_datetime, exclude_booking_id=booking_id
    )
    if clash:
        raise HTTPException(status_code=409, detail=f"Cannot reschedule: Clashes with {clash.event_details}")

    for key, value in update_data.model_dump().items():
        setattr(booking, key, value)
        
    db.commit()
    db.refresh(booking)

    try:
        append_booking_to_excel(booking)
    except Exception as e:
        print(f"[EXCEL WARN] Could not sync to excel on serverless disk: {e}")

    return booking


@router.delete("/bookings/{booking_id}")
def cancel_booking(
    booking_id: int,
    admin: Admin = Depends(get_current_admin), 
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # 1. Update database status
    booking.status = "CANCELLED"
    db.commit()
    db.refresh(booking)

    # 2. Attempt Excel sync safely
    try:
        append_booking_to_excel(booking)
    except Exception as e:
        print(f"[EXCEL WARN] Could not write to Excel: {e}")

    # 3. Send email synchronously before Lambda/Vercel shuts down
    if booking.email:
        try:
            send_cancellation_email(
                to_email=booking.email,
                faculty_name=booking.faculty_name,
                venue=booking.venue,
                event_details=booking.event_details,
                start_time=booking.start_datetime.strftime("%d-%b-%Y, %I:%M %p"),
                end_time=booking.end_datetime.strftime("%d-%b-%Y, %I:%M %p")
            )
        except Exception as e:
            print(f"[EMAIL ERROR] Failed during cancellation dispatch: {e}")

    return {"message": "Booking successfully cancelled and notification email sent"}
