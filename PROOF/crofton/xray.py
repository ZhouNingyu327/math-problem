"""Direction 2 test: line-measure (X-ray / Crofton) relaxation.
Relaxation R(a): for EVERY line L, sum_i |Q_i ∩ L| >= |S_a ∩ L|  (S_a=[0,a]^2).
Every cover satisfies R(a). We search for 6 unit squares satisfying R(a) for a>2 (sampled lines, float)."""
import numpy as np, math, sys
from scipy.optimize import minimize

def chord(t, ctr_proj, psi, side):
    # chord length of a square (side 'side', relative angle psi in [0,pi/4]) along lines n.x=t
    c, s = math.cos(psi), math.sin(psi)
    w = side*(c+s); lo = ctr_proj - w/2
    x = t - lo
    H = side/c
    ramp = side*s
    l = np.where(x <= 0, 0.0, np.where(x < ramp, H*x/np.maximum(ramp,1e-15), np.where(x <= side*c, H, np.where(x < w, H*(w-x)/np.maximum(ramp,1e-15), 0.0))))
    if ramp < 1e-12:
        l = np.where((x >= 0) & (x <= side), H, 0.0)
    return l

def rel(phi, th):
    d = (phi - th) % (math.pi/2)
    return min(d, math.pi/2 - d)

NPHI, NT = 180, 240
phis = np.linspace(0, math.pi, NPHI, endpoint=False)

def deficit(x, a, ret_max=False):
    poses = x.reshape(6, 3)
    tot = 0.0; mx = 0.0
    for phi in phis:
        n = np.array([math.cos(phi), math.sin(phi)])
        # S_a projections
        cS = n @ np.array([a/2, a/2])
        psiS = rel(phi, 0.0)
        wS = a*(math.cos(psiS)+math.sin(psiS))
        t = cS + (np.arange(NT)+0.5)/NT*wS - wS/2
        need = chord(t, cS, psiS, a)
        have = np.zeros_like(t)
        for cx, cy, th in poses:
            have += chord(t, n @ np.array([cx, cy]), rel(phi, th), 1.0)
        d = np.maximum(need - have, 0)
        tot += (d**2).sum(); mx = max(mx, d.max())
    return (tot, mx) if ret_max else tot

if __name__ == '__main__':
    a = float(sys.argv[1]); rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 0)
    best = None
    for rs in range(int(sys.argv[3]) if len(sys.argv) > 3 else 6):
        # start: 4 corner squares + 2 random
        x0 = [0.5, 0.5, 0, a-0.5, 0.5, 0, 0.5, a-0.5, 0, a-0.5, a-0.5, 0]
        x0 += list(rng.uniform([0.3, 0.3, 0], [a-0.3, a-0.3, 1.5])) + list(rng.uniform([0.3, 0.3, 0], [a-0.3, a-0.3, 1.5]))
        x0 = np.array(x0) + rng.normal(0, 0.05, 18)
        r = minimize(deficit, x0, args=(a,), method='Powell', options={'maxfev': 6000, 'xtol': 1e-7, 'ftol': 1e-14})
        tot, mx = deficit(r.x, a, True)
        print(f"a={a} restart {rs}: sumsq={tot:.3e} maxdeficit={mx:.3e}", flush=True)
        if best is None or tot < best[0]:
            best = (tot, mx, r.x)
        if mx < 1e-9: break
    print("BEST", best[0], best[1], best[2].round(6).tolist())
