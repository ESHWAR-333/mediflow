from kafka import KafkaConsumer
import json
from app.config import KAFKA_BOOTSTRAP_SERVERS, TOPIC

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="notification-group"
)

def start_consumer():
    print("Notification Service started...")

    for message in consumer:
        event = message.value
        data = event["data"]

        send_notification(data)

def send_notification(data):
    print("📩 Sending notification...")
    print(f"Booking Confirmed for {data['patient_id']}")
    print(f"Doctor: {data['doctor_id']}")
    print(f"Time: {data['preferred_time']}")