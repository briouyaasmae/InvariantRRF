# Paper-facing closure values

These values are included as an audit index. The CSV/JSON outputs produced by the notebooks remain the machine-readable source of truth.

## MC-RRF primary source-count scaling

Designated condition: family size 8, mild 5% candidate-preserving perturbation, source depth 100, `k=60`, `K=10`.

- MC-RRF lower absolute nDCG@10 drift: **8/8** dataset-by-attacked-source conditions.
- MC-RRF higher exact set preservation: **8/8**.
- Holm-significant drift reductions: **8/8**.
- Macro absolute-drift reduction: **0.108236**.
- Macro set-preservation gain: **0.930789**.
- Ordinary set preservation range: **0.0000-0.0735**.
- MC-RRF set preservation range: **0.9000-0.9829**.

## Nested-RRF replication audit

At depth 50 over 13 real-family dataset-by-copied-member conditions:

| Method | Ordered top-10 preservation | Set preservation | Top-1 preservation | Mean abs. nDCG@10 drift |
|---|---:|---:|---:|---:|
| Flat ordinary RRF | 10.1% | 55.5% | 96.7% | 0.0133 |
| Plain nested RRF | 41.2% | 75.4% | 97.9% | 0.0062 |
| MC-RRF | 100% | 100% | 100% | 0.0000 |

Plain nested RRF fails perfect ordered and set replication preservation in **13/13** conditions. MC-RRF is exactly invariant in all 13.

## AutoMC provenance recovery

Depth 50, qrels-free threshold selection:

- selected global RBO threshold: **0.75**;
- macro exact partition recovery: **0.541**;
- macro pairwise family F1: **0.722**;
- macro top-10 set agreement with declared MC-RRF: **0.671**;
- per-dataset/scenario qrels-free optima span **0.50-0.80**;
- FiQA leave-one-dataset-out transfer: exact recovery **0.113**, set agreement **0.140**, mean absolute nDCG@10 difference **0.0619**.

## Corrected SPLADE two-checkpoint closure

| Dataset | Mean RBO | Ord. set | MC set | Ord. delta | MC delta | MC-Ord. | 95% CI | Holm p |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| SciFact | 0.797 | 0.257 | 0.393 | +0.0001 | -0.0007 | -0.0008 | [-0.0100,+0.0083] | 1.000 |
| ArguAna | 0.882 | 0.392 | 0.640 | +0.0073 | -0.0019 | -0.0092 | [-0.0126,-0.0059] | 1.33e-8 |

The ArguAna values above are the final closure values. Older 39.0/64.2 variants and the older delta/p-value combination are not authoritative.

## StableRRF

Designated BM25-1000/dense-100 baseline, ordered top-10 certification:

- SciFact: **29.3%**
- TREC-COVID: **2.0%**
- FiQA: **21.9%**
- ArguAna: **76.2%**

At dense cap 1000 with fixed `k=60`:

- SciFact: **83.0%**
- TREC-COVID: **48.0%**
- FiQA: **77.2%**
- ArguAna: **84.1%**

## Partial-observation descriptive reproduction

BM25+dense ordered top-10 reproduction against the deepest generated reference:

| Dataset | depth 50 | depth 100 |
|---|---:|---:|
| SciFact | 20.3% | 46.0% |
| TREC-COVID | 4.0% | 20.0% |
| FiQA | 12.5% | 38.3% |
| ArguAna | 80.1% | 94.3% |

These are empirical reproduction rates, not StableRRF certificates.
