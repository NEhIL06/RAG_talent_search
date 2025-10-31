
import numpy as np

def precision_at_k(relevance_list, k):
    return sum(relevance_list[:k]) / float(k)

def recall_at_k(relevance_list, k, total_relevant):
    if total_relevant == 0:
        return 0.0
    return sum(relevance_list[:k]) / float(total_relevant)

def mean_reciprocal_rank(ranks):
    rr = [1.0/r if r>0 else 0.0 for r in ranks]
    return float(np.mean(rr)) if len(rr)>0 else 0.0

# Example evaluate harness (requires labeled testset)
def evaluate_system(system_retrieve_fn, testset):
    # testset: list of {'query': str, 'relevant_ids': [ids...]}
    recalls = []
    precisions = []
    mrrs = []
    for q in testset:
        retrieved = system_retrieve_fn(q['query'], k=10)  # should return ranked ids
        retrieved_ids = [r['id'] for r in retrieved]
        relevance_list = [1 if rid in q['relevant_ids'] else 0 for rid in retrieved_ids]
        total_relevant = len(q['relevant_ids'])
        recalls.append(recall_at_k(relevance_list, 5, total_relevant))
        precisions.append(precision_at_k(relevance_list, 5))
        # rank of first relevant
        try:
            first_rel = relevance_list.index(1) + 1
        except ValueError:
            first_rel = 0
        mrrs.append(1.0/first_rel if first_rel>0 else 0.0)
    return {'Recall@5': float(np.mean(recalls)), 'Precision@5': float(np.mean(precisions)), 'MRR': float(np.mean(mrrs))}
