# STATUS: S(6)=2 proof attempt

**Bottom line: S(6)=2 is NOT proved.**
**No continuum kill of fat C moduli; no a-interval closed.**

## This round — L-moduli continuum cover
1. **Explicit parameterization:** M(a,δ)=Θ×[0,1]² where Θ=admissible angles for
   S=Γ∪{p_top} (single interval ≈[18°,81°] near a_φ) and (α,β) slide in R(θ).
   (`bnb/pose/moduli_L_cover.py`)
2. **Continuum certificates** (Lipschitz excl-margin / extent — not Monte Carlo):
   kill only a **thin slide-boundary** layer (~1–4% of vol(M)).
3. **CORE nonempty:** certified positive-volume subcell
   θ∈[~31°,~69°], α,β∈[0.4,0.7] (~5.4% of Θ×[0,1]²) on which every embedding
   covers the exclusive disk (grid+margin check). Matches Free-space topology:
   V_disks ∪ Free(S) ∪ F_strip leaves **no** uncovered witness on the core.
4. Open B F-needle: **skipped** (no analytic path beyond FHeight; a_top unchanged).
5. Prior: OpenB-FHeight / R2TopDiam proved; δ≥2g0 retracted; moduli sampling certs failed.

## Sharpest remaining
1. Meet deep-δ **CORE** L-moduli on (2,a_φ] — needs invariant beyond strip/Free witnesses
2. Open B C-on-top (2,a_top]; C-on-right (2,a_cr]
3. Razor (2,a_ψ]

## Proved?
**No.**

## Round (2026-10-07 21:45 CST) — approach triage, no closure
- Perimeter/boundary-length + area deficit: boundary of side a needs length 4a>8; six unit squares
  can supply boundary length up to 6·√2-type chords, so S_bd(6)=1+√2>2 shows no pure boundary count works;
  combined with area deficit 6-a²≈2 the slack is too large near a→2+. Not viable alone.
- Weighted density: any density must give weight ≤ 1/6 of total per unit square in every pose; the 2x2-grid
  + 2 spare squares config has 2 full squares of slack at a=2, so a fixed density cannot separate a=2 from a>2. Fails.
- Rigidity at a=2: the extremal covers at a=2 are NOT isolated (two spare squares free), so local
  perturbation analysis has a positive-dimensional moduli set; same obstruction as the fat CORE lobe.
- No case closed. Remaining list unchanged.

## Round 2026-10-07 ~22:00 CST: LP duals / multi-exclusive disks: FAILED (see lp/LP_NEGATIVE.md)
Fractional covering bound near a=2 is about 5.19 < 6, and at most 5 pairwise-exclusive points fit, so neither approach can
close anything without the full forced-incidence structure. Core kill fraction unchanged (~2-4%).

## Round 2026-10-07 ~22:10 CST: quantitative rigidity (V_i -> grid quarters): FALSE
rigidity/nonrigid_a2.py: a cover of [0,2]^2 by 6 unit squares (checked with Shapely, uncovered area 0) in which the vertex item
V3 is tilted 20 deg (centre (0.3,1.7)); C=[0.05,1.05]x[1,2] holds the centre and F patches the left sliver.
Limits of covers as a->2+ therefore include non-grid V placements, so no epsilon(a)->0 rigidity
for the V_i holds, and the 'thin cross' reduction (B) has no valid premise. The cross length count itself
(two unit squares cover at most 2*sqrt2 < 4 of a thin plus) would be sound IF U contained such a cross.
No case closed.

## Round 2026-10-07 ~22:25 CST: a=2 families and slack numerics (rigidity/slack.py), floating point only
Powell search minimizing uncovered area of [0,a]^2, 6 random restarts per start:
 grid start: a=2.001 2.1e-4, 2.01 7.9e-4, 2.03 8.3e-3
 tilted-V3 start: a=2.001 1.0e-4, 2.01 4.5e-4, 2.03 4.6e-3
No positive slack direction (no cover with a>2 found). The deficit looks sublinear in a-2 (~(a-2)^0.65 between
2.001 and 2.01), which hints that the tilted family degenerates softly. Optimizer noise is large, so this is NOT a scaling law.
No family classification is certified. No case closed.

## Round 2026-10-07 ~23:30 CST: family enumeration + growth table (rigidity/families.py, families.jsonl), floating point only
a=2 random global search: 13/48 runs reach uncovered area <1e-9. Tilted items (>2 deg) per run: 1 (1 run), 2 (2), 3 (3), 4 (7).
So the a=2 moduli space is large: many covers have several tilted items. Clustering by type is not done beyond this count.
Min uncovered area, 12 Powell restarts each:
 a      : 2.0005  2.001   2.002   2.004   2.008   2.016
 grid   : 4.4e-5  2.7e-4  1.9e-4  3.1e-4  3.7e-4  2.1e-3
 tilt   : 5.2e-5  1.0e-4  1.5e-4  6.5e-5  5.4e-4  9.4e-4
