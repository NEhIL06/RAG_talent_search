from elasticsearch import Elasticsearch
import json, os

ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
INDEX_NAME = "resumes"

def create_index():
    es = Elasticsearch(ES_HOST)
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
