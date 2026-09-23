# Evidence, attribution & limitations

[Case study](README.md) · [Technical walkthrough](TECHNICAL_NOTES.md)

## Source material

| Source | Used for |
| --- | --- |
| Supplied `Report v1.pdf`, titled “Từ suy giảm doanh thu đến phục hồi tăng trưởng” | Team-reported business findings and forecasting narrative |
| Supplied `Datathon2026_Round1.zip` | Source inspection, archived metrics, notebooks, and submission dates |
| [Original team repository](https://github.com/DinhVinhBinhNghi/Datathon2026) | Public access to the code and artifacts |
| Source commit `97d72fc24bca0fc40763890ac717c1ccb07f54cd` | Stable links to the reviewed version |

The supplied forecasting script and the pinned public script have the same Git blob SHA: `4b87c3538d56cf976f9497c10bc657cd1326db9f`.

The supplied report identifies the team as **IKIGAI**. The archived repository README uses **The Gridbreakers**. This page uses the report's team name and preserves the original source attribution.

## Personal contribution and team outcome

Nguyễn Thanh Ngân contributed to audit and cleaning, feature engineering, ensemble forecasting, leakage-aware validation work, optimization, and post-processing. The team code, analysis, and charts are not presented as independently authored by Ngân.

The Third Prize is a **DATATHON 2026 Final team award**. It is not a Round 1 model ranking or a forecasting accuracy measure.

## Claims retained and qualified

| Claim | Treatment in this portfolio |
| --- | --- |
| Daily revenue decreased by approximately 41.5% after 2018 | Attributed to the team report; consistent with its archived metric file |
| Sessions increased 31%; conversion decreased from 0.97% to 0.35% | Attributed to the report; descriptive comparison, not a causal experiment |
| Ensemble uses 33 features, three boosting libraries, and five seeds | Confirmed by source inspection |
| Archived submission contains 548 dates | Counted from the supplied CSV: 2023-01-01 to 2024-07-01 |
| 2021–2022 holdout evaluation | Reported in the document; not reproduced by the reviewed final script |
| Grouped SHAP percentages | Hard-coded in the reviewed script; not used here as verified model explanations |
| H1/2024 revenue recovery of +331M | A report scenario based on assumed conversion/retention improvements, not achieved business impact |
| Number of priority inventory SKUs | Omitted: the supplied report and archived metric file contain different counts |

## Reproduction status

Completed for this portfolio:

- Read the supplied report and forecasting script.
- Verified the public script matches the supplied archive.
- Counted submission rows and inspected date endpoints.
- Checked the implementation behind the feature count, model blend, and exported explanation tables.

Not completed:

- Training on the original competition CSVs, which are absent from the supplied ZIP.
- Independent reproduction of the report's business metrics or leaderboard score.
- Leakage-safe backtesting with fold-specific feature summaries.
- Fresh SHAP calculation or validation of the fixed explanation percentages.

## Attribution

The source repository, figures, notebooks, and competition report are team work. This portfolio adds a personal case study and a documented technical review. Source links stay with the original team repository; this page does not apply a new license to those materials.
