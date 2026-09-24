# Technical design & evaluation

[Case study](README.md) · [Evidence & limitations](EVIDENCE.md)

## Scope

This page documents the team's existing final-submission script. It is not a new implementation or a claim that a fresh training run has been completed.

The source was supplied privately for review. Original files and links to repositories containing the competition materials are omitted from this public page. Numerical constants below describe implementation settings, not measured business outcomes.

## 1. Build calendar and historical summaries

The script derives date fields and cyclical features, then adds historical summaries from sales, inventory, web traffic, returns, and shipments. A separate input specifies the prediction dates. This page describes input categories without distributing records or their aggregate values.

The final feature list contains:

- 8 calendar features.
- 8 Fourier/cyclical features.
- 3 seasonal revenue summaries.
- 8 auxiliary operational aggregates.
- 6 data-derived pattern features.

## 2. Train and combine revenue models

The script fits LightGBM, XGBoost, and CatBoost to `log1p(Revenue)` using seeds `42, 1337, 2024, 7, 99`. Predictions are transformed back with `expm1` and averaged across models and seeds.

This runs separately for earlier and later historical periods. The final revenue blend is equivalent to:

```text
model_signal = 0.54 * ensemble_A + 0.46 * ensemble_B

Revenue = 0.58 * model_signal
        + 0.02 * day_of_year_median
        + 0.04 * month_weekday_mean
        + 0.36 * month_day_median
```

Revenue is then clipped to be non-negative.

The numerical weights are fixed in the script. The report describes validation and sensitivity checks, but the reviewed script does not reproduce the process that selected those weights.

## 3. Estimate COGS

A five-seed LightGBM ensemble predicts margin separately for each period. The margin target and predictions are clipped to `[0.02, 0.35]`.

The initial prediction is:

```text
COGS = Revenue * (1 - blended_margin)
```

Historical month/day COGS-to-revenue patterns then adjust selected dates. These adjustments can move final COGS outside the initial margin bounds; the clipped margin should not be described as a guarantee on the final output.

## 4. Reproduction boundary

The original training data and team source package are not distributed here. Source inspection is the basis for this walkthrough; training and evaluation have not been rerun for this portfolio.

For an executable example that needs no original project data, see the separate [synthetic recommender demo](../hybrid-product-recommender/README.md). That demo does not reproduce or validate this forecasting model.

## 5. Output checks and explanation limits

The script exports dated Revenue and COGS predictions. Before using any new submission, verify its date order against the requested dates, uniqueness, row count, column order, finite values, and non-negative predictions. Those explicit submission assertions are absent from the reviewed final script.

The script also exports two copies of a fixed-percentage feature-group table. These percentages are not newly calculated SHAP values and should not be presented as verified model explanations. The script does not itself render a SHAP chart.

## 6. Evaluation that remains to be reproduced

The team report mentions a time-based holdout. The final-submission script does not perform that split or calculate holdout metrics.

A defensible backtest should:

1. Choose a chronological cutoff and reserve later dates for validation.
2. Restrict sales and auxiliary records to information actually available at the cutoff, including delivery outcomes.
3. Rebuild target summaries, data-derived flags, seasonal profiles, and missing-value fallbacks from the training portion only.
4. Compare a seasonal baseline, a single-period model, and the two-period ensemble on the same validation dates.
5. Select weights without using the final evaluation period, and report the metric, dates, baseline, and improvement together.

The current script builds target-based summaries before splitting into model periods. Reusing those summaries in a retrospective holdout would contaminate validation. In training, each row also contributes to some of its own target summaries, creating self-inclusion risk. Fold-safe or out-of-fold feature construction needs separate implementation and evaluation.

This portfolio update documents these boundaries; it does not claim to have fixed or retrained the source pipeline.
