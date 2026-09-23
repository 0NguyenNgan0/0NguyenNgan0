"""Dense implicit ALS + TF-IDF; intentionally sized for an educational demo."""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from .data import WEIGHTS

METHODS = ("popularity", "als", "content", "hybrid")


def implicit_als(interactions, factors=12, iterations=15, alpha=10.0,
                 regularization=0.1, seed=42):
    """Minimize sum c_ui(p_ui - x_u@y_i)^2 + lambda*(||X||² + ||Y||²).

    p = 1[r > 0], c = 1 + alpha*r. Each half-step is a ridge solve.
    Dense matrices are suitable only for this small synthetic example.
    """
    r = np.asarray(interactions, dtype=float)
    if r.ndim != 2 or min(r.shape) == 0 or not np.isfinite(r).all() or (r < 0).any():
        raise ValueError("Interactions must be a nonempty, finite, nonnegative matrix.")
    if (factors < 1 or iterations < 1 or not np.isfinite(alpha) or alpha < 0
            or not np.isfinite(regularization) or regularization <= 0):
        raise ValueError("Invalid ALS parameters.")
    rng = np.random.default_rng(seed)
    x = rng.normal(0, 0.01, (r.shape[0], factors))
    y = rng.normal(0, 0.01, (r.shape[1], factors))
    confidence = 1 + alpha * r
    preference = (r > 0).astype(float)
    ridge = regularization * np.eye(factors)
    losses = []
    for _ in range(iterations):
        for u in range(len(x)):
            c = confidence[u]
            x[u] = np.linalg.solve(y.T @ (c[:, None] * y) + ridge,
                                   y.T @ (c * preference[u]))
        for i in range(len(y)):
            c = confidence[:, i]
            y[i] = np.linalg.solve(x.T @ (c[:, None] * x) + ridge,
                                   x.T @ (c * preference[:, i]))
        losses.append(float(np.sum(confidence * (preference - x @ y.T) ** 2)
                            + regularization * (np.sum(x * x) + np.sum(y * y))))
    return x, y, losses


def _scale(values):
    """Min-max calibration on the eligible candidates, including negative ALS scores."""
    span = np.ptp(values)
    return (values - values.min()) / span if span > 1e-12 else np.zeros_like(values)


class HybridRecommender:
    def __init__(self, seed=42, als_weight=0.6, sparse_threshold=3):
        if not 0 <= als_weight <= 1 or sparse_threshold < 1:
            raise ValueError("Invalid hybrid weight or history threshold.")
        self.seed = seed
        self.als_weight = als_weight
        self.sparse_threshold = sparse_threshold

    def fit(self, catalog, train_events):
        self.catalog = sorted(catalog, key=lambda p: p.product_id)
        self.item_ids = [p.product_id for p in self.catalog]
        if not self.catalog or len(set(self.item_ids)) != len(self.item_ids):
            raise ValueError("Catalog must be nonempty with unique product IDs.")
        self.item_index = {pid: i for i, pid in enumerate(self.item_ids)}
        events = list(set(train_events))
        if not events:
            raise ValueError("At least one training event is required.")
        if any(e.product_id not in self.item_index or e.event_type not in WEIGHTS
               or not e.user_id or e.timestamp.tzinfo is None for e in events):
            raise ValueError("Invalid training event, catalog reference, or timestamp.")
        self.train_end = max(e.timestamp for e in events)
        self.user_index = {u: i for i, u in enumerate(sorted({e.user_id for e in events}))}
        self.interactions = np.zeros((len(self.user_index), len(self.item_ids)))
        for event in events:
            self.interactions[self.user_index[event.user_id], self.item_index[event.product_id]] += WEIGHTS[event.event_type]
        self.popularity = self.interactions.sum(axis=0)
        self.user_factors, self.item_factors, self.losses = implicit_als(
            self.interactions, seed=self.seed)
        # Metadata is available for every catalog item at recommendation time.
        documents = [f"category_{p.category or 'unknown'} brand_{p.brand or 'unknown'}"
                     for p in self.catalog]
        self.vectorizer = TfidfVectorizer()
        self.features = self.vectorizer.fit_transform(documents).toarray()
        profiles = self.interactions @ self.features
        norms = np.linalg.norm(profiles, axis=1, keepdims=True)
        self.profiles = profiles / np.maximum(norms, 1e-12)
        return self

    def seen(self, user_id):
        u = self.user_index.get(user_id)
        return set() if u is None else {
            self.item_ids[i] for i in np.flatnonzero(self.interactions[u])}

    def route(self, user_id):
        count = len(self.seen(user_id))
        return "popularity" if count == 0 else ("content" if count < self.sparse_threshold else "hybrid")

    def recommend(self, user_id, k=10, method="hybrid"):
        if method not in METHODS or not isinstance(k, int) or isinstance(k, bool) or k < 1:
            raise ValueError("Use a supported method and a positive integer k.")
        seen = self.seen(user_id)
        eligible = np.array([i for i, pid in enumerate(self.item_ids) if pid not in seen], dtype=int)
        if len(eligible) == 0:
            return []
        # Baselines stay independent of the sparse-user switch. All methods use
        # popularity for an unknown user because no profile/factor is available.
        selected = self.route(user_id) if method == "hybrid" else method
        u = self.user_index.get(user_id)
        if u is None or selected == "popularity":
            scores = self.popularity[eligible]
        elif selected == "als":
            scores = self.item_factors[eligible] @ self.user_factors[u]
        elif selected == "content":
            scores = self.features[eligible] @ self.profiles[u]
        else:
            als = self.item_factors[eligible] @ self.user_factors[u]
            content = self.features[eligible] @ self.profiles[u]
            scores = self.als_weight * _scale(als) + (1 - self.als_weight) * _scale(content)
        # Fixed item-ID ordering resolves ties reproducibly; return fewer than k
        # only when fewer eligible items exist.
        order = np.argsort(-scores, kind="stable")[:k]
        return [self.item_ids[eligible[i]] for i in order]
