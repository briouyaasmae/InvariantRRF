# Reproducibility notes

## Primary constants

- RRF `k = 60`
- requested output `K = 10`
- canonical BM25 depth = 1000
- canonical dense generation depth = 1000
- designated StableRRF dense cap = 100
- StableRRF dense-cap sensitivity = 100, 250, 500, 1000
- SPLADE depth = 500 on SciFact and ArguAna
- MC-RRF source-count primary family size = 8
- primary perturbation = 5% candidate-preserving local swaps

## Dense checkpoint discipline

Notebook 01 trains `intfloat/e5-base-v2` using only official SciFact training qrels, for a fixed three epochs with seed 41. No validation/test metric is used for checkpoint selection. The final checkpoint is SHA-256 locked before test qrels are loaded and is strictly reloaded with the exact `TextEncoder` class.

The final audit checkpoint SHA-256 is:

`f3d7430db18124e6141652a990bf08a5499c85428340bc8a4fcfe379c83acea4`

The same checkpoint generates dense top-1000 rankings for all four datasets. Shallower dense caps are literal prefixes.

## Canonical artifact contract

The final canonical ZIP contains `RUN_MANIFEST.json`. Downstream notebooks verify source hashes before using the runs. Do not mix files from separate canonical executions.

Important run names include:

- `<Dataset>_dense_STRICT_top1000.json`
- `<Dataset>_bm25_top1000.json`
- SciFact/ArguAna `<Dataset>_splade_ensemble_top500.json`
- `SciFact_dense_STRICT_top100.json`

## SPLADE closure

Notebook 03 reuses the exact canonical BM25 and EnsembleDistil files and generates only `naver/splade-cocondenser-selfdistil`. Its closure package records source hashes and corrected statistics.

## Nested-RRF / AutoMC audit

Notebook 04 is fusion-only. The nested baseline uses ordinary RRF within a real family, then ordinary RRF again across the family consensus and outside sources. Each member is copied once in turn and methods are compared against their own pre-copy outputs.

AutoMC groups inputs using finite-prefix RBO connected components. Threshold selection never uses qrels. Qrels are read only afterward to quantify absolute nDCG@10 differences from declared MC-RRF.

## Figure generation

`scripts/build_figures.py` reads only notebook output tables. It does not train or retrieve. Guards protect the final corrected SPLADE values, the 13-condition nested audit, the qrels-aware nDCG drift output, and monotone StableRRF dense-cap certification.
