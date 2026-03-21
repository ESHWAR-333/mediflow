from kafka import KafkaProducer
import json
from .config import KAFKA_BOOTSTRAP_SERVERS
from .schemas import Event

class KafkaEventProducer:

    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8') #converts dict to json to bytes 
        )

    def send_event(self, topic: str, event: Event, key: str = None):
        self.producer.send(
            topic=topic,
            key=key.encode('utf-8') if key else None, #used for partitioning (booking_id)
            value=event.model_dump(mode="json")
        )
        self.producer.flush()