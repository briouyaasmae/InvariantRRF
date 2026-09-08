#!/usr/bin/env python3
"""Build the final InvariantRRF figures from the four notebook output packages.

No retrieval is rerun. This script searches direct files and ZIP members beneath
--input-root for the paper-facing CSV artifacts produced by notebooks 01--04.
"""
from pathlib import Path
import argparse, hashlib, json, shutil, zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

TARGETS = {
    "canonical_scaling": ("canonical_scaling_macro_summary.csv", ("canonical", "deepdense", "taskadaptivek")),
    "stable_dense_caps": ("secondary_stable_dense_cap_summary.csv", ("canonical", "deepdense", "taskadaptivek")),
    "partial_observation": ("canonical_partial_observation_summary.csv", ("partial", "observation", "closure")),
    "splade_boundary": ("splade_family_paper_table_v43closure.csv", ("splade", "twocheckpoint", "closure")),
    "nested_replication": ("nested_rrf_replication_summary.csv", ("novelty", "strengthening", "v44")),
    "automc": ("automc_provenance_summary.csv", ("novelty", "strengthening", "v44")),
}
DATASET_ORDER = ["SciFact", "TREC-COVID", "FiQA", "ArguAna"]


def sha256_file(path, chunk=1024*1024):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        while True:
            b=f.read(chunk)
            if not b: break
            h.update(b)
    return h.hexdigest()


def score_path(path, hints):
    s=str(path).lower()
    return sum(1 for h in hints if h.lower() in s)


def locate_artifact(input_root, cache, basename, hints=()):
    direct=list(input_root.rglob(basename)) if input_root.exists() else []
    if direct:
        direct.sort(key=lambda p:(score_path(p,hints),-len(str(p))), reverse=True)
        return direct[0], 'direct'
    hits=[]
    for zp in (list(input_root.rglob('*.zip')) if input_root.exists() else []):
        try:
            with zipfile.ZipFile(zp,'r') as zf:
                for member in zf.namelist():
                    if Path(member).name==basename:
                        hits.append((score_path(zp,hints)+score_path(member,hints),str(zp),member,zp))
        except zipfile.BadZipFile:
            continue
    if not hits:
        raise FileNotFoundError(f'Could not find {basename} under {input_root}')
    hits.sort(reverse=True)
    _,_,member,zp=hits[0]
    dest=cache/f'{hashlib.sha256((str(zp)+"::"+member).encode()).hexdigest()[:10]}_{basename}'
    with zipfile.ZipFile(zp,'r') as zf, zf.open(member) as src, dest.open('wb') as dst:
        shutil.copyfileobj(src,dst)
    return dest, f'zip:{zp.name}:{member}'


