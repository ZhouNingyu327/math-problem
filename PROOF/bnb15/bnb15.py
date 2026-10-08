"""Prototype 15-dim pose B&B for the meet deep-delta core (C fixed per subcell).
Soundness: outward interval evaluation in float64 with safety margin MARG=1e-9 (>> rounding error for |coords|<3);
not mpmath-certified. Kill = some witness point surely outside all six squares, or an item surely missing a forced point.
"""
import sys, math, json, time, heapq, os
import numpy as np
sys.path.insert(0,'/workspace/square-cover-6/proof/bnb/pose')
from geometry import MeetSlice, feasible_center_intervals
from run_slices import dfit_of
from moduli_L_cover import world_center
MARG=1e-9
def trig(t0,t1):  # t in [0,pi/2]
    return (math.cos(t1),math.cos(t0)),(math.sin(t0),math.sin(t1))
def imul(a0,a1,b0,b1):
    p=(a0*b0,a0*b1,a1*b0,a1*b1)  # arrays ok
    return np.minimum.reduce(p),np.maximum.reduce(p)
def miss(box,W):
    """box=(x0,x1,y0,y1,t0,t1); W (N,2). True where point surely outside every pose in box."""
    x0,x1,y0,y1,t0,t1=box
    (c0,c1),(s0,s1)=trig(t0,t1)
    dx0,dx1=W[:,0]-x1,W[:,0]-x0; dy0,dy1=W[:,1]-y1,W[:,1]-y0
    a=imul(dx0,dx1,c0,c1); b=imul(dy0,dy1,s0,s1)
    u0,u1=a[0]+b[0],a[1]+b[1]
    a=imul(dx0,dx1,-s1,-s0); b=imul(dy0,dy1,c0,c1)
    v0,v1=a[0]+b[0],a[1]+b[1]
    au=np.where(u0>0,u0,np.where(u1<0,-u1,0)); av=np.where(v0>0,v0,np.where(v1<0,-v1,0))
    return (au>0.5+MARG)|(av>0.5+MARG)
def setup(a,frac,cell):
    sl=MeetSlice(a,frac*dfit_of(a)); pts=sl.C_forced(True)
    th0,th1,al0,al1,be0,be1=cell
    xs=[];ys=[]
    for th in np.linspace(th0,th1,5):
        fe=feasible_center_intervals(pts,th)
        lou,hiu,lov,hiv=fe
        for al in (al0,al1):
            for be in (be0,be1):
                x,y=world_center(th,lou+al*(hiu-lou),lov+be*(hiv-lov)); xs.append(x);ys.append(y)
    pad=2e-3  # crude pad for interior of cell (prototype; not certified hull)
    Cbox=(min(xs)-pad,max(xs)+pad,min(ys)-pad,max(ys)+pad,th0,th1)
    h=math.sqrt(2)/2
    corners=[(0,0),(a,0),(0,a),(a,a)]
    items=[(cx-h,cx+h,cy-h,cy+h,0.0,math.pi/2) for cx,cy in corners]
    Fp=sl.F_forced(); fy=[p[1] for p in Fp]
    items.append((a-h,a+h,min(fy)-h,max(fy)+h,0.0,math.pi/2))
    forced=[np.array([c]) for c in corners]+[np.array(Fp)]
    return sl,Cbox,items,forced
def run(a=2.005,frac=0.01,cell=None,tlimit=600,ngrid=41,out="ckpt.json"):
    cell=cell or (math.radians(45),math.radians(45.5),0.55,0.56,0.55,0.56)
    sl,Cbox,items,forced=setup(a,frac,cell)
    g=np.linspace(0,a,ngrid); W=np.array([(x,y) for x in g for y in g])
    W=W[~miss(Cbox,W)==False] if False else W
    Wc=W[miss(Cbox,W)]          # points C surely misses
    def vol(b): return np.prod([ (bb[1]-bb[0])*(bb[3]-bb[2])*(bb[5]-bb[4]) for bb in b])
    root=tuple(items); V0=vol(root)
    heap=[(-V0,0,root)]; seq=1; killed=0.0; nproc=0; t=time.time(); leaf=0.0
    while heap and time.time()-t<tlimit:
        nv,_,B=heapq.heappop(heap); v=-nv; nproc+=1
        dead=False
        for bb,fp in zip(B,forced):
            if miss(bb,fp).any(): dead=True;break
        if not dead:
            m=np.ones(len(Wc),bool)
            for bb in B: m&=miss(bb,Wc)
            dead=m.any()
        if dead: killed+=v; continue
        # split widest (scaled) dim
        best=None
        for i,bb in enumerate(B):
            for d,(lo,hi,sc) in enumerate([(bb[0],bb[1],1),(bb[2],bb[3],1),(bb[4],bb[5],0.7)]):
                w=(hi-lo)*sc
                if best is None or w>best[0]: best=(w,i,d)
        _,i,d=best; bb=list(B[i]); lo,hi=bb[2*d],bb[2*d+1]; mid=(lo+hi)/2
        for nlo,nhi in ((lo,mid),(mid,hi)):
            nb=bb.copy(); nb[2*d]=nlo; nb[2*d+1]=nhi
            NB=B[:i]+(tuple(nb),)+B[i+1:]
            heapq.heappush(heap,(-v/2,seq,NB)); seq+=1
    rep={"a":a,"frac":frac,"cell":cell,"processed":nproc,"elapsed":time.time()-t,"rate":nproc/(time.time()-t),
         "killed_frac":killed/V0,"open":len(heap),"n_witness":int(len(Wc))}
    json.dump(rep,open(out,"w"),indent=1); print(rep,flush=True); return rep
if __name__=="__main__":
    run(tlimit=float(sys.argv[1]) if len(sys.argv)>1 else 120)
