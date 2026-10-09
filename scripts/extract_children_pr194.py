#!/usr/bin/env python3
"""Extract the complex network's child histogram from PR #200 of CrocSwap/integer-mult-bounds.

Source: research/paired-cube-diagonal-bit-168/certificate.json at commit
a1175449f34d39ff933d9d8ab23ced1f32b290ec (PR #200, Chafik Boukhalfa), field complex.profile; sha256 pinned below.
That package certifies the complete complex supplier of the PR #168 v4 lineage with its own physical frames, reuse
pairs and terminal sinks (m = 66, 13,163 roles per cover vertex, rank deficit 1,320, largest child 20).
usage: extract_children_pr194.py PATH/TO/certificate.json"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIN = '1600b77cb1f41c0f87967f20133eccda5e6c5f215b70361dfd0c49c861248e59'


def main():
    raw = Path(sys.argv[1]).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == PIN, 'unexpected source file %s' % digest
    sys.set_int_max_str_digits(100000)
    d = json.loads(raw)
    p = d['complex_profile']
    hist = {str(r): n for r, n in sorted(((int(r), n) for r, n in p['child_histogram'].items()), key=lambda t: t[0])
            if n}
    out = dict(
        description='Per-vertex child list of the source-assisted complex supplier of CrocSwap/integer-mult-bounds PR #194 '
                    '(PR #184 frame-flow compression with exact dirty lifts on the PR #168 v4 modules). A child of width rho '
                    'applies C^{(x)rho} (or its inverse) after rank-zero adapters; roles_per_vertex counts persistent arrays '
                    'per cover vertex.',
        source=dict(repository='https://github.com/CrocSwap/integer-mult-bounds',
                    commit='a8c87783785be6fe20c4a8bb2ac4b3eec295a179',
                    path='research/source-assisted-v4/certificate.json', field='complex_profile',
                    sha256=digest, certified_complex_saving=d['complex_saving']),
        m=p['m'], h=p.get('h', 22), v=p.get('v', 1320), R=p.get('R'), loss=p.get('loss', 440),
        roles_per_vertex=p['W_per_vertex'], rank_per_vertex=p['rank_per_vertex'],
        deficit_per_vertex=p['deficit_per_vertex'], child_histogram=hist)
    (ROOT / 'certificates' / 'network-children-pr194.json').write_text(json.dumps(out, indent=1) + '\n')
    print('wrote certificates/network-children-pr194.json from %s' % digest)


if __name__ == '__main__':
    main()
