[![DOI](https://zenodo.org/badge/1361227484.svg)](https://doi.org/10.5281/zenodo.22658600)
# InvariantRRF reproducibility package

This repository contains the four source notebooks and supporting scripts used
to reproduce the experiments associated with:

**Representation-Reliable Reciprocal Rank Fusion: Provenance Mass Conservation and Exact Top-K Certification**

The package is code- and reproducibility-focused.

The repository separates the primary canonical rerun from three targeted
closure/audit notebooks. Later notebooks consume frozen artifacts from earlier
notebooks rather than silently regenerating them.

## Repository map

```text
notebooks/
  01_canonical_experiments.ipynb
  02_partial_observation_closure.ipynb
  03_splade_two_checkpoint_closure.ipynb
  04_nested_rrf_automc_audit.ipynb
scripts/
  build_figures.py
  verify_repository.py
docs/
  RUN_ORDER.md
  RESULTS.md
  REPRODUCIBILITY.md
data/
  README.md
outputs/
  README.md
figures/
  README.md
LICENSE
NOTICE.md
CITATION.cff
requirements.txt
Makefile
```

## Four-notebook run order

### 1. Canonical experiments

`notebooks/01_canonical_experiments.ipynb`

Run in a fresh Kaggle GPU session. It:

- trains the fixed 3-epoch `intfloat/e5-base-v2` checkpoint from official SciFact training qrels only;
- locks and strictly reloads the checkpoint before test judgments are used;
- generates dense top-1000 rankings for SciFact, TREC-COVID, FiQA and ArguAna;
- generates BM25 families and the fixed EnsembleDistil SPLADE runs used by the canonical study;
- runs MC-RRF scaling, perturbation, `k x K`, provenance-misspecification and StableRRF analyses;
- writes `RUN_MANIFEST.json` and SHA-256 hashes.

Use the final archive:

`InvariantRRF_Canonical_STRICT_DeepDense_TaskAdaptiveK_Results.zip`

The canonical notebook also expects the prepared MPDR-form benchmark bundle
used in the audit. See `data/README.md`.

### 2. Partial-observation closure

`notebooks/02_partial_observation_closure.ipynb`

CPU is sufficient. Attach the canonical ZIP from step 1. The notebook
auto-discovers it, verifies the frozen runs, and writes:

`InvariantRRF_V43_PartialObservation_Closure.zip`

No retraining or retriever inference is performed.

### 3. SPLADE two-checkpoint closure

`notebooks/03_splade_two_checkpoint_closure.ipynb`

Attach the same canonical ZIP and the benchmark text/qrels bundle. This
notebook reuses frozen BM25 and EnsembleDistil rankings and generates only:

`naver/splade-cocondenser-selfdistil`

for SciFact and ArguAna. It writes the corrected two-checkpoint closure
package. No BM25 or EnsembleDistil regeneration is performed.

### 4. Nested-RRF + AutoMC audit

`notebooks/04_nested_rrf_automc_audit.ipynb`

Attach:

- the canonical ZIP from step 1;
- the SPLADE closure ZIP from step 3;
- the benchmark folders if qrels-aware nDCG drift is required.

This fusion-only notebook runs the real-family nested-RRF replication audit
and the qrels-free AutoMC provenance-recovery/threshold-transfer audit.

## Build figures from the frozen outputs

After the four notebook outputs are attached or copied under one directory:

```bash
python scripts/build_figures.py --input-root /path/to/notebook_outputs --output-dir figures
```

The script produces these three primary figure files:

- `Figure1_MC_RRF_SetPreservation.pdf`
- `Figure2_NestedRRF_ReplicationAudit.pdf`
- `Figure3_StableRRF_DenseCap_Certification.pdf`

It also writes PNG fallbacks, diagnostic figures, figure-source CSVs, and a
SHA-256 input manifest. Generated figure files are excluded from Git by
default and can be regenerated from the experiment outputs.

## Verify the repository

```bash
python scripts/verify_repository.py
```

The verifier checks:

- exactly four source notebooks are present;
- notebook execution counts and outputs are stripped;
- account-specific private Kaggle paths are absent;
- the GPL license and software citation metadata are present.

## Installation

A practical local environment is:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The canonical and SPLADE notebooks are GPU-oriented and were designed for
Kaggle. The closure and fusion-only audits can run on CPU once their frozen
inputs exist.

## Reproducibility policy

- No relevance labels are used to construct provenance families or select the AutoMC threshold.
- The primary RRF constant remains `k=60` and output depth `K=10`.
- The designated StableRRF baseline remains BM25 cap 1000 and dense cap 100.
- Dense-cap 250/500/1000 analyses expose deeper prefixes of the same frozen dense top-1000 rankings.
- The SPLADE closure reuses canonical BM25 + EnsembleDistil and generates only SelfDistil.
- Figure building is read-only with respect to all four experiment outputs.

See `docs/REPRODUCIBILITY.md` for the artifact chain and `docs/RESULTS.md` for
the paper-facing closure values.

## Large files

Model weights, generated ranked-list ZIPs, benchmark corpora, and generated
figures are intentionally excluded from Git. They are reproducible/downloadable
inputs or notebook outputs and can be attached as Kaggle notebook inputs. See
`.gitignore` and `data/README.md`.

## Citation

See `CITATION.cff`. If you use this implementation in academic work, please
cite the associated InvariantRRF paper and the repository where appropriate.

## License

Original code, scripts, and Jupyter notebooks in this repository are licensed
under **GPL-3.0-or-later**. See `LICENSE` and `NOTICE.md`.

Third-party datasets, pretrained models, libraries, and benchmark resources
remain subject to their original licenses and terms.
