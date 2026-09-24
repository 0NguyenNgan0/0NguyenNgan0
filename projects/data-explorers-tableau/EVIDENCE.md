# Evidence and review notes

[Case study](README.md) · [Metric definitions](METRICS.md)

The evidence is a privately supplied team Tableau workbook and a competition brief. The workbook contains three dashboards and 26 worksheets. I contributed to data cleaning and modeling, team coordination, and presentation structure; these counts are team scope, not personal output.

## Structural review

A small generic [inspection helper](inspect_workbook.py) was added for this portfolio review. It is not part of the original competition submission. The publicly available text reports only aggregate workbook size and high-level findings, without distributing the packaged workbook, its embedded data extracts, a machine-readable structural summary, source names, internal columns, or raw formulas.

The saved definition suggests several items to check in an authorized Tableau session:

- A measure label may not match the field plotted in one worksheet.
- A renewal share needs a distinct label from cohort retention.
- A threshold title and its underlying boundary may differ.
- Target gaps use different sign conventions across calculations.
- Rule-based customer segments should not be described as validated risk predictions.

These observations come from the saved definition. The original dashboard has not been tested interactively; filter behavior, refresh, data totals, and business impact are unverified.

## Publication and attribution

The competition brief restricts redistribution of the supplied data. The workbook and its embedded extracts, records, screenshots, and business values are excluded from this public folder. The team created the workbook; this portfolio records my contribution and a limited structural review. The Third Prize DATATHON case study belongs to a different competition.
