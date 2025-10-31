
# Simple query runner that ties retriever + reranker + (optional) LLM explanation
from src.retriever import HybridRetriever
from src.rerank import ReRanker
try:
    # Placeholder for Gemini/Google Generative AI SDK usage
    import google.generativeai as genai
except Exception:
    genai = None

def run_query(query_text, top_k=5):
    retriever = HybridRetriever()
    candidates = retriever.hybrid_retrieve(query_text, k=50)
    texts = [c['text'] for c in candidates]
    metas = [c['metadata'] for c in candidates]
    reranker = ReRanker()
    ranked = reranker.rerank(query_text, texts, candidates_meta=metas)[:top_k]

    # Optional: call Gemini/other LLM for explanations (placeholder)
    explanations = None
    if genai is not None:
        try:
            prompt = f"Provide a short JSON array of candidate_id and short rationale for each candidate given query: {query_text}\nCandidates:\n" + "\n".join([r['text'] for r in ranked])
            # NOTE: Replace with correct Gemini API usage; this is a placeholder
            resp = genai.generate_text(prompt)
            explanations = resp
        except Exception as e:
            explanations = str(e)

    return {'ranked': ranked, 'explanations': explanations}


if __name__ == '__main__':
    print(run_query('Looking for Python ML engineer with TensorFlow and API experience'))
