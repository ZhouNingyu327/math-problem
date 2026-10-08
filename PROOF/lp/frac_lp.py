# Fractional dual bound: max sum y_p s.t. every unit-square pose covers weight<=1.
# If value>6 for a>2, S(6)<=2 would follow (after rigorous pose-continuum check).
import numpy as np, itertools, sys
from scipy.optimize import linprog
a=float(sys.argv[1]) if len(sys.argv)>1 else 2.01
n=13
g=np.linspace(0,a,n); P=np.array([(x,y) for x in g for y in g])
rows=[]
for th in np.linspace(0,np.pi/2,10,endpoint=False):
  c,s=np.cos(th),np.sin(th)
  for cx in np.linspace(0,a,30):
    for cy in np.linspace(0,a,30):
      d=P-[cx,cy]; u=d@[c,s]; v=d@[-s,c]
      m=(abs(u)<=.5)&(abs(v)<=.5)
      if m.any(): rows.append(m.astype(float))
A=np.unique(np.array(rows),axis=0)
r=linprog(-np.ones(len(P)),A_ub=A,b_ub=np.ones(len(A)),bounds=(0,None),method="highs")
print(a,"poses",len(A),"frac packing value (upper est.)",-r.fun)
y=r.x; S=[(tuple(P[i]),round(y[i],3)) for i in range(len(P)) if y[i]>1e-6]
print(len(S),S)
# dense check: max covered weight over fine poses
best=0
for th in np.linspace(0,np.pi/2,180,endpoint=False):
  c,s=np.cos(th),np.sin(th)
  for cx in np.linspace(0,a,120):
    for cy in np.linspace(0,a,120):
      d=P-[cx,cy]; u=d@[c,s]; v=d@[-s,c]
      best=max(best,y[(abs(u)<=.5)&(abs(v)<=.5)].sum())
print("dense max pose weight",best,"=> valid bound",-r.fun/best)
