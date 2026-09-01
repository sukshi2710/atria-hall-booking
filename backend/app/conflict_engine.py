from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.models import Booking

def check_hall_clash(
    db: Session, 
    venue: str, 
    start_time: datetime, 
    end_time: datetime, 
    exclude_booking_id: Optional[int] = None
) -> Optional[Booking]:
    """
    Returns an existing confirmed Booking if a clash is detected; otherwise None.
    """
    query = db.query(Booking).filter(
        Booking.venue == venue,
        Booking.status == "CONFIRMED",
        Booking.start_datetime < end_time,
        Booking.end_datetime > start_time
    )
    if exclude_booking_id:
        query = query.filter(Booking.id != exclude_booking_id)
        
    return query.first()