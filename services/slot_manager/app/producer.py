from libs.kafka_client import KafkaEventProducer, Event

producer = KafkaEventProducer()

def publish_slot_event(data: dict):
    event = Event.create(
        event_type="slot.updated",
        source="slot-manager",
        data=data
    )

    producer.send_event(
        topic="slot.updated",
        event=event,
        key=data["booking_id"]
    )