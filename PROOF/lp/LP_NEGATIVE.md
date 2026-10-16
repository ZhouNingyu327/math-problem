# Fractional-LP / dual-weight approach: obstruction (numerical, 2026-10-07)
lp/frac_lp.py: 13x13 grid on [0,2.01]^2, 7748 sampled poses -> LP dual 6.0, but this is an
artifact of under-sampled poses: dense check (180 angles x 120^2 centres) gives max pose weight
1.156, so the honest dual bound is 6/1.156 ~ 5.19 < 6.
Consequence: no global dual weighting on a finite point set can certify >6 squares near a=2
(fractional covering number ~5.2). With C fixed anywhere, the residual is about 4.03 < 5, so a per-cell
LP also fails unless the forced incidence structure of V1-V4/F is encoded, which is exactly
what the existing pose B&B already does. The same counting kills the multi-exclusive-disk idea:
points that pairwise need different squares (distance >sqrt2) number at most 5 in a side-2.01 square.
Status: approach FAILS (obstruction, not a bug). No case closed.
