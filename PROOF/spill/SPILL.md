# Spill + overlap area accounting: viability (2026-10-08)
Exact identity for any 6 unit squares and S=[0,a]^2:
  6 = a^2 - uncovered + spill + overcount,  where spill = sum area(Q_i \ S) and overcount = sum area(Q_i ∩ S) - area(∪Q_i ∩ S).
So for a cover, spill + overcount = 6 - a^2 EXACTLY. Proving "spill + forced overlap > 6 - a^2" is literally equivalent to S(6)=2.
A lower bound L(a) on waste must satisfy L(2) <= 2 (the side-2 covers exist) and L(a) > 6 - a^2 ~ 2 - 4(a-2) for a > 2, i.e. it must be first-order sharp at a=2.
Numerics (waste.py, best near-covers from families.jsonl):
  near-covers at a in [2.0005, 2.016]: spill 0.003-0.075, overcount 1.90-1.98 (grid and tilted-V3 families).
  13 exact a=2 covers from random global search: spill 0.20-1.13, overcount 0.87-1.80.
  The grid cover with both spare squares inside S has spill 0, overcount 2.
=> Spill is NOT forced near the optimum (it can be ~0), so the spill lemma (sqrt(b^2-1)/2 for side chord b>1) has no bite. The tight near-covers use
   axis-parallel corner tiles with b<=1 and keep spill tiny. All the slack goes into overcount, which belongs to the two "spare"
   squares and can be placed anywhere, so no pairwise forced-overlap bound exists (two squares sharing two points can overlap in measure ~0).
Central-cross hybrid: the same identity holds on any subregion R (sum of areas in R = area(R) + overcount_R - uncovered_R). For R a cross
   of width w around the midlines, the near-covers have overcount_R of order w, again with no a-dependent excess. Same obstruction.
VERDICT: not viable as a standalone method. It could only work inside a case split where every tile's position is pinned (then it is
   the B&B again). No case closed.
