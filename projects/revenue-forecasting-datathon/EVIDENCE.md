# Evidence, attribution & limitations

[Case study](README.md) · [Technical notes](TECHNICAL_NOTES.md)

## Source material and publication boundaries

This case study was prepared by reviewing a team report and a source archive supplied privately for portfolio preparation. The report supports the project context; inspection of the forecasting script supports the implementation description.

The public portfolio does not reproduce or link the original report, archive, notebooks, charts, prediction files, dataset-derived business metrics, or source repository containing those materials. Source identifiers, internal configuration values, and original submission date ranges are omitted. Model architecture is described separately from measured outcomes.

This boundary applies to the current portfolio pages. It does not establish the access settings of copies held elsewhere or remove earlier versions from Git history.

## Personal contribution and team outcome

Nguyễn Thanh Ngân contributed to audit and cleaning, feature engineering, ensemble forecasting, validation review, optimization, and post-processing. The supplied report identifies team **IKIGAI**. The team code, analysis, charts, and report are not presented as independently authored by Ngân.

The Third Prize is a **DATATHON 2026 Final team award**. It is not a Round 1 model ranking or a forecasting accuracy measure.

## Claims retained and qualified

| Claim | Basis and limitation |
| --- | --- |
| Ensemble uses several boosting libraries and historical feature groups | Confirmed by source inspection during portfolio preparation; not evidence of predictive accuracy |
| Revenue combines model predictions with seasonal summaries | Confirmed by source inspection; the weight-selection process has not been reproduced |
| Time-based holdout evaluation | Described in the supplied report; the reviewed final script does not implement that evaluation |
| Grouped explanation percentages | Fixed values in the reviewed script; not verified SHAP explanations |
| Business improvement scenarios | Proposed scenarios, not demonstrated production impact; numerical claims are omitted |

## Reproduction status

Portfolio preparation included reading the supplied report and forecasting script and checking the implementation behind the feature groups, model blend, and exported explanation tables. This is a source review, not an independently reproduced experiment.

The following have not been completed for this case study:

- Training on the original competition CSVs, which are absent from the supplied archive.
- Independent reproduction of business metrics or a leaderboard score.
- Leakage-safe backtesting with fold-specific feature summaries.
- Fresh SHAP calculation or validation of the fixed explanation percentages.

The separate [synthetic recommender demo](../hybrid-product-recommender/README.md) can be run without the competition materials. It is a different project and does not validate this forecasting pipeline.

## Attribution

The original implementation and competition materials remain team work. This portfolio adds a personal case study and a documented technical review. It does not redistribute or apply a new license to the original materials.
