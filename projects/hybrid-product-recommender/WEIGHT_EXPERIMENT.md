# Hybrid weight sensitivity experiment

This synthetic-only experiment was implemented and executed with Codex assistance
on 2026-09-24. It is a reproducible portfolio exercise, not an original team
benchmark, a claim of unaided implementation, or evidence of production impact.

## Question and controlled setup

What changes when the warm-user blend moves from 60% ALS / 40% content to
30% ALS / 70% content?

Both runs use seed 42, K=10, the same global cutoff (2025-02-01 UTC), 72 fictional
products, 1,362 training events, and 640 held-out events. The same 80 users are
evaluated: 60 warm, 10 sparse, and 10 new. Training, candidate filtering, score
normalization, routing, and evaluation are unchanged. Only the blending weight
changes. No original dataset or private report is loaded.

Environment: Python 3.12.14, NumPy 2.3.5, scikit-learn 1.8.0. Small floating-point
differences can occur on other platforms.

## Reproduce

From this project directory, with its dependencies installed:

```bash
python -m recommender --seed 42 --k 10 --als-weight 0.6 --output outputs/baseline.json
python -m recommender --seed 42 --k 10 --als-weight 0.3 --output outputs/weight_03.json
python -m unittest discover -s tests -v
```

The JSON report records the actual weight in `configuration.als_weight`.
Reports are written only when `--output` is specified. `outputs/` is ignored by
git; the table below contains only aggregate synthetic results.

## Observed results

All values are fractions, macro-averaged over the same eligible users.

| Hybrid configuration | Precision@10 | Recall@10 | NDCG@10 | Catalog coverage |
| --- | ---: | ---: | ---: | ---: |
| ALS 0.6 / content 0.4 | 0.19375 | 0.52228 | 0.38835 | 1.00000 |
| ALS 0.3 / content 0.7 | 0.20500 | 0.55540 | 0.40813 | 1.00000 |

| Cohort | NDCG@10, ALS 0.6 | NDCG@10, ALS 0.3 |
| --- | ---: | ---: |
| Warm (60 users) | 0.44831 | 0.47469 |
| Sparse (10 users) | 0.34364 | 0.34364 |
| New (10 users) | 0.07329 | 0.07329 |

The popularity, ALS-only, and content-only baselines are unchanged. Content-only
still has higher overall NDCG@10 (0.42312) than either hybrid configuration.

## Interpretation and limits

- The weight is applied after separate min-max normalization of ALS and content
  scores on eligible candidates. It does not change ALS training.
- Only warm users use the blend. Sparse users use content, while new users use
  popularity; changing the blend therefore leaves these cohorts unchanged.
- Increasing the content share improves the observed ranking metrics on this
  fixture. The generator explicitly favors product categories, so this result
  is consistent with its design. It does not establish that 0.3 is optimal.
- This is a single-seed sensitivity exercise, with no significance claim or
  independent final test. Selecting a weight using these holdout results would
  turn the holdout into validation data. A separate later test period would then
  be needed for an unbiased final assessment.
- The default stays at 0.6 to preserve existing demo behavior; this exercise does
  not silently replace the original recorded run.

## Checks performed

All 13 tests passed in the environment above: the 10 existing model/evaluation
checks plus 3 CLI tests. The new tests verify actual weight reporting and saved
JSON output, unchanged baselines and sparse/new cohorts, a changed warm result
on the fixed fixture, and clean rejection of out-of-range, nonnumeric, NaN, and
infinite weights before a report is written.

The CLI tests are included automatically by the existing unittest discovery
command used in GitHub Actions. This local result alone does not assert that a
new remote CI run has passed.
