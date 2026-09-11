# math-problem

Research notes on open mathematical problems.

## Current focus: \(S(6)=2\)?

Largest square coverable by 6 unit squares (rigid motions, overlaps allowed).

\(S(n)\) = largest edge length of a square coverable by \(n\) unit squares.

**Main object:** a rigorous proof attempt that \(S(6)=2\), in
[`PROOF/ATTEMPT.md`](PROOF/ATTEMPT.md) and [`PROOF/GAPS.md`](PROOF/GAPS.md).

Those notes do **not** contain a complete proof. \(S(6)=2\) is **not** proved.

G1 (\(k=0\)): 0-/1-/4-meet die for all \(a>2\); Cascade for \(a>a_\varphi\);
local Open B C-on-top for \(a>a_{\mathrm{top}}\approx 2.0361747746\) and
C-on-right for \(a>a_{\mathrm{cr}}\approx 2.0036185600\) (R2TopDiam / FHeight
do not lower those cuts). Residual: meet deep-\(\delta\) \((2,a_\varphi]\),
C-on-top \((2,a_{\mathrm{top}}]\), C-on-right \((2,a_{\mathrm{cr}}]\), Open C
razor \((2,a_\psi]\). One G2 subcase for \(a>2^{5/4}\); one G4 representative
for \(a>\sqrt{5}\). G2–G5 otherwise open. Ledger: [`PROOF/LOCAL_SYNC.md`](PROOF/LOCAL_SYNC.md).

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
