# Data and pretrained-model inputs

Large benchmark corpora and model weights are not committed to Git.

## Public resources used by the notebooks

- BEIR benchmark collections: SciFact, TREC-COVID, FiQA, ArguAna.
- Dense initialization: `intfloat/e5-base-v2`.
- SPLADE EnsembleDistil: `naver/splade-cocondenser-ensembledistil`.
- SPLADE SelfDistil closure: `naver/splade-cocondenser-selfdistil`.

Notebook 01 downloads the SciFact Hugging Face data needed for the leakage-clean train/test split. For the four-dataset canonical rerun it also expects the prepared MPDR-form benchmark bundle used by the original audit, with the following directory names somewhere under the attached input root:

```text
mpdr/data/
  scifact_mpdr/dev/{queries.jsonl,docs.jsonl,qrels.tsv}
  trec-covid_mpdr/dev/{queries.jsonl,docs.jsonl,qrels.tsv}
  fiqa_mpdr/dev/{queries.jsonl,docs.jsonl,qrels.tsv}
  arguana_mpdr/dev/{queries.jsonl,docs.jsonl,qrels.tsv}
```

The repository notebooks recursively discover this layout under `/kaggle/input`, so no user-specific Kaggle path is required.

The final aligned evaluation query counts are 300, 50, 648 and 1401 respectively. The ArguAna audit uses the inherited 1401-query qrel-aligned subset consistently across all methods.
