from mpmath import iv
r2=iv.sqrt(2)
def surv(s2):
  ok=[]
  for nc in range(5):
    for nd in range(4+nc,7):
      if nc==0 and nd>4: continue
      for ns in range(0,7-nd):
        ni=6-nd-ns
        if (2*(4-nc)+2*r2*nc+r2*ns>8)==False or (2*nd+s2*ns+2*r2*ni>12)==False: continue
        ok.append((nc,nd,ns,ni))
  return ok
for name,s2 in [("paper 1.5sqrt2 (FALSE for n=2)",1.5*r2),("observed sup 3sqrt2-2",3*r2-2),("1+sqrt2",1+r2)]:
  print(name,surv(s2))
