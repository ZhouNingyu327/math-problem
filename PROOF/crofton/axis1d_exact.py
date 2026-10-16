"""Rigorous: axis-direction X-ray relaxation is satisfiable at side a (exact rational check).
All six squares have the same rational rotation (c,s) (Pythagorean), so the chord profile along horizontal lines
(as a function of height) is a trapezoid: support length c+s, plateau c-s, height 1/c, area 1; vertical lines give the
same profile. Taking centres (x_i,y_i) = (m_i, m_sigma(i)) with any permutation sigma, both axis X-rays reduce to the 1D sum
F(t) = sum_i T(t - m_i). F is piecewise linear, so min over [0,a] is attained at a breakpoint or endpoint: checked exactly."""
import numpy as np, math, sys
from fractions import Fraction as Fr
from scipy.optimize import differential_evolution
c, s = Fr(sys.argv[2]), Fr(sys.argv[3]); assert c*c + s*s == 1 and c >= s >= 0
a = Fr(sys.argv[1])
def T(x):  # exact trapezoid, centred at 0
    w = c + s; H = 1/c; x = abs(x)
    if x >= w/2: return Fr(0)
    if x <= (c - s)/2: return H
    return H*(w/2 - x)/s
cf, sf, af = float(c), float(s), float(a)
def Tf(x):
    w = cf+sf; H = 1/cf; x = np.abs(x)
    return np.clip(H*(w/2 - x)/sf, 0, H)
ts = np.linspace(0, af, 3001)
f = lambda m: -(sum(Tf(ts - mi) for mi in m) - af).min()
r = differential_evolution(f, [(-0.7, af+0.7)]*6, seed=0, maxiter=2000, popsize=40, tol=1e-12, polish=True)
m = [Fr(round(v*10000), 10000) for v in sorted(r.x)]
bps = {Fr(0), a}
for mi in m:
    for d in [-(c+s)/2, -(c-s)/2, (c-s)/2, (c+s)/2]:
        if 0 <= mi + d <= a: bps.add(mi + d)
marg = min(sum(T(t - mi) for mi in m) - a for t in bps)
print(f"a={a} (c,s)=({c},{s}) tilt={math.degrees(math.atan2(sf,cf)):.3f}deg centres={[str(v) for v in m]}")
print("EXACT min over [0,a] of sum of chords minus a =", marg, "=", float(marg), "->", "AXIS X-RAY SATISFIED" if marg >= 0 else "fails")
