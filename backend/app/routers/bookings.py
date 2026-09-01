from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Booking
from app.schemas import BookingCreate, BookingOut
from app.conflict_engine import check_hall_clash
from app.excel_service import append_booking_to_excel
from app.email_service import send_success_email, send_clash_email

router = APIRouter(prefix="/api/v1/bookings", tags=["Bookings"])

@router.post("", response_model=BookingOut)
def create_booking(
    booking_in: BookingCreate, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    # 1. Run Conflict Detection Engine
    clash = check_hall_clash(
        db=db,
        venue=booking_in.venue,
        start_time=booking_in.start_datetime,
        end_time=booking_in.end_datetime
    )

    # 2. Case: Failure / Slot Clash
    if clash:
        # Dispatch clash email directly
        send_clash_email(
            faculty_name=booking_in.faculty_name,
            recipient_email=booking_in.email,
            venue=booking_in.venue,
            start_dt=booking_in.start_datetime,
            end_dt=booking_in.end_datetime,
            clashing_event=clash
        )
        
        # Return 409 error to the UI
        raise HTTPException(
            status_code=409, 
            detail=f"Slot clash detected: '{clash.event_details}' ({clash.start_datetime.strftime('%I:%M %p')} - {clash.end_datetime.strftime('%I:%M %p')}). A clash notification has been emailed to you."
        )

    # 3. Case: Success
    new_booking = Booking(**booking_in.model_dump(), status="CONFIRMED")
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    # Queue confirmation email and Excel writing
    background_tasks.add_task(send_success_email, new_booking)
    background_tasks.add_task(append_booking_to_excel, new_booking)

    return new_booking