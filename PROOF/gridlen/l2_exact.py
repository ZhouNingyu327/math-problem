import sympy as sp
n,e=sp.symbols('n epsilon',positive=True)
r=sp.sqrt(2); a=n+e; q=a/n
V=[(q,0),(q,r),(q+r/2,r/2),(q-r/2,r/2)]
# vertical chord at x=q: from y=0 to y=sqrt2 (the vertical diagonal) -> sqrt2, inside S since sqrt2<a
# horizontal chord at y=q: |y-c| = q - sqrt2/2, half-width = sqrt2/2 - (q - sqrt2/2) = sqrt2 - q
tot=r+2*(r-q)
for N in (2,4):
    t=tot.subs(n,N)
    lim=sp.limit(t,e,0)
    print(N,"total",sp.simplify(t),"limit",lim,"limit-1.5sqrt2 =",sp.nsimplify(lim-sp.Rational(3,2)*r),
          float(lim-sp.Rational(3,2)*r))
    # validity: single-sided (touches only bottom) needs q-sqrt2/2>0, q+sqrt2/2<a, sqrt2<a, and q<sqrt2 (chord exists)
    for cond in [q-r/2>0, q+r/2<a, r<a, q<r]:
        print("  ",cond.subs(n,N), sp.simplify(cond.subs({n:N,e:sp.Rational(1,1000)})))
