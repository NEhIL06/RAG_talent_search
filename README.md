# 🧠 TalentMatch AI — Hybrid RAG-Powered Talent Intelligence Engine

**TalentMatch AI** is an intelligent job–candidate matching engine powered by a **Hybrid Retrieval-Augmented Generation (RAG)** architecture.  
It combines **semantic vector search (ChromaDB)** and **keyword BM25 retrieval (Elasticsearch)** to deliver highly accurate, explainable, and production-ready AI-driven matching between resumes and job descriptions.

---

## 🚀 Overview

### 🎯 The Problem
Traditional resume search engines rely heavily on keyword matching, missing out on semantically similar skills (e.g., *"deep learning"* vs *"neural networks"*).  
This results in irrelevant matches and inefficient hiring.

### 💡 The Solution
TalentMatch AI bridges that gap using **Hybrid Retrieval**:
- **Dense embeddings (SentenceTransformer)** → understand meaning and context  
- **Sparse retrieval (Elasticsearch BM25)** → capture exact keyword overlap  
- **Score fusion** → combine both strengths for higher accuracy  
- **CrossEncoder re-ranker** → fine-grained candidate ranking  
- **FastAPI backend** → production-ready REST API for AI-powered search

---

## 🧩 Architecture

```
       ┌────────────────────────────┐
       │     Raw Data (Resumes)     │
       └─────────────┬──────────────┘
                     │
                     ▼
     ┌─────────────────────────────────┐
     │     Ingestion / Indexing        │
     │ - Embed resumes with            │
     │   SentenceTransformer           │
     │ - Store vectors in ChromaDB     │
     │   (persistent)                  │
     │ - Index raw text into           │
     │   Elasticsearch                 │
     └─────────────────────────────────┘
                     │
                     ▼
      ┌───────────────────────────┐
      │        Query Flow         │
      │ - User inputs job query   │
      │ - HybridRetriever fetches │
      │   from Chroma + ES        │
      │ - Scores combined (α)     │
      └─────────────┬─────────────┘
                    ▼
    ┌───────────────────────────────────┐
    │  CrossEncoder Re-Ranker           │
    │  Fine-grained reranking of top-K  │
    │  candidates                       │
    └───────────────────────────────────┘
                    │
                    ▼
       ┌──────────────────────────┐
       │  FastAPI Backend          │
       │  `/ingest` → Build indexes│
       │  `/query`  → Hybrid search│
       └──────────────────────────┘
```

---

## ⚙️ Tech Stack

| Layer | Tool / Library | Purpose |
|-------|----------------|----------|
| **Backend** | FastAPI | REST API service |
| **Embeddings** | SentenceTransformer (`all-mpnet-base-v2`) | Semantic representation |
| **Vector Store** | ChromaDB | Dense vector persistence |
| **Keyword Search** | Elasticsearch (BM25) | Sparse retrieval |
| **Reranking** | CrossEncoder (`MiniLM-L-6-v2`) | Fine-grained relevance scoring |
| **Infra** | Docker, Docker Compose | Local orchestration |
| **Metrics** | Recall@K, Precision@K, MRR | Retrieval evaluation |
| **LLM (Planned)** | Google Gemini | Explanations for match reasoning |

---

## 📁 Project Structure

```
talentmatch_ai_repo/
│
├── data/
│   ├── resumes.json              # Sample resumes
│   └── jobs.json                 # Sample job descriptions
│
├── src/
│   ├── ingest.py                 # Embedding + Chroma ingestion
│   ├── index_bm25.py             # Elasticsearch indexing
│   ├── retriever.py              # HybridRetriever (ES + Chroma)
│   ├── rerank.py                 # CrossEncoder re-ranker
│   ├── eval.py                   # Evaluation metrics (Recall@K etc.)
│   └── query.py                  # Hybrid query runner
│
├── app/
│   └── main.py                   # FastAPI app
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🧱 Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/talentmatch-ai.git
cd talentmatch-ai
```

### 2️⃣ Build and run containers

```bash
docker compose build --no-cache
docker compose up -d
```

This launches:
- **Elasticsearch** → http://localhost:9200
- **FastAPI** → http://localhost:8080

### 3️⃣ Ingest data

```bash
docker exec -it <web_container_id> bash
python src/index_bm25.py     # Create BM25 index
python src/ingest.py         # Create Chroma embeddings
```

### 4️⃣ Run queries

```bash
python src/query.py
```

Or use the FastAPI endpoint:

```bash
curl -X POST "http://localhost:8080/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "Looking for an AI Engineer with TensorFlow and API experience"}'
```

### 5️⃣ Evaluate retrieval accuracy

```bash
python src/eval.py
```

**Metrics:**
- Recall@K
- Precision@K
- Mean Reciprocal Rank (MRR)

---

## 📊 Results & Observations

- Dense-only baseline achieved limited accuracy for skill-based queries.
- Hybrid fusion (α=0.6) improved **Recall@5 by ~18%** and **Precision@5 by ~22%**.
- Future addition of Gemini explanations will make match decisions transparent and human-readable.

---

## 🧩 Future Enhancements

- [ ] `/eval` endpoint for real-time evaluation
- [ ] Integration with Gemini API for natural-language rationale
- [ ] Frontend dashboard (Streamlit or React)
- [ ] Resume/job ingestion from real datasets
- [ ] Custom Elasticsearch analyzers for synonyms

---

## 👨‍💻 Author

**Nehil Chandrakar**  
Full-Stack & AI Engineer | Focused on Agentic AI, Generative Search, and Scalable ML Systems

📍 Bangalore, India  
📧 your.email@example.com  
🌐 [GitHub](https://github.com/your-username) • [LinkedIn](https://linkedin.com/in/your-profile)

---

## 🏁 License

MIT License © 2025 Nehil Chandrakar