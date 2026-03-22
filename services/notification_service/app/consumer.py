from kafka import KafkaConsumer
import json
from app.config import KAFKA_BOOTSTRAP_SERVERS, TOPIC
from app.pdf_generator import generate_booking_pdf
from app.minio_client import upload_pdf

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="notification-group"
)


def start_consumer():
    print("Notification Service started...")

    for message in consumer:
        event = message.value
        data = event["data"]
        booking_id = data.get("booking_id", "unknown")
        patient_id = data.get("patient_id", "unknown")

        print(f"Received slot.updated for booking: {booking_id}")

        try:
            pdf_bytes = generate_booking_pdf(data)
            print(f"Generated PDF for booking: {booking_id} ({len(pdf_bytes)} bytes)")

            download_url = upload_pdf(booking_id, pdf_bytes)
            print(f"Confirmation ready for patient {patient_id}")
            print(f"Download URL: {download_url}")

            send_notification(data, download_url)  # only send if PDF succeeded

        except Exception as e:
            print(f"Failed to process booking {booking_id}: {e}")


def send_notification(data: dict, download_url: str):
    print("📩 Sending notification...")
    print(f"  Patient  : {data['patient_id']}")
    print(f"  Doctor   : {data['doctor_id']}")
    print(f"  Time     : {data['preferred_time']}")
    print(f"  Urgency  : {data.get('urgency_score', 'N/A')}")
    print(f"  PDF      : {download_url}")