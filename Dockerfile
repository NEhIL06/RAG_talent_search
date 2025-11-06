# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY ./app ./app
COPY ./data ./data

EXPOSE 8080

# This command runs automatically on Render startup
CMD ["bash", "-c", "python src/index_bm25.py && python src/ingest.py && uvicorn app.main:app --host 0.0.0.0 --port 8080"]
