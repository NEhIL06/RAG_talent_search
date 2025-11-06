from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from elasticsearch import Elasticsearch
import numpy as np, os

class HybridRetriever:
    def __init__(self, chroma_dir='./chroma_store', es_index='resumes', alpha=0.6):
        es_host = os.getenv("ES_HOST", "http://localhost:9200")
        es_username = os.getenv("ES_USERNAME")
        es_password = os.getenv("ES_PASSWORD")
        if es_username and es_password:
            self.es = Elasticsearch(es_host, basic_auth=(es_username, es_password))
        else:
            self.es = Elasticsearch(es_host)
        self.es_index = es_index
        self.alpha = float(os.getenv("ALPHA", alpha))
        chroma_dir = os.getenv("CHROMA_DIR", chroma_dir)
        self.client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=chroma_dir))
        self.embed_model = SentenceTransformer("all-mpnet-base-v2")
        self.collection = self.client.get_collection("resumes")

    def bm25_search(self, query, k=20):
        res = self.es.search(index=self.es_index, size=k, query={"multi_match": {"query": query, "fields": ["skills", "summary", "experience"]}})
        hits = []
        for hit in res["hits"]["hits"]:
            src = hit["_source"]
            hits.append({
                "id": hit["_id"],
                "text": f"{src['name']} | {src['skills']} | {src['summary']}",
                "metadata": src,
                "bm25_score": hit["_score"]
            })
        return hits

    def dense_search(self, query, k=20):
        results = self.collection.query(query_texts=[query], n_results=k)
        hits = []
        for i, _id in enumerate(results["ids"][0]):
            hits.append({
                "id": _id,
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "dense_score": results["distances"][0][i]
            })
        return hits

    def hybrid_retrieve(self, query, k=10):
        bm25_hits = self.bm25_search(query, k=50)
        dense_hits = self.dense_search(query, k=50)

        # Normalize BM25 & dense scores
        if bm25_hits:
            bm25_scores = np.array([h["bm25_score"] for h in bm25_hits])
            bm25_scores = (bm25_scores - bm25_scores.min()) / (bm25_scores.ptp() + 1e-9)
            for i, h in enumerate(bm25_hits):
                h["norm_score"] = bm25_scores[i]

        if dense_hits:
            dense_scores = np.array([h["dense_score"] for h in dense_hits])
            dense_scores = 1 / (1 + dense_scores)
            dense_scores = (dense_scores - dense_scores.min()) / (dense_scores.ptp() + 1e-9)
            for i, h in enumerate(dense_hits):
                h["norm_score"] = dense_scores[i]

        # Combine by id
        combined = {}
        for h in bm25_hits:
            combined[h["id"]] = h
        for h in dense_hits:
            if h["id"] in combined:
                combined[h["id"]]["norm_score"] = self.alpha * h["norm_score"] + (1 - self.alpha) * combined[h["id"]].get("norm_score", 0)
            else:
                combined[h["id"]] = h

        results = sorted(combined.values(), key=lambda x: x.get("norm_score", 0), reverse=True)
        return results[:k]
