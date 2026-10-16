# T(w)=max over unit-square poses of the average height (yL+yR)/2 of a trapezoid
# {0<=x<=w, 0<=y<=line from (0,yL) to (w,yR)} contained in the square (bottom edge y=0 contained).
# Equivalent: max over poses with segment [0,w]x{0} inside square, of (top(0)+top(w))/2 where top(x)=upper end of vertical chord at x
# (convexity => trapezoid inside iff its 4 vertices inside).
import numpy as np
def T(w,n=400):
    best=0
    for th in np.linspace(0,np.pi/4,n):
        c,s=np.cos(th),np.sin(th)
        # square = {p: |u|<=.5,|v|<=.5}, u=(p-z).(c,s), v=(p-z).(-s,c); centre z free.
        # place bottom segment endpoints P0=(0,0),P1=(w,0); search centre over a grid
        for zx in np.linspace(-.8,w+.8,90):
            for zy in np.linspace(-.2,1.2,90):
                def top(x):
                    # max y with (x,y) in square, given (x,0) in square
                    ys=np.linspace(0,1.5,301); dx=x-zx; dy=ys-zy
                    u=dx*c+dy*s; v=-dx*s+dy*c; ok=(abs(u)<=.5)&(abs(v)<=.5)
                    if not ok[0]: return None
                    # chord is an interval starting at y=0
                    k=np.argmin(ok) if not ok.all() else len(ys); return ys[k-1]
                t0=top(0.0); t1=top(w)
                if t0 is None or t1 is None: continue
                best=max(best,(t0+t1)/2)
    return best
for w in [0.3,0.414,0.5,0.6,0.7,0.8]:
    print(w,T(w,60),flush=True)
