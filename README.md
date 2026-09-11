# math-problem

Research notes and computational experiments for open mathematical problems.

## Current focus

Largest square coverable by 6 unit squares (side 1), allowing rotations and overlaps.

Notation: \(S(n)\) = largest edge length of a square coverable by \(n\) unit squares.

Known facts:

- \(S(5)=2\) is proved, so \(S(6)\ge 2\) (area \(\ge 4\)).
- Area upper bound: \(S(6)\le\sqrt{6}\approx 2.449\).
- Best published construction for \(n=6\) is the trivial side-2 covering (area 4).
- Conjecture (Dósa–Lángi–Tuza, [arXiv:2601.16535](https://arxiv.org/abs/2601.16535), 2026): \(S(6)=2\).
- For \(n=7\) there is a known covering of area \(\approx 4.871\) (Trevor Green), side \(3/2+1/\sqrt{2}\approx 2.207\).

Numerical experiments for this problem live in [`cover6/`](cover6/). Results, figures, and honest conclusions are in [`RESULTS.md`](RESULTS.md). **Numerics are not a proof.**

### Run

```bash
python -m pip install -r requirements.txt
python -m pytest
python -m cover6 baseline
python -m cover6 experiment --budget default --seed 0
```

Budgets: `tiny` (smoke), `default` (the committed run), `serious` (longer annealing).

See [`cover6/README.md`](cover6/README.md) for the module layout and extra commands.
See [`RESULTS.md`](RESULTS.md) for the committed numbers, figures, and caveats.
