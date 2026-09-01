import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "super-secret-jwt-token-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    DATABASE_URL: str = "sqlite:////tmp/hall_booking.db" if os.getenv("VERCEL") else "sqlite:///./hall_booking.db"
    
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 465
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SENDER_NAME: str = "Campus Hall Booking"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
