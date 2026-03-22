from pydantic import BaseModel

class AppointmentRequest(BaseModel):
    patient_id: str
    doctor_id: str
    symptoms: str
    preferred_time: str