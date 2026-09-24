# Reddit Sarcasm Detection

**Team NLP course project · RoBERTa · Feature fusion · Error analysis**

Classifying whether a Reddit comment is sarcastic using both the comment and its parent context. The project compares classical text classifiers, a fine-tuned RoBERTa baseline, and an experimental model with handcrafted features and bidirectional cross-attention.

**Main lesson:** in the team's reported experiment, the more complex architecture did not establish an F1 improvement over the RoBERTa baseline. Error analysis and evaluation design were as important as adding model components.

[Portfolio index](../README.md) · [Methods and evaluation](TECHNICAL_NOTES.md) · [Evidence and scope](EVIDENCE.md)

## The problem

Sarcasm can depend on the relationship between a reply and its context, rather than on an obvious keyword. Short replies, understated sarcasm, community-specific language, and references to outside knowledge can all make the binary decision difficult.

The task takes a parent comment and a reply as input and predicts sarcastic or non-sarcastic. The team used SARC, the Self-Annotated Reddit Corpus, for an academic experiment. Original comments and dataset files are not included in this portfolio.

## My contribution

I contributed to preprocessing and exploratory analysis, handcrafted linguistic features, fine-tuning RoBERTa, and error analysis as part of the team. The complete experiment and reported results are team work.

## Approaches compared

| Approach | Representation | Purpose |
| --- | --- | --- |
| TF-IDF + Logistic Regression | Unigrams and bigrams from context and comment | Establish a classical baseline |
| TF-IDF + Linear SVM | The same text representation | Compare another linear classifier |
| Fine-tuned RoBERTa | Context and comment encoded together as a text pair | Model contextual relationships |
| Feature Fusion + Cross-Attention | Separate passes through a shared RoBERTa encoder, bidirectional attention, pooling, and ten linguistic features | Test explicit interaction and feature fusion |

The reports describe preprocessing that preserves capitalization and punctuation, because these can carry useful stylistic cues. The handcrafted features cover overlap, sentiment, relative length, agreement and intensifier markers, capitalization, question marking, and polarity signals.

## Findings from the team report

- The fine-tuned RoBERTa baseline achieved stronger F1 than the classical baselines in the reported setting.
- The experimental architecture reduced false positives while increasing false negatives. Its F1 did not improve over the main baseline, and the reported bootstrap interval for the difference included zero.
- Remaining errors often involved understated sarcasm, very short replies, community language, outside knowledge, or ambiguous proxy labels.
- The report identified duplicate content and overlap in authors and communities across the splits. These limit what the experiment establishes about generalization to unseen users or domains.

These are qualitative summaries of the team's reported findings, not independently reproduced results. An interval containing zero does not establish that the models are equivalent. Original numerical results, error examples, and data-derived figures are not republished here.

## What this project demonstrates

The project connects baseline construction, representation design, fine-tuning, and error analysis. It also provides a concrete example of documenting a negative experimental result: adding attention and features did not demonstrate an F1 gain in the reported setup.

The next methodological steps described in the reports include component ablations, evaluation on unseen authors or communities, and out-of-domain testing. These remain follow-up work, not completed portfolio features.

## Available material

This is a documentation case study based on the supplied PDF presentation and Word report. No NLP training notebook, runnable source, checkpoint, or prediction file was supplied for verification in this review. The original `PYTHON_PJ.ipynb` belongs to the separate product recommendation project and is not evidence for this NLP experiment.

The public folder contains newly written documentation and an architecture schematic. Original datasets, comments, author identifiers, reports, screenshots, and model artifacts remain private.
