from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(String, primary_key=True)
    patient_id = Column(String)
    doctor_id = Column(String)
    symptoms = Column(String)
    preferred_time = Column(String)