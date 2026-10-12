# AUDIT3: second skeptical audit round (2026-10-10, ~09:30 CST)
Written by the same auditor as AUDIT2. I edited none of the existing files. My new scripts are in audit2_code/:
myn*.c, canonn.py, wcert.py, relp.py, wk.py and wk.out.

## Verdict summary
| Item | Verdict |
|---|---|
| (1) Own enumerator for general n: 0 classes for n = 4, 5, 6 and 27 for n = 7 | **CONFIRMED** |
| (1) Rules under weak convexity | Enumerator rules OK. **But Q(ad,bc) is NOT strict** when 4 vertices are collinear. |
| (2a) LP certificates in the weak setting | **GAP: 1,859 of 34,962 certificates are not weak-valid as claimed** |
| (2b) The 4,814 carried-over verdicts | **GAP: 9 classes are carried over on the translate lemma, which fails under weak convexity** |
| (2c) Saturation by distances only | Sound |
| (2d) Straight-vertex split (both formulations, several 180° vertices) | Sound as a method. 40 cases re-verified with my own code, 0 disagreements. |
| (2e) Weak 7-gon (27 classes) | **CONFIRMED** with my own code (25 unit, 2 zero-dim with D = 8) |
| (3) Write-ups | The strict-convex main result is consistent with the ledger. **The weak-convexity appendix overclaims** (details below). |

**Bottom line:**
- The strictly convex result (n_3 = 9) is unaffected by anything found here.
- The claim "n_3 = 9 also for weakly convex polygons" is **NOT yet established**: 1,407 octagon classes (1,859 − 461 + 9) lack a weak-valid refutation.

## (1) Enumerator for general n
My from-scratch DFS (same structure as AUDIT2/my.c, with N and P = N(N−1)/2 as parameters; files myn4.c … myn7.c, with myn7.c kept) gave:
- 0 labelled survivors for n = 4, 5, 6;
- 378 labelled survivors for n = 7, which collapse to **27 D_7 classes**.

Those 27 classes are equal as a set to both weak/s7w.txt and s7.txt. This means n ≤ 6 now rests on two independently written enumerators, not one.

**Rules under weak convexity** (distinct points on ∂K in boundary order, not all collinear):
- **E, C1, C3, C2:** OK. C3: the mirror points are strictly separated, so the line meets int K. C2: 3 collinear points of ∂K lie on a supporting line, which contradicts C3.
- **O:** OK. If chord jl is a supporting line, then the boundary arc through i is the segment [j,l], so p_i is the midpoint of jl. Thales gives exactly 90°, so all strict consequences still hold.
- **Q (ab,cd):** strict. In the collinear case the gap is 2|bc| > 0.
- **Q (ad,bc): NOT strict in general.** If a, b, c, d all lie on one side of K (possible once a side carries ≥ 4 of the points, i.e. two consecutive 180° vertices), then |ac| + |bd| = |ad| + |bc| exactly. weak/WEAK.md's "the same holds for (ad, bc)" is false in this case: [a,d] ⊇ [b,c], so the disjointness argument fails.
- **The enumerator's combinatorial use of Q is still sound.** A forbidden combination such as ac ≤ ad and bd ≤ bc would, in the collinear case, force ac = ad, i.e. c = d, which is impossible. So the 40,096 and 27 class sets stand.

## (2) Weak-convexity reasoning
**(a) LP certificates.** I re-checked all 34,962 certificates with my own code (wcert.py), treating TRI rows AND Q(ad,bc) rows as non-strict.
- 33,103 put positive weight on a strict row (Q(ab,cd) or O), or have a negative coefficient. These are weak-valid.
- **1,859 rely on strictness only through Q(ad,bc) rows**, so they are not valid for weakly convex realisations with 4 collinear vertices.
- I tried to re-solve these 1,859 with an LP that requires a genuinely strict row (relp.py):
  - 461 rescued, with exact rational certificates;
  - 500 are LP-infeasible, so no certificate exists from these rows;
  - 898 failed only at my naive rationalisation step and may well be rescuable.
- Open lists: wbad.json (1,398 classes) and winf.json (the 500).
- **Easy fix:** every such realisation has a 180° vertex, so running the straight-vertex split (already implemented) on these classes would close them, or show they stay open.

**(b) The 4,814 carried-over verdicts.**
- weak/classify.py marks an entry as "R-dist" whenever its hint factors are all distances. It does not exclude kind = "trans" (the "R+s" translate systems).
- The translate lemma needs STRICT convexity. Under weak convexity, conv(A) ⊕ [0,u] can carry a 6th point on an edge.
- **9 classes are carried over solely on translate systems: 363, 364, 365, 2128, 2148, 2150, 2155, 2171, 2173.** None of them was re-run in weak_alg or the straight split.
- The other 6 translate classes (38, 1408, 2130, 2357, 2370, 2540) were correctly re-done.
- The remaining tiers (raw-I, R-dist hint, sat-chain with distance-only hints, cert0-dist) look correct. They use only squared-distance factors.

**(c) Saturation by distances only:** sound. Points are distinct, so V(J) contains every weak realisation. The "nonconvex" test (two strictly opposite orientation signs) also excludes weak convexity, since a ccw weakly convex polygon has every orient(a<b<c) ≥ 0.

**(d) Straight-vertex split:** sound.
- Every weakly but not strictly convex realisation has at least one vertex with orient(i−1, i, i+1) = 0.
- Refuting every i covers polygons with several 180° vertices, since such a realisation lies in at least one J_i.
- For distinct points, the λ-formulation (λ(1−λ) ≠ 0) is equivalent to the orient = 0 formulation for a boundary vertex.
- Saturating by a subset of distance factors chosen mod p is sound.
- Re-verification: 40 random closed (class, i) entries from straight.jsonl, rebuilt with my own encoding and saturated by all 27 distances (wk.py). **40/40 agree**: all units are unit, and the nonconvex ones have the same vdim (4, 6, 6, 6, 4, 4).
- Limitation: for those nonconvex cases I compared only D. I did not independently re-certify the real points.

**(e) Weak 7-gon:** my own encoding with J = sat(I, all 20 distances) gives 25 unit and 2 zero-dim with vdim 8 (classes 8 and 13). This matches weak7.jsonl. The real-root convexity of classes 8 and 13 was not independently re-checked.

## (3) Write-ups
**note_en.pdf, main body** (strict convexity): consistent with the ledger (A 34,962 / B 5 / C 3,860 / C′ 1,077 / C″ 192). Minor issues:
- §3 says the classes satisfy "E, C1–C3, O, Q and TRI", but the enumerators do not use TRI. TRI is used only in the LP.
- Tier B mentions "Fact D2"; NOTES and AUDIT2 use Fact (D). The terminology should be harmonised.

**note_en.pdf appendix and report_zh.pdf caveat 3 / §(weak): OVERCLAIM.** Each of these statements is wrong or not established:
- "Q stays valid and strict": false for (ad,bc) with 4 collinear points.
- "All 34,962 Gordan certificates remain valid": false for 1,859, of which 461 were re-certified by me.
- "4,814 algebraic verdicts carry over": 9 of them are translate-lemma based.
- "n_3 = 9 also for weakly convex polygons [C]+[P]".
- "for n ≤ 6 this rests on a single enumerator": now outdated, since my enumerator confirms it.

**Recommended wording until fixed:** the weak-convexity octagon case is "reduced to 1,407 classes (1,398 LP gaps + 9 translate classes), which can be handled by the straight-vertex split". The strict result stands as stated.