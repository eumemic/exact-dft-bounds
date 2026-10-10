#!/usr/bin/env python3
"""Derive the five-stage bridged-layout children (Jacob Sussman, wht-power-saving-lean) from a three-stage
source-assisted children file of this repository: H_inv = (H3 - 2v e_2)/3 is the per-invocation ledger and
H5 = 5 H_inv + 2v (e42 + e21 + e46 + e4) per cover vertex, m = 5h = 110, W = 4v + R (the ledger stated by
CrocSwap/integer-mult-bounds PR #250 for the PR #234 five-stage complex supplier).
usage: five_stage_children.py certificates/network-children-prNNN.json certificates/network-children-prNNN-five.json"""
import hashlib, json, sys
from pathlib import Path

def main():
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    raw = src.read_bytes(); d = json.loads(raw)
    v, h = d['v'], d['h']; assert d['m'] == 3 * h and h == 22 and v == 1320
    H3 = {int(r): n for r, n in d['child_histogram'].items() if n}; H3[2] -= 2 * v
    assert all(n % 3 == 0 and n >= 0 for n in H3.values())
    Hinv = {r: n // 3 for r, n in H3.items() if n}
    R = d['roles_per_vertex'] - 2 * v
    H5 = {r: 5 * n for r, n in Hinv.items()}
    for r in (42, 21, 46, 4): H5[r] = H5.get(r, 0) + 2 * v
    W = 4 * v + R; rank = sum(r * n for r, n in H5.items())
    out = dict(description='Per-vertex child list of the same helper circuit in Sussman\'s five-stage bridged layout, derived from '
                           + src.name + ' by H5 = 5 H_inv + 2v (e42 + e21 + e46 + e4), H_inv = (H3 - 2v e2)/3; a priced transfer, '
                           'not a kernel-checked certificate of that word in that layout.',
               source=dict(d['source'], derived_from=src.name, derived_from_sha256=hashlib.sha256(raw).hexdigest(),
                           layout='five-stage bridged (jacobalansussman/wht-power-saving-lean f010392c923279e3dd59ef3aa5fedad23affc5fd)'),
               m=5 * h, h=h, v=v, R=R, loss=d.get('loss'), roles_per_vertex=W, rank_per_vertex=rank,
               deficit_per_vertex=W * 5 * h - rank, child_histogram={str(r): n for r, n in sorted(H5.items())})
    dst.write_text(json.dumps(out, indent=1) + '\n'); print('wrote', dst, 'W', W, 'rank', rank, 'deficit', W * 5 * h - rank)

if __name__ == '__main__':
    main()
