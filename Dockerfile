# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
RUN pip install --no-cache-dir --prefer-binary --progress-bar off -r requirements.txt

COPY ./src ./src
COPY ./app ./app
COPY ./data ./data

EXPOSE 8080

# This command runs automatically on Render startup
CMD ["bash", "-c", "python src/index_bm25.py && python src/ingest.py && uvicorn app.main:app --host 0.0.0.0 --port 8080"]
