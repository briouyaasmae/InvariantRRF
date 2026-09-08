# Generated figures

Run:

```bash
python scripts/build_figures.py --input-root /path/to/four-notebook-outputs --output-dir figures
```

The script produces the three primary figure files:

- `Figure1_MC_RRF_SetPreservation.pdf`
- `Figure2_NestedRRF_ReplicationAudit.pdf`
- `Figure3_StableRRF_DenseCap_Certification.pdf`

It also writes PNG fallbacks, diagnostic figures, figure-source CSVs, and a
SHA-256 input manifest. Generated figure files are ignored by Git so they can
be recreated from the frozen experiment outputs.
