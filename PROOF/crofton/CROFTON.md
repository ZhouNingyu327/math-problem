# Direction 2: Crofton / line-section (X-ray) arguments, 2026-10-08

**Verdict: no closure. The linear (Crofton-integrated) form is a special weighted-area argument, so the LP obstruction applies to it.
The axis-direction pointwise form is provably too weak (exact construction at a=2.2). The all-direction pointwise form is a genuine
relaxation of covering, but it carries no configuration-free certificate, and the numerics are inconclusive.**

Relaxation X(a), for a configuration Q_1..Q_6: for every line L, sum_i |Q_i ∩ L| >= |S_a ∩ L|. Every cover satisfies X(a).

1. **Linear consequences = weighted area (proved, elementary).** For any nonnegative weight w on lines,
   sum_L w(L)|K ∩ L| = ∫_K W_w(x) dx, where W_w(x) = ∫_{L∋x} w(L) (Fubini). So any fixed-weight sum of the X-ray inequalities is a
   weighted-area inequality with the density W_w >= 0. These densities form a subclass of the densities in lp/LP_NEGATIVE.md, where
   the best density gives only 6/1.156 ≈ 5.19 < 6 squares near a=2 (numerical). Hence no Crofton/integral-geometric
   counting argument with configuration-independent weights can prove S(6)=2. This also covers covariogram-type counting: such
   arguments bound sum_{i,j}|Q_i∩(Q_j+v)|, whose cross terms are unbounded.
2. **Axis-only pointwise form is too weak (rigorous, exact rationals; axis1d_exact.py, axis1d_exact.log).** With every square
   given the same rotation (cos,sin)=(15/17,8/17) (28.07°) and centres (m_i, m_sigma(i)), both axis X-rays reduce to a 1D sum of
   trapezoids. Exact check at breakpoints: at a=21/10 the margin is 1/6 > 0, and at a=11/5 it is 11449/300000 > 0. So six unit squares can
   dominate the horizontal and vertical line sections of [0,2.2]^2. Line sections in the two axis directions (even pointwise
   per line) cannot prove anything below a=2.2. Numerically (axis1d.py, differential evolution) the axis form stays satisfiable at a=2.2 with mixed tilts.
3. **All-direction pointwise form.** The same construction badly violates the 30°–150° directions (deficit up to 1.7 at a=2.1). Powell/NM
   searches with 180 directions found no X-feasible configuration at a=2.005 (best max deficit 0.010 ≈ 2(a-2)). An earlier
   36-direction search "succeeded" only by exploiting the sparse direction sampling: a dense recheck gave deficit 0.27 (xray_check.py).
   So it is open whether X(a) is infeasible for all a>2. Even if it is, X(a) has the same "for all configurations" quantifier as covering, with no dual
   certificate (by item 1), so proving infeasibility needs per-configuration work (a B&B in pose space). Not pursued as a proof route.
