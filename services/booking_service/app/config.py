import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
KAFKA_TOPIC = "booking.created"

DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://mediflow:mediflow123456@localhost:5432/mediflow"
)