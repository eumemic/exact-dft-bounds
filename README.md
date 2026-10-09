# Exact DFT with a 4.856·10⁻⁴ power saving in the logarithm

$$
T(n)=O\!\left(n(\log n)^{\theta}(\log\log n)^{4-\theta}\right),\qquad
\theta = 1-\frac{607}{1250000} = 1-4.856\times10^{-4}.
$$

This bound applies to the exact discrete Fourier transform of every length n and to exact
complex convolution. It uses the exact complex-arithmetic model of OpenAI's
[An explicit power saving for the exact discrete Fourier transform](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/main.pdf)
(25 September 2026), where 1 − θ ≈ 2.1·10⁻¹³. The saving here is about 2.3·10⁹ times larger, and
for every fixed κ < 4.856·10⁻⁴ the cost is O(n (log n)^(1−κ)).

**[Proof note (PDF)](artifacts/batched-dft-note.pdf)** · [LaTeX](notes/batched-dft-note.tex) ·
[network children](certificates/network-children.json) · [moment certificate](certificates/moment.json)

## What changes

OpenAI's exponent comes from a fixed finite network through its Theorem 2.6. That recurrence
charges every unit of residual dimension as a separate directional step, so each unit pays
a full level of recursion. Two changes:

1. **Batched recursion** (Theorem 3.1 of the note). A frame transition of residual dimension ρ
   is executed as a single recursive call to C^{⊗ρf} after a linear-time address change. The
   condition becomes the moment inequality Σ_ρ N_ρ (ρ/m)^θ < W. Power-of-two padding is no
   longer needed. The same accounting was introduced for integer multiplication by icekylinx in
   [CrocSwap/integer-mult-bounds](https://github.com/CrocSwap/integer-mult-bounds).
2. **A better network** (Proposition 4.1). We use the paired-cube complex supplier of
   CrocSwap/integer-mult-bounds at commit `d1d6c07`, the merged PR #144 integration: m = 72,
   29,937 roles per cover vertex, rank deficit 1,936, largest child 60. Its batched critical
   saving is about 4.85657·10⁻⁴. We certify θ = 1 − 607/1250000 exactly.

OpenAI's Sections 3–5 (exact-width Fourier words, sector synchronization, small-prime working
lengths, chirp convolution) use their Theorem 2.6 only through the bound O(2^k (k+1)^θ), so
they carry the new exponent over unchanged.

## Verify

```sh
make verify    # exact rational check of the moment; needs Python 3.11+
make note      # builds artifacts/batched-dft-note.pdf with tectonic
```

`scripts/verify_moment.py` bounds every term of Σ_ρ n_ρ (ρ/72)^θ above in exact rational
arithmetic, using an artanh series for the logarithms with a geometric tail and
exp(x) ≤ 1 + x + x²/(2(1 − x/3)). It passes with margin 3.16·10⁻³ out of W = 29,937. As a
control, the same check fails at a = 4.8566·10⁻⁴. `scripts/extract_children.py` regenerates
the children file from the pinned upstream certificate (SHA-256 recorded in
[SOURCES.json](SOURCES.json)).

## Scope

This is a paper proof with an exact finite certificate. It is not formally verified. OpenAI's
paper is formalized in Lean; the changes here are not. The network's exact operator identities
are proved in the cited notes of CrocSwap/integer-mult-bounds and checked there by scripts and
maintainer review. That repository's integer-multiplication bound is conditional on its own
analytic and tape assembly. None of those hypotheses is used here. The constants are
astronomically large (the network has about 2^2446 roles), so this is an asymptotic existence
and explicitness result, with no practical crossover.

## Credits

The finite network is community work; full attribution is in the
[NOTICE](https://github.com/CrocSwap/integer-mult-bounds/blob/d1d6c070f5a8c684727ee7ec35d930f9ebfa9758/NOTICE)
and review records of CrocSwap/integer-mult-bounds at `d1d6c07`, and all of it applies here.
Principal contributors to this network:

- **icekylinx** (with OpenAI GPT-6 Astra and Codex assistance): the paired-cube identity
  K + H + B = I, signed overlap channels, the original-source involution, coordinate-star
  centers, the frame and carrier compiler and chronological gauges; the arbitrary-subspace
  Clifford frame theorem and three-stage Cayley cover; copied retained centers; endpoint
  gauges; and the batched recursion adapted here.
- **an664** (with OpenAI Codex assistance): completed-core workspace sharing (PR #128).
- **eumemic** (with Claude assistance): the positive producer DAG behind the coarse query
  modules (PR #117), and earlier compressed complex networks and source frames.
- **Aurel Prosz (Paureel)**: the copy/transform/read/discard interface and two-stage topology.
  **Zhihao Chen (jacklightChen)**: translated complex endpoints and two-stage composition.
  **Swapnil Jain**: two-stage development. **dleen**: retained totals and bank sharing in the
  complex network.
- **Douglas Colkitt**: the integer-mult-bounds repository and framework, integration and review.
- **OpenAI**: the original complex phase network of *Integer multiplication below n log n*,
  and the exact-transform framework reused here.

This repository contributes only the batched recursion in the exact-DFT model, the moment
certificate, and the observation that the community network applies. Prepared by eumemic
with substantial assistance from Claude (Anthropic). Apache-2.0; see [LICENSE](LICENSE) and
[NOTICE](NOTICE). This is not an OpenAI release or endorsement.
