import numpy as np, json
from multiprocessing import Pool
from slack import unc, grid, tilt
from scipy.optimize import minimize
def run(args):
    name,x0,a,seed,sig=args
    rng=np.random.default_rng(seed)
    x=(x0*[a/2,a/2,1]).ravel()+rng.normal(0,sig,18)
    r=minimize(unc,x,args=(a,),method="Powell",options={"maxiter":1500,"xtol":1e-7,"ftol":1e-13})
    return name,a,float(r.fun),r.x.tolist(),[name,a,seed]
if __name__=="__main__":
    rand=np.zeros((6,3))
    jobs=[("random",np.c_[np.random.default_rng(s).uniform(0,2,(6,2)),np.random.default_rng(s).uniform(0,1.57,6)],2.0,s,0.0) for s in range(48)]
    As=[2.0005,2.001,2.002,2.004,2.008,2.016]
    for nm,x0 in [("grid",grid),("tilt",tilt)]:
        for a in As:
            jobs+=[(nm,x0,a,1000+s,0.03) for s in range(12)]
    import os
    done=set()
    if os.path.exists("families.jsonl"):
        for l in open("families.jsonl"): d=json.loads(l); done.add(tuple(d[4]))
    jobs=[j for j in jobs if (j[0],j[2],j[3]) not in done]
    jobs=[j for j in jobs if j[0]!="random"]+[j for j in jobs if j[0]=="random"]
    with Pool(8) as p, open("families.jsonl","a") as fo:
        for r in p.imap_unordered(run,jobs):
            fo.write(json.dumps(r)+"\n"); fo.flush()
    res=[json.loads(l) for l in open("families.jsonl")]
    json.dump(res,open("families.json","w"))
    out={}
    for nm,a,f,*_ in res: out.setdefault((nm,a),[]).append(f)
    for k in sorted(out): print(k,"min",min(out[k]),"n",len(out[k]),"zeros(<1e-9)",sum(v<1e-9 for v in out[k]))
