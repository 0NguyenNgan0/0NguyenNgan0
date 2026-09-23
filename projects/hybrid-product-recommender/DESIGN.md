# Design and evaluation notes

## Data and availability

The generator creates 72 fictional products in four categories and 80 fictional users. Sixty users have substantial training history, ten have two training events, and ten first appear after the cutoff. Eight products have catalog metadata but no training events. The full catalog is available before the cutoff; the generator is not fitted to or derived from original data.

Events have `user_id`, `product_id`, `event_type`, and a timezone-aware `timestamp`. Catalog records have `product_id`, `category`, and `brand`. Event weights are view = 1, cart = 2, purchase = 3. Exact duplicate events are removed; separate repeated interactions still contribute to confidence.

The global cutoff is **2025-02-01 00:00 UTC**, a fictional experimental date. Training is strictly before it, and holdout begins at or after it. Popularity, interaction matrices, user profiles, and latent factors use only training interactions. TF-IDF uses the catalog metadata assumed available at that point; it never reads holdout events. This is a fixed-snapshot evaluation, with no updates during the holdout period.

## Implicit ALS

For each user and product, sum the training event weights into `r_ui`. Define binary preference `p_ui = 1[r_ui > 0]` and confidence `c_ui = 1 + alpha * r_ui`. Alternating ridge solves minimize:

```text
sum_ui c_ui * (p_ui - x_u dot y_i)^2
    + regularization * (sum_u ||x_u||² + sum_i ||y_i||²)
```

The default demo uses 12 factors, 15 iterations, alpha 10, regularization 0.1, and seed 42. Missing interactions retain confidence 1; they are not omitted. An item with no training interactions has a zero ALS factor after its ridge solve. Content can still retrieve it.

This formulation follows [Hu, Koren and Volinsky, Collaborative Filtering for Implicit Feedback Datasets (2008)](https://yifanhu.net/PUB/cf.pdf). The implementation uses dense matrices for readability and a small catalog; it is not the scalable implementation in the paper. The tests check that its objective decreases across alternating updates.

## Content and hybrid

TF-IDF represents category and brand tokens using [scikit-learn's TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html). A user's vector is the normalized weighted sum of training-item vectors; dot products then give cosine similarity to catalog items.

The hybrid routes new users to training-period popularity, sparse users to content, and other users to a weighted ALS/content score. Each component is min-max scaled over that user's unseen candidates, with a constant score vector mapped to zeros. This permits negative raw ALS scores without assuming they are probabilities. The mixture weight is a demonstration choice, not a calibrated probability or a validated optimum.

All rankings exclude seen products. Ties are resolved by product ID. A request returns fewer than K items only when the unseen catalog contains fewer than K items. Popularity is the sum of training weights and has **no recency decay**; it is not labeled a trending model.

## Evaluation contract

For each holdout user, build the unique relevant set from all held-out event types, then remove items seen in training. This measures novel-item discovery, not purchase conversion or repeat consumption. Users with no novel relevant items are counted and excluded for every method. Unknown products or overlapping timestamps cause an explicit error instead of silent skipping.

- **Precision@K:** hits / K, even when fewer than K candidates are available.
- **Recall@K:** hits / number of novel relevant products.
- **NDCG@K:** binary discounted gain with log2(rank + 1), divided by the ideal gain for min(K, relevant count).
- **Aggregation:** arithmetic mean of each user's metric over the shared eligible population; also reported by history cohort.
- **Catalog coverage:** number of distinct recommended items / full catalog size across evaluated users.

The model is fitted once. Methods use the same population, candidate universe, seen-item filtering, and fixed K. Pure ALS and content baselines bypass the sparse-user switch; both fall back to popularity for users with zero history. This shared fallback is stated explicitly so cold-start results are not mistaken for personalization.

No model selection is performed with this holdout. A real study should add a separate earlier validation period, choose relevance definitions deliberately, use multiple time windows, and consider exposure bias and item availability. A single synthetic run cannot support a general claim of model superiority.

## Relationship to the course project

| Aspect | Team source notebook | Public demo |
| --- | --- | --- |
| Data | Original project events, kept private | Independent synthetic generator |
| Collaborative component | `implicit` ALS package | Small NumPy implicit ALS implementation |
| Content component | Category/brand TF-IDF and item similarity | Category/brand TF-IDF and weighted user profile |
| Hybrid idea | Collaborative/content weighting and fallbacks | Explicit warm/sparse/new routing |
| Evaluation | Notebook variables and experiment-specific logic | Function arguments, shared population, chronological checks |
| Results | Original outputs not republished | Clearly labeled synthetic metrics |

The public implementation is an educational adaptation. It does not reproduce the original notebook's numerical results, experimental settings, or complete feature set. Product-page context and real-time updates are outside this version.
