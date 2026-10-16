"""bnb15 v2: structural pruning + DFS + multiprocessing. float64 outward intervals + 1e-9 margin (prototype, not mpmath)."""
import sys, math, json, time, os
import numpy as np
from multiprocessing import Pool
from bnb15 import miss, setup
SQ2=math.sqrt(2)
# item order: 0=V1(0,0) 1=V2(a,0) 2=V4(0,a) 3=V3(a,a) 4=F
def build(a,frac,cell,ng):
    sl,Cbox,items,forced=setup(a,frac,cell)
    g=np.linspace(0,a,ng); W=np.array([(x,y) for x in g for y in g])
    W=W[miss(Cbox,W)]                       # C surely misses these: other items must cover
    allowed=np.ones((len(W),5),bool)
    eps=1e-12
    left=W[:,0]<eps; top=W[:,1]>a-eps; right=W[:,0]>a-eps; bot=W[:,1]<eps
    allowed[left]=False; allowed[left][:,[0,2]]=True
    allowed[np.ix_(left,[0,2])]=True
    allowed[top]=False; allowed[np.ix_(top,[2,3])]=True          # Case I: V4,V3 cover the top
    allowed[np.ix_(right,[0,2])]=False                          # V1,V4 cannot reach right side (a>sqrt2)
    allowed[np.ix_(bot,[2,3])]=False
    allowed[np.ix_(left,[4])]=False                             # F misses left side
    D=np.sqrt(((W[:,None,:]-W[None,:,:])**2).sum(-1))>SQ2+1e-9  # far pairs
    return items,forced,W,allowed,D
def test(B,forced,W,allowed,D):
    for bb,fp in zip(B,forced):
        if miss(bb,fp).any(): return True
    M=np.stack([~miss(bb,W) for bb in B],1) & allowed           # possible coverers
    cnt=M.sum(1)
    if (cnt==0).any(): return True
    single=cnt==1
    if single.any():
        idx=np.where(single)[0]; who=M[idx].argmax(1)
        for i in range(5):
            p=idx[who==i]
            if len(p)>1 and D[np.ix_(p,p)].any(): return True
            # forced corner/F points vs these singles
    return False
def split(B):
    best=None
    for i,bb in enumerate(B):
        for d,sc in ((0,1),(1,1),(2,0.7)):
            w=(bb[2*d+1]-bb[2*d])*sc
            if best is None or w>best[0]: best=(w,i,d)
    _,i,d=best; bb=list(B[i]); lo,hi=bb[2*d],bb[2*d+1]; m=(lo+hi)/2
    out=[]
    for nlo,nhi in ((lo,m),(m,hi)):
        nb=bb.copy(); nb[2*d]=nlo; nb[2*d+1]=nhi; out.append(B[:i]+(tuple(nb),)+B[i+1:])
    return out
def vol(B): return float(np.prod([(b[1]-b[0])*(b[3]-b[2])*(b[5]-b[4]) for b in B]))
G=None
def worker(args):
    root,tlimit,wid,checkpoints=args
    items,forced,W,allowed,D=G
    V0=vol(root); stack=[root]; killed=0.0; n=0; t0=time.time(); log=[]; ci=0
    while stack:
        el=time.time()-t0
        if ci<len(checkpoints) and el>=checkpoints[ci]:
            log.append((checkpoints[ci],killed/V0,n,len(stack))); ci+=1
        if el>tlimit: break
        B=stack.pop(); n+=1
        if test(B,forced,W,allowed,D): killed+=vol(B); continue
        stack.extend(split(B))
    log.append((time.time()-t0,killed/V0,n,len(stack)))
    return wid,V0,log,len(stack)==0
def init(a,frac,cell,ng):
    global G; G=build(a,frac,cell,ng)
if __name__=="__main__":
    tl=float(sys.argv[1]); ng=int(sys.argv[2]) if len(sys.argv)>2 else 41
    a=2.005;frac=0.01;cell=(math.radians(45),math.radians(45.5),0.55,0.56,0.55,0.56)
    init(a,frac,cell,ng); items=G[0]
    roots=[tuple(items)]
    while len(roots)<64: roots=[c for r in roots for c in split(r)]
    cps=[60,300,1200,3600,7200]
    sel=None
    if len(sys.argv)>3:
        sel=set(json.load(open(sys.argv[3])))
    todo=[(i,R) for i,R in enumerate(roots) if sel is None or i in sel]
    per=float(sys.argv[4]) if len(sys.argv)>4 else tl/8
    with Pool(8,initializer=init,initargs=(a,frac,cell,ng)) as p, open(f"v2_log_{int(tl)}_{ng}.jsonl","w") as fo:
        res=[]
        for r in p.imap_unordered(worker,[(R,per,i,[c/8 for c in cps]) for i,R in todo]):
            res.append(r); fo.write(json.dumps(r)+"\n"); fo.flush()
    Vt=sum(r[1] for r in res)
    print("roots",len(res),"cleared roots",sum(r[3] for r in res),"total killed frac",sum(r[1]*r[2][-1][1] for r in res)/Vt,
          "boxes",sum(r[2][-1][2] for r in res))
