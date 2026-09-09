#!/usr/bin/env python3
"""Build the three primary InvariantFusion manuscript figures from frozen outputs.

No retrieval is rerun. The script searches direct files and ZIP members beneath
--input-root for the paper-facing CSV artifacts produced by notebook 01,
notebook 05, and notebook 06.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import zipfile

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

TARGETS = {
    "exact_copy": (
        "generalized_exact_copy_audit.csv",
        ("informationfusion", "strengthening"),
    ),
    "nested_replication": (
        "nested_replication_per_query.csv",
        ("informationfusion", "final", "validation"),
    ),
    "stable_dense_caps": (
        "secondary_stable_dense_cap_summary.csv",
        ("canonical", "deepdense", "taskadaptivek"),
    ),
}

DATASET_ORDER = ["SciFact", "TREC-COVID", "FiQA", "ArguAna"]
KERNEL_ORDER = [
    "borda",
    "exp20",
    "inverse_rank",
    "inverse_sqrt",
    "log_discount",
    "rrf60",
]
KERNEL_LABELS = {
    "borda": "Borda",
    "exp20": "Exponential",
    "inverse_rank": "Inverse rank",
    "inverse_sqrt": "Inverse sqrt",
    "log_discount": "Log discount",
    "rrf60": "RRF",
}


def sha256_file(path, chunk=1024 * 1024):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        while True:
            block = f.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def score_path(path, hints):
    s = str(path).lower()
    return sum(1 for h in hints if h.lower() in s)


def locate_artifact(input_root, cache, basename, hints=()):
    direct = list(input_root.rglob(basename)) if input_root.exists() else []
    if direct:
        direct.sort(key=lambda p: (score_path(p, hints), -len(str(p))), reverse=True)
        return direct[0], "direct"

    hits = []
    for zp in list(input_root.rglob("*.zip")) if input_root.exists() else []:
        try:
            with zipfile.ZipFile(zp, "r") as zf:
                for member in zf.namelist():
                    if Path(member).name == basename:
                        score = score_path(zp, hints) + score_path(member, hints)
                        hits.append((score, str(zp), member, zp))
        except zipfile.BadZipFile:
            continue

    if not hits:
        raise FileNotFoundError(f"Could not find {basename} under {input_root}")

    hits.sort(reverse=True)
    _, _, member, zp = hits[0]
    token = hashlib.sha256((str(zp) + "::" + member).encode()).hexdigest()[:10]
    dest = cache / f"{token}_{basename}"
    with zipfile.ZipFile(zp, "r") as zf, zf.open(member) as src, dest.open("wb") as dst:
        shutil.copyfileobj(src, dst)
    return dest, f"zip:{zp.name}:{member}"


def save(fig, base):
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".png"), dpi=300, bbox_inches="tight")
    plt.close(fig)


def build_figure1(exact_df, out, srcdir):
    required = {
        "kernel",
        "ordinary_set_preservation",
        "family_budget_set_preservation",
    }
    missing = required - set(exact_df.columns)
    if missing:
        raise AssertionError(f"Figure 1 input missing columns: {sorted(missing)}")

    assert set(KERNEL_ORDER).issubset(set(exact_df["kernel"]))
    assert np.allclose(exact_df["family_budget_set_preservation"], 1.0)

    f1 = (
        exact_df.groupby("kernel", as_index=False)
        .agg(
            ordinary=("ordinary_set_preservation", "mean"),
            riaf=("family_budget_set_preservation", "mean"),
        )
        .set_index("kernel")
        .loc[KERNEL_ORDER]
        .reset_index()
    )
    f1["label"] = f1["kernel"].map(KERNEL_LABELS)
    f1.to_csv(srcdir / "Figure1_CrossKernel_ExactCopy.csv", index=False)

    x = np.arange(len(f1))
    width = 0.36
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    ax.bar(x - width / 2, f1["ordinary"], width=width, label="Ordinary additive fusion")
    ax.bar(x + width / 2, f1["riaf"], width=width, label="RIAF")
    ax.set_xticks(x)
    ax.set_xticklabels(f1["label"], rotation=20, ha="right")
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("Exact top-10 set preservation")
    ax.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.22))
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    save(fig, out / "Figure1_CrossKernel_ExactCopy")


def build_figure2(nested_df, out, srcdir):
    required = {
        "total_attacked_multiplicity",
        "flat_set_preserved",
        "nested_set_preserved",
        "family_budget_set_preserved",
    }
    missing = required - set(nested_df.columns)
    if missing:
        raise AssertionError(f"Figure 2 input missing columns: {sorted(missing)}")

    assert set(nested_df["total_attacked_multiplicity"].astype(int)) >= {2, 4, 8}
    assert np.allclose(nested_df["family_budget_set_preserved"], 1.0)

    f2 = (
        nested_df.groupby("total_attacked_multiplicity", as_index=False)
        .agg(
            flat=("flat_set_preserved", "mean"),
            nested=("nested_set_preserved", "mean"),
            riaf=("family_budget_set_preserved", "mean"),
        )
        .sort_values("total_attacked_multiplicity")
    )
    f2.to_csv(srcdir / "Figure2_NestedReplication_AcrossKernels.csv", index=False)

    x = f2["total_attacked_multiplicity"].to_numpy(int)
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    ax.plot(x, f2["flat"], marker="o", linewidth=1.8, label="Flat additive fusion")
    ax.plot(x, f2["nested"], marker="s", linewidth=1.8, label="Nested fusion")
    ax.plot(x, f2["riaf"], marker="^", linewidth=1.8, label="RIAF")
    ax.set_xticks([2, 4, 8])
    ax.set_ylim(0, 1.08)
    ax.set_xlabel("Multiplicity of the copied family member")
    ax.set_ylabel("Exact top-10 set preservation")
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.22))
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    save(fig, out / "Figure2_NestedReplication_AcrossKernels")


def build_figure3(stable_df, out, srcdir):
    required = {"dataset", "dense_cap", "order_cert_rate"}
    missing = required - set(stable_df.columns)
    if missing:
        raise AssertionError(f"Figure 3 input missing columns: {sorted(missing)}")

    f3 = stable_df[stable_df["dense_cap"].astype(int).isin([100, 250, 500, 1000])].copy()
    f3["dataset"] = pd.Categorical(f3["dataset"], categories=DATASET_ORDER, ordered=True)
    f3 = f3.sort_values(["dataset", "dense_cap"])

    for ds, g in f3.groupby("dataset", observed=False):
        if len(g):
            vals = g.sort_values("dense_cap")["order_cert_rate"].to_numpy(float)
            assert np.all(np.diff(vals) >= -1e-15), f"non-monotone certification for {ds}"

    f3.to_csv(srcdir / "Figure3_Stable_DenseCap_Certification.csv", index=False)

    markers = ["o", "s", "^", "D"]
    linestyles = ["-", "--", "-.", ":"]
    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    for i, ds in enumerate(DATASET_ORDER):
        g = f3[f3["dataset"] == ds]
        if len(g):
            ax.plot(
                g["dense_cap"],
                100 * g["order_cert_rate"],
                marker=markers[i],
                linestyle=linestyles[i],
                linewidth=1.8,
                label=ds,
            )
    ax.set_xticks([100, 250, 500, 1000])
    ax.set_ylim(0, 102)
    ax.set_xlabel("Dense observation cap")
    ax.set_ylabel("Ordered top-10 certified (%)")
    ax.legend(frameon=False, ncol=2)
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    save(fig, out / "Figure3_Stable_DenseCap_Certification")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--input-root",
        type=Path,
        default=Path("/kaggle/input") if Path("/kaggle/input").exists() else Path.cwd(),
    )
    ap.add_argument("--output-dir", type=Path, default=Path("figures"))
    args = ap.parse_args()

    input_root = args.input_root.resolve()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    srcdir = out / "source_data"
    cache = out / "_artifact_cache"
    srcdir.mkdir(parents=True, exist_ok=True)
    cache.mkdir(parents=True, exist_ok=True)

    artifacts = {}
    origins = {}
    for key, (basename, hints) in TARGETS.items():
        p, origin = locate_artifact(input_root, cache, basename, hints)
        artifacts[key] = p
        origins[key] = origin
        print(f"{key:20s} -> {p} [{origin}]")

    exact_df = pd.read_csv(artifacts["exact_copy"])
    nested_df = pd.read_csv(artifacts["nested_replication"])
    stable_df = pd.read_csv(artifacts["stable_dense_caps"])

    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.labelsize": 11,
            "legend.fontsize": 9.5,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
        }
    )

    build_figure1(exact_df, out, srcdir)
    build_figure2(nested_df, out, srcdir)
    build_figure3(stable_df, out, srcdir)

    manifest = {
        key: {
            "basename": TARGETS[key][0],
            "origin": origins[key],
            "sha256": sha256_file(path),
        }
        for key, path in artifacts.items()
    }
    (out / "FIGURE_INPUT_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8"
    )
    shutil.rmtree(cache, ignore_errors=True)
    print("Wrote figures to", out)


if __name__ == "__main__":
    main()
