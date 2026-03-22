FROM python:3.11-slim

WORKDIR /app

COPY services/notification_service/app ./app
COPY services/notification_service/requirements.txt .
COPY libs ./libs

RUN pip install -r requirements.txt

CMD ["python", "-u",  "-m", "app.main"]