# Audit of Lemma 2 in arXiv:2609.15876v1 (Sriswasdi, 14 Sep 2026)
Source: PDF from arxiv.org/pdf/2609.15876, extracted with pdftotext.

## Exact definitions and statement (quoted)
- "We denote by Sn the square with side length n + eps, for arbitrarily small eps > 0, and peri(Sn) its perimeter."
- "We denote by grid(Sn) the set of (n + 1) x (n + 1) evenly-spaced line segments parallel to the sides of Sn (including the sides
  of Sn itself) that divide Sn into n^2 equal cells. Note that our definition of grid(Sn) contain peri(Sn)."
- "... one that intersects with exactly one side of peri(Sn) as a single-sided perimeter tile."
  (A double-sided tile is one that "intersects with two sides ... including one that covers a corner".)
- "Lemma 2. A single-sided perimeter tile cannot cover grid(Sn) by more than 1.5 sqrt2 unit length."
- Proof (summary of the quoted text): WLOG the tile meets the top side. Step 1: if the lowest vertex A is not on a vertical grid segment,
  translate horizontally to increase "its coverage of the vertical grid segment". Step 2: if B or C is above the top side, translate
  down. "Hence ... optimal ... lowest vertex lying on a vertical segment ... second highest vertex lying on the top side." Then
  coverage = d_theta + h_theta = 1/cos(theta) + cos(theta) <= 1.5 sqrt2.
- No other hypotheses appear: the tile may overhang Sn, and coverage means the length of tile ∩ grid(Sn) (tile ∩ peri for peri).

## Does our counterexample meet every hypothesis? Yes.
Setting n=4, a=4+eps, q=a/4. Tile: unit square rotated 45 deg, centre (q, sqrt2/2 - t), t>=0 small.
- It intersects exactly one side (the bottom): it meets y=0, and its x-range [q-sqrt2/2, q+sqrt2/2] ⊂ (0,a) and top sqrt2-t < a.
  To rule out a degenerate single-point contact, take t=1/100: then it meets the bottom in a segment of length 2t.
- Exact lengths (sympy, l2_audit_n4.py, eps=1/1000):
  t=0:     y=1q: 2sqrt2-4001/2000; x=1q: sqrt2; total 3sqrt2-4001/2000 = 2.242141 > 1.5sqrt2 = 2.121320.
  t=1/100: y=0: 1/50; y=1q: 2sqrt2-4041/2000; x=1q: sqrt2-1/100; total 3sqrt2-4021/2000 = 2.232141 > 1.5sqrt2.
  General formula: 3sqrt2 - 2q - t. It exceeds 1.5sqrt2 whenever 2q+t < 1.5sqrt2 (e.g. every eps<0.12, t<0.1).
- Lemma 2 is therefore FALSE under the paper's own definitions.
  (Orientation: the paper assumes the top side WLOG; our tile is its mirror image at the bottom.)

## Failing step
Steps 1-2 track only the side being touched plus ONE vertical grid segment ("coverage = d_theta + h_theta"). They ignore the
interior grid line PARALLEL to that side at distance q=a/n (just over 1). Since q < sqrt2, a tilted tile reaches it: at 45 deg it adds a chord
of 2(sqrt2-q) ~ 0.83, while the touched-side chord shrinks to ~0. The "hence optimal" claim fails because the translations of
Steps 1-2 are not monotone for this third segment.
Sup observed: Nelder-Mead (l2_M.py, 400 starts) gives max grid coverage 2.24214 (= our example), so the true bound is likely 3sqrt2-2q.

## Impact on Theorem 1 (n=4)
- With 1.5sqrt2 replaced by 3sqrt2-2, counting admits (nc,nd,ns) = (0,4,6),(0,4,7),(0,4,8),(1,5,6),(2,6,5) (interval-checked,
  gridlen_param-style). Theorem 1 ("exactly 4 double-sided, exactly 6 single-sided") does NOT follow as written.
- Attempted repair with a joint per-tile bound g + lam*p <= M(lam) (p = side coverage, g = grid coverage), which uses the fact that the
  bad tiles barely touch the side. Floating point, not certified (l2_repair.py, l2_M.py):
  M(0.1) ~ 2.26274 (~1.6sqrt2). To kill (0,4,7) one needs M(0.1) <= (32+0.8-12sqrt2)/7 ~ 2.26150, so the repair fails by ~0.0012.
  Other lam values do worse (for lam=0.2, M~2.379 vs the 2.376 needed).
- Verdict: the gap is real. A simple joint counting fix does not close it (marginally). The case ns=7 (and others) would need an extra
  argument, e.g. extending the paper's spill-area step. Not attempted here.
- Side note: the paper's intro says Dósa–Lángi–Tuza [2] "proved that a square with side length slightly larger than 2 cannot be fully covered
  by 6 unit squares". DLT (arXiv 2601.16535 v3) state this as Conjecture 1.1 and prove S(5)=2. That looks like a citation error; S(6)=2 is still open.
No one was contacted.
