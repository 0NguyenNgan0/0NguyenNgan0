# Metric definitions and review

[Case study](README.md) · [Dashboard walkthrough](DASHBOARD_GUIDE.md)

The descriptions below paraphrase the team's Tableau workbook. Exact internal field names and expressions are intentionally omitted. These are definitions to verify with authorized data, not verified numerical outcomes or a claim that I authored every calculation.

| Metric | Meaning | Check before using it |
| --- | --- | --- |
| Premium revenue | Sum of premiums in the chosen scope | Confirm record grain so joins do not duplicate amounts |
| Contract and customer counts | Distinct entities under the same filters | Confirm that identifiers and filter scope are consistent |
| Average premium per contract | Premium total divided by distinct contracts | Check for duplicate premium rows and zero denominators |
| Renewal share | Share of contracts marked as renewals | Do not describe it as customer retention without an eligible cohort |
| Target attainment | Total actual divided by total target | Match period and organizational scope; handle missing targets |
| Target gap | Difference between actual and target | State which sign means a shortfall |
| Cross-selling | Count of relevant product groups per customer in a stated scope | Distinguish product groups within a channel from business lines overall |

Some saved labels and formulas disagree at a threshold boundary or appear to describe a different measure. These findings need review in Tableau before numerical claims are published. The original workbook has not been modified; no financial totals have been independently reconciled.
