
from sentence_transformers import CrossEncoder


# Cross-encoder re-ranker wrapper
class ReRanker:
    def __init__(self, model_name='cross-encoder/ms-marco-MiniLM-L-6-v2'):
        self.model = CrossEncoder(model_name)

    def rerank(self, query, candidate_texts, candidates_meta=None):
        # candidate_texts: list of strings
        pairs = [[query, t] for t in candidate_texts]
        scores = self.model.predict(pairs)
        ranked = sorted(zip(candidate_texts, scores), key=lambda x: x[1], reverse=True)
        return [{'text': t, 'score': s, 'meta': (candidates_meta[i] if candidates_meta else {})} for i,(t,s) in enumerate(ranked)]
