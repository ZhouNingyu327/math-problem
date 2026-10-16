# Two-square strip lemma (2026-10-08)
Claim S2: two unit squares A,B cannot cover R=[0,w]x[0,h] with h>2 once w >= w*, where w* ~ 0.51 (numerical).
Reduction (rigorous):
 - The corners BL,TL are >2>sqrt2 apart, so they lie in different squares; the same holds for BR,TR. BL and TR are also >sqrt2 apart.
   Hence WLOG A holds BL,BR and B holds TL,TR.
 - A meets the left side in [0,yL] and B meets it in [yL',h] with yL'<=yL; likewise yR'<=yR on the right. By convexity A contains the trapezoid
   with base [0,w]x{0} and heights yL,yR, and B contains the mirrored one with heights h-yL', h-yR'.
   One of them therefore has average height >= h/2 > 1.
 - So S2 holds for every w with T(w) <= 1, where T(w) = max average height of a "bottom-horizontal, vertical-sided" trapezoid of width w in a unit square.
T(w) numerics (trap2.py, 300 Nelder-Mead starts, exact chord formula):
 w=0.40: 1.0687, 0.45: 1.0362, 0.48: 1.0184, 0.50: 1.0072, 0.52: 1.0000, 0.55/0.6/0.7: 1.0000 (attained axis-aligned).
 At 45 deg, T = sqrt2-w (crosses 1 at sqrt2-1); intermediate angles do better, so w* ~ 0.51.
STATUS: the reduction is proved. T(w)<=1 for w>=0.52 is NUMERICAL only. A proof needs an analytic argument near theta=0 (T=1 is
attained there, so a pure interval B&B degenerates).
Application to the meet core (step 2): NOT achieved. The core_probe "two items in the column" allocation is only the relaxed
optimum. In the real meet case F is forced onto the right residual {a}x(mu+delta, y_tip], so the right column receives V2, F and V4,
three items. The left column x<~0.82 and the right column x>~1.3 are within sqrt2 of each other (gap ~0.48-0.97), so a single item
can serve both. No pigeonhole closes, and C's 45-deg diamond spans x~[0.33,1.74], so the columns are not even C-free.
Core kill fraction: unchanged (~2-4%).
