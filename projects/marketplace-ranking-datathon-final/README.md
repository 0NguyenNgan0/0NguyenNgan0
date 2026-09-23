# Marketplace Learning-to-Rank — Datathon 2026 Final

**Team IKIGAI · Third Prize, DATATHON 2026 Final · Python · DuckDB · LightGBM**

A team competition project for recommending real-estate listings on a marketplace. The task was to produce ten ranked listings per user while considering both user relevance and the distribution of exposure across sellers.

[Portfolio index](../README.md) · [Technical notes](TECHNICAL_NOTES.md) · [Evidence and scope](EVIDENCE.md)

## The problem

A property marketplace serves buyers looking for suitable listings and sellers seeking qualified contact. A useful recommendation system needs to retrieve plausible listings from a large catalog, distinguish stronger contact intent from weaker engagement, and avoid concentrating all exposure on a small part of the supply.

The team's solution combined multiple candidate sources, a learned ranker, and a final marketplace-oriented score adjustment. This case study describes the competition implementation from the supplied source archive and presentation. It is separate from the [Round 1 revenue forecasting project](../revenue-forecasting-datathon/README.md).

## My contribution

I contributed to assigned technical implementation work for the team project and to presenting and defending the solution. The modeling workflow below is described as a **team deliverable**. The marketplace data analysis was a separate part of the team's work, rather than my personal contribution.

The team received **Third Prize in the DATATHON 2026 Final**. This is a team achievement and does not imply sole authorship of the pipeline.

## How the solution works

| Stage | Implementation in the supplied code | Purpose |
| --- | --- | --- |
| Prepare interaction signals | DuckDB aggregation with different weights for contact and other engagement | Turn event history into user, item, and pair signals |
| Retrieve candidates | Re-engagement, co-visitation, category popularity, city/category popularity, and global popularity | Cover both familiar interests and users with little history |
| Learn the order | LightGBM LambdaRank with 44 declared features | Rank candidates using user preferences, listing attributes, recency, and pair history |
| Adjust marketplace exposure | Freshness multiplier and a seller-based score adjustment | Explore the relevance/exposure trade-off before selecting the final list |
| Build the submission | Top-ten formatting, fallback, and validation code | Produce a consistent competition submission |

The example configuration allocates up to 200 candidates per user before the final top-ten selection. User, item, and user–item feature groups are centralized so training and scoring can use a shared feature specification.

## Engineering decisions worth discussing

- **Intent weighting:** contact actions receive more weight than general interactions. Pageviews remain available as features without receiving positive contact weight.
- **Cold-start coverage:** global and contextual popularity complement personalized retrieval sources.
- **Recency and affinity:** features describe how recently a user or listing was active and how closely a listing matches the user's preferred categories.
- **Memory-conscious processing:** the archive contains SQL aggregation, intermediate Parquet artifacts, and user-bucket processing in candidate merging and reranking.
- **Submission checks:** the code checks user coverage, ten rows per user, duplicate pairs, rank bounds, missing values, and output formatting.

These describe mechanisms found in the code. They are not independently measured speed, memory, or business-impact claims.

## Results and interpretation

The presentation and repository documentation report internal ranking evaluation and competition leaderboard results. Those measures use different evaluation settings and should not be presented as interchangeable accuracy percentages. This portfolio does not reproduce the original experiment or republish its data-derived charts and numerical results.

Two details matter when explaining the project:

1. Internal ranker validation uses a user split after constructing labels and sampling candidates; it is not the same as evaluating the complete recommendation pipeline on the hidden competition period.
2. The seller rule in the inspected reranker changes scores after a within-seller threshold. It does **not** enforce a hard maximum of two listings per seller in the final list.

See the [technical notes](TECHNICAL_NOTES.md) for the evaluation setup and implementation boundaries.

## Available evidence

The supplied final-round presentation and source archive support the problem framing, pipeline design, declared feature schema, and validation mechanisms. This public folder contains newly written documentation only. Original datasets, identifiers, cached features, trained artifacts, submissions, slides, and data-derived figures are not included.

For an executable recommendation example using fully synthetic data, see the separate [Hybrid Product Recommender demo](../hybrid-product-recommender/README.md). That demo is an independent portfolio adaptation with a different model and is not a reproduction of this competition pipeline.
