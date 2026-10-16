# Direction 3: finite point-set (FPS) obstructions, 2026-10-08 (in progress)

**S(6)=2 is NOT proved.** This directory gives a solver-independent kind of certificate for "6 unit squares cannot cover side a0":
a finite point set P in [0,a0]^2 that no 6 unit squares cover.

## Method (fps.py, exactdfs.py, verify_cert.py)
* Superset family F. Use frames theta_k=(k+1/2)*90deg/K. A unit square with orientation within D/2 of theta_k lies in a frame-theta_k
  axis box of side s=cos(D/2)+sin(D/2) (=sqrt(1+sin D)) with the same centre. So every unit-square-coverable subset of P is contained
  in a candidate box set {p : u_p in [u_i,u_i+s'], v_p in [v_j,v_j+s']}, with s'=s+1e-9 to absorb float error (coordinates <=3, so
  rounding error is ~1e-15 << 1e-9). Dominated sets are removed. F is therefore an over-approximation: certificates are valid for
  squares of side s (K=360: s=1.00218), which is stronger than for unit squares.
* Sanity check: 20000 random unit squares, each covered subset is contained in a member of F (0 failures in every run).
* Exact check: bitset DFS (exactdfs.py). It branches on the uncovered point with fewest candidate sets, keeps only candidates
  maximal on the uncovered points (dominated choices can be swapped), and prunes with a greedy set of pairwise-incompatible points.
  Complete and independent of any MIP solver. HiGHS min-set-cover (optimum 7) is used only to search/guide.
* Lazy refinement (lazysym.py): odd k x k grid plus D4-orbits of points taken from the gaps of realised and polished near-covers.

## Certificates (each says: no 6 unit squares cover side a0, hence S(6) < a0)
| a0   | P                          | |F|    | HiGHS opt | exact DFS                    |
|------|----------------------------|--------|-----------|------------------------------|
| 2.15 | 7x7 grid (49 pts)          | 377    | 7         | NO 6-cover, 1.1e4 nodes, <1s |
| 2.10 | 11x11 grid (121)           | 4556   | 7         | NO 6-cover, 4.4e6 nodes, 5s (also K=1440, slack 1e-6) |
| 2.06 | 15x15 grid (225)           | 27387  | 7         | NO 6-cover, 3.0e8 nodes, 722s |
| 2.05 | 13x13 grid + 3 orbits (253)| 18561  | 7         | NO 6-cover, 6.3e8 nodes, 510s wall (pardfs, 3 procs; 136/136 root branches) |
| 2.04 | 15x15 grid + 7 orbits (281)| 40185  | 7         | NO 6-cover, 1.68e9 nodes, 2297s wall (pardfs, 3 procs; 181/181 root branches) |
| **2.03** | **17x17 grid + 112 added pts (401)** | 109633 (K=1440) | 7 | **NO 6-cover, 7.995e9 nodes, 11795.7s wall** (pardfs_sym, mirror-reduced + resume; 120/120 root classes) |
Uniform odd grids: k=15 is coverable at 2.05 (cover found), but certifies 2.06. Even k is useless (4 squares cover any even grid up to
about 2.1, since no points lie on the midlines).
These bounds are case-independent and monotone in a: S(6)<a0 closes every case on [a0, sqrt(6)].
Previously they were weaker than the hand case analysis above 2.03617; with a0=2.03 they now improve Open B C-on-top
and all of G2–G5 from above. Same float-enumeration caveat as every row: written error bound (rounding ~1e-15 << 1e-9 slack), not interval arithmetic.

## a=2.03 VERIFIED (2026-10-08 ~23:40 CST)
* Point set: 17x17 odd grid + 112 lazy-added points = **401 points** (`lazysym_2.03_1440_17.json`, K=1440, s≈1.00055).
* Exact bitset DFS with diagonal-mirror reduction (`pardfs_sym.py`): validity of the reduction checked exactly in code
  (sigma maps P onto P as an index permutation and F onto F by bitset equality; root point fixed by sigma).
  Final line of `pardfs_2.03_sym.log`:
  `EXACT PARALLEL DFS (mirror-reduced, resumed): NO 6 SETS COVER P nodes 7995493457, wall 11795.7s`.
* Hence **S(6) < 2.03** 【computer-verified, not interval arithmetic】.
* Consequence (see STATUS.md): all cases closed for a ≥ 2.03 (subject to the float caveat); G2–G5 open only on (2, 2.03);
  Open B C-on-top shrinks from (2, 2.03617] to (2, 2.03); other open cases unchanged.
* Reproduce: `python3 pardfs_sym.py lazysym_2.03_1440_17.json 1440 1e-9 6` (or `verify_cert.py` serial).

## Lower a (not certified)
* a=2.035, K=360, 15x15 base: after 2 lazy rounds (253 pts) still 6-coverable as a set system; superseded by the 2.03 certificate.
* a=2.025 seeded lazy (K=1440, 17x17 + scaled 2.03 points): `lazysym_2.025_seeded.log` / `lazysym_2.025_1440_17_seeded.json` (not yet an exact DFS certificate).
* Near-cover gaps are thin strips of width ~(a-2), so |P| grows like 1/(a-2). This route shrinks ranges from above only; it cannot reach a→2+.
