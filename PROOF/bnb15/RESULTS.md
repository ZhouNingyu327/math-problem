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
