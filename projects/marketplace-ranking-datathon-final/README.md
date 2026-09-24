# Marketplace Learning-to-Rank — Datathon 2026 Final

**Team IKIGAI · Third Prize, DATATHON 2026 Final · Python · LightGBM**

A team competition project for recommending real-estate listings. The public page focuses on the problem, team approach, contribution boundary, and evaluation limits. Internal interaction definitions, labels, configuration, dates, and dataset-derived results are omitted.

[Portfolio index](../README.md) · [Technical notes](TECHNICAL_NOTES.md) · [Evidence and scope](EVIDENCE.md)

## The problem

A marketplace needs to find plausible listings for a user, order them by likely relevance, and consider how exposure is distributed. These goals can conflict and need separate evaluation.

## My contribution

I contributed to assigned technical implementation work and to presenting and defending the team solution. Marketplace data analysis was a separate part of the team's work. The pipeline described here is a **team deliverable**, not a claim of sole authorship.

Team IKIGAI received **Third Prize in the DATATHON 2026 Final**. This is a team achievement, separate from the [Round 1 revenue forecasting case study](../revenue-forecasting-datathon/README.md).

## Team approach

| Stage | Purpose |
| --- | --- |
| Candidate retrieval | Gather potentially relevant listings from multiple signals and a fallback for limited history |
| Learned ranking | Use LightGBM LambdaRank to order the candidates |
| Marketplace adjustment | Adjust ranking scores to consider freshness and distribution of exposure |
| Submission validation | Check coverage, duplicates, ranking format, and missing values |

These stages were found in the privately supplied source. The portfolio does not publish the team's signal definitions, feature schema, weights, thresholds, time windows, or original code.

## Evaluation limits

The team's internal ranker validation, a complete recommendation pipeline evaluation, and the competition leaderboard are distinct settings. They should not be quoted as interchangeable accuracy figures. Candidate recall matters because a ranker cannot select a relevant listing that retrieval omitted.

The inspected seller adjustment changes scores; it is not a strict limit on how many items from a seller may appear in the final list. The source review has not reproduced training, tested the original submission against hidden labels, or established production impact. More detail on these boundaries appears in the [technical notes](TECHNICAL_NOTES.md).

## Available evidence

A privately supplied team presentation and source archive support the general architecture and review findings. The public folder distributes no original datasets, identifiers, slides, code, model artifacts, submissions, numerical benchmarks, or links to those materials.

For an independently runnable educational example on fictional data, see the separate [Hybrid Product Recommender demo](../hybrid-product-recommender/README.md). It does not reproduce this competition pipeline.
