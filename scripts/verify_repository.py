#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import sys

EXPECTED_NOTEBOOKS = [
    '01_canonical_experiments.ipynb',
    '02_partial_observation_closure.ipynb',
    '03_splade_two_checkpoint_closure.ipynb',
    '04_nested_rrf_automc_audit.ipynb',
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    args = ap.parse_args()
    root = args.repo.resolve()
    errors = []

    nbdir = root / 'notebooks'
    actual = sorted(p.name for p in nbdir.glob('*.ipynb'))
    if actual != EXPECTED_NOTEBOOKS:
        errors.append(f'notebook set mismatch: {actual}')

    for name in EXPECTED_NOTEBOOKS:
        p = nbdir / name
        try:
            nb = json.loads(p.read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'{name}: invalid JSON: {exc}')
            continue
        for i, cell in enumerate(nb.get('cells', [])):
            if cell.get('cell_type') == 'code':
                if cell.get('execution_count') is not None:
                    errors.append(f'{name} cell {i}: execution_count not stripped')
                if cell.get('outputs'):
                    errors.append(f'{name} cell {i}: outputs not stripped')
        text = p.read_text(encoding='utf-8')
        if '/kaggle/input/notebooks/asmae' in text:
            errors.append(f'{name}: private Kaggle account path remains')

    if (root / 'manuscript').exists():
        errors.append('manuscript/ directory must not be included in the code-only package')

    license_path = root / 'LICENSE'
    if not license_path.exists():
        errors.append('LICENSE is missing')
    else:
        license_text = license_path.read_text(encoding='utf-8', errors='replace')
        if 'GNU GENERAL PUBLIC LICENSE' not in license_text or 'Version 3, 29 June 2007' not in license_text:
            errors.append('LICENSE is not the GNU GPL version 3 license text')

    notice_path = root / 'NOTICE.md'
    if not notice_path.exists():
        errors.append('NOTICE.md is missing')
    else:
        notice_text = notice_path.read_text(encoding='utf-8')
        if 'GPL-3.0-or-later' not in notice_text:
            errors.append('NOTICE.md does not declare GPL-3.0-or-later')

    cff_path = root / 'CITATION.cff'
    if not cff_path.exists():
        errors.append('CITATION.cff is missing')
    else:
        cff_text = cff_path.read_text(encoding='utf-8')
        if 'license: GPL-3.0-or-later' not in cff_text:
            errors.append('CITATION.cff license is not GPL-3.0-or-later')

    if errors:
        print('REPOSITORY VERIFY: FAIL')
        for error in errors:
            print(' -', error)
        sys.exit(1)

    print('REPOSITORY VERIFY: PASS')
    print(' notebooks: 4')
    print(' manuscript directory: absent')
    print(' license: GPL-3.0-or-later')
    print(' citation metadata: present')


if __name__ == '__main__':
    main()
