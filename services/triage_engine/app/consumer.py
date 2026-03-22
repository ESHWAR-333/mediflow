from kafka import KafkaConsumer
import json
from app.config import KAFKA_BOOTSTRAP_SERVERS, INPUT_TOPIC
from app.scoring import calculate_urgency
from app.producer import publish_triage_event

consumer = KafkaConsumer(
    INPUT_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="triage-group"
)

def start_consumer():
    print("Triage Engine started...")

    for message in consumer:
        event = message.value
        data = event["data"]

        urgency = calculate_urgency(data["symptoms"])

        data["urgency_score"] = urgency

        print(f"🧠 Scored {urgency} for booking {data['booking_id']}")

        publish_triage_event(data)