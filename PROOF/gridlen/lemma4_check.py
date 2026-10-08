from lemma2_check import tile,cov
import numpy as np
a=2.001;rng=np.random.default_rng(2);best=(0,None)
for _ in range(200000):
    cx,cy,t=rng.uniform(-.7,1.4),rng.uniform(-.7,1.4),rng.uniform(0,np.pi/2)
    s,c=cov(tile(cx,cy,t),a)
    if s>=2 and c>best[0]: best=(c,(cx,cy,t))
print("random max double-sided grid coverage",best)
