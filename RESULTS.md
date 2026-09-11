# Results: covering a square with 6 unit squares

The primary research object is the proof attempt in
[`PROOF_ATTEMPT.md`](PROOF_ATTEMPT.md). That write-up does **not** establish
\(S(6)=2\); it proves a combinatorial classification and closes one
combinatorial subfamily for sides \(a>\sqrt{5}\).

**Numerics are not a proof.** This file records what the code in `cover6/` actually computed.

Notation: \(S(n)\) is the largest edge length of a square that can be covered by \(n\) unit squares (rigid motions and overlaps allowed). \(S_{\mathrm{bd}}(n)\) is the analogous quantity for covering only the **boundary**.

## 结论 / Conclusion (short)

| Question | Numerical outcome |
|----------|-------------------|
| Does the trivial \(s=2\) covering with \(n=6\) pass a shapely + sampling check? | **Yes.** Uncovered area \(=0\). |
| Did any \(s>2\) candidate for \(n=6\) survive a rigorous interior coverage check? | **No.** Best fully covered side remains \(s=2\). |
| Does that prove \(S(6)=2\)? | **No.** |
| Boundary only: can 6 unit squares cover the perimeter of a square with \(s>2\)? | **Yes, numerically.** A verified construction covers the boundary at \(s=2.33\) (interior has a large star-shaped hole). This is consistent with \(S(5)=2 < S_{\mathrm{bd}}(5)\approx 2.072\). |

中文：平凡的边长 2 覆盖通过了严格检查。针对 \(n=6\)、边长 \(s>2\) 的内部覆盖，96 次多起点搜索均留下正的未覆盖面积，**没有**任何 \(s>2\) 的候选通过 shapely 多边形检验。这**不是** \(S(6)=2\) 的证明。另一方面，六个单位正方形**可以**在数值上覆盖边长 \(s=2.33\) 的正方形**边界**（内部有大洞），说明 \(S_{\mathrm{bd}}(6)\ge 2.33\) 是一个数值下界候选，类似于 \(n=5\) 时“边界比内部更容易”的现象。

## Known facts used

