[![DOI](https://zenodo.org/badge/1361227484.svg)](https://doi.org/10.5281/zenodo.22658600)

# InvariantFusion / InvariantRRF reproducibility package

This repository contains the six source notebooks and supporting scripts used
to reproduce the experiments associated with the current manuscript:

**InvariantFusion: Representation-Invariant Additive Rank Fusion with Exact Top-K Completion Certification**

The repository name `InvariantRRF` is retained for archival continuity with the
original release and Zenodo record. The current manuscript generalizes the
RRF-specific formulation to monotone non-negative additive rank fusion.


The workflow keeps the original frozen retrieval artifacts separate from later
closure and strengthening audits. Later notebooks consume verified artifacts
from earlier stages instead of silently retraining or regenerating them.

## Repository map

```text
notebooks/
  01_canonical_experiments.ipynb
  02_partial_observation_closure.ipynb
  03_splade_two_checkpoint_closure.ipynb
  04_nested_rrf_automc_audit.ipynb
  invariantrrf-informationfusion-strengthening-audit.ipynb
  invariantrrf-informationfusion-final-validation.ipynb
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

## Six-notebook run order

### 1. Canonical experiments

`notebooks/01_canonical_experiments.ipynb`

Run in a fresh Kaggle GPU session. It:

- trains the fixed 3-epoch `intfloat/e5-base-v2` checkpoint from official SciFact training qrels only;
- locks and strictly reloads the checkpoint before test judgments are used;
- generates dense top-1000 rankings for SciFact, TREC-COVID, FiQA and ArguAna;
- generates BM25 families and the fixed EnsembleDistil SPLADE runs used by the canonical study;
- runs the original MC-RRF scaling, perturbation, `k x K`, provenance-misspecification and StableRRF analyses;
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

Attach the canonical ZIP and the benchmark text/qrels bundle. This notebook
reuses frozen BM25 and EnsembleDistil rankings and generates only:

`naver/splade-cocondenser-selfdistil`

for SciFact and ArguAna. It writes:

`InvariantRRF_V43_SPLADE_TwoCheckpoint_Closure.zip`

No BM25 or EnsembleDistil regeneration is performed.

### 4. Nested-RRF + AutoMC audit

`notebooks/04_nested_rrf_automc_audit.ipynb`

Attach:

- the canonical ZIP from step 1;
- the SPLADE closure ZIP from step 3;
- the benchmark folders if qrels-aware nDCG drift is required.

This fusion-only notebook runs the original real-family nested-RRF replication
audit and the qrels-free AutoMC provenance-recovery/threshold-transfer audit.
It writes:

`InvariantRRF_V44_Novelty_Strengthening_Results.zip`

AutoMC remains exploratory and is not part of the current InvariantFusion
formal guarantee.

### 5. Information Fusion strengthening audit

`notebooks/invariantrrf-informationfusion-strengthening-audit.ipynb`

Attach:

- the canonical ZIP from step 1;
- the SPLADE closure ZIP from step 3;
- the same MPDR benchmark bundle.

This notebook is the first generalized InvariantFusion audit. It:

- tests exact-copy sensitivity across six additive rank kernels: RRF,
  inverse rank, inverse square root, exponential, logarithmic discount and
  Borda-style fusion;
- applies the fixed provenance-family budget construction across those kernels;
- evaluates controlled redundant-family growth and real BM25/SPLADE families;
- compares flat, family-budget, nested and min-max score-sum fusion;
- audits the SPLADE redundancy/complementarity boundary;
- performs an exhaustive-completion falsification test on sampled small states;
- optionally generates independent MiniLM and BGE-small retrieval runs on
  SciFact and ArguAna.

It writes:

`InvariantRRF_InformationFusion_Strengthening_Results.zip`

The optional MiniLM/BGE section needs model-download access and is most
convenient on a Kaggle GPU. Failure of that optional download section does not
invalidate the frozen-run structural audits.

### 6. Information Fusion final validation

`notebooks/invariantrrf-informationfusion-final-validation.ipynb`

Attach the same canonical ZIP, SPLADE closure ZIP and benchmark bundle. No
external model download is required.

This notebook performs the final property-focused validation used by the
current manuscript:

- replication of individual members inside already multi-member real BM25 and
  SPLADE families;
- six additive kernels;
- source depths 50 and 100;
- copied-member multiplicities 2, 4 and 8;
- flat, nested and representation-invariant family-budget fusion;
- systematic finite-state completion enumeration for the exact top-K
  certificate.

It writes:

`InvariantRRF_InformationFusion_Final_Validation_Results.zip`

The systematic certificate audit covers 25,056 deterministic states and
1,595,808 admissible completions across the six kernels, with the final run
reporting zero set/order certificate disagreements.

## Build the current manuscript figures

After the canonical, Information Fusion strengthening and final-validation
outputs are attached or copied under one directory:

```bash
python scripts/build_figures.py --input-root /path/to/notebook_outputs --output-dir figures
```

The script produces the three current primary figures:

- `Figure1_CrossKernel_ExactCopy.pdf`
- `Figure2_NestedReplication_AcrossKernels.pdf`
- `Figure3_Stable_DenseCap_Certification.pdf`

PNG fallbacks, figure-source CSV files, and a SHA-256 input manifest are also
written. Generated figures are excluded from Git by default.

## Verify the repository

```bash
python scripts/verify_repository.py
```

The verifier checks:

- exactly six source notebooks are present;
- notebook execution counts and saved outputs are stripped;
- account-specific private Kaggle paths are absent;
- the GPL license and software citation metadata are present.

## Installation

A practical local environment is:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The canonical and SPLADE-generation stages are GPU-oriented and were designed
for Kaggle. The partial-observation, nested, generalized fusion, and final
finite-state audits can run on CPU once their frozen inputs exist. The optional
MiniLM/BGE retrieval extension benefits from a GPU.

## Reproducibility policy

- No relevance labels are used to construct declared provenance families.
- AutoMC threshold selection is qrels-free and remains exploratory.
- The original RRF experiments keep `k=60` and output depth `K=10` unless a
  sensitivity analysis explicitly changes them.
- The current generalized method treats RRF as one instance of a monotone
  non-negative additive rank kernel.
- The designated RRF completion-certification baseline remains BM25 cap 1000
  and dense cap 100.
- Dense-cap 250/500/1000 analyses expose deeper prefixes of the same frozen
  dense top-1000 rankings.
- The SPLADE closure reuses canonical BM25 + EnsembleDistil and generates only
  SelfDistil.
- The two Information Fusion notebooks do not retrain or modify the frozen E5,
  BM25 or SPLADE source runs.
- Figure building is read-only with respect to experiment outputs.

See `docs/REPRODUCIBILITY.md` for the artifact chain and `docs/RESULTS.md` for
the manuscript-facing validation values.

## Large files

Model weights, generated ranked-list ZIPs, benchmark corpora, and generated
figures are intentionally excluded from Git. They are reproducible/downloadable
inputs or notebook outputs and can be attached as Kaggle notebook inputs. See
`.gitignore`, `data/README.md`, and `outputs/README.md`.

## Citation and archived releases

The DOI badge at the top points to the **Zenodo concept DOI** for this software
record, so it remains stable across repository versions:

`10.5281/zenodo.22658600`

See `CITATION.cff` for software citation metadata. For an exact experimental
snapshot, cite the version-specific Zenodo DOI associated with the release you
used.

If you use this implementation in academic work, please cite the associated
InvariantFusion paper and this repository where appropriate.

## License

Original code, scripts, and Jupyter notebooks in this repository are licensed
under **GPL-3.0-or-later**. See `LICENSE` and `NOTICE.md`.

Third-party datasets, pretrained models, libraries, and benchmark resources
remain subject to their original licenses and terms.
