import sys,math,json,numpy as np
sys.path.insert(0,'/workspace/square-cover-6/proof/bnb/pose'); sys.path.insert(0,'/workspace/square-cover-6/proof/rigidity')
from geometry import MeetSlice, feasible_center_intervals
from run_slices import dfit_of
from moduli_L_cover import world_center
from slack import sq
from shapely.geometry import box
from shapely.ops import unary_union
from scipy.optimize import minimize
a=float(sys.argv[1]); th=math.radians(float(sys.argv[2])); al=be=0.55
sl=MeetSlice(a,0.01*dfit_of(a)); pts=sl.C_forced(True)
lou,hiu,lov,hiv=feasible_center_intervals(pts,th)
cx,cy=world_center(th,lou+al*(hiu-lou),lov+be*(hiv-lov))
C=sq(cx,cy,th); print("C centre",cx,cy,"gap",sl.gamma,"ptop",sl.p_top)
S=box(0,0,a,a)
def unc(x):
    P=x.reshape(5,3); return S.difference(unary_union([C]+[sq(*p) for p in P])).area
rng=np.random.default_rng(0);best=None
starts=[[.5,.5,0],[a-.5,.5,0],[.5,a-.5,0],[a-.5,a-.5,0],[a-.5,1.2,0]]
for k in range(16):
    x=(np.array(starts)+rng.normal(0,.08,(5,3))).ravel()
    r=minimize(unc,x,method="Powell",options={"maxiter":2500,"xtol":1e-7,"ftol":1e-13})
    if best is None or r.fun<best.fun: best=r
P=best.x.reshape(5,3); U=S.difference(unary_union([C]+[sq(*p) for p in P]))
print("min uncovered",best.fun)
geoms=getattr(U,'geoms',[U])
for g in sorted(geoms,key=lambda g:-g.area)[:5]:
    print(" piece area %.2e centroid (%.4f,%.4f) bounds %s"%(g.area,g.centroid.x,g.centroid.y,[round(b,4) for b in g.bounds]))
json.dump({"a":a,"C":[cx,cy,th],"others":P.tolist(),"unc":best.fun},open(f"/workspace/square-cover-6/proof/rigidity/core_probe_{a}_{sys.argv[2]}.json","w"))
