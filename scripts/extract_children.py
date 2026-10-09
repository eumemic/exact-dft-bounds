#!/usr/bin/env python3
"""Extract the complex network's child histogram from CrocSwap/integer-mult-bounds.

Source: certificates/paired-cube-complex-input.json at commit
d1d6c070f5a8c684727ee7ec35d930f9ebfa9758 (the merged PR #144 integration), sha256 pinned below.
usage: extract_children.py PATH/TO/paired-cube-complex-input.json"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIN = '11894aa8fd4d5e258ec534726eba5fc9c9fa7b826f993e229425c31ee2ad2440'


def main():
    raw = Path(sys.argv[1]).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == PIN, 'unexpected source file %s' % digest
    sys.set_int_max_str_digits(100000)
    d = json.loads(raw)
    hist = {str(r): n for r, n in sorted(((int(r), n) for r, n in d['child_histogram'].items()), key=lambda t: t[0])
            if n}
    out = dict(
        description='Per-vertex child list of the paired-cube complex supplier of CrocSwap/integer-mult-bounds '
                    '(PR #144 integration). A child of width rho applies C^{(x)rho} (or its inverse) after rank-zero '
                    'adapters; roles_per_vertex counts persistent arrays per cover vertex.',
        source=dict(repository='https://github.com/CrocSwap/integer-mult-bounds',
                    commit='d1d6c070f5a8c684727ee7ec35d930f9ebfa9758',
                    path='certificates/paired-cube-complex-input.json', sha256=digest),
        m=d['m'], h=d['h'], v=d['v'], R=d['R'], loss=d['loss'],
        roles_per_vertex=d['W_per_vertex'], rank_per_vertex=d['rank_per_vertex'],
        deficit_per_vertex=d['deficit_per_vertex'], child_histogram=hist)
    (ROOT / 'certificates' / 'network-children.json').write_text(json.dumps(out, indent=1) + '\n')
    print('wrote certificates/network-children.json from %s' % digest)


if __name__ == '__main__':
    main()
