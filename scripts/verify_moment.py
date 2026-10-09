#!/usr/bin/env python3
"""Exact certificate for the batched tensor moment of a finite complex network.

Checks, in exact rational arithmetic, that

    sum_rho N_rho * (rho/m)**theta  <  W,      theta = 1 - a,

for the child histogram N of the network in certificates/network-children.json.
By Theorem 3.1 of notes/batched-dft-note.tex this gives C^{(x)k} in O(2^k (k+1)^theta)
operations in the exact model of OpenAI's "An explicit power saving for the exact discrete
Fourier transform", and with it the exact transform at every length.

Bounds used (all exact):
  (rho/m)**theta = (rho/m) * exp(a * ln(m/rho)),
  ln(x) <= 2*sum_{j<J} y**(2j+1)/(2j+1) + 2*y**(2J+1)/((2J+1)(1-y**2)),  y = (x-1)/(x+1),
  exp(x) <= 1 + x + x**2 / (2*(1 - x/3))  for 0 <= x < 3.
usage: verify_moment.py [--a NUM/DEN] [--write certificates/moment.json]"""
import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHILDREN = ROOT / 'certificates' / 'network-children.json'
DEFAULT_A = Fraction(4856, 10**7)


def ln_upper(x, terms=4000):
    """Rational upper bound for ln(x), x > 1 rational, via the artanh series with a tail bound."""
    y = (x - 1) / (x + 1)
    y2 = y * y
    # Round each partial term up onto a fixed grid so the rationals stay small.
    grid = 10**60
    s = 0
    p = y
    for j in range(terms):
        k = 2 * j + 1
        t = p / k
        s += -((-t.numerator * grid) // t.denominator)
        p *= y2
        if p < Fraction(1, 10**70):
            break
    k = 2 * (j + 1) + 1
    tail = 2 * p / (k * (1 - y2))
    return Fraction(2 * s, grid) + tail


def exp_upper(x):
    assert 0 <= x < 3
    return 1 + x + x * x / (2 * (1 - x / 3))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--a', default=None, help='saving a = 1 - theta as NUM/DEN (default 4856/10^7)')
    ap.add_argument('--write', type=Path)
    o = ap.parse_args()
    a = Fraction(o.a) if o.a else DEFAULT_A
    raw = CHILDREN.read_bytes()
    data = json.loads(raw)
    m = data['m']
    W = data['roles_per_vertex']
    hist = {int(r): int(n) for r, n in data['child_histogram'].items() if int(n)}
    assert all(1 <= r < m for r in hist), 'every child must be strictly narrower than a role'
    rank = sum(r * n for r, n in hist.items())
    assert rank == data['rank_per_vertex'], 'rank sum mismatch'
    assert W * m - rank == data['deficit_per_vertex'], 'deficit mismatch'
    total = Fraction(0)
    for r, n in sorted(hist.items()):
        L = ln_upper(Fraction(m, r))
        total += n * Fraction(r, m) * exp_upper(a * L)
    margin = W - total
    ok = margin > 0
    print('children file sha256 %s' % hashlib.sha256(raw).hexdigest())
    print('m %d  W %d  rank sum %d  deficit %d  max child %d' % (m, W, rank, W * m - rank, max(hist)))
    print('a = %s = %.10e   theta = 1 - a' % (a, float(a)))
    print('upper bound of sum N_rho (rho/m)^theta = %.12f   W = %d   margin %.6e   %s'
          % (float(total), W, float(margin), 'PASS' if ok else 'FAIL'))
    if o.write:
        scale = 10**30
        upper = -((-total.numerator * scale) // total.denominator)   # total rounded up on a 1e-30 grid
        o.write.write_text(json.dumps(dict(
            children_sha256=hashlib.sha256(raw).hexdigest(), m=m, roles_per_vertex=W, rank_per_vertex=rank,
            deficit_per_vertex=W * m - rank, max_child=max(hist), a=str(a), theta=str(1 - a),
            moment_upper_bound='%d/10^30' % upper, margin_lower_bound='%d/10^30' % (W * scale - upper),
            passed=ok, bounds='ln: artanh series with tail; exp(x) <= 1 + x + x^2/(2(1 - x/3))'), indent=1) + '\n')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
