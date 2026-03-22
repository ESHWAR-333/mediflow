from libs.kafka_client import KafkaEventProducer, Event

producer = KafkaEventProducer()

def publish_triage_event(data: dict):
    event = Event.create(
        event_type="triage.scored",
        source="triage-engine",
        data=data
    )

    producer.send_event(
        topic="triage.scored",
        event=event,
        key=data["booking_id"]
    )