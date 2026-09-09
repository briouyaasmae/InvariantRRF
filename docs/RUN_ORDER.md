# Run order and artifact dependency graph

```text
01_canonical_experiments.ipynb
  |
  +--> InvariantRRF_Canonical_STRICT_DeepDense_TaskAdaptiveK_Results.zip
        |
        +--> 02_partial_observation_closure.ipynb
        |      \--> InvariantRRF_V43_PartialObservation_Closure.zip
        |
        +--> 03_splade_two_checkpoint_closure.ipynb
               \--> InvariantRRF_V43_SPLADE_TwoCheckpoint_Closure.zip
                      |
                      +--> 04_nested_rrf_automc_audit.ipynb

Canonical ZIP + SPLADE closure ZIP + benchmark bundle
  |
  +--> invariantrrf-informationfusion-strengthening-audit.ipynb
  |      \--> InvariantRRF_InformationFusion_Strengthening_Results.zip
  |
  +--> invariantrrf-informationfusion-final-validation.ipynb
         \--> InvariantRRF_InformationFusion_Final_Validation_Results.zip

Canonical + Information Fusion strengthening + final-validation outputs
  \--> scripts/build_figures.py
         \--> figures/Figure1..Figure3 + figure-source CSVs
```

## Why the order matters

The original closure/audit stages consume frozen canonical ranking artifacts
rather than regenerate them with different checkpoints or cutoffs.

- Notebook 02 performs no retriever inference.
- Notebook 03 regenerates only SelfDistil SPLADE.
- Notebook 04 performs fusion-only analyses and may read qrels only for post-hoc nDCG differences.
- Notebook 05 generalizes the representation-count audit to six additive rank kernels and optionally generates MiniLM/BGE architecture controls.
- Notebook 06 is a property-focused final validation. It uses the canonical and SPLADE frozen runs directly and does not depend on notebook 05 output.
- Notebook 06 performs no external model download.

The two Information Fusion notebooks are additive validation stages. They do
not alter the immutable canonical retrieval artifacts.
