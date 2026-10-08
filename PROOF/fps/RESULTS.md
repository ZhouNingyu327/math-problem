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
| 2.04 | 15x15 grid + 7 orbits (281)| 40185  | 7         | running                      |
Uniform odd grids: k=15 is coverable at 2.05 (cover found), but certifies 2.06. Even k is useless (4 squares cover any even grid up to
about 2.1, since no points lie on the midlines).
These bounds are weaker than the existing case analysis (all a > 2.03617 already closed). They are an independent and much
smaller audit trail for that range. The aim was to push a0 below 2.03617 (lazysym at 2.035 and 2.03 running).
