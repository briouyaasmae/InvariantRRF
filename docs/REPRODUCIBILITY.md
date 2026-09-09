# Reproducibility notes

## Current methodological scope

The original repository was built around MC-RRF and StableRRF. The current
InvariantFusion manuscript generalizes those ideas to a monotone non-negative
additive rank-fusion class.

- **RIAF**: Representation-Invariant Additive Fusion. Authority is attached to
  declared provenance families and distinct ranking classes rather than to the
  physical number of supplied copies.
- **ECC**: Exact Completion Certification. Tight score extrema over an open-tail
  completion model determine whether strict top-K membership or order is fixed.

RRF remains one important kernel instance and the original RRF-specific
artifacts remain frozen for auditability.

## Primary constants inherited from the canonical RRF study

- RRF `k = 60`
- requested output `K = 10`
- canonical BM25 depth = 1000
- canonical dense generation depth = 1000
- designated RRF completion-certification dense cap = 100
- dense-cap sensitivity = 100, 250, 500, 1000
- SPLADE depth = 500 on SciFact and ArguAna
- original source-count primary family size = 8
- original primary perturbation = 5% candidate-preserving local swaps

## Dense checkpoint discipline

Notebook 01 trains `intfloat/e5-base-v2` using only official SciFact training
qrels, for a fixed three epochs with seed 41. No validation/test metric is used
for checkpoint selection. The final checkpoint is SHA-256 locked before test
qrels are loaded and is strictly reloaded with the exact `TextEncoder` class.

The final audit checkpoint SHA-256 is:

`f3d7430db18124e6141652a990bf08a5499c85428340bc8a4fcfe379c83acea4`

The same checkpoint generates dense top-1000 rankings for all four datasets.
Shallower dense caps are literal prefixes.

## Canonical artifact contract

The canonical ZIP contains `RUN_MANIFEST.json`. Downstream notebooks verify
source hashes before using the runs. Do not mix files from separate canonical
executions.

Important run names include:

- `<Dataset>_dense_STRICT_top1000.json`
- `<Dataset>_bm25_top1000.json`
- SciFact/ArguAna `<Dataset>_splade_ensemble_top500.json`
- `SciFact_dense_STRICT_top100.json`

## SPLADE closure

Notebook 03 reuses the exact canonical BM25 and EnsembleDistil files and
generates only `naver/splade-cocondenser-selfdistil`. Its closure package
records source hashes and corrected statistics.

## Nested-RRF / AutoMC audit

Notebook 04 is fusion-only. The nested baseline uses ordinary RRF within a real
family, then ordinary RRF again across the family consensus and outside
sources. Each member is copied once in turn and methods are compared against
their own pre-copy outputs.

AutoMC groups inputs using finite-prefix RBO connected components. Threshold
selection never uses qrels. Qrels are read only afterward to quantify nDCG
behavior. AutoMC is exploratory and is not part of the current formal method.

## Information Fusion strengthening audit

Notebook 05 verifies that representation-count sensitivity is not specific to
RRF. It evaluates six additive rank kernels:

- normalized RRF60;
- inverse rank;
- inverse square root;
- exponential decay;
- logarithmic discount;
- Borda-style linear decay.

The same fixed-family-budget construction is tested without using qrels to
form provenance families. Real-family controls use BM25 parameter variants and
SPLADE EnsembleDistil/SelfDistil checkpoints. Min-max score-sum fusion is
included as a score-based control.

The optional architecture extension generates `all-MiniLM-L6-v2` and
`BAAI/bge-small-en-v1.5` runs on SciFact and ArguAna. Those rankers are treated
as genuinely distinct sources, not as members of one provenance family.

## Information Fusion final validation

Notebook 06 duplicates individual members inside already multi-member real
families. It crosses:

- 5 real family scenarios;
- 6 additive kernels;
- depths 50 and 100;
- copied-member multiplicities 2, 4 and 8.

The resulting 468 summary conditions compare flat additive fusion, nested
fusion and the representation-invariant family-budget construction against
each method's own pre-copy output.

The same notebook performs a deterministic finite-state audit of ECC using:

- a four-document universe;
- two sources;
- prefix lengths one or two;
- source weights in `{0.5, 1, 2}`;
- `K` in `{1, 2}`;
- all six kernels;
- every admissible ordered tail completion for each retained state.

The final run contains 25,056 states and 1,595,808 completion evaluations and
reports zero set/order certificate disagreements. This is finite verification,
not a substitute for the analytical proof in the manuscript.

## Figure generation

`scripts/build_figures.py` reads only frozen output tables. It does not train or
retrieve. The current primary figures use:

- `generalized_exact_copy_audit.csv` from notebook 05;
- `nested_replication_per_query.csv` from notebook 06;
- `secondary_stable_dense_cap_summary.csv` from notebook 01.

Input SHA-256 hashes are recorded in `figures/FIGURE_INPUT_MANIFEST.json` when
the script is run.
