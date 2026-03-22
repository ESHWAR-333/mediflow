import os
 
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
 
INPUT_TOPIC = "booking.created"
OUTPUT_TOPIC = "triage.scored"