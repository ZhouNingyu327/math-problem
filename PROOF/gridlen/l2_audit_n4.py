# Exact (sympy) audit for n=4, a=4+eps: 45-deg unit square, centre (q, sqrt2/2 - t), q=a/4.
import sympy as sp
from sympy import Point, Polygon, Segment, sqrt, Rational as R
def run(eps,t,n=4):
    a=n+eps; q=a/n; h=sqrt(2)/2
    cx,cy=q,h-t
    V=[Point(cx,cy-h),Point(cx+h,cy),Point(cx,cy+h),Point(cx-h,cy)]
    T=Polygon(*V)
    lines=[("y=%d q"%k,Segment(Point(0,k*q),Point(a,k*q))) for k in range(n+1)]+\
          [("x=%d q"%k,Segment(Point(k*q,0),Point(k*q,a))) for k in range(n+1)]
    tot=0; sides=[]
    for name,L in lines:
        I=[g for g in T.intersection(L)]
        # T convex: intersection with a segment is a segment or point(s); also include case where segment interior lies inside
        pts=[p for p in I if isinstance(p,Point)]+[p for g in I if isinstance(g,Segment) for p in g.points]
        pts+=[p for p in L.points if T.encloses_point(p) or any(e.contains(p) for e in T.sides)]
        ln=0
        if len(pts)>=2:
            ln=max(sp.simplify(p.distance(r)) for p in pts for r in pts)
        if name in("y=0 q","y=%d q"%n,"x=0 q","x=%d q"%n) and len(pts)>0: sides.append(name)
        if ln!=0: print("  ",name,sp.nsimplify(sp.simplify(ln)),float(ln))
        tot+=ln
    tot=sp.simplify(tot)
    print("eps=%s t=%s sides met:%s total=%s = %.6f ; 1.5sqrt2=%.6f ; exceeds: %s"%(eps,t,sides,tot,float(tot),float(R(3,2)*sqrt(2)),sp.simplify(tot-R(3,2)*sqrt(2)).is_positive))
run(R(1,1000),0)
run(R(1,1000),R(1,100))
