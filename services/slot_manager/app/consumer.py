from kafka import KafkaConsumer
import json
from app.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from app.redis_lock import acquire_lock
from app.producer import publish_slot_event

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    group_id="slot-manager-group"
)

def start_consumer():
    
    print("Slot Manager started...")

    for message in consumer:
        event = message.value
        data = event["data"]

        print("EVENT RECEIVED:", data)

        slot_key = f"{data['doctor_id']}:{data['preferred_time']}"

        if acquire_lock(slot_key):
            print(f"✅ Slot locked: {slot_key}")
            publish_slot_event(data)  # 🔥 NEW LINE
        else:
            print(f"❌ Slot already booked: {slot_key}")