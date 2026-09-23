"""Generate fictional catalog metadata and events without reading any files."""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import numpy as np

UTC = timezone.utc
CUTOFF = datetime(2025, 2, 1, tzinfo=UTC)
WEIGHTS = {"view": 1.0, "cart": 2.0, "purchase": 3.0}


@dataclass(frozen=True)
class Product:
    product_id: str
    category: str
    brand: str


@dataclass(frozen=True)
class Event:
    user_id: str
    product_id: str
    event_type: str
    timestamp: datetime


def make_synthetic_data(seed=42):
    """72 products, 60 active + 10 sparse + 10 new users; no real records.

    The entire fictional catalog is available before the cutoff. Eight products
    have metadata but no training interactions, to illustrate item cold start.
    Category preference is deliberately simple, not calibrated to real data.
    """
    rng = np.random.default_rng(seed)
    categories = ["audio", "computing", "camera", "home"]
    catalog = [Product(f"demo_item_{c * 18 + j:03d}", category,
                       f"fictional_brand_{j % 3}")
               for c, category in enumerate(categories) for j in range(18)]
    events = []
    for u in range(80):
        user = f"demo_user_{u:03d}"
        preferred = u % 4
        train_count = int(rng.integers(18, 28)) if u < 60 else (2 if u < 70 else 0)
        for phase, count in [("train", train_count), ("test", 8)]:
            for j in range(count):
                category = preferred if rng.random() < 0.8 else int(rng.integers(4))
                item = category * 18 + int(rng.integers(16 if phase == "train" else 18))
                kind = str(rng.choice(list(WEIGHTS), p=[0.60, 0.25, 0.15]))
                start = datetime(2025, 1, 1, tzinfo=UTC) if phase == "train" else CUTOFF
                time = start + timedelta(days=j + 1, seconds=u)
                events.append(Event(user, catalog[item].product_id, kind, time))
    return catalog, sorted(events, key=lambda e: (e.timestamp, e.user_id))


def temporal_split(events, cutoff=CUTOFF):
    """One global boundary: train < cutoff; holdout >= cutoff. Remove exact duplicates."""
    if cutoff.tzinfo is None or any(e.timestamp.tzinfo is None for e in events):
        raise ValueError("Use timezone-aware timestamps and cutoff.")
    ordered = sorted(set(events), key=lambda e: (e.timestamp, e.user_id, e.product_id))
    return ([e for e in ordered if e.timestamp < cutoff],
            [e for e in ordered if e.timestamp >= cutoff])
