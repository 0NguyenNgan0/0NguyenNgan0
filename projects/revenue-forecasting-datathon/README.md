# Revenue Forecasting & Business Diagnosis
### Datathon 2026 · Round 1 · Team IKIGAI

Investigating a decline in e-commerce revenue and forecasting daily revenue and cost of goods sold (COGS) across a changing business environment.

**My focus:** contributions to data auditing and cleaning, feature engineering, ensemble forecasting, leakage-aware validation, model optimization, and post-processing.

[Team source code](https://github.com/DinhVinhBinhNghi/Datathon2026) · [Technical walkthrough & reproduction](TECHNICAL_NOTES.md) · [Evidence & limitations](EVIDENCE.md) · [Back to my profile](../../README.md)

## The business problem

The competition dataset describes a Vietnamese fashion e-commerce business. The team investigated whether falling revenue reflected normal seasonality or a longer-term change in customer and operating behavior.

The work had two connected outputs:

- **Business diagnosis:** connect revenue trends with customer activity, promotions, conversion, and inventory.
- **Forecasting:** generate daily Revenue and COGS predictions for the 548 dates in the archived submission, from January 1, 2023 to July 1, 2024.

## My contribution within the team

I contributed to data auditing and cleaning, feature engineering, ensemble forecasting, validation work aimed at reducing leakage, model optimization, and post-processing. The pipeline, business analysis, charts, and report are team deliverables; this page does not claim sole ownership of them.

The team's **Third Prize at the DATATHON 2026 Final** is a separate competition achievement. This case study covers the **Round 1 forecasting project**.

## Selected findings from the team report

| Observation | Team-reported finding | Decision it motivates |
| --- | --- | --- |
| Revenue shifted to a lower level after 2018 | Average daily revenue decreased by about **41.5%** | Model the change in business regime alongside seasonality |
| More sessions did not translate into more orders | Annual sessions increased by **31%**, while conversion fell from **0.97% to 0.35%** | Investigate the product-to-checkout funnel |
| Promotions had weak margins | Promotional orders accounted for **35.3%** of post-2018 revenue, with about **0.2% gross margin** | Evaluate promotions using both margin and repeat purchases |

These are descriptive findings reported by the team, not causal estimates or independently recomputed results.

![Team chart of monthly revenue and gross margin, showing the change after 2018](https://github.com/DinhVinhBinhNghi/Datathon2026/blob/97d72fc24bca0fc40763890ac717c1ccb07f54cd/outputs/figures/main/A1_overlay_revenue_margin_vi.png?raw=true)

*Original team figure; labels are in Vietnamese. [Open full-size chart](https://github.com/DinhVinhBinhNghi/Datathon2026/blob/97d72fc24bca0fc40763890ac717c1ccb07f54cd/outputs/figures/main/A1_overlay_revenue_margin_vi.png).*

## Forecasting approach

| Component | Implementation in the reviewed script |
| --- | --- |
| Calendar and seasonal inputs | 33 features spanning calendar fields, sine/cosine transforms, seasonal target summaries, operational aggregates, and data-derived flags |
| Two training periods | Model A: 2013–2018; Model B: 2019–2022 |
| Revenue ensemble | LightGBM, XGBoost, and CatBoost, each trained with five seeds for each period |
| Seasonal blend | 58% model signal + 42% seasonal profile signal |
| Period blend | 54% Model A + 46% Model B |
| COGS | Revenue multiplied by one minus estimated margin, followed by historical-pattern adjustments |

The two model periods share feature summaries built from the available history. They are not fully isolated feature pipelines. Details and evaluation implications are in the [technical notes](TECHNICAL_NOTES.md).

## Deliverables and verification status

- A team business report, supporting analysis notebooks, and charts.
- A forecasting script and an archived submission containing **548 dated predictions**.
- A source review supporting the architecture above.

The original competition CSVs are not included in the supplied archive, so I have not rerun training or independently verified a holdout score for this portfolio. No model accuracy score is claimed here.

## What this project taught me

The most useful distinction is between **building a forecast** and **demonstrating that it generalizes**. The reviewed script produces a final submission, but a trustworthy backtest also needs every learned feature summary to be rebuilt using only the history available at each validation cutoff.

The business work makes a similar distinction: a revenue recovery scenario can guide an experiment, but it is not evidence of revenue already achieved.

## Explore the work

- [Forecasting script](https://github.com/DinhVinhBinhNghi/Datathon2026/blob/97d72fc24bca0fc40763890ac717c1ccb07f54cd/scripts/run_forecast_final.py)
- [Forecasting notebook](https://github.com/DinhVinhBinhNghi/Datathon2026/blob/97d72fc24bca0fc40763890ac717c1ccb07f54cd/notebooks/05_sales_forecast_final.ipynb)
- [Audit notebook](https://github.com/DinhVinhBinhNghi/Datathon2026/blob/97d72fc24bca0fc40763890ac717c1ccb07f54cd/notebooks/01_data_audit.ipynb)
- [Join-validation notebook](https://github.com/DinhVinhBinhNghi/Datathon2026/blob/97d72fc24bca0fc40763890ac717c1ccb07f54cd/notebooks/02_join_validation.ipynb)
- [Team report archived in the source repository](https://github.com/DinhVinhBinhNghi/Datathon2026/blob/97d72fc24bca0fc40763890ac717c1ccb07f54cd/reports/tables/Datathon2026_Ikigai_Report.pdf)

Code and artifact links are pinned to the reviewed source commit. See [evidence and attribution](EVIDENCE.md) for the source boundaries.
