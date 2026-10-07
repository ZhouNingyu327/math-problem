# Length lemmas of arXiv 2609.15876 (Sriswasdi), checked for n=2 (side a>2, 6 unit squares)
Grid(S_n) = sides of S_n plus the interior lines at multiples of a/n (for n=2: the two midlines).

- L1 (single-sided tile covers <=sqrt2 of the perimeter): TRUE. Any chord of a unit square is <=sqrt2.
- L3 (interior tile covers <=2sqrt2 of the grid): TRUE for n=2. It meets only the two midlines, each chord <=sqrt2.
- L4 (double-sided tile covers <=2 of the perimeter): TRUE (standard corner lemma, legs x and l(x), x+l(x)<=2).
  The grid part (<=2) is consistent with numerics (2e5 random poses, max 1.966) but NOT proved here.
- L5 (all double-sided tiles at one corner cover <=2sqrt2 of the perimeter): TRUE. The paper's proof is fine: each such tile meets both
  sides, so the farthest covered points P1,P2 satisfy |CP_i| <= dist(P_i, other side) <= sqrt2.
- **L2 (single-sided tile covers <=1.5sqrt2 of the grid): FALSE**, for n=2 and also for n=4.
  Exact counterexample: q=a/n (slightly >1). Take the 45-degree unit square with vertices (q,0), (q,sqrt2), (q+-sqrt2/2, sqrt2/2).
  It meets only the bottom side (at (q,0)). Its chord on the vertical line x=q is [0,sqrt2] (length sqrt2), and its chord on the
  horizontal line y=q has length 2(sqrt2-q). Total 3sqrt2-2q -> 3sqrt2-2 ~ 2.2426 > 1.5sqrt2 ~ 2.1213.
  The paper's proof only considers vertical grid segments and misses the horizontal line y=a/n, which lies within reach because
  sqrt2 > a/n. (Checked with Shapely: lemma2_check.py prints 2.2416 for n=2 and 2.2421 for n=4.)
  The best value seen in random search for n=2 is about 2.22-2.24, so the true sup is probably 3sqrt2-2. Not proved.
- Consequence for 2609.15876's Theorem 1 (n=4): with L2 replaced by 3sqrt2-2, the counting no longer forces
  (nc,nd,ns)=(0,4,6). Extra mixes survive: (0,4,7),(0,4,8),(1,5,6),(2,6,5) (gridlen_param-style check, interval arithmetic).
  So that paper's n=4 proof has a gap as written, unless they handle it elsewhere (not seen in the text we read).
- Consequence for us: GridLen's 4 surviving mixes are unchanged for every s2 in {1.5sqrt2, 3sqrt2-2, 1+sqrt2}
  (gridlen_param.py). They really follow from the perimeter count (L1,L4,L5) plus nd=6 being killed by the grid count.
  Their content ("some non-corner tile meets the boundary", "at most 1 interior tile") is already implied by our
  midpoint taxonomy, so the length budget adds NO new cut to the pose B&B. Refining the grid (thirds, lines through
  witness points) only adds lines with spacing <1, where the length caps lose force (a tile can meet 2+ parallel lines).
