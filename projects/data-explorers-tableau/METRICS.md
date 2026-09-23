# Metric definitions

[Case study](README.md) · [Dashboard walkthrough](DASHBOARD_GUIDE.md)

The formulas below were read from the team's workbook. They document the existing logic; they are not a claim that every calculation was authored by me or that all outputs have been independently reconciled.

## Sales measures

| Measure | Tableau expression | Interpretation |
| --- | --- | --- |
| Premium revenue | `SUM([PHIBH])` | Sum of insurance premium values |
| Contracts | `COUNTD([MA_HD])` | Distinct contract identifiers |
| Customers | `COUNTD([MA_KH])` | Distinct customer identifiers |
| Average premium per contract | `SUM([PHIBH]) / COUNTD([MA_HD])` | Premium per distinct contract within the calculation scope |

Distinct counts help define the denominator, but they do not by themselves guarantee that a premium sum is unaffected by duplicate records or relationship behavior. Reconciling totals requires the underlying data and Tableau evaluation.

## Renewal share

```tableau
COUNTD(
    IF [LOAI_HD] = "Tái tục" THEN [MA_HD] END
)
/
COUNTD([MA_HD])
```

The denominator is all distinct contracts, not a cohort of contracts eligible for renewal. Describe the output as **renewal share**.

The workbook also defines a normalized contract-type field using lowercase and trimmed text, with accented and unaccented renewal labels. This particular share formula uses the original exact-match field instead. Its treatment of inconsistent labels needs reconciliation with the intended business definition.

## Target attainment

```tableau
SUM([Actual]) / SUM([KPI])
```

This is a ratio of totals. It is not the same as an unweighted average of department percentages.

The workbook includes both gap conventions:

```tableau
// Shortfall: positive means below target
SUM([KPI]) - SUM([Actual])

// Variance: positive means above target
SUM([Actual]) - SUM([KPI])
```

Both can be useful, but the label and sign convention must be explicit.

## Department-level attainment and coverage

The workbook defines a fixed department-level ratio:

```tableau
{ FIXED [Tên Phòng Ban] : SUM([Actual]) / SUM([KPI]) }
```

The coverage calculation counts distinct departments whose attainment is **at least 80%**, divided by the distinct department count. The worksheet title says `>80%`, while the expression uses `>= 0.8`; departments exactly at 80% are included by the formula.

This threshold is not equivalent to meeting the full target, which requires attainment of at least 100%.

## Cross-selling

For a customer within a channel, one field counts distinct product groups:

```tableau
{ FIXED [TEN_KENH_BAN], [MA_KH] : COUNTD([NHOMSANPHAM]) }
```

A related calculation counts customers with at least two product groups and divides by all distinct customers in scope.

Another field counts distinct business lines per customer:

```tableau
{ FIXED [MA_KH] : COUNTD([Line Business]) }
```

In the second example, the readable caption replaces the workbook's internal calculation ID. Product groups within a channel and business lines across a customer are different definitions of cross-selling; they should not share one unlabeled KPI.

These fields exist in the workbook. Their existence alone does not establish that every dashboard displays them.

## Data preparation visible in the formulas

The definitions include:

- Missing department and branch labels replaced with explicit “unassigned” labels.
- Missing employee names assigned an “unknown employee” display label.
- Contract dates grouped by month.
- Department names reformatted for display.
- Contract-type text normalized for some calculations.
- A date flag excluding the month containing the latest contract date.

The last rule is a heuristic for selecting complete months. Its presence does not prove that the flag is applied to every view or that the latest month is actually incomplete.

## Checks before publishing numerical insights

Reconcile premium totals and distinct counts at the intended grain; verify the time period and filter scope; handle zero or missing KPI denominators; confirm gap signs and threshold boundaries; and test whether labels remain accurate after selections.

This portfolio publishes definitions and structural evidence rather than unverified data values.
