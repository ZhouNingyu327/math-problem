import fps, numpy as np, time, sys
K=int(sys.argv[1])
for a in [float(v) for v in sys.argv[2].split(',')]:
    for k in [int(v) for v in sys.argv[3].split(',')]:
        g=np.linspace(0,a,k); P=np.array([(x,y) for x in g for y in g])
        t=time.time(); S,s=fps.family(P,K=K); M=fps.members(S,len(P))
        r,obj,db=fps.cover_status(M,6,600)
        print(k,a,S.shape[0],'CERT' if r=='CERT' else ('cover' if isinstance(r,list) else r), obj, db, round(time.time()-t,1),flush=True)
