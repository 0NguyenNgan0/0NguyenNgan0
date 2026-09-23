# Technical walkthrough & reproduction

[Case study](README.md) · [Evidence & limitations](EVIDENCE.md)

## Scope

This page documents the team's existing final-submission script. It is not a new implementation or a claim that a fresh training run has been completed.

Reviewed source: [`scripts/run_forecast_final.py`](https://github.com/DinhVinhBinhNghi/Datathon2026/blob/97d72fc24bca0fc40763890ac717c1ccb07f54cd/scripts/run_forecast_final.py), commit `97d72fc24bca0fc40763890ac717c1ccb07f54cd`.

## 1. Build calendar and historical summaries

The script reads six CSV files. It derives date fields and cyclical features, then adds summaries from sales, inventory, web traffic, returns, and shipments.

| Input file | Columns consumed by the reviewed script |
| --- | --- |
| `sales.csv` | `Date`, `Revenue`, `COGS` |
| `sample_submission.csv` | `Date` |
| `inventory.csv` | `snapshot_date`, `stockout_days`, `fill_rate`, `sell_through_rate` |
| `web_traffic.csv` | `date`, `sessions`, `unique_visitors` |
| `returns.csv` | `return_date` |
| `shipments.csv` | `ship_date`, `delivery_date`, `shipping_fee` |

The original README also lists `promotions.csv`, but the reviewed final forecasting script does not read it. Other team analysis scripts may require additional files.

The final feature list contains:

- 8 calendar features.
- 8 Fourier/cyclical features.
- 3 seasonal revenue summaries.
- 8 auxiliary operational aggregates.
- 6 data-derived pattern features.

## 2. Train and combine revenue models

The script fits LightGBM, XGBoost, and CatBoost to `log1p(Revenue)` using seeds `42, 1337, 2024, 7, 99`. Predictions are transformed back with `expm1` and averaged across models and seeds.

This runs separately for 2013–2018 and 2019–2022. The final revenue blend is equivalent to:

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

## 4. Run the original script

Obtain the competition CSVs through an authorized source. The portfolio does not distribute them.

Clone the original team repository and select the reviewed version:

```bash
git clone https://github.com/DinhVinhBinhNghi/Datathon2026.git
cd Datathon2026
git checkout 97d72fc24bca0fc40763890ac717c1ccb07f54cd
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install dependencies and place the six input CSVs in `data/raw/`:

```bash
python -m pip install -r requirements.txt
python scripts/run_forecast_final.py --data-dir data/raw --out submissions/submission.csv
```

Run from the team repository root. The requirements file does not pin package versions; this is a reproduction guide, not a verified environment lockfile. The reviewed script trains 30 revenue models, 10 margin models, and one additional diagnostic model.

## 5. Interpret the outputs

| Output | Meaning |
| --- | --- |
| `submissions/submission.csv` | Predicted `Date, Revenue, COGS` |
| `outputs/modeling/shap_group_comparison.csv` | Fixed percentages exported by the script; not newly calculated SHAP values |
| `outputs/modeling/feature_group_importance_comparison.csv` | A duplicate of that fixed-percentage table |

The script does not itself render the SHAP chart, despite the original README describing the PNG as a run output.

Before using a new submission, independently verify exact date order against the sample, unique dates, matching row count, column order, finite values, and non-negative predictions. The reviewed script writes the CSV but does not contain the explicit submission assertions described in the original documentation.

## 6. Evaluation that remains to be reproduced

The team report mentions a 2021–2022 time-based holdout. The final-submission script does not perform that split or calculate holdout metrics.

A defensible backtest should:

1. Choose a chronological cutoff and reserve later dates for validation.
2. Restrict sales and auxiliary records to information actually available at the cutoff, including delivery outcomes.
3. Rebuild target summaries, data-derived flags, seasonal profiles, and missing-value fallbacks from the training portion only.
4. Compare a seasonal baseline, a single-period model, and the two-period ensemble on the same validation dates.
5. Select weights without using the final evaluation period, and report the metric, dates, baseline, and improvement together.

The current script builds target-based summaries before splitting into model periods. Reusing those summaries in a retrospective holdout would contaminate validation. In training, each row also contributes to some of its own target summaries, creating self-inclusion risk. Fold-safe or out-of-fold feature construction needs separate implementation and evaluation.

This portfolio update documents these boundaries; it does not claim to have fixed or retrained the source pipeline.
