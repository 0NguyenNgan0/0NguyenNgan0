# Dashboard walkthrough

[Case study](README.md) · [Metric definitions](METRICS.md) · [Evidence](EVIDENCE.md)

The original pages use Vietnamese labels. This guide translates their purpose and proposes a clear reading sequence, based on worksheet placement and definitions. It does not report a new analysis of the underlying records.

## 1. Business results

**Original title:** Báo cáo kết quả kinh doanh  
**Workbook page:** Dashboard 1

Begin with the KPI cards: total premium revenue, distinct contracts, distinct customers, average premium per contract, and renewal share. Then inspect the time trend, revenue composition, distribution channels, and top product groups.

| View | Question to ask |
| --- | --- |
| Premium revenue and contract count | Is a change driven by contract volume or average premium? |
| Revenue over time | Is the comparison using equivalent, complete periods? |
| Revenue by distribution channel | Which channels contribute most to the observed total? |
| Product group composition | Is revenue concentrated in a small set of products? |
| Renewal share | How much of the contract mix is labeled as renewal? |

Premium revenue is not profit: claim costs and other expenses would be needed for a profitability conclusion.

One worksheet is named “Tỷ lệ tái tục” (renewal rate), but its saved row shelf references the revenue calculation. The actual visual and its filters need checking in Tableau before presenting it as a rate. The separate “Tỷ trọng tái tục” card does reference the renewal-share formula.

## 2. Customers and products

**Original title:** Khách hàng và Sản phẩm  
**Workbook page:** Dashboard 2

The page contains customer tiers, age groups, a customer profile view, top product packages, and a quadrant comparing asset price and premium.

| View | Intended analytical use |
| --- | --- |
| Revenue by customer tier | Understand segment contribution |
| Revenue by age group | Explore differences in the observed customer mix |
| Top product packages | Identify products for further investigation |
| Asset-value/premium quadrant | Flag potential follow-up segments |

The quadrant uses comparisons with average asset price and average premium. It is a rule-based segmentation. A label such as “high risk” in that rule should not be interpreted as a validated underwriting or claims-risk model. An “upsell potential” label is likewise a hypothesis to assess, not a predicted purchase probability.

## 3. KPI and sales effectiveness

**Original title:** KPI và Hiệu quả bán hàng  
**Workbook page:** Dashboard 3

This page combines overall attainment, total KPI gap, department performance coverage, channel gaps, department rankings, and sales classification by contract volume and premium value.

Use it to separate three questions:

1. **How far are we from target?** Compare total actual performance with the corresponding total target.
2. **Where is the gap concentrated?** Examine department and channel comparisons at matching time and organizational scope.
3. **What kind of support might help?** Inspect volume/value groups as a starting point for a coaching discussion.

The sales classification compares employee-level contract count and premium revenue with reference averages. It is a descriptive segmentation, not an employee performance or causal assessment.

## Interaction and layout evidence

The workbook defines all three dashboards at a fixed **1366 × 768** layout. One explicit generated selection/highlight action is defined for the sales volume/value worksheet. Categorical filters and tooltips also appear in worksheet definitions.

These are configuration observations. A full interaction review still needs Tableau to check selection behavior, filter scope, navigation, text placement, and readability.

## Demonstration sequence for an authorized local review

- Open the original workbook in an environment authorized to access the competition data.
- Start with the business results page and state the period and metric definitions.
- Move to customers/products to explain a segmentation question.
- Finish with KPI performance and connect a gap to a proposed management follow-up.
- Check the metric and label issues listed in [Evidence](EVIDENCE.md) before recording a presentation.

No public workbook download or live Tableau link is included.
