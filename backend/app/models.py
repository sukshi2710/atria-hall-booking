import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_reference = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()), index=True)
    faculty_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    venue = Column(String(50), nullable=False, index=True) # 'Seminar Hall' or 'Placement Hall'
    department = Column(String(50), nullable=False)
    event_details = Column(Text, nullable=False)
    start_datetime = Column(DateTime, nullable=False, index=True)
    end_datetime = Column(DateTime, nullable=False, index=True)
    status = Column(String(20), default="CONFIRMED") # 'CONFIRMED', 'CANCELLED', 'CLASH_REJECTED'
    sharepoint_item_id = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False)