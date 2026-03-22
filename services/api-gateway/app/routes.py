from fastapi import APIRouter
from app.models import AppointmentRequest
from app.producer import publish_booking_event
import uuid

router = APIRouter()

@router.post("/appointments")
def create_appointment(request: AppointmentRequest):

    booking_id = str(uuid.uuid4())

    event_data = {
        "booking_id": booking_id,
        "patient_id": request.patient_id,
        "doctor_id": request.doctor_id,
        "symptoms": request.symptoms,
        "preferred_time": request.preferred_time
    }

    publish_booking_event(event_data)

    return {
        "booking_id": booking_id,
        "status": "CREATED",
        "message": "Appointment created successfully"
    }