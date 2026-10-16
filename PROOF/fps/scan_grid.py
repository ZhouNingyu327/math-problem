import fps, numpy as np, time, sys
K=int(sys.argv[1]) if len(sys.argv)>1 else 360
for k in [7,9,11,13]:
    for a in [2.0,2.05,2.1,2.15,2.2]:
        g=np.linspace(0,a,k); P=np.array([(x,y) for x in g for y in g])
        t=time.time(); S,s=fps.family(P,K=K); M=fps.members(S,len(P))
        r=fps.solve_cover(M,6,120)
        print(k,a,S.shape[0],'feasible' if isinstance(r,list) else r, round(time.time()-t,1),flush=True)
