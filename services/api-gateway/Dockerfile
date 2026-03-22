FROM python:3.11-slim

WORKDIR /app

COPY services/api-gateway/app ./app
COPY services/api-gateway/requirements.txt .
COPY libs ./libs

RUN pip install -r requirements.txt

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]