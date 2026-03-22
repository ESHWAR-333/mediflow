FROM python:3.11-slim

WORKDIR /app

COPY services/analytics_service/app ./app
COPY services/analytics_service/requirements.txt .
COPY libs ./libs

RUN pip install -r requirements.txt

CMD ["python", "-u", "-m", "app.main"]