# backend/Dockerfile
FROM python:3.9

WORKDIR /app

COPY /backend/requirements.txt .
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY /backend/app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]