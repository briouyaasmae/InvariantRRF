# Generated figures

Run:

```bash
python scripts/build_figures.py --input-root /path/to/notebook-outputs --output-dir figures
```

The current script reads the canonical, Information Fusion strengthening, and
Information Fusion final-validation outputs and produces:

- `Figure1_CrossKernel_ExactCopy.pdf`
- `Figure2_NestedReplication_AcrossKernels.pdf`
- `Figure3_Stable_DenseCap_Certification.pdf`

PNG fallbacks are written alongside the PDFs. Figure-source CSV files and a
SHA-256 manifest of the input tables are written under `figures/source_data/`
and `figures/FIGURE_INPUT_MANIFEST.json`.

Generated figure files are ignored by Git so they can be recreated from the
frozen experiment outputs.
