# Extremal / jammed-optimum approach (2026-10-08, ~16:00-17:00 CST)

**Bottom line: no case closed. S(6)=2 is NOT proved.** This round set up the "analyse the hypothetical optimum
a*>2 directly" framework. It gives several exact structural facts (E1-E6 below, proofs sketched but elementary)
and one new negative result (D5). It does not reduce the remaining work to anything smaller than the existing
case analysis.

## Setup
Configuration P=(c_i,theta_i), i=1..6, closed unit squares Q_i. S_a=[-a/2,a/2]^2. A(P)=sup{a : S_a ⊂ ∪Q_i}.
Depth d_i(x)=1/2-||R(theta_i)^T(x-c_i)||_inf (signed); m_P(x)=max_i d_i(x).

## Rigorous facts
**E1 (attainment).** S(6)=max_P A(P) is attained: covering S_a is a closed condition, and tiles missing S_a can be
moved to a compact region. If S(6)>2, then the existing closed cases (all a > a_top≈2.0362 are excluded; see STATUS)
put the maximum a* in (2, a_top].

**E2 (exact depth identity).** mu*(a):=max_P min_{x∈S_a} m_P(x) satisfies **mu*(a)=(1-a/S(6))/2 for every a**.
(A depth->=mu cover of S_a is a cover by concentric squares of side 1-2mu. Rescale by 1/(1-2mu).)
So S(6)=2 iff mu*(2)=0, i.e. iff **six OPEN unit squares never cover the CLOSED square [0,2]^2**. The a-problem
becomes a fixed-a=2 "open cover" problem, and the max-min-depth objective is a well-posed local-optimisation target.
This is used in the numerics below.

**E3 (essentiality).** In every 6-cover with a>2 each tile has a private region with nonempty interior
(else the other 5 cover S_a up to a null set, hence by closedness cover it, which contradicts S(5)=2).

**E4 (first-order jamming, Gordan form).** At a local maximiser of A, let K be the tight set (points of S_a lying in no
open tile). Near each tight point the cover condition is a cone-covering condition by the tiles' local half-planes or
quarter-planes and by the exterior half-planes of S. Branchwise linearisation and Gordan's alternative (semi-infinite
version: K is compact) give multipliers lambda>=0 on tight constraints and mu>=0, not all zero, with
sum lambda_c grad g_c + mu e_a = 0.

**E5 (no self-stress; tension identity).** Every margin g_c is positively 1-homogeneous under joint dilation
(centres, a, tile side s). Euler's identity plus E4 gives  **a·mu = s·sum_c lambda_c d_s g_c**. Growing every tile
strictly improves every tight constraint (each tight point involves at least one tile), so d_s g_c>0. Hence mu=0
forces lambda=0: **there are no self-stresses, mu>0**, and
  a = (total tile tension) / (total boundary pull),
where each tile is pulled outward along its edge normals at its tight points, and S is pulled inward at boundary
tight points. (Virial form: sum over tiles of sum F·(x-c_i) equals (a/2)·sum of the boundary pulls.) The identity holds
at **every** jammed configuration, so it does not bound a by itself. An inequality "tension <= 2·pull" for all
jammed 6-configurations would be equivalent to S(6)=2.

**E6 (per-tile equilibrium rule).** A stressed tile is in force and torque balance under outward normal forces
(edge points) or forces in the outward normal cone (vertex points). So it has tight points on **both** edges of an
opposite pair (or in opposite vertex cones). With a single pair, the force centroids on the two edges are aligned.

## Numerics (floating point only)
* `exact.py`: exact min depth by enumerating vertices of the piecewise-linear depth landscape (triples of the
  24 edge-affine pieces, pairs on the sides, corners).
* `xslp.py`: exchange-SLP local maximisation of min depth at a=2 (coverable side = 2/(1-2t)). 106 random starts:
  max side 1.9999979; histogram (<1.8,1.8-1.9,1.9-1.95,1.95-1.98,1.98-1.99,1.99-1.999,>1.999)=(8,22,25,20,13,12,6).
  **No local maximum above 2.** The six best (>1.999) all converge toward 4 axis-parallel grid tiles plus 2 tilted
  spares, i.e. the non-isolated a=2 family. No separate rigid local maximum was seen in (1.99,2), but SLP stalls
  are possible, so this is not a classification.
