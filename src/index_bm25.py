from elasticsearch import Elasticsearch
from elasticsearch import AuthenticationException
import json, os

ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
ES_USERNAME = os.getenv("ES_USERNAME")
ES_PASSWORD = os.getenv("ES_PASSWORD")
ES_API_KEY = os.getenv("ES_API_KEY")  # Optional: base64 "id:api_key" or tuple
INDEX_NAME = "resumes"

def _make_client():
    if ES_API_KEY:
        api_key_value = ES_API_KEY.strip()
        if ":" in api_key_value and "\n" not in api_key_value and " " not in api_key_value:
            api_key_id, api_key_secret = api_key_value.split(":", 1)
            return Elasticsearch(ES_HOST, api_key=(api_key_id, api_key_secret))
        return Elasticsearch(ES_HOST, api_key=api_key_value)
    if ES_USERNAME and ES_PASSWORD:
        return Elasticsearch(ES_HOST, basic_auth=(ES_USERNAME, ES_PASSWORD))
    return Elasticsearch(ES_HOST)

def create_index():
    es = _make_client()
    try:
        # Validate auth early
        es.info()
    except AuthenticationException:
        raise RuntimeError("Elasticsearch auth failed. Set ES_USERNAME/ES_PASSWORD or ES_API_KEY env vars.")
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)

    es.indices.create(
        index=INDEX_NAME,
        body={
            "mappings": {
                "properties": {
                    "name": {"type": "text"},
                    "skills": {"type": "text"},
                    "summary": {"type": "text"},
                    "experience": {"type": "text"}
                }
            }
        }
    )
    print(f"✅ Created index: {INDEX_NAME}")
    return es

def index_data():
    es = create_index()
    with open("data/resumes.json") as f:
        resumes = json.load(f)
    for i, r in enumerate(resumes):
        es.index(
            index=INDEX_NAME,
            id=i,
            document={
                "name": r["name"],
                "skills": r["skills"],
                "summary": r.get("summary", ""),
                "experience": r.get("experience", "")
            }
        )
    es.indices.refresh(index=INDEX_NAME)
    print("✅ Indexed all resumes.")

if __name__ == "__main__":
    index_data()
