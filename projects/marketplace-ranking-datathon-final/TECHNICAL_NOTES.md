# Technical notes

These notes summarize a privately reviewed team source archive. They explain design choices and evaluation boundaries without publishing internal configuration, user behavior definitions, feature schema, dates, or original code. The pipeline has not been executed for this portfolio.

## Retrieval and ranking

The system separates candidate retrieval from learned ranking. Multiple sources propose items, and a fallback helps when little history is available. Deduplication and candidate limits matter: a configured quota does not guarantee the same number of unique candidates for every user.

A LightGBM LambdaRank model orders the resulting candidate set. Its output is a ranking score, not a calibrated probability. Cached or intermediate features must be tied to the correct training cutoff; reusing stale artifacts after a configuration change can invalidate an evaluation.

## Time and validation

The training example builds labels for a later period and uses a split of the resulting candidate population for internal ranker validation. Evaluating a complete recommendation pipeline on a later period is a different question. The latter must check both candidate recall and final ranking, with historical features restricted to information available at the cutoff.

The source includes some ordering checks, but these do not by themselves prove that every joined attribute, snapshot, and cache is free of future information. This portfolio review is not a full leakage audit. Numerical validation and leaderboard results have not been independently reproduced.

## Marketplace adjustment

The inspected rule adjusts ranking scores by freshness and seller position. It does not impose a strict cap on seller exposure. Multiplying signed scores can have counterintuitive effects when scores are negative, so the observed exposure effect would need to be measured on authorized data. Deployment and online testing are future work, not verified outcomes of this project.

## Submission checks

The original validator checks the expected structure, coverage, duplicate rows, rank bounds, and missing values. A successful format check does not prove model quality. Original records, trained models, submissions, and benchmarks are not distributed here.
