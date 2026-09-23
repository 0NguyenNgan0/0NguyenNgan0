# Hybrid Product Recommender

**Runnable Python demo · implicit ALS · TF-IDF · cold-start routing · synthetic data only**

A small product recommendation pipeline combining collaborative signals with product metadata. It demonstrates how recommendations change for users with rich history, sparse history, or no history, and compares four methods on a chronological holdout.

This is a **new portfolio reimplementation inspired by a team course project**, not a reproduction of its original experiment or benchmark. The original dataset, notebook outputs, report, personal identifiers, and team files are not distributed here.

[Portfolio index](../README.md) · [Design and evaluation](DESIGN.md) · [Demo notebook](demo.ipynb) · [Recorded synthetic run](sample_report.json)

## Run in a few minutes

Use **Python 3.12**. From the repository root:

```bash
cd projects/hybrid-product-recommender
python -m venv .venv
```

Activate the environment:

```bash
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell (use this instead)
.venv\Scripts\Activate.ps1
```

Install dependencies, run the demo, and run the tests:

```bash
python -m pip install -r requirements.txt
python -m recommender
python -m unittest discover -s tests -v
```

The demo generates a fictional catalog and event history **in memory**, trains on January events, and evaluates February events. No dataset download, account, API key, Google Drive mount, or network request is required by the demo after dependency installation.

Optional: save aggregate results or try a different synthetic seed:

```bash
python -m recommender --seed 42 --k 10 --output outputs/report.json
python -m recommender --seed 17 --k 5
```

To explore the notebook, open `demo.ipynb` in a Python notebook editor with the same environment, or install JupyterLab separately (`python -m pip install jupyterlab`) and run `jupyter lab demo.ipynb` from this folder. Jupyter is optional; the CLI is the primary reproducible entry point.

## What the pipeline does

| User history at training cutoff | Hybrid behavior |
| --- | --- |
| No interactions | Weighted training-period popularity |
| 1–2 distinct products | TF-IDF similarity to the user's weighted content profile |
| At least 3 distinct products | 60% normalized ALS score + 40% normalized content score |

Every method excludes previously seen products and uses the same catalog candidates. Product metadata is assumed available before the cutoff, including items without interactions. All example identifiers start with `demo_`; brands are explicitly fictional.

The four comparison methods are **popularity, ALS, content, and routed hybrid**. ALS and content baselines do not inherit the hybrid's sparse-user switch. All methods share a popularity fallback for completely new users.

## Project background and contribution

The source academic project was team work in Python for Data Science at the University of Science, VNU-HCM. Its approach combined implicit ALS, product content, and fallback recommendations.

**My contribution to the original team project:** shared work on problem definition, data loading and preparation, EDA, hybrid and cold-start design, Precision/Recall evaluation, testing and debugging, and task coordination. These are team contributions, not a claim of sole authorship of the original system.

This public demo is newly written for the portfolio. It replaces the original data with an independent generator, replaces the original `implicit` package backend with a small NumPy ALS implementation, and uses explicit evaluation functions and tests. See [design differences](DESIGN.md#relationship-to-the-course-project) before interpreting its results.

## Evaluation and limits

The holdout measures **discovery of previously unseen products**. Relevant items are unique held-out interactions of any supported event type, excluding products seen in training. Precision@K, Recall@K, and NDCG@K are macro-averaged over the same eligible users for every method; catalog coverage and warm/sparse/new cohort results are also reported.

Synthetic preferences deliberately favor product categories. This may favor content-based recommendations. The example scores demonstrate working code and evaluation bookkeeping; **they do not establish real-world accuracy, business impact, or that hybrid outperforms a baseline**. Hyperparameters are fixed, not tuned on the holdout. Dense ALS is educational and not intended for a large production catalog.

For the recorded run and validation details, see [RESULTS.md](RESULTS.md).

## Files

| File | Purpose |
| --- | --- |
| `recommender/data.py` | Synthetic generator, typed records, chronological split |
| `recommender/model.py` | Weighted interactions, implicit ALS, TF-IDF, routing and ranking |
| `recommender/evaluate.py` | Shared holdout population and ranking metrics |
| `recommender/__main__.py` | CLI and optional JSON report |
| `demo.ipynb` | Walkthrough using the same implementation |
| `tests/test_recommender.py` | Behavioral and mathematical checks |

## Data boundary

Only new code, explanatory text, and synthetic examples are included. Original datasets and source notebook outputs remain private. The demo does not load local data files. Ignore rules reduce accidental additions of common data formats but are not a privacy enforcement mechanism: review any future additions before publishing.