- \(S(5)=2\) is proved (Januszewski; Dósa–Lángi–Tuza [arXiv:2601.16535](https://arxiv.org/abs/2601.16535)). Hence \(S(6)\ge 2\).
- Area bound: \(S(6)\le\sqrt{6}\approx 2.449\).
- Best published **interior** construction for \(n=6\) is the trivial side-2 tiling (area 4).
- Conjecture (Dósa–Lángi–Tuza, 2026): \(S(6)=2\).
- \(S(3)=\sqrt{\varphi}\approx 1.272\) (Dudeney); reconstructed and verified here.
- \(S(7)\ge 3/2+1/\sqrt{2}\approx 2.207\) (Trevor Green, area \(11/4+3/\sqrt{2}\)). Exact published coordinates were not reconstructed; the optimizer did **not** rediscover a full \(n=7\) covering with \(s>2\).

## Pipeline

Each candidate \((s,\text{poses})\) is tested in two ways:

1. Dense sampling of the filled square, the four sides, and the four corners (Chebyshev outside-amount in each unit square’s local frame).
2. Exact polygons (shapely): uncovered area of \([0,s]^2\setminus\bigcup\) squares, and leftover length of the target perimeter.

A configuration is marked `covered` only if uncovered area \(\le 10^{-8}\), uncovered boundary \(\le 10^{-6}\), and every sample (including corners) is covered. A slightly eroded target (`buffer(-1e-9)`) is used for `covered_strict`.

Repro (seed `0`):

```bash
python -m pip install -r requirements.txt
python -m pytest
python -m cover6 baseline
python -m cover6 experiment --budget default --seed 0
```

Elapsed wall time of the committed default experiment: **852 s** (~14 min) on 4 CPUs.

## Interior covering, \(n=6\)

### Baseline \(s=2\)

Four axis-aligned unit squares tile \([0,2]^2\); two extras sit at the center.  
Artifact: [`artifacts/baseline/n6_s2_trivial.json`](artifacts/baseline/n6_s2_trivial.json)

- uncovered area \(=0\)
- uncovered boundary \(=0\)
- `covered_strict = true`

Negative control: the same 2×2 block on a square of side \(2.05\) leaves a plus-shaped gap (uncovered area \(\approx 0.152\)).

### Adiabatic growth

Starting from the trivial covering and increasing \(s\) in steps of \(0.01\), coverage **breaks immediately at \(s=2.01\)** (uncovered area \(\approx 0.089\)). The trivial layout does not deform into a larger covering under local search.

### Multi-start search

96 trials at \(s\in\{2.0, 2.02, 2.05, 2.10\}\): structured seeds (corners, midpoints, Type I bent strip, C4 rotations), jitter, dual annealing, and a reduced C4 parameterization. Seed `0`.

| \(s\) | min shapely uncovered area | fully covered? |
|------|----------------------------|----------------|
| 2.00 | \(0\) | yes |
| 2.02 | \(0.0245\) | **no** |
| 2.05 | \(0.0740\) | **no** |
| 2.10 | \(0.1542\) | **no** |

The leftover area grows with \(s-2\), as one would expect from a plus-shaped gap that two extra squares cannot close while the four corners stay covered.

**Best fully covered \(s\) for \(n=6\): \(2.0\).**  
No \(s>2\) candidate survived the polygon check.

## Boundary covering, \(n=6\) (not the original \(S(6)\) problem)

Dósa–Lángi–Tuza determine \(S_{\mathrm{bd}}(n)\) for all \(n\equiv 0,1\pmod{4}\) (in particular \(S_{\mathrm{bd}}(5)\approx 2.072> S(5)=2\)), and leave \(n=6\) open.

Ansatz: four maximal vertex L-embeddings (Lemma 2.2) with long legs on a pair of opposite sides, plus two \(45^\circ\) side-squares whose diagonals cover length \(\sqrt{2}\) on the other pair. Equal-side length of this family is
\[
s_\star = 2\sqrt{\frac{1+\sqrt{3}}{2}}\approx 2.33754,
\]
the unique \(s=2x\) with \(x\sqrt{x^2-1}=\sqrt{2}/2\).

Local polish of this seed, checked with shapely:

| \(s\) | uncovered **boundary** | uncovered **area** (interior hole) | corners uncovered |
|------|------------------------|--------------------------------------|-------------------|
| 2.00 | \(0\) | 0.388 | 0 |
| 2.15 | \(0\) | 1.264 | 0 |
| 2.25 | \(0\) | 1.526 | 0 |
| 2.30 | \(0\) | 1.721 | 0 |
| 2.32 | \(0\) | 1.791 | 0 |
| 2.325 | \(0\) | 1.816 | 0 |
| **2.33** | **\(0\)** | **1.823** | **0** |
| 2.33754 | \(7.8\times 10^{-4}\) | 1.863 | 1 |

At \(s=2.33\) the leftover perimeter is empty (shapely `boundary.difference(union)` is empty; 600-point boundary sample clean). The interior is **not** covered: a star-shaped hole of area \(\approx 1.82\).

Artifacts: [`artifacts/boundary_n6/best_boundary.json`](artifacts/boundary_n6/best_boundary.json), figure `best_boundary.png`.

This is a **numerical lower bound candidate** \(S_{\mathrm{bd}}(6)\ge 2.33\), not a proof. It also shows the checker will report coverage when a covering (here: of the perimeter) actually exists.

## \(n=7\) control (incomplete)

Green’s covering shows \(S(7)\ge 2.207\), so every \(s\le 2.207\) is feasible in principle (a covering of a larger concentric square covers a smaller one after a suitable placement). The same optimizer:

| \(s\) | min uncovered area | fully covered? |
|------|--------------------|----------------|
| 2.00 | \(0\) | yes (trivial) |
| 2.05 | \(0.00392\) | **no** (near miss) |
| 2.10 | \(0.0280\) | no |
| 2.15 | \(0.107\) | no |

The search **did not** recover Green’s construction and **did not** certify any \(s>2\) covering for \(n=7\). The \(s=2.05\) hole of size \(\sim 4\times 10^{-3}\) is much smaller than the \(n=6\) hole at the same \(s\) (\(\sim 7\times 10^{-2}\)), but a near miss is still a miss.

So the \(n=6\) negative search should **not** be read as “the optimizer would have found a covering if one existed.” It is only evidence that several natural families and a moderate global search failed.

## Checker sanity (positive)

- \(n=3\), Dudeney / Friedman equality case \(s=\sqrt{\varphi}\): uncovered area \(\sim 10^{-31}\), `covered_strict=true`. Artifact: [`artifacts/known/n3_dudeney.json`](artifacts/known/n3_dudeney.json).
- \(n=4\) and \(n=6\) trivial \(s=2\): exact cover.
- Boundary construction above: perimeter covered at \(s=2.33\).

## Honest limitations

1. 18-dimensional rigid-motion search is non-convex. Dual annealing with the default budget is not an exhaustive search of pose space.
2. Failure to find Green’s \(n=7\) covering shows false negatives are possible.
3. Thin gaps of width \(s-2\) can hide between a coarse sample grid; the committed conclusions use shapely area/boundary, not sampling alone.
4. Floating-point polygons can hide or fake slivers at scale \(10^{-16}\); we require empty leftover polygons and a strict negative buffer for interior “covered.”
5. Nothing here substitutes for a case analysis in the style of the \(S(5)=2\) proofs.

## Files

| Path | Contents |
|------|----------|
| `artifacts/baseline/` | Trivial \(s=2\) (pass) and \(s=2.05\) gap (fail) |
| `artifacts/known/` | Dudeney \(n=3\); Type-I seed for Green \(n=7\) (not a covering) |
| `artifacts/search_n6/` | Search log, grow log, best interior trials, plus-shaped hole figure |
| `artifacts/search_n7/` | Search log; \(s=2.05\) near-miss |
| `artifacts/boundary_n6/` | Boundary covering at \(s=2.33\) and \(s=2.25\) |
| `artifacts/experiment_summary.json` | Machine-readable summary of the default run |

## References

- G. Dósa, Z. Lángi, Z. Tuza, *Covering a square by congruent squares*, [arXiv:2601.16535](https://arxiv.org/abs/2601.16535).
- E. Friedman, D. Paterson, *Covering squares with unit squares*, Geombinatorics 15 (2006); [online figures](https://erich-friedman.github.io/packing/squcosqu/).
- J. Januszewski, *A note on covering a square of side length \(2+\varepsilon\) with unit squares*, Amer. Math. Monthly 116 (2009).
- H. E. Dudeney, *Puzzles and Curious Problems*, Problem 219 (three tablecloths).
