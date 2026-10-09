# Exact DFT with a 4.856·10⁻⁴ power saving in the logarithm

$$
T(n)=O\!\left(n(\log n)^{\theta}(\log\log n)^{4-\theta}\right),\qquad
\theta = 1-\frac{607}{1250000} = 1-4.856\times10^{-4}.
$$

This bound applies to the exact discrete Fourier transform of every length n. It also applies to
exact complex convolution when general multiplication is allowed for the pointwise products (as in
OpenAI's Corollary 1.3). It uses the exact complex-arithmetic model of OpenAI's
[An explicit power saving for the exact discrete Fourier transform](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/main.pdf)
(25 September 2026), where 1 − θ ≈ 2.1·10⁻¹³. The saving here is about 2.3·10⁹ times larger, and
for every fixed κ < 4.856·10⁻⁴ the cost is O(n (log n)^(1−κ)).

The result depends on the correctness of a community-built finite network (see Scope).

**[Proof note (PDF)](artifacts/batched-dft-note.pdf)** · [LaTeX](notes/batched-dft-note.tex) ·
[network children](certificates/network-children.json) · [moment certificate](certificates/moment.json)

## What changes

OpenAI's exponent comes from a fixed finite network through its Theorem 2.6. That recurrence
charges every unit of residual dimension as a separate directional step, so each unit pays
a full level of recursion. Two changes:

1. **Batched recursion** (Theorem 3.1 of the note). A frame transition of residual dimension ρ
   is executed as a single recursive call to C^{⊗ρf} after a linear-time address change. The
   condition becomes the moment inequality Σ_ρ N_ρ (ρ/m)^θ < W, and no power-of-two padding is
   needed. A normal-form lemma (Lemma 4.1) shows that a transition's width depends only on its
   binary symplectic action, so errors in exact phases can change only adapters. The same
   accounting was introduced for integer multiplication by icekylinx in
   [CrocSwap/integer-mult-bounds](https://github.com/CrocSwap/integer-mult-bounds).
2. **A better network** (Proposition 4.2). We use the paired-cube complex supplier of that
   repository at commit `d1d6c07`, the merged PR #144 integration: m = 72, 29,937 roles per cover
   vertex, rank deficit 1,936, largest child 60. Its batched critical saving is 4.85657…·10⁻⁴.
   We check the moment inequality at θ = 1 − 607/1250000 in exact rational arithmetic. This is
   an independent re-check: the upstream repository certifies the same moment at 4856569/10¹⁰,
   which our script also confirms.

OpenAI's Sections 3–5 (exact-width Fourier words, sector synchronization, small-prime working
lengths, chirp convolution) use their Theorem 2.6 only through three things: the bound
O(2^k (k+1)^θ), the fact that only constants in Q(i) are needed, and its word-size accounting.
Theorem 3.1 provides all three, so the new exponent carries over.

## Verify

```sh
make verify    # exact rational check of the moment plus source pins; Python 3.11+
make note      # builds artifacts/batched-dft-note.pdf with tectonic
```

`scripts/verify_moment.py` bounds every term of Σ_ρ n_ρ (ρ/72)^θ above in exact rational
arithmetic, using an artanh series for the logarithms (terms rounded up, with a geometric tail)
and exp(x) ≤ 1 + x + x²/(2(1 − x/3)). It passes with margin 3.16·10⁻³ out of W = 29,937. As a
control, the same check fails at a = 4.8566·10⁻⁴. `scripts/extract_children.py` regenerates the
children file from the pinned upstream certificate (SHA-256 recorded in [SOURCES.json](SOURCES.json)).

## Scope

This is a paper proof with an exact finite certificate, and it is not formally verified. OpenAI's
Lean formalization (`lean/docs/130.md` in openai/math) covers their original uniform 10⁻¹³ DFT and
convolution statements, not the changes here.

The theorem depends on the network of Proposition 4.2. Its construction and proofs live in
CrocSwap/integer-mult-bounds, which has had maintainer review with AI assistance but no independent
human peer review. Upstream records say what is checked how:
- by script: the local scalar map on all 3,097,600 source/target entries, binary frame and rank
  data, and integer replays of the mixer;
- the frame checks cover binary geometry, not exact complex phases;
- the sharing, routing and precision arguments are written proofs.

By Lemma 4.1, the child histogram depends only on the binary frame data.

Upstream, the network feeds a conditional integer-multiplication bound. That bound retains
several hypotheses: the analytic reduction, semantic precision, exact recovery, uniform
recursion, fixed-tape setup, the opposite-bank primitive, ordered-affine streaming, prime packing
and ordinary leaves. None of them is used here.

The constants are astronomically large: the network has about 2^2570 roles, and the recursion's
base range is of order 10⁹ bits. This is an asymptotic existence and explicitness result with no
practical crossover.

## Credits

The finite network is community work. Full attribution is in the
[NOTICE](https://github.com/CrocSwap/integer-mult-bounds/blob/d1d6c070f5a8c684727ee7ec35d930f9ebfa9758/NOTICE)
and review records of CrocSwap/integer-mult-bounds at `d1d6c07`, and all of it applies here; the
pertinent NOTICE blocks are reproduced in this repository's [NOTICE](NOTICE). Principal
contributors to this network:

- **icekylinx** (with OpenAI GPT-6 Astra and Codex assistance):
  - the paired-cube identity K + H + B = I, signed overlap channels, the original-source
    involution and coordinate-star centers;
  - the frame and carrier compiler and chronological gauges;
  - the arbitrary-subspace Clifford frame theorem and three-stage Cayley cover;
  - copied retained centers and endpoint gauges;
  - the batched recursion adapted here.
- **an664** (with OpenAI Codex assistance): completed-core workspace sharing (PR #128).
- **eumemic** (with Claude assistance): the positive producer DAG behind the coarse query
  modules (PR #117), and earlier compressed complex networks and source frames.
- **Aurel Prosz (Paureel)**: the copy/transform/read/discard interface and two-stage topology.
- **Zhihao Chen (jacklightChen)**: translated complex endpoints and two-stage composition.
- **Swapnil Jain**: two-stage development.
- **dleen**: retained totals and stage sharing (PR #4).
- **Douglas Colkitt**: the integer-mult-bounds repository and framework, integration and review.
- **OpenAI**: the original complex phase network of *Integer multiplication below n log n*,
  and the exact-transform framework reused here.

This repository contributes the batched recursion and normal-form lemma in the exact-DFT model,
an independent re-check of the moment, and the observation that the community network applies.
It was prepared by eumemic with substantial assistance from Claude (Anthropic). Licensed
Apache-2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE). This is not an OpenAI release or
endorsement.
