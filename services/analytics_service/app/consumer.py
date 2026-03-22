from kafka import KafkaConsumer
import json
from datetime import datetime
from sqlalchemy import text
from app.config import KAFKA_BOOTSTRAP_SERVERS, TOPICS
from app.db import SessionLocal

consumer = KafkaConsumer(
    *TOPICS,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="analytics-group"
)


def start_consumer():
    print(f"Analytics service started. Listening to: {TOPICS}")

    for message in consumer:
        event = message.value
        topic = message.topic

        try:
            data = event.get("data", {})

            time = event.get("timestamp", datetime.utcnow().isoformat())
            event_id = event.get("event_id", "unknown")
            event_type = event.get("event_type", topic)
            source = event.get("source", "unknown")

            booking_id = data.get("booking_id")
            patient_id = data.get("patient_id")
            doctor_id = data.get("doctor_id")
            urgency_score = data.get("urgency_score")

            db = SessionLocal()

            db.execute(text("""
                INSERT INTO analytics_events (
                    time, event_id, event_type, source,
                    booking_id, patient_id, doctor_id,
                    urgency_score, payload
                ) VALUES (
                    :time, :event_id, :event_type, :source,
                    :booking_id, :patient_id, :doctor_id,
                    :urgency_score, :payload
                )
            """), {
                "time": time,
                "event_id": event_id,
                "event_type": event_type,
                "source": source,
                "booking_id": booking_id,
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "urgency_score": urgency_score,
                "payload": json.dumps(data)
            })

            db.commit()
            db.close()

            print(f"Stored [{event_type}] booking={booking_id} urgency={urgency_score}")

        except Exception as e:
            print(f"Failed to store analytics event: {e}")