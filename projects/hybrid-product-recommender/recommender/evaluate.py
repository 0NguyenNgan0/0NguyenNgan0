"""Comparable macro metrics on novel held-out interactions."""
from collections import defaultdict

import numpy as np

from .data import WEIGHTS
from .model import METHODS


def ranking_metrics(recommendations, relevant, k):
    """Fixed-k precision penalizes short lists; binary relevance, macro-ready."""
    if k < 1 or not relevant or len(recommendations) > k or len(set(recommendations)) != len(recommendations):
        raise ValueError("Expected unique top-k recommendations and nonempty relevance.")
    hits = np.array([float(pid in relevant) for pid in recommendations])
    dcg = float(np.sum(hits / np.log2(np.arange(len(hits)) + 2)))
    ideal = float(np.sum(1 / np.log2(np.arange(min(k, len(relevant))) + 2)))
    return {"precision_at_k": float(hits.sum() / k),
            "recall_at_k": float(hits.sum() / len(relevant)),
            "ndcg_at_k": dcg / ideal}


def evaluate(model, test_events, k=10):
    if not isinstance(k, int) or isinstance(k, bool) or k < 1:
        raise ValueError("k must be a positive integer.")
    truth = defaultdict(set)
    for event in test_events:
        if (event.timestamp.tzinfo is None or event.timestamp <= model.train_end
                or event.product_id not in model.item_index
                or event.event_type not in WEIGHTS or not event.user_id):
            raise ValueError("Holdout must follow training and contain valid catalog events.")
        truth[event.user_id].add(event.product_id)
    # This demo measures discovery of unseen products, not repeat consumption.
    novel = {u: products - model.seen(u) for u, products in truth.items()}
    relevant = {u: products for u, products in novel.items() if products}
    if not relevant:
        raise ValueError("No users with novel held-out interactions to evaluate.")
    cohorts = {u: ("new" if not model.seen(u) else
                   "sparse" if len(model.seen(u)) < model.sparse_threshold else "warm")
               for u in relevant}
    report = {"data": "synthetic_only", "k": k, "users_in_holdout": len(truth),
              "evaluated_users": len(relevant), "skipped_no_novel_items": len(truth) - len(relevant),
              "cohort_counts": {c: list(cohorts.values()).count(c) for c in ("warm", "sparse", "new")},
              "methods": {}}
    for method in METHODS:
        rows, recommended = {}, set()
        for user in sorted(relevant):
            recs = model.recommend(user, k, method)
            rows[user] = ranking_metrics(recs, relevant[user], k)
            recommended.update(recs)
        def mean_for(users):
            return {metric: float(np.mean([rows[u][metric] for u in users]))
                    for metric in ("precision_at_k", "recall_at_k", "ndcg_at_k")}
        report["methods"][method] = {
            **mean_for(rows), "catalog_coverage": len(recommended) / len(model.item_ids),
            "by_cohort": {c: mean_for([u for u in rows if cohorts[u] == c])
                          for c in ("warm", "sparse", "new") if c in cohorts.values()}}
    return report
