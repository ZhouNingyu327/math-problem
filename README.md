# math-problem

Research notes on open mathematical problems.

## Current focus: \(S(6)=2\)?

Largest square coverable by 6 unit squares (rigid motions, overlaps allowed).

\(S(n)\) = largest edge length of a square coverable by \(n\) unit squares.

**Main object:** a rigorous proof attempt that \(S(6)=2\), in
[`PROOF_ATTEMPT.md`](PROOF_ATTEMPT.md).

That document does **not** contain a complete proof. It proves the distance
and combinatorial classification, reduces the problem to five remaining lemmas
(11 dihedral orbits of important-point assignments), and isolates a single
bottleneck: a constrained 3-square covering of a quadrant of side \(a/2>1\).

### Known facts

- \(S(5)=2\) is proved (Januszewski; Dósa–Lángi–Tuza), so \(S(6)\ge 2\).
- Area: \(S(6)\le\sqrt{6}\approx 2.449\).
- Best published construction for \(n=6\): trivial side 2 (area 4).
- Conjecture: Dósa–Lángi–Tuza, [arXiv:2601.16535](https://arxiv.org/abs/2601.16535), Conjecture 1.1: \(S(6)=2\).
- \(S_{\mathrm{bd}}(6)>2\) is expected (and supported numerically at \(s=2.33\)); a proof cannot go through “the boundary is uncoverable”.

### Proof-attempt checks

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest
python3 -m proof
```

### Numerical toolkit (secondary)

Code in [`cover6/`](cover6/) searches for counterexample constructions with
\(s>2\). Results: [`RESULTS.md`](RESULTS.md). **Numerics are not a proof.**
No \(s>2\) interior covering survived the polygon check in the committed run.

```bash
python3 -m cover6 baseline
python3 -m cover6 experiment --budget default --seed 0
```
