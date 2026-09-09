# Manuscript-facing validation values

These values are an audit index. CSV/JSON outputs produced by the notebooks
remain the machine-readable source of truth.

## 1. Generalized exact-copy audit

Across four datasets, two attacked source types and six additive rank kernels,
ordinary additive fusion is representation-count sensitive while RIAF is
exact-copy invariant in all 48 dataset/kernel/source conditions.

Macro exact top-10 set preservation after one exact copy:

| Kernel | Ordinary additive fusion | RIAF |
|---|---:|---:|
| Borda | 0.1420 | 1.0000 |
| Exponential | 0.0544 | 1.0000 |
| Inverse rank | 0.0708 | 1.0000 |
| Inverse square root | 0.0651 | 1.0000 |
| Log discount | 0.0731 | 1.0000 |
| RRF60 | 0.1209 | 1.0000 |

All six kernels exhibit an ordinary-fusion ordered-top-10 failure in at least
one dataset/source condition.

## 2. Controlled redundant-family scaling across kernels

At family size 8 under the 5% candidate-preserving perturbation:

| Kernel | Ordinary set | RIAF set | Ordinary abs. nDCG drift | RIAF abs. drift |
|---|---:|---:|---:|---:|
| Borda | 0.0195 | 0.8846 | 0.1033 | 0.0053 |
| Exponential | 0.0119 | 0.9169 | 0.1232 | 0.0054 |
| Inverse rank | 0.0110 | 0.9225 | 0.1073 | 0.0087 |
| Inverse square root | 0.0114 | 0.9290 | 0.1253 | 0.0061 |
| Log discount | 0.0120 | 0.9080 | 0.1215 | 0.0064 |
| RRF60 | 0.0173 | 0.9311 | 0.1122 | 0.0050 |

Nested fusion is an important empirical mitigation on these highly redundant
synthetic families, but the real-family replication audit below shows that it
is not an exact invariance mechanism.

## 3. Real-family nested replication audit across kernels

Notebook 06 evaluates 468 real-family/kernel/depth/copy conditions. RIAF
preserves both ordered top-10 and top-10 membership exactly in every condition,
with zero nDCG drift from its own pre-copy output.

For RRF60 at depth 50:

| Copied-member multiplicity | Flat set preservation | Nested set preservation | RIAF set preservation |
|---:|---:|---:|---:|
| 2 | 0.5545 | 0.7536 | 1.0000 |
| 4 | 0.2761 | 0.6047 | 1.0000 |
| 8 | 0.1467 | 0.5571 | 1.0000 |

For every one of the six kernels at both tested depths, all 39 grouped
real-family attack conditions contain nested ordered and set preservation
failures. Thus hierarchical fusion attenuates source-count sensitivity without
providing exact replication invariance.

## 4. Exact Completion Certification finite-state audit

Systematic finite-state validation uses a four-document universe, two sources,
prefix lengths one/two, weights `{0.5, 1, 2}`, `K` in `{1, 2}`, and all six
additive kernels.

- deterministic states: **25,056**;
- admissible completion evaluations: **1,595,808**;
- set false positives: **0**;
- set false negatives: **0**;
- order false positives: **0**;
- order false negatives: **0**.

Each kernel contributes 4,176 states and 265,968 completion evaluations.

## 5. Real-family relevance boundary

The SPLADE checkpoint family confirms that representation invariance is not a
universal relevance objective.

| Dataset | Mean RBO | Ordinary set | Fixed-budget set | Ordinary delta nDCG | Fixed-budget delta nDCG |
|---|---:|---:|---:|---:|---:|
| SciFact | 0.797 | 0.257 | 0.393 | +0.0001 | -0.0007 |
| ArguAna | 0.882 | 0.392 | 0.640 | +0.0073 | -0.0019 |

On ArguAna, the additional related SPLADE checkpoint improves ordinary-fusion
nDCG, showing that shared provenance and useless redundancy are not equivalent.

## 6. Additional retrieval architectures

The optional architecture-control runs completed successfully:

- SciFact MiniLM nDCG@10: **0.6451**;
- SciFact BGE-small nDCG@10: **0.7127**;
- ArguAna MiniLM nDCG@10: **0.3712**;
- ArguAna BGE-small nDCG@10: **0.4359**.

Adding the source as a genuinely distinct RRF input to BM25+dense changes
nDCG@10 by:

- SciFact + MiniLM: **-0.0081**;
- SciFact + BGE-small: **+0.0123**;
- ArguAna + MiniLM: **+0.0144**;
- ArguAna + BGE-small: **+0.0352**.

These controls show that InvariantFusion does not imply suppressing genuinely
distinct evidence sources.

## 7. RRF completion-certification application

Designated BM25-1000/dense-100 ordered top-10 certification:

- SciFact: **29.3%**;
- TREC-COVID: **2.0%**;
- FiQA: **21.9%**;
- ArguAna: **76.2%**.

At dense cap 1000 with fixed RRF `k=60`:

- SciFact: **83.0%**;
- TREC-COVID: **48.0%**;
- FiQA: **77.2%**;
- ArguAna: **84.1%**.

These are application-level certification rates. The general ECC correctness
claim is the analytical result plus the finite-state falsification audit above.

## 8. Exploratory AutoMC result

AutoMC remains an exploratory provenance-inference audit rather than a current
InvariantFusion contribution. At depth 50 its selected global RBO threshold is
0.75, macro exact partition recovery is 0.541, and macro pairwise family F1 is
0.722. The formal method therefore keeps provenance declaration as an explicit
input.
