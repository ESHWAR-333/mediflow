FROM python:3.11-slim

WORKDIR /app

COPY services/triage_engine/app ./app
COPY services/triage_engine/requirements.txt .
COPY libs ./libs

RUN pip install -r requirements.txt

CMD ["python", "-u", "-m", "app.main"]