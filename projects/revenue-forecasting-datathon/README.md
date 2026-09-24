# Revenue Forecasting & Business Diagnosis
### Datathon 2026 · Round 1 · Team IKIGAI

Investigating e-commerce revenue changes and forecasting daily revenue and cost of goods sold (COGS).

**My focus:** contributions to data auditing and cleaning, feature engineering, ensemble forecasting, validation review, model optimization, and post-processing.

[Technical notes](TECHNICAL_NOTES.md) · [Evidence & limitations](EVIDENCE.md) · [Back to my profile](../../README.md)

## The business problem

The team connected business diagnosis with daily Revenue and COGS forecasting. The public case study describes the questions and methods; original data, reports, charts, submission values, and dataset-derived business metrics are not reproduced or linked here.

| Business question | Analytical approach |
| --- | --- |
| Does a revenue change reflect seasonality or a different operating regime? | Compare seasonal patterns and consider models for different historical periods |
| How do traffic and conversion relate to revenue? | Examine the customer funnel while distinguishing association from causation |
| How should promotions be evaluated? | Consider margin and repeat purchases alongside revenue |
| How might operations affect demand and profitability? | Audit inventory, returns, and shipment records before building historical summaries |

These are analytical questions, not published findings about the underlying business.

## My contribution within the team

I contributed to data auditing and cleaning, feature engineering, ensemble forecasting, validation review, model optimization, and post-processing. Leakage-safe backtesting has not been reproduced for this portfolio. The pipeline, business analysis, charts, and report are team deliverables; this page does not claim sole ownership of them.

The team's **Third Prize at the DATATHON 2026 Final** is a separate competition achievement. This case study covers the **Round 1 forecasting project**.

## Forecasting approach

| Component | Implementation in the reviewed script |
| --- | --- |
| Calendar and seasonal inputs | Calendar fields, cyclical transforms, seasonal target summaries, and operational aggregates |
| Two training periods | Separate ensembles for earlier and later historical periods |
| Revenue ensemble | LightGBM, XGBoost, and CatBoost across multiple training runs |
| Seasonal blend | Fixed combination of model predictions and historical seasonal profiles |
| Period blend | Fixed combination of the two period-specific ensembles |
| COGS | Revenue multiplied by one minus estimated margin, followed by historical-pattern adjustments |

The two model periods share feature summaries built from the available history. They are not fully isolated feature pipelines. Details and evaluation implications are in the [technical notes](TECHNICAL_NOTES.md).

## Deliverables and verification status

The original team work includes a business report, analysis notebooks, charts, a forecasting script, and a prediction submission. These materials are not distributed through this portfolio.

The architecture above is supported by source inspection during portfolio preparation. Training on the original competition CSVs and independent holdout evaluation have not been reproduced for this portfolio. No model accuracy score or achieved business impact is claimed here.

## Key technical lesson

Producing a forecast does not establish that it generalizes. A trustworthy backtest needs every learned feature summary to be rebuilt using only information available at each validation cutoff. Likewise, a business recovery scenario can guide an experiment without establishing that the proposed revenue improvement has occurred.

## Explore the portfolio

- [Technical design and evaluation boundaries](TECHNICAL_NOTES.md)
- [Evidence, team attribution, and limitations](EVIDENCE.md)
- [Separate runnable recommender demo using synthetic data](../hybrid-product-recommender/README.md)
