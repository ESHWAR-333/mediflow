from minio import Minio
from minio.error import S3Error
from io import BytesIO
from app.config import (
    MINIO_ENDPOINT, MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY, MINIO_BUCKET, MINIO_SECURE
)

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE
)


def ensure_bucket():
    if not client.bucket_exists(MINIO_BUCKET):
        client.make_bucket(MINIO_BUCKET)
        print(f"Created bucket: {MINIO_BUCKET}")


def upload_pdf(booking_id: str, pdf_bytes: bytes) -> str:
    ensure_bucket()

    object_name = f"confirmations/{booking_id}.pdf"

    client.put_object(
        bucket_name=MINIO_BUCKET,
        object_name=object_name,
        data=BytesIO(pdf_bytes),
        length=len(pdf_bytes),
        content_type="application/pdf"
    )

    url = client.presigned_get_object(
        bucket_name=MINIO_BUCKET,
        object_name=object_name,
    )

    print(f"Uploaded PDF: {object_name}")
    return url