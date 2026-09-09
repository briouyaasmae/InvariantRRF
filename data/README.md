# Data and pretrained-model inputs

Large benchmark corpora and model weights are not committed to Git.

## Public resources used by the notebooks

- BEIR benchmark collections: SciFact, TREC-COVID, FiQA, ArguAna.
- Canonical dense initialization: `intfloat/e5-base-v2`.
- SPLADE EnsembleDistil: `naver/splade-cocondenser-ensembledistil`.
- SPLADE SelfDistil closure: `naver/splade-cocondenser-selfdistil`.
- Optional architecture control: `sentence-transformers/all-MiniLM-L6-v2`.
- Optional architecture control: `BAAI/bge-small-en-v1.5`.

Notebook 01 downloads the SciFact Hugging Face data needed for the leakage-clean
train/test split. For the four-dataset canonical rerun it also expects the
prepared MPDR-form benchmark bundle used by the original audit, with the
following directory names somewhere under the attached input root:

```text
mpdr/data/
  scifact_mpdr/dev/{queries.jsonl,docs.jsonl,qrels.tsv}
  trec-covid_mpdr/dev/{queries.jsonl,docs.jsonl,qrels.tsv}
  fiqa_mpdr/dev/{queries.jsonl,docs.jsonl,qrels.tsv}
  arguana_mpdr/dev/{queries.jsonl,docs.jsonl,qrels.tsv}
```

The repository notebooks recursively discover this layout under `/kaggle/input`,
so no user-specific Kaggle path is required.

The final aligned evaluation query counts are 300, 50, 648 and 1401,
respectively. The ArguAna audit uses the inherited 1401-query qrel-aligned
subset consistently across all methods.

## Which notebooks need benchmark text?

- Notebook 01: benchmark bundle required for the canonical four-dataset run.
- Notebook 02: consumes the canonical artifact; no retriever inference.
- Notebook 03: needs benchmark text for SelfDistil SPLADE generation.
- Notebook 04: benchmark qrels are needed only for qrels-aware post-hoc metrics.
- Notebook 05: needs the benchmark bundle; optional MiniLM/BGE generation also
  needs model-download access.
- Notebook 06: needs the benchmark qrels plus frozen canonical/SPLADE archives;
  no new model download is required.
