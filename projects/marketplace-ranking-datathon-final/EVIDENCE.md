# Evidence and publication scope

This case study was prepared by reviewing the supplied final-round presentation and source archive. Source files were inspected privately; they are not attached to this public folder. Page references below use PDF page positions, starting at 1.

## Claim-to-source map

| Claim | Source inspected | What it supports |
| --- | --- | --- |
| Real-estate recommendation task; team IKIGAI | `IKIGAI_chung kết.pdf`, pages 1–3; archive root README | Project identity and marketplace objective |
| Five candidate sources | Presentation page 9; `model/config/local.example.yaml`; `model/src/candidates/sources/`; `model/src/candidates/merge.py` | Retrieval design, example quotas, merge behavior |
| LambdaRank with 44 declared features | Presentation pages 10–11; `model/src/ranker/feature_spec.py`; `model/src/ranker/train.py` | Ranker choice and 39 numeric + 5 categorical feature declarations |
| Weighted intent and relevance labels | Example configuration; `model/src/ranker/train.py`; `model/src/evaluation/ground_truth.py` | Event weights and label construction |
| Distinct validation settings | `model/src/ranker/train.py`; `model/src/evaluation/metrics.py` | User-based validation on sampled candidates versus binary submission metrics |
| Soft seller adjustment | Presentation page 12; `model/src/rerank/health_reranker.py` | Score-transform implementation; not a hard final-list cap |
| Bucketing and intermediate artifacts | `model/src/candidates/merge.py`; ranker and reranker source | Memory-oriented implementation structure |
| Submission checks | `model/src/submission/validator.py` | Checks and warning-only conditions present in source |
| Proposed operational work | Presentation pages 13–14 | Deployment ideas, not evidence of deployment |
| Personal contribution | Participant-confirmed scope | Assigned technical implementation and presentation/defense; excludes ownership of marketplace data analysis |
| Third Prize, DATATHON 2026 Final | Participant-reported team achievement, already recorded in the portfolio | Team award; the presentation and archive are not an award certificate |

## Review performed

- Read the archived project documentation, configuration, feature specification, training, candidate-merging, ground-truth, evaluation, reranking, and submission-validation code.
- Rendered and visually reviewed the 21-page presentation because many slides contain text embedded in images.
- Counted the feature declarations from the Python syntax tree rather than copying a stale comment.
- Compared presentation wording with code behavior, including seller constraints, label thresholds, and validation scope.
- Checked local links in the newly written portfolio pages before publication.

This was a source and documentation review. The competition pipeline and archived tests were not run, original data was not loaded, and reported experiment results were not independently reproduced. The ten tests in the separate synthetic recommender project do not validate this competition pipeline.

## What is public

This folder publishes newly written descriptions of the problem, team approach, confirmed contribution scope, and implementation lessons. It does not distribute source datasets, real user/item/seller identifiers, original slides or figures, trained models, cached feature tables, submission files, or numerical benchmark outputs.

The archive's role wording is not used to infer a leadership title or sole authorship. Technical components are attributed to the team unless a narrower personal contribution has been confirmed.
