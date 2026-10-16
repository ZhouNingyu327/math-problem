# 15-dim pose B&B prototype (bnb15.py), 2026-10-08
Setup: a=2.005, delta=0.01 dfit. C fixed to the subcell theta in [45,45.5] deg, alpha,beta in [0.55,0.56] (C pose hull taken from 5 theta samples + pad 2e-3;
NOT a certified hull). V1..V4 centres within sqrt2/2 of their corners, F centre within sqrt2/2 of the right residual, angles in [0,90].
Kills: an item surely misses its forced point(s) (corner / F residual points), or some grid point (41x41, the 1295 that C surely misses)
is surely missed by all five. float64 outward intervals + margin 1e-9 (not mpmath).
Single core, ~1650 boxes/s, priority = largest volume first:
  t=60s:   killed 22.2%  (open boxes 75k)
  t=300s:  killed 52.1%  (open 370k)
  t=1200s: killed 67.9%  (open 1.43M, ~10 GB of the 15 GB RAM in use)
Open fraction ~ t^-0.29, so reaching 0 on ONE tiny C-subcell would take astronomically long (>1e6 x longer), and memory blows up first.
The core has ~(38deg/0.5deg)*(0.3/0.01)^2 ~ 7e4 such subcells per (a,delta) slice. VERDICT: infeasible as built.
Needed to make it viable: much stronger per-box tests (the meet incidences V3-V4 on top, Cascade/FG stub constraints, Prop L on quarters,
exclusive disks) and depth-first refinement with box-local witness points. Even then the scaling looks hopeless without a structural reduction.

## v2 (bnb15b.py), 2026-10-08 15:45-17:00 CST
Added: edge-host restrictions from MEET/CASCADE (left side only V1,V4; top only V4,V3 [Case I]; V1,V4 miss the right side; V2,V3 miss the bottom... see code;
F misses the left side), forced-singleton coupling (a witness with a unique possible host forces that host; two forced points of one item
more than sqrt2 apart kills), DFS per root (memory-bounded), 64 roots on 8 cores, per-root JSONL checkpoints.
NOT implemented: Prop L quarter kills, exclusive disks, adaptive per-box witnesses, symmetry reduction, KKT pruning.
Same subcell (a=2.005, delta=0.01 dfit, theta in [45,45.5], alpha,beta in [0.55,0.56]), float64 + 1e-9 margin, C hull sampled (not certified).
Run 1 (41x41 witnesses, 300 cpu-s/root): killed after 7.5 / 37.5 / 150 / 300 cpu-s per root = 32.8% / 55.4% / 67.8% / 85.5%; 32/64 roots cleared
  (clear times spread 13-290 s).
Run 2 (51x51 witnesses, 600 cpu-s/root, the 32 uncleared roots restarted): 7 more cleared; these roots reach 80.4%.
Overall: 90.2% of subcell volume killed, 39/64 roots cleared, ~2.7e7 boxes, ~5.3 CPU-hours.
Convergence: many uncleared roots STALL (e.g. 14: 57.8->58.2%, 15: 82.8->82.9%, 30: 31.8->33.5%, 62: 35.0->36.6% between 450 and 600 s).
  This is consistent with boxes where some configuration covers every FINITE witness point while leaving real gaps. A fixed witness grid
  cannot kill those; adaptive witnesses (exact uncovered-region test per box) are required.
Projection: even at ~10 CPU-hours per subcell, the core needs ~7e4 subcells per (a,delta) slice times many slices, i.e. ~1e6+ CPU-hours.
VERDICT: not convergent as built; infeasible at full-core scale without a structural reduction. No case closed.
