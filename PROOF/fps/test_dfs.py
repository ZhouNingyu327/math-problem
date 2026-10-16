import fps, exactdfs, numpy as np, time, sys
for a,k in [(2.15,7),(2.1,11),(2.0,9),(2.05,11),(2.06,15)]:
    g=np.linspace(0,a,k); P=np.array([(x,y) for x in g for y in g])
    S,s=fps.family(P,K=360)
    t=time.time(); r,st=exactdfs.no_cover(S,len(P),6); print(a,k,S.shape[0],'NO 6-COVER' if r else 'cover exists',st,round(time.time()-t,1),flush=True)
