from kafka import KafkaConsumer
import json
from app.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from app.db import SessionLocal
from app.models import Booking

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="booking-group"
)

def start_consumer():
    print("Booking service started...")

    for message in consumer:
        event = message.value
        data = event["data"]

        print("Received event:", data)

        db = SessionLocal()

        booking = Booking(
            booking_id=data["booking_id"],
            patient_id=data["patient_id"],
            doctor_id=data["doctor_id"],
            symptoms=data["symptoms"],
            preferred_time=data["preferred_time"]
        )

        db.add(booking)
        db.commit()
        db.close()

        print("Saved booking:", data["booking_id"])