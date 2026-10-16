import numpy as np, math, sys, json
import xray
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
a = float(sys.argv[1]); x = np.array(json.loads(sys.argv[2]))
for nphi, nt in [(360, 1000), (1440, 2000)]:
    xray.NT = nt; xray.phis = np.linspace(0, math.pi, nphi, endpoint=False)
    print(nphi, nt, 'sumsq, max deficit:', xray.deficit(x, a, True))
# exact-ish worst direction search near the worst sampled
def sq(cx, cy, th):
    c, s = math.cos(th), math.sin(th)
    return Polygon([(cx + c*dx - s*dy, cy + s*dx + c*dy) for dx, dy in [(-.5,-.5),(.5,-.5),(.5,.5),(-.5,.5)]])
U = box(0, 0, a, a).difference(unary_union([sq(*p) for p in x.reshape(6, 3)]))
print('uncovered area of S_a (not a cover):', U.area)
