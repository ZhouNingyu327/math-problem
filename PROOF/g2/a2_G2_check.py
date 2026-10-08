import json, math
from shapely.geometry import Polygon, box, LineString
from shapely.ops import unary_union
d = json.load(open('a2_G2.json'))
def sq(cx, cy, th):
    co, si = math.cos(th), math.sin(th)
    return Polygon([(cx + co*dx - si*dy, cy + si*dx + co*dy) for dx, dy in [(-.5,-.5),(.5,-.5),(.5,.5),(-.5,.5)]])
V1 = box(0, 0, 1, 1); V2 = box(1, 0, 2, 1); V3 = box(1, 1, 2, 2); C = box(0, 0.4, 1, 1.4); V4 = sq(*d['V4']); F = sq(*d['F'])
S = box(0, 0, 2, 2); bd = LineString([(0, 1), (1, 1), (1, 2), (0, 2), (0, 1)])
five = unary_union([V1, V2, V3, V4, C])
print("uncovered area of [0,2]^2 by all six:", S.difference(unary_union([five, F])).area)
r = bd.difference(five)
print("length of bd(Q4) covered by NO item except F:", r.length, " pieces:", [ [tuple(round(t, 4) for t in p) for p in g.coords] for g in getattr(r, 'geoms', [r])])
print("uncovered area of [0,2]^2 by the five items other than F:", S.difference(five).area)
