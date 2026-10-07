# Counterexample to Lemma 2 of arXiv 2609.15876 (exact; l2_exact.py, sympy)
Setting: S_n=[0,n+eps]^2, grid lines at multiples of q=(n+eps)/n. Lemma 2 claims that a single-sided perimeter tile covers
at most 1.5*sqrt2 of grid(S_n).
Tile: the unit square rotated 45 degrees with vertices (q,0), (q,sqrt2), (q+-sqrt2/2, sqrt2/2), i.e. centre (q, sqrt2/2).
- It meets only the bottom side: q-sqrt2/2>0, q+sqrt2/2<n+eps, and its top sqrt2 lies below n+eps.
- Its chord on the vertical grid line x=q is its diagonal, from (q,0) to (q,sqrt2): length sqrt2 (inside S_n).
- Its chord on the horizontal grid line y=q (valid since 1<q<sqrt2) has length 2(sqrt2-q).
- Total = 3sqrt2 - 2 - 2eps/n, which exceeds 1.5sqrt2 exactly when eps < n(1.5sqrt2-2) ~ 0.1213n.
  The limit excess is 1.5sqrt2-2 ~ 0.1213. This holds for every n>=2, including n=2 and n=4.
The paper's proof (Steps 1-2, Fig. 3) only accounts for the top side and one vertical segment. It misses the parallel grid
line at distance q (<sqrt2) from the side. With 3sqrt2-2 in place of 1.5sqrt2, the n=4 counting admits extra
(nc,nd,ns) mixes: (0,4,7),(0,4,8),(1,5,6),(2,6,5).
