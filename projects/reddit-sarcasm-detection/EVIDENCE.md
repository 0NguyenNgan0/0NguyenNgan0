# Evidence and scope

The source materials are two presentations of the same team project: `NLP PJ.pdf` and `Report.docx`. They were inspected privately and are not attached to this public folder. PDF page references count from the first page; Word references use section numbers from the report.

| Portfolio statement | Source inspected | Evidence boundary |
| --- | --- | --- |
| Reddit sarcasm classification using context and comment | PDF pages 1 and 4; Word sections 1–2 | Task and academic project identity |
| Preprocessing and split audit | PDF pages 5–6; Word sections 2–4 | Reported workflow; no code-level leakage audit performed here |
| Ten handcrafted features | PDF page 8; Word section 5 | Feature names and stated meaning, not verified extractor implementation |
| TF-IDF and RoBERTa baselines | PDF pages 11–13; Word sections 6–7 | Reported models and configurations |
| Shared encoder, fusion, and cross-attention | PDF page 18; Word section 9 | Documented architecture, not a reproduced training run |
| No demonstrated F1 improvement from the experimental model | PDF pages 20 and 23; Word sections 9 and 11–12 | Team-reported comparison and uncertainty; numerical results remain private |
| Error categories and interpretation | PDF pages 15–16 and 21; Word sections 8 and 10 | Qualitative analysis, not causal attribution |
| Validation-based threshold selection | Word section 7.4 | Described procedure; predictions unavailable for verification |
| Generalization limits and proposed follow-up | PDF pages 24–25; Word sections 12–14 | Explicitly unfinished ablation and out-of-domain work |
| My personal contribution | Participant-confirmed scope | Preprocessing/EDA, handcrafted features, RoBERTa fine-tuning, and error analysis within the team |

## Review performed

The PDF text and Word document text/tables were read, and the PDF architecture and comparison pages were visually inspected. The case study uses the reported architecture and qualitative conclusions while keeping personal contribution separate from the full team output.

Some slide phrasing is clarified in the new notes: baseline RoBERTa uses self-attention over the paired input, and a confidence interval containing zero is not evidence of model equivalence. The reported random-split result is not treated as a formal upper bound on all future performance.

No NLP source notebook, checkpoint, original dataset, or prediction-level output was provided for this review. The experiment, statistics, and trained model were not rerun. The separate recommender project's CI does not validate this NLP case study.

## Publication boundary

Only new explanatory Markdown and a redrawn architecture schematic are published. Original reports, raw or processed comments, author identifiers, student identifiers, screenshots, data-derived charts, numeric benchmark tables, model weights, and prediction files are excluded.

The project is attributed to the team. The personal contribution statement does not imply sole ownership of the complete pipeline or a leadership title.
