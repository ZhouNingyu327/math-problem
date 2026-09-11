# cover6

Python package for numerical experiments on

> \(S(n)\): the largest edge length of a square coverable by \(n\) unit squares,
> allowing rigid motions (translation + rotation) and overlaps.

The open case of interest is \(n=6\). The code **does not prove** \(S(6)=2\);
it searches for counterexample constructions with \(s>2\) and records whether
any candidate survives a polygon coverage check (shapely) plus dense sampling.

## Layout

| Path | Role |
|------|------|
| `geometry.py` | Unit-square poses `(cx, cy, θ)`, local coordinates, sampling grids |
| `coverage.py` | Sampling loss; shapely uncovered area and uncovered boundary length |
| `configs.py` | Trivial 2×2, Dudeney \(n=3\), Type-I / Green \(n=7\) seeds, C4 ansatze |
| `optimize.py` | Local polish (L-BFGS-B), dual annealing, adiabatic growth, multi-start |
| `visualize.py` | SVG/PNG figures of coverings (uncovered region in red) |
| `experiment.py` | End-to-end suite that writes `artifacts/` |

## Commands

```bash
# from the repository root
python -m pip install -r requirements.txt
python -m pytest

python -m cover6 baseline                         # verify s=2, n=6
python -m cover6 experiment --budget default --seed 0
python -m cover6 boundary --s 2.33
python -m cover6 search --n 6 --s-list 2.0 2.05 2.10 --budget default
python -m cover6 search --n 7 --s-list 2.0 2.05 2.10 --budget default
python -m cover6 verify artifacts/baseline/n6_s2_trivial.json
python -m cover6 plot artifacts/baseline/n6_s2_trivial.json --out /tmp/cover
```

Reproducible default seed: `0`.

## Coverage checks

For a candidate `(s, poses)` the code reports:

1. **Dense sampling** of the target square and its boundary (Chebyshev
   “outside amount” in each unit square’s local frame).
2. **Polygon uncovered area** of `[0,s]² \ ∪ squares` via shapely.
3. **Uncovered boundary length** of the target perimeter.
4. A slightly **eroded** target (`buffer(-1e-9)`) for a stricter pass/fail.

A configuration is marked `covered` only if the uncovered area is \(\le 10^{-8}\),
the uncovered boundary is \(\le 10^{-6}\), and every sample (including the four
corners) is covered.

Interior search for \(n=6\) found no \(s>2\) covering. A separate **boundary**
ansatz (`python -m cover6 boundary --s 2.33`) produces a verified perimeter
covering of a square with side \(2.33\) whose interior is *not* covered; see
[`RESULTS.md`](../RESULTS.md).

## Parameterization

Each covering square is a rigid unit square with center `(cx, cy)` and
rotation `θ ∈ [0, π/2)` (square symmetry). For \(n=6\) this is 18 numbers.
A reduced C4 ansatz orbits one prototype square about the target center and
adds the remaining squares as free poses.

The target is always the axis-aligned square `[0,s] × [0,s]`. W.l.o.g. the
target is not rotated.

## References

- Dósa, Lángi, Tuza, *Covering a square by congruent squares*,
  [arXiv:2601.16535](https://arxiv.org/abs/2601.16535).
- Friedman–Paterson, *Covering squares with unit squares*,
  [erich-friedman.github.io/papers/covering](https://erich-friedman.github.io/papers/covering/covering.html).
- Green’s \(n=7\) covering: side \(3/2 + 1/\sqrt{2}\), area \(11/4 + 3/\sqrt{2}\).
