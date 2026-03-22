FROM python:3.11-slim

WORKDIR /app

COPY services/slot_manager/app ./app
COPY services/slot_manager/requirements.txt .
COPY libs ./libs

RUN pip install -r requirements.txt

CMD ["python", "-u", "-m", "app.main"]