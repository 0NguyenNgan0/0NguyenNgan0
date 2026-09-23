# Evidence and review notes

[Case study](README.md) · [Metric definitions](METRICS.md)

## Sources

- The supplied team workbook, `Phân tích dữ liệu_Serendipity.twbx`, containing `Completed.twb` and four Hyper extracts.
- The supplied Data Explorers Round 1 brief, describing an insurance business and three required reporting areas.
- Previously confirmed personal contributions: data cleaning/modeling, task coordination, and presentation structure.

The separately supplied file named “Đề thi Vòng 2” is a **Datathon** brief about marketplace recommendations. It is not used as evidence for this Data Explorers case study.

## Verified structure

| Business data source | Calculated columns defined at source level |
| --- | ---: |
| CHANNEL_COMPARE | 8 |
| PB_COMPARE | 17 |
| KPI | 4 |
| SALES_ANALYSIS | 44 |
| **Total** | **73** |

There are also two parameter definitions. Counting every calculation element throughout the XML gives 130, including repeated worksheet dependencies and other definitions. That total should not be described as 130 distinct calculated fields.

The workbook contains **26 worksheet definitions, 3 dashboards, and 4 embedded Hyper files**. All three dashboards declare a fixed 1366 × 768 layout.

A small standard-library [inspection helper](inspect_workbook.py) and its [structural summary](workbook_summary.json) accompany this page. The helper was added for this portfolio review; it is not part of the original competition submission.

## Findings that require Tableau review

| Finding in the saved definition | Why it matters |
| --- | --- |
| A worksheet named “Tỷ lệ tái tục” references the revenue calculation on its row shelf | The name alone does not establish that the plotted measure is a renewal rate |
| Renewal share divides renewal contracts by all contracts | It measures contract mix, not cohort retention |
| The coverage title uses `>80%`, while the formula uses `>= 0.8` | The exact boundary differs |
| A coverage label contains a literal percentage alongside a dynamic field | Static text may stop matching the value after data or scope changes |
| Department “near target” and channel “near target” counts use different thresholds | The labels need clear definitions and do not necessarily exclude over-target groups |
| Sales-level fixed expressions group by employee name | Duplicate names could conflate different employees |
| Both `KPI - Actual` and `Actual - KPI` appear | Gap labels must make the direction clear |
| Asset/premium quadrant labels include “high risk” | The rule is not evidence of a validated insurance-risk model |

These are review observations derived from the workbook definitions. The original workbook has not been modified, and the issues have not been presented as fixed.

## Validation performed

- Parsed the packaged workbook and inspected source-level calculated columns.
- Matched dashboard worksheets to their referenced data sources.
- Checked selected formula definitions against the labels used in this case study.
- Ran the structural inspection helper on the supplied workbook and reviewed its output.

Not performed: opening the dashboard in Tableau, querying Hyper records, recomputing financial totals, or testing interactive filtering and refresh. No business-performance percentages or customer-level records are published.

## Data handling and attribution

The competition brief prohibits redistributing its supplied data. A TWBX packages data as well as the visual workbook, so the original TWBX, Hyper extracts, raw records, and data-bearing screenshots are excluded from this public folder.

The descriptions and selected formulas document the team's approach. They do not imply that Ngân personally authored every worksheet, calculation, or dashboard.
