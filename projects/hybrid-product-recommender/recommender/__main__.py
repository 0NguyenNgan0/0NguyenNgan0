"""Run with python -m recommender; writes only when --output is supplied."""
import argparse
import json
from pathlib import Path
import platform

import numpy as np
import sklearn

from .data import CUTOFF, make_synthetic_data, temporal_split
from .evaluate import evaluate
from .model import HybridRecommender


def unit_interval(value):
    """Reject invalid blend weights before generating data or fitting a model."""
    try:
        weight = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a finite number between 0 and 1")
    if not 0 <= weight <= 1:
        raise argparse.ArgumentTypeError("must be a finite number between 0 and 1")
    return weight


def main():
    parser = argparse.ArgumentParser(description="Synthetic-only hybrid recommender demo")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--k", type=int, default=10)
    parser.add_argument("--als-weight", type=unit_interval, default=0.6,
                        help="ALS share for warm-user hybrid scoring (0 to 1; default: 0.6)")
    parser.add_argument("--output", type=Path, help="Optional synthetic aggregate JSON report")
    args = parser.parse_args()
    catalog, events = make_synthetic_data(args.seed)
    train, test = temporal_split(events)
    model = HybridRecommender(seed=args.seed, als_weight=args.als_weight).fit(catalog, train)
    report = evaluate(model, test, args.k)
    report["configuration"] = {"seed": args.seed, "cutoff": CUTOFF.isoformat(),
                               "products": len(catalog), "train_events": len(train),
                               "test_events": len(test), "als_weight": model.als_weight}
    report["environment"] = {"python": platform.python_version(), "numpy": np.__version__,
                              "scikit_learn": sklearn.__version__}
    report["examples"] = {u: {"route": model.route(u), "items": model.recommend(u, args.k)}
                          for u in ("demo_user_000", "demo_user_060", "demo_user_070")}
    output = json.dumps(report, indent=2) + "\n"
    print(output, end="")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
