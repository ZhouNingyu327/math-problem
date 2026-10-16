"""Axis-direction X-ray relaxation reduces to 1D: exist tilts th_i in [0,45deg] and shifts t_i with
sum_i T_{th_i}(t - t_i) >= a on [0,a], T_th = chord profile of a unit square tilted th (trapezoid, area 1,
support cos+sin, plateau cos-sin, height 1/cos). (Same shifts work for x and y.)  Maximise margin."""
import numpy as np, math, sys
from scipy.optimize import minimize, differential_evolution
def T(x, th):
    c, s = math.cos(th), math.sin(th); H = 1/c; w = c+s
    x = np.asarray(x)
    if s < 1e-12: return np.where((x>=0)&(x<=1), 1.0, 0.0)
    return np.clip(np.minimum(H*x/s, H*(w-x)/s), 0, H)
def margin(z, a, ts):
    th = np.clip(z[:6], 0, math.pi/4); sh = z[6:]
    tot = np.zeros_like(ts)
    for i in range(6): tot += T(ts - sh[i], th[i])
    return (tot - a).min()
a = float(sys.argv[1]); ts = np.linspace(0, a, 4001)
bounds = [(0, math.pi/4)]*6 + [(-1.5, a)]*6
r = differential_evolution(lambda z: -margin(z, a, ts), bounds, seed=int(sys.argv[2]), maxiter=3000, popsize=40, tol=1e-12, polish=False, workers=1)
print(a, 'margin', -r.fun, 'tilts(deg)', np.degrees(np.clip(r.x[:6],0,math.pi/4)).round(3).tolist(), 'shifts', r.x[6:].round(4).tolist())
