# Counterexample to quantitative rigidity: a cover of [0,2]^2 by 6 unit squares where the
# vertex item V3 at corner (0,2) is tilted 20 deg, so V_i need not approach the grid quarters as a->2+.
from shapely.geometry import box
from shapely import affinity
from shapely.ops import unary_union
def sq(cx,cy,deg=0): return affinity.rotate(box(cx-.5,cy-.5,cx+.5,cy+.5),deg,origin=(cx,cy))
V1=sq(.5,.5); V2=sq(1.5,.5); V4=sq(1.5,1.5); V3=sq(.3,1.7,20)
C=box(.05,1,1.05,2); F=box(-.9,.9,.1,1.9)
U=box(0,0,2,2).difference(unary_union([V1,V2,V3,V4,C,F]))
print("uncovered area",U.area, "V3 contains corner",V3.covers(box(0,2,0,2).centroid), "C contains centre", C.covers(box(1,1,1,1).centroid))
