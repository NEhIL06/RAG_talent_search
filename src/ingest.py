
import json
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# Simple ingest script that persists to ChromaDB (duckdb+parquet)
def main():
    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_store"))
    # Use SentenceTransformer model for embeddings (you can change model name)
    model_name = "all-mpnet-base-v2"
    embed_model = SentenceTransformer(model_name)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model=embed_model)

    collection = client.get_or_create_collection(name="resumes", embedding_function=ef)

    with open("data/resumes.json") as f:
        resumes = json.load(f)

    docs = []
    metadatas = []
    ids = []
    for i, r in enumerate(resumes):
        content = f"{r['name']} | Skills: {r['skills']} | Summary: {r.get('summary','')}"
        docs.append(content)
        metadatas.append({"name": r['name'], "experience": r.get('experience',''), "skills": r['skills']})
        ids.append(f"res_{i}")

    # Add to chroma collection
    collection.add(documents=docs, metadatas=metadatas, ids=ids)
    client.persist()
    print("Ingest complete. Persisted to ./chroma_store")


if __name__ == '__main__':
    main()