def save(fig, base):
    fig.savefig(base.with_suffix('.pdf'), bbox_inches='tight')
    fig.savefig(base.with_suffix('.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input-root', type=Path, default=Path('/kaggle/input') if Path('/kaggle/input').exists() else Path.cwd())
    ap.add_argument('--output-dir', type=Path, default=Path('figures'))
    args=ap.parse_args()
    out=args.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
    supp=out/'supplement'; srcdir=out/'source_data'; cache=out/'_artifact_cache'
    for d in [supp,srcdir,cache]: d.mkdir(parents=True,exist_ok=True)

    artifacts={}
    origins={}
    for key,(basename,hints) in TARGETS.items():
        p,origin=locate_artifact(args.input_root.resolve(), cache, basename, hints)
        artifacts[key]=p; origins[key]=origin
        print(f'{key:22s} -> {p} [{origin}]')

    scaling=pd.read_csv(artifacts['canonical_scaling'])
    stable=pd.read_csv(artifacts['stable_dense_caps'])
    partial=pd.read_csv(artifacts['partial_observation'])
    splade=pd.read_csv(artifacts['splade_boundary'])
    nested=pd.read_csv(artifacts['nested_replication'])
    automc=pd.read_csv(artifacts['automc'])

    # Input guards.
    assert set(stable.dense_cap.astype(int)) >= {100,250,500,1000}
    assert set(splade.dataset)=={'SciFact','ArguAna'}
    arg=splade[splade.dataset=='ArguAna'].iloc[0]
    assert np.isclose(float(arg.ordinary_set_preservation),0.392,atol=5e-4)
    assert np.isclose(float(arg.MC_set_preservation),0.640,atol=5e-4)
    n50=nested[nested.depth.astype(int)==50]
    for m in ['Flat ordinary RRF','Plain nested RRF','MC-RRF']:
        assert len(n50[n50.method==m])==13
    mc=n50[n50.method=='MC-RRF']
    assert np.allclose(mc.order_preservation,1.0) and np.allclose(mc.set_preservation,1.0)
    # Final qrels-aware novelty run: nDCG drift must be populated for non-MC rows.
    assert n50.loc[n50.method!='MC-RRF','mean_abs_ndcg_drift'].notna().all()

    plt.rcParams.update({'font.size':11,'axes.titlesize':12,'axes.labelsize':11,'legend.fontsize':9.5,'xtick.labelsize':10,'ytick.labelsize':10})

    # Figure 1: family-size scaling.
    f1=scaling[scaling.perturbation.astype(str).str.lower()=='mild'].groupby('family_size',as_index=False).agg(
        ordinary_set_preservation=('ordinary_set_preservation','mean'),
        mc_set_preservation=('mc_set_preservation','mean')).sort_values('family_size')
    f1.to_csv(srcdir/'Figure1_MC_RRF_SetPreservation.csv',index=False)
    fig,ax=plt.subplots(figsize=(7.2,4.4))
    ax.plot(f1.family_size,100*f1.ordinary_set_preservation,marker='o',linewidth=1.8,label='Ordinary RRF')
    ax.plot(f1.family_size,100*f1.mc_set_preservation,marker='s',linestyle='--',linewidth=1.8,label='MC-RRF')
    ax.set_xticks(f1.family_size.astype(int)); ax.set_ylim(-2,102)
    ax.set_xlabel('Represented members in attacked provenance family'); ax.set_ylabel('Exact top-10 set preservation (%)')
    ax.set_title('Representation count changes ordinary RRF, not family budget'); ax.legend(frameon=False); ax.grid(axis='y',alpha=.25); fig.tight_layout()
    save(fig,out/'Figure1_MC_RRF_SetPreservation')

    # Figure 2: nested-RRF audit.
    order=['Flat ordinary RRF','Plain nested RRF','MC-RRF']
    f2=n50.groupby('method',as_index=False).agg(ordered_top10=('order_preservation','mean'),set_top10=('set_preservation','mean'),top1=('top1_preservation','mean'),mean_abs_ndcg_drift=('mean_abs_ndcg_drift','mean'))
    f2['method']=pd.Categorical(f2.method,categories=order,ordered=True); f2=f2.sort_values('method').reset_index(drop=True)
    f2.to_csv(srcdir/'Figure2_NestedRRF_ReplicationAudit.csv',index=False)
    x=np.arange(len(f2)); w=.34; fig,ax=plt.subplots(figsize=(7.4,4.6))
    ax.bar(x-w/2,100*f2.ordered_top10,width=w,label='Ordered top-10',hatch='//')
    ax.bar(x+w/2,100*f2.set_top10,width=w,label='Top-10 set',hatch='..')
    ax.set_xticks(x); ax.set_xticklabels(order); ax.set_ylim(0,105); ax.set_ylabel('Replication preservation (%)')
    ax.set_title('Within-family exact-copy audit on real heterogeneous families'); ax.legend(frameon=False); ax.grid(axis='y',alpha=.25); fig.tight_layout()
    save(fig,out/'Figure2_NestedRRF_ReplicationAudit')

    # Figure 3: StableRRF dense-cap certification.
    f3=stable[stable.dense_cap.astype(int).isin([100,250,500,1000])].copy()
    f3['dataset']=pd.Categorical(f3.dataset,categories=DATASET_ORDER,ordered=True); f3=f3.sort_values(['dataset','dense_cap'])
    for ds,g in f3.groupby('dataset',observed=False):
        if len(g): assert np.all(np.diff(g.sort_values('dense_cap').order_cert_rate.to_numpy(float))>=-1e-15)
    f3.to_csv(srcdir/'Figure3_StableRRF_DenseCap_Certification.csv',index=False)
    fig,ax=plt.subplots(figsize=(7.2,4.6)); markers=['o','s','^','D']; ls=['-','--','-.',':']
    for i,ds in enumerate(DATASET_ORDER):
        g=f3[f3.dataset==ds]
        if len(g): ax.plot(g.dense_cap,100*g.order_cert_rate,marker=markers[i],linestyle=ls[i],linewidth=1.8,label=ds)
    ax.set_xticks([100,250,500,1000]); ax.set_ylim(-2,102); ax.set_xlabel('Dense observation cap'); ax.set_ylabel('Ordered top-10 certified (%)')
    ax.set_title('StableRRF certification vs observable dense depth'); ax.legend(frameon=False,ncol=2); ax.grid(axis='y',alpha=.25); fig.tight_layout()
    save(fig,out/'Figure3_StableRRF_DenseCap_Certification')

    # Supplement S1: partial observation.
    s1=partial[partial.configuration=='BM25+dense'].copy(); s1['dataset']=pd.Categorical(s1.dataset,categories=DATASET_ORDER,ordered=True); s1=s1.sort_values(['dataset','requested_depth'])
    s1.to_csv(srcdir/'FigureS1_PartialObservation_OrderedReproduction.csv',index=False)
    fig,ax=plt.subplots(figsize=(7.2,4.6)); markers=['o','s','^','D']; ls=['-','--','-.',':']
    for i,ds in enumerate(DATASET_ORDER):
        g=s1[s1.dataset==ds]
        if len(g): ax.plot(g.requested_depth,100*g.ordered_top10_reproduction_rate,marker=markers[i],markersize=4,linestyle=ls[i],linewidth=1.5,label=ds)
    ax.set_xscale('log'); ax.set_xticks([5,10,20,50,100,200,500,1000]); ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.set_ylim(-2,102); ax.set_xlabel('Observed prefix depth per source'); ax.set_ylabel('Ordered top-10 reproduction (%)'); ax.set_title('Empirical reproduction vs observation depth')
    ax.legend(frameon=False,ncol=2); ax.grid(axis='y',alpha=.25); fig.tight_layout(); save(fig,supp/'FigureS1_PartialObservation_OrderedReproduction')

    # Supplement S2: SPLADE boundary.
    s2=splade.copy(); s2['dataset']=pd.Categorical(s2.dataset,categories=['SciFact','ArguAna'],ordered=True); s2=s2.sort_values('dataset').reset_index(drop=True)
    s2.to_csv(srcdir/'FigureS2_SPLADE_TwoCheckpoint_Boundary.csv',index=False); x=np.arange(len(s2)); w=.34
    fig,ax=plt.subplots(figsize=(6.4,4.4)); ax.bar(x-w/2,100*s2.ordinary_set_preservation,width=w,label='Ordinary RRF',hatch='//'); ax.bar(x+w/2,100*s2.MC_set_preservation,width=w,label='MC-RRF',hatch='..')
    ax.set_xticks(x); ax.set_xticklabels(s2.dataset.astype(str)); ax.set_ylim(0,100); ax.set_ylabel('Exact top-10 set preservation (%)'); ax.set_title('Two-checkpoint SPLADE family at depth 50'); ax.legend(frameon=False); ax.grid(axis='y',alpha=.25); fig.tight_layout(); save(fig,supp/'FigureS2_SPLADE_TwoCheckpoint_Boundary')

    # Supplement S3: AutoMC threshold audit.
    a=automc[automc.depth.astype(int)==50].groupby('threshold',as_index=False).agg(exact_partition_recovery=('exact_partition_recovery','mean'),pair_f1=('pair_f1','mean'),set_agreement=('set_agreement_with_declared_mc','mean')).sort_values('threshold')
    sel=a.copy(); sel['tie_distance']=(sel.threshold-.75).abs(); sel=sel.sort_values(['exact_partition_recovery','pair_f1','tie_distance','threshold'],ascending=[False,False,True,True]); threshold=float(sel.iloc[0].threshold); assert np.isclose(threshold,.75)
    a.to_csv(srcdir/'FigureS3_AutoMC_ThresholdAudit.csv',index=False)
    fig,ax=plt.subplots(figsize=(7.2,4.5)); ax.plot(a.threshold,100*a.exact_partition_recovery,marker='o',label='Exact partition recovery'); ax.plot(a.threshold,100*a.pair_f1,marker='s',linestyle='--',label='Pairwise family F1'); ax.plot(a.threshold,100*a.set_agreement,marker='^',linestyle='-.',label='Top-10 set agreement vs declared MC-RRF'); ax.axvline(threshold,linestyle=':',linewidth=1.2,label=f'Selected threshold = {threshold:.2f}'); ax.set_ylim(0,100); ax.set_xlabel('Finite-prefix RBO grouping threshold'); ax.set_ylabel('Macro rate (%)'); ax.set_title('AutoMC provenance-threshold sensitivity at depth 50'); ax.legend(frameon=False); ax.grid(axis='y',alpha=.25); fig.tight_layout(); save(fig,supp/'FigureS3_AutoMC_ThresholdAudit')

    manifest={k:{'basename':TARGETS[k][0],'origin':origins[k],'sha256':sha256_file(v)} for k,v in artifacts.items()}
    (out/'FIGURE_INPUT_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True),encoding='utf-8')
    shutil.rmtree(cache,ignore_errors=True)
    print('Wrote figures to',out)

if __name__=='__main__':
    main()
