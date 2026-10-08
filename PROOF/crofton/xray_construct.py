import numpy as np, math, itertools, sys
import xray
xray.NPHI, xray.NT = 180, 400
xray.phis = np.linspace(0, math.pi, 180, endpoint=False)
a = float(sys.argv[1]); th = math.radians(float(sys.argv[2])); cs = [float(v) for v in sys.argv[3].split(',')]
best = None
cells = [(i, j) for i in range(3) for j in range(3)]
for sel in itertools.combinations(cells, 6):
    if any(sum(1 for c in sel if c[0] == r) != 2 for r in range(3)) or any(sum(1 for c in sel if c[1] == r) != 2 for r in range(3)):
        continue
    for signs in itertools.product([1, -1], repeat=6):
        x = []
        for (i, j), sg in zip(sel, signs):
            x += [cs[i], cs[j], sg * th]
        tot, mx = xray.deficit(np.array(x), a, True)
        if best is None or mx < best[0]:
            best = (mx, tot, sel, signs)
print(a, 'best max deficit over 180 directions', best)
