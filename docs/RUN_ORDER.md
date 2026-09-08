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

All four output families
  \--> scripts/build_figures.py
         \--> figures/Figure1..Figure3 + supplementary figures
```

## Why the order matters

The later notebooks are closure/audit stages. They must consume the frozen canonical ranking artifacts rather than regenerate them with different checkpoints or cutoffs.

- Notebook 02 performs no retriever inference.
- Notebook 03 regenerates only SelfDistil SPLADE.
- Notebook 04 performs fusion-only analyses and may read qrels only for post-hoc nDCG differences.
