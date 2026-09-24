# Recorded synthetic run

These are **synthetic demonstration results**, not results from the original team dataset and not a claim of real-world performance.

## Configuration

- Seed: 42; K: 10; global cutoff: 2025-02-01 00:00 UTC.
- 72 fictional products; 1,362 training events; 640 held-out events.
- 80 evaluated users: 60 warm, 10 sparse, 10 new; no users skipped for lack of novel relevant items.
- Python 3.12.14, NumPy 2.3.5, scikit-learn 1.8.0.

Run from this project directory:

```bash
python -m recommender --seed 42 --k 10 --output outputs/report.json
python -m unittest discover -s tests -v
```

## Results

All ranking metrics are macro averages across the same 80 users. Values are fractions, not percentages.

| Method | Precision@10 | Recall@10 | NDCG@10 | Catalog coverage |
| --- | --- | --- | --- | --- |
| Popularity | 0.0563 | 0.1549 | 0.1058 | 0.2639 |
| Als | 0.1125 | 0.2760 | 0.2223 | 0.8889 |
| Content | 0.2087 | 0.5689 | 0.4231 | 1.0000 |
| Hybrid | 0.1938 | 0.5223 | 0.3883 | 1.0000 |

The content baseline performs best on this particular synthetic run. The generator strongly associates preferences with categories, and item metadata directly includes categories. Combining ALS with content does not improve on content alone here. This is a useful limitation to document, not a reason to change the holdout or tune against it.

All methods use the same popularity fallback for new users; their new-user scores therefore match. Full per-cohort metrics and fictional recommendation examples are in [sample_report.json](sample_report.json). Small numerical differences can occur across numerical-library platforms; fixed seeds do not guarantee identical floating-point results everywhere.

## Validation performed

- The original recorded run passed ten standard-library tests covering chronological boundaries, duplicate removal, deterministic data generation, cold-start routing, seen-item exclusion, top-K behavior, ALS objective reduction, cold-item content retrieval, hand-calculated metrics, holdout argument usage, repeat-consumption exclusions, and invalid inputs. The current suite has 13 tests, including three CLI input/output checks added later.
- The CLI completed with seed 42 / K=10 and an alternate seed / K=5.
- Every notebook code cell executed sequentially with the project environment; the notebook outputs contain only synthetic examples and aggregate results. A Jupyter UI session was not used for this check.

Dependencies were verified in the environment listed above. A fresh dependency installation on every operating system was not tested. No original data files were used in this run.