Fitted exponents (log-log): grid ~0.86, tilt ~0.76. Rows are non-monotone, so the optimizer is far from converged
and these are upper estimates of the true minima. No near-zero deficit at any a>2, so no counterexample sign.
No clean linear lower bound, so no interval-certified local kill was attempted. No case closed.

## Round 2026-10-07 ~23:55 CST: literature and new tool
- Literature: arXiv 2601.16535 still lists S(6)=2 as Conjecture 1.1 (known: 6<=Pi(2)<=7). NEW: Sriswasdi,
  arXiv 2609.15876 (Sep 2026) proves 17 unit squares cannot cover 4+eps, by counting perimeter/grid-line length plus spill area.
- Lemma GridLen (gridlen/verify_gridlen.py, interval-checked, valid for every a>2; it relies on Lemmas 1-5 of 2609.15876, which we have NOT re-proved):
  any 6-cover has (nc,nd,ns,n_interior) in {(0,4,1,1),(0,4,2,0),(1,5,0,1),(1,5,1,0)}.
  In particular: (i) at least one non-corner tile meets bd(S) (C and F cannot both be interior);
  (ii) at most one corner has 2 double-sided tiles; (iii) at most 1 interior tile.
- Spill-area step does NOT transfer: the area slack at n=2 is about 2 (vs 1 at n=4); the spill bound (b^2-1)/2 per side tile is far too small.
- Not yet cross-checked against the k / Open A-B-C taxonomy to see whether (i)-(iii) kill a whole open case. That is the best lead.
- Helly/KKM nerve idea: not attempted (no concrete statement found). No case closed.

## Round 2026-10-08 ~00:10 CST: GridLen lemmas re-checked (gridlen/LEMMAS.md)
- L1, L3, L4 (perimeter part), L5: proved. **L2 of arXiv 2609.15876 is FALSE** (exact counterexample with total 3sqrt2-2 > 1.5sqrt2,
  for both n=2 and n=4). That also opens a gap in that paper's n=4 Theorem 1: extra type-mixes survive.
- GridLen conclusions for n=6 are robust, but they are implied by the existing taxonomy, so they add no new B&B cut.
  Kill fraction unchanged. Grid refinement offers no help (spacing <1). No case closed.

## Round 2026-10-08 ~00:30 CST: core probe + L2 exact
- gridlen/L2_COUNTEREXAMPLE.md + l2_exact.py: sympy-exact. Total 3sqrt2-2-2eps/n > 1.5sqrt2 for eps<0.1213n, for all n>=2.
- rigidity/core_probe.py: a=2.005, delta=0.01 dfit, C fixed at the core pose (alpha=beta=0.55, theta=35/45/60 deg); the other 5 squares
  free (meet constraints on V_i NOT imposed), 16 Powell restarts.
  Min uncovered area is 3.4e-3 to 4.1e-3 (about 2*0.7*(a-2), i.e. LINEAR in a-2). The uncovered set is always two thin horizontal strips
  of height a-2 (y in [0,eps] and [1,1+eps]), spanning a column of width ~0.7 on one side of C (x in ~[1.3,a] or [0,0.82]),
  covered by two stacked axis-aligned squares.
  Reading: once C is pinned in the core, the deficit comes from a column of height a>2 and width ~0.7 next to C that gets only
  two items (a vertical-stacking obstruction), not from anything near p_top or Gamma.
  Candidate invariant (NOT proved): with C in the core, S\C contains a rectangle of width w>=w0 and height a whose
  cover needs >=3 items, while the counting leaves only 2. This needs the item-assignment step (which items can reach the column), i.e. a 5-item
  (15-dim) residual B&B. Not built yet.
- Core kill fraction: unchanged (~2-4% of Theta x [0,1]^2). No case closed.

## Round 2026-10-08 ~00:50 CST: two-square strip lemma (strip/STRIP.md)
Reduction proved: covering w x h (h>2) by 2 squares forces a trapezoid of average height >1. Numerically T(w)<=1 iff w>=~0.51 (not certified).
Applying it to the core FAILS as stated: F reaches the right column (3 items there), the columns are within sqrt2 of each other, and C overlaps them.
Core kill fraction unchanged. No case closed.

## Round 2026-10-08 ~01:00 CST: six structural ideas tested (ideas/VERDICTS.md). None viable; no case closed.

## Round 2026-10-08 ~01:20 CST: L2 audit (gridlen/L2_AUDIT.md)
Lemma 2 of 2609.15876 is false under its own definitions (exact sympy check, n=4, including a positive-length side contact). The proof
misses the parallel interior grid line. Theorem 1 does not follow as written; a joint-bound repair fails narrowly (numerical).
Also: that paper miscites DLT as proving S(6)=2 (DLT state it as a conjecture).

## Round 2026-10-08 ~00:35 CST: 15-dim B&B prototype (bnb15/RESULTS.md)
One tiny C-subcell at a=2.005: 22% / 52% / 68% of the volume killed after 1 / 5 / 20 min; open fraction ~t^-0.29, memory-bound.
Projected total time: infeasible (astronomical), even for one subcell, with ~7e4 subcells per slice. No closure.
