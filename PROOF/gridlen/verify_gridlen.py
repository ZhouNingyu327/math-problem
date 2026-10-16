# Sriswasdi (arXiv 2609.15876) peri/grid length counting adapted to n=2, N=6, any a>2.
# Lemmas used (from that paper, valid for side a>2, so grid lines are a/2>1 apart):
#  L1 single-sided: peri<=sqrt2; L2 single-sided: grid<=1.5sqrt2; L3 interior: grid<=2sqrt2;
#  L4 double-sided: peri,grid<=2; L5 corner with >=2 double-sided tiles: peri<=2sqrt2.
# peri length 4a>8, grid length 6a>12; nd>=4+nc; nd+ns<=6.
# Check at a=2 (worst case: strict > needed, so the a=2 value with non-strict comparison is the sound test).
from mpmath import iv
r2=iv.sqrt(2)
ok=[]
for nc in range(5):
  for nd in range(4+nc,7):
    for ns in range(0,7-nd):
      ni=6-nd-ns
      peri=2*(4-nc)+2*r2*nc+r2*ns
      grid=2*nd+1.5*r2*ns+2*r2*ni
      if (peri>8)==False or (grid>12)==False: continue   # cert. infeasible (upper bound <=8 or <=12)
      if nc==0 and nd>4: continue  # nc=0 means each corner has <=1 double-sided tile
      ok.append((nc,nd,ns,ni))
print("surviving (nc,nd,ns,n_interior):",ok)