* The 13 exact a=2 covers in `rigidity/families.jsonl` all have min depth 0 (global maximisers if S(6)=2), with tight
  sets containing whole boundary segments (flush axis-parallel tiles). Every one keeps >=2 tiles within 2 deg of
  axis-parallel, even when 4 are tilted. So the maximiser set at value 2 is a large positive-dimensional
  semi-algebraic set.

## D5: shape-relaxation tests. diameter, width and area witnesses are insufficient (numerical refutation)
Candidate lemma D(5): for 5 unit squares and a>2, the uncovered set of S_a has diameter > sqrt2. (It would imply
S(6)=2. It is what an adaptive two-exclusive-point argument needs.) Test: replace the 6th tile by a larger convex K
and ask whether 5 unit squares + K cover S_a. A cover refutes every argument that uses only properties K shares with
a unit square.
* K = disk of diameter sqrt2 (`d5_disk.py`): **covers at a=2.01, 2.03, 2.06.** At a=2.01 the 5-square uncovered set U
  has all vertices within 0.70709 < sqrt2/2 of one point, so diam(U) <= 1.41377 < sqrt2 and **D(5) is FALSE**.
* K = disk(diam sqrt2) ∩ strip(width 1), which is diameter <= sqrt2 and width <= 1, area 1.285 (`d5_lens.py`): **covers at a=2.01 and a=2.03**. At a=2.06, 8 Powell starts gave a best leftover of 7e-4 (no cover found; run stopped).
  The cover survives shrinking every piece by 1e-7. Here U5 has area 0.651 < 1, diam <= sqrt2, width <= 1, yet
  no unit square covers it (Powell over 171 starts: min leftover area 0.0095, consistent with S(6)=2).
  (The a=2.01 details were checked. The a=2.03 cover is the raw optimiser output in d5_witnesses.json.)
Consequence: **no argument that uses only the diameter, width and area of the uncovered set of 5 tiles
can prove S(6)=2, and neither can one that sees a single tile only through its diameter and width.** The exact square shape of each tile, its corners and both widths, is essential. This sharpens
lp/LP_NEGATIVE.md (fixed witnesses) and the multi-disk approach (exclusive disks encode only diameter).
All shapely/float, not certificates. The refutations are robust (positive shrink margin), but they are numerical.

## Verdicts
1. **Extremal/rigidity at a*** (priority 1): **framework set up (E1-E6, elementary proof sketches; E4 needs branchwise care at vertex-type tight points), no closure.** Turning it into a proof needs a
   classification of the tight-point incidence patterns (contact "tensegrities") of jammed 6-configurations with
   a in (2,2.0362], then solving the KKT polynomial systems for each pattern. Counting alone does not help:
   each tight point costs one equation, so the 3k+1 needed constraints for k stressed tiles are generically
   available. The maximiser set at a=2 is large and degenerate, so this enumeration is at least as large as the current B&B.
   Possible future use: E6 plus E5 as extra pruning rules inside B&B **only** if the B&B is restricted to optima.
   That is legitimate by E1, but a pose box rarely certifies "not jammed", so the gain is unclear.
2. **Private regions / S(5) equality case:** "some tile's private region misses a side-2 sub-square, so the other 5 cover
   side 2, so the S(5) equality structure pins them": fails. 5-covers of [0,2]^2 are not rigid (shifted-row "brick"
   covers stick out of the sub-square and supply the frame). Near-covers have large private regions anyway. Not viable.
3. **Literature (n=5,7 tools):** only DLT 2601.16535 (S(5), S_bd), Januszewski 2009 (S(5)=2), Soifer 2006,
   Friedman-Paterson 2006, Sriswasdi 2609.15876 (GridLen, L2 false). There is no n=6 partial result or tool we do not already use.
   (Search engines' summaries wrongly say S(6)=2 is proved; DLT state it as Conjecture 1.1.)
4. **Sharpness meta-lesson:** any valid argument must be tight on the whole a=2 maximiser set (including covers with 4
   tilted tiles). E2 turns this into: *show the open squares miss a point of [0,2]^2 for every closed a=2 cover and
   every non-cover*. Global counts with slack at a=2 cannot work.

Best lead from this round: none that closes a case. E2's open-cover form and E5/E6 are clean tools to keep.
D5 removes adaptive diameter, width and area witness arguments.
