# Technical notes

These notes describe the supplied `DATATHON_IKIGAI-main.zip` snapshot. Configuration values are implementation settings, not newly measured results. The original pipeline has not been executed as part of preparing this case study.

## Candidate generation

The model separates retrieval from ranking. Five source modules propose items:

| Source | Example quota | Signal |
| --- | ---: | --- |
| Re-engagement | 50 | Listings previously interacted with by the user |
| Co-visitation | 80 | Related listings connected through interaction histories |
| Category popularity | 30 | Popular listings in a preferred category |
| City/category popularity | 20 | Popular listings matching local/category context |
| Global popularity | 20 | Broad fallback for limited-history users |

The quotas sum to 200. Actual distinct candidates can be fewer because sources overlap or lack eligible items. `merge.py` normalizes scores using a maximum per source, deduplicates user–item pairs, and retains the top configured number of candidates per user. This is not a guarantee that every user receives every source's full quota.

Unlike the separate synthetic product demo, this competition design intentionally includes previously viewed listings through re-engagement: returning to a property listing can be relevant to a later contact decision.

## Interaction weights and labels

The example weights assign 3 to phone/chat/Zalo/SMS contact actions, 1 to `other_interaction`, and 0 positive-contact weight to pageviews. Pageview counts can still enter the feature set.

The ranker creates graded relevance labels from the sum of weighted future interactions for each user–item pair:

| Weighted interaction sum | Relevance label |
| --- | ---: |
| Zero | 0 |
| Greater than zero and below 3 | 1 |
| At least 3 and below 6 | 2 |
| At least 6 | 3 |

These are score thresholds, not exact counts of contact actions: several lower-weight interactions can also cross a threshold. LambdaRank learns an ordering from those labels; its raw output is not a calibrated probability of contact.

## Features and memory handling

The actual lists in `model/src/ranker/feature_spec.py` declare **39 numeric and 5 categorical features**, for a total of 44. Older comments in that file contain a different count; the lists are the source for the count used here.

Features include candidate score, user activity and category affinity, listing attributes and popularity, user–item interaction history, and recency tiers. Identifier columns are defined separately from model features.

Candidate merging and reranking use user buckets and intermediate Parquet files. The training code materializes labeled and sampled intermediates before loading the sampled training frame. These reduce the size of individual operations but do not establish a bounded-memory guarantee for every stage. Cache existence checks are present; changing configuration should also invalidate dependent artifacts before rerunning.

## Temporal setup and validation

The supplied example configuration uses:

| Purpose | Period or boundary |
| --- | --- |
| History available for ranker features | Through 12 March 2026 |
| Internal future-label window | 13 March–9 April 2026 |
| History available for competition prediction | Through 9 April 2026 |
| Hidden competition target window | 10 April–7 May 2026 |

Within the labeled candidate frame, training keeps users with positive candidate labels and samples negatives. It then splits users into training and validation groups; the example validation ratio is 10%. LightGBM evaluates the graded-label ranking task on that sampled candidate population.

The separate submission evaluator calculates binary Recall@K and NDCG@K from ground-truth sets. Missing predictions receive zero for users with nonempty ground truth. Thus internal LightGBM validation, local submission evaluation, and leaderboard evaluation differ in labels, candidate population, or period. Candidate recall must also be assessed: a ranker cannot retrieve a relevant listing omitted by candidate generation.

The included `test_no_leakage.py` checks configuration ordering and date formats. Those tests alone do not prove that every join, metadata snapshot, or reused cache is free of future information. The source review here is not a full leakage audit.

## Marketplace reranking

The inspected SQL applies a multiplier to recent listings, assigns a within-user/within-seller rank, and multiplies scores beyond a configured seller threshold by 0.5. It then reranks by the adjusted score.

This is a **soft score adjustment**, not a hard seller cap. For signed ranker scores, multiplying a negative score by 0.5 can increase it; multiplying a negative score by a freshness factor above 1 can decrease it. The intended effect therefore needs testing against the actual score distribution. A hard exposure constraint would require explicit constrained selection and checks on the final list.

The presentation discusses serving latency, refreshes, online experiments, and operational guardrails as potential deployment work. The supplied materials do not establish a production deployment or a completed online experiment.

## Submission boundary

The archived validator checks the expected header, total rows, user coverage, ten rows per user, rank bounds, duplicate user/rank and user/item pairs, null values, and BOM handling. Unknown catalog items and oversize files produce warnings in the inspected implementation. A validator pass should therefore be interpreted alongside those warnings.

No original records, trained model, competition submission, or benchmark outputs are distributed with this documentation.
