from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional
from typing import Literal

class BookingCreate(BaseModel):
    faculty_name: str
    email: EmailStr
    venue: Literal["Seminar Hall", "Placement Hall"]  # Ensure exact name match
    department: str
    event_details: str
    start_datetime: datetime
    end_datetime: datetime
    
    
    @field_validator("venue")
    def validate_venue(cls, v):
        allowed = ["Seminar Hall", "Placement Hall"]
        if v not in allowed:
            raise ValueError(f"Venue must be one of {allowed}")
        return v

    @field_validator("end_datetime")
    def validate_timestamps(cls, v, values):
        if "start_datetime" in values.data and v <= values.data["start_datetime"]:
            raise ValueError("End datetime must be strictly after start datetime")
        return v

class BookingOut(BaseModel):
    id: int
    booking_reference: str
    faculty_name: str
    email: str
    venue: str
    department: str
    event_details: str
    start_datetime: datetime
    end_datetime: datetime
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class AdminLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str