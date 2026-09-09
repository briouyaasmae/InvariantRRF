# Generated outputs

This directory is intentionally empty in Git.

Recommended retained archives after running the six notebooks:

1. `InvariantRRF_Canonical_STRICT_DeepDense_TaskAdaptiveK_Results.zip`
2. `InvariantRRF_V43_PartialObservation_Closure.zip`
3. `InvariantRRF_V43_SPLADE_TwoCheckpoint_Closure.zip`
4. `InvariantRRF_V44_Novelty_Strengthening_Results.zip`
5. `InvariantRRF_InformationFusion_Strengthening_Results.zip`
6. `InvariantRRF_InformationFusion_Final_Validation_Results.zip`

Keep the canonical ZIP immutable once downstream notebooks have been run from
it. Its internal `RUN_MANIFEST.json` is the cross-notebook integrity anchor.

For the current InvariantFusion manuscript, the most important new audit
archives are items 5 and 6. They contain the cross-kernel/generalization tables,
real-family replication tests, optional architecture controls, and systematic
completion-certificate validation.

These large result ZIPs are excluded from Git. Archive the exact release
artifacts in Zenodo when creating the corresponding repository release.
