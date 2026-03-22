from libs.kafka_client import KafkaEventProducer, Event
from app.config import SERVICE_NAME

producer = KafkaEventProducer()

def publish_booking_event(data: dict):
    event = Event.create(
        event_type="booking.created",
        source=SERVICE_NAME,
        data=data
    )

    producer.send_event(
        topic="booking.created",
        event=event,
        key=data["booking_id"]
    )