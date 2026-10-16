# Area identity: 6 = a^2 - uncovered + spill + overcount, where overcount = sum(area(Qi∩S)) - area(union∩S).
import json,collections,numpy as np
from slack import sq
from shapely.geometry import box
from shapely.ops import unary_union
best={}
for l in open("families.jsonl"):
    r=json.loads(l); k=(r[0],r[1])
    if k not in best or r[2]<best[k][2]: best[k]=r
rows=[]
for k in sorted(best):
    nm,a,f,x=best[k][:4]
    if nm=="random": continue
    S=box(0,0,a,a); Q=[sq(*x[i:i+3]) for i in range(0,18,3)]
    ins=[q.intersection(S) for q in Q]; U=unary_union(ins)
    spill=sum(q.area-qi.area for q,qi in zip(Q,ins)); over=sum(qi.area for qi in ins)-U.area; unc=a*a-U.area
    rows.append((nm,a,6-a*a,spill,over,unc))
    print("%s a=%.4f slack6-a2=%.4f spill=%.4f overcount=%.4f uncovered=%.2e"%rows[-1])
# also random zero-area covers at a=2
for l in open("families.jsonl"):
    r=json.loads(l)
    if r[0]=="random" and r[2]<1e-9:
        a=2.0;x=r[3];S=box(0,0,a,a);Q=[sq(*x[i:i+3]) for i in range(0,18,3)];ins=[q.intersection(S) for q in Q]
        print("random a=2 cover: spill=%.3f overcount=%.3f"%(sum(q.area-qi.area for q,qi in zip(Q,ins)),sum(qi.area for qi in ins)-unary_union(ins).area))
