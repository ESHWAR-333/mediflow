from libs.kafka_client import KafkaEventProducer, Event

producer = KafkaEventProducer()

event = Event.create(
    event_type="test.event",
    source="test-script",
    data={"message": "hello from mediflow"}
)

producer.send_event(
    topic="test-topic",
    event=event,
    key="test-key"
)

print("Event sent successfully!")