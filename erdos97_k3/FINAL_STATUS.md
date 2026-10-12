# Erdős #97 side question, k = 3: is n_3 = 9?  — FINAL STATUS (2026-10-10 06:40 CST, after AUDIT2 fixes)

## Claim (computer-assisted; NOT peer-reviewed, NOT externally audited)
No strictly convex octagon (every vertex a corner: interior angle < 180°, no three vertices collinear) has every vertex with at least 3 other vertices at a common distance from it.
Together with Danzer's nonagon (n_3 ≤ 9) and the n = 7 case (sallerk, Sep 2026; independently re-done here), this gives **n_3 = 9**.
Literature check (forum thread #97 and sallerk's repo re-read 10 Oct 05:3x and again 06:3x; sallerk's repo has no p97 commit after 17 Sep, its last commit is 22 Sep (p827); arXiv/web search found no n_3 paper): the k = 3 status there is still n_3 ∈ {8, 9}.
No n = 8, k = 3 result was found. (A search-engine "synthesis" asserting n_3 = 9 is unsupported by its own sources.)
The Lean "convex octagon" PR (lean-pool #278) is about k = 4.

## Proof structure
1. Reduction to witness patterns: choose 3 equidistant witnesses T_i per vertex (labels 0..7 in ccw order).
   Necessary conditions, each proved in audit/AUDIT.md §1: E (equalities), C1–C3 (veljjanoski), O (obtuse middle, sallerk),
   Q (classical diagonal-sum inequality of a convex quadrilateral), TRI (strict triangle inequality), D_8 symmetry.
2. Enumeration: 40,096 classes (enum8.c). An independent enumerator (enum_b.c, different data structures and canonical form)
   gives the identical class set.
3. Refutation of every class. Ledger: ledger8.tsv (built by ledger.py, which asserts coverage of all 40,096):

| Tier | Method | Classes |
|---|---|---|
| A exact-LP | Gordan certificate y ≥ 0 over linear consequences of E/O/Q/TRI; all re-verified in exact Fractions by independent code (audit/audit_cert.py) | 34,962 |
| B hand | hand proofs, written out in full in HANDPROOFS.md (incl. a proof of Fact (D2) and the expanded #2547 argument): #28 (exterior-angle sum), #366, #2547, #2550 (parallelogram lemma), #4190. Every forced linear relation is derived by hand (rule R) and re-derived with Singular slimgb over Q on the full system (forced_sing.log: 11 relations unit, every control non-unit; audit/rule_R.sing proves rule R itself) | 5 |
| C Singular-exact | Singular slimgb/std over Q gives the unit ideal for I, for I + Rabinowitsch (distances/orientations ≠ 0), or for the translate-lemma system | 3,860 |
| C′ certified zero-dim | exact solution count D (Singular over Q; radical where needed) + msolve parametrisation VERIFIED exactly in flint (w squarefree, all generators ≡ 0 mod w, injective form, deg w = D) + arb root enclosures cross-checked with an exact Sturm count + certified orientation signs ⇒ every real solution nonconvex (or no solution) | 1,077 |
| C″ Singular-sat | Singular sequential saturation over Q = (1) | 192 |
| D msolve-only | — | 0 |
| X uncertified | — | 0 |

   #3090 (the last open class) was closed by a hand reduction (60° rhombus {1,3,5,7}, equilateral 0,2,6) to a 19-variable system.
   It has 8 distinct complex solutions (vdim of the radical = 8 = deg w), all 8 real, all certified nonconvex (c3090.py).
   The 15 translate-lemma classes are in tier C: the lemma (conv(A ∪ (A+u)) = conv A ⊕ [0,u] has ≤ 5 vertices) is proved by hand,
   and the polynomial system it needs was re-proved unit by Singular.

## UPDATE 08:45 CST (AUDIT3): the weak case is DOWNGRADED. The weakly convex octagon case is reduced to 1,407 classes, and closing them is in progress.
- The 08:30 claim "n_3 = 9 also for weakly convex polygons" is WITHDRAWN.
- Q(ad,bc) is non-strict when 4 vertices are collinear. Because of this, 1,398 LP certificates (audit2_code/wbad.json) do not cover the weak case.
  In addition, 9 classes were carried over via the translate lemma, which needs strict convexity.
- Weak n ≤ 7: closed. For n ≤ 6, two independent enumerators (ours and AUDIT3's) give 0 classes.
- The strictly convex result is unaffected.
- 09:35: all 1,407 gaps are closed (weak/straight3.py, all unit), so n_3 = 9 also holds for weakly convex polygons [C]. The corrected weak argument PASSED audit AUDIT4.
  Independent nonconvexity re-check: 156/156 pass (incl. #385), 2 weak7 cases consistent.

## Convexity convention (AUDIT2 gap 3)
- The result is about STRICTLY convex octagons. This matches Danzer's nonagon (all 9 vertices are corners), the erdosproblems #97 forum
  convention (mysticflounder, veljjanoski: "strictly convex position"), and the usual meaning of "vertex of a convex polygon".
  Erdős's own wording ([Er46b], [Er75f, p.100], [Er87b]) is just "convex polygon" / "convex n-gon"; he does not discuss 180° vertices.
- Weakly convex octagons (some 180° "vertices") are NOT covered. They do not reduce to smaller strictly convex cases: deleting the
  180° points also deletes witnesses that other vertices need, and the deleted points still need their own 3 witnesses.
  Which steps fail under non-strict convexity:
  * C2 (three collinear centres impossible) fails: points on one hull edge are collinear.
  * O, Q, TRI hold only with ≥ (degenerate quadrilaterals and triangles), so a Gordan certificate Σ y_r L_r ≤ 0 is no longer a
    contradiction. The LP tier would have to be redone with strictness kept only where it is still provable.
  * Rabinowitsch factors for orientations ≠ 0 are invalid. Squared-distance factors stay valid (vertices are distinct).
  * Fact (D2) needs exterior angles > 0. With 0° exterior angles, the edge directions are only non-decreasing.
  * C1, C3 and E still hold.
  Handling this case means a new enumeration with weaker rules plus new algebra. It is not done. It is stated as an open variant.

## Cross-checks
- slimgb vs std: 50 random cases, 49 identical, 1 std timeout, 0 disagreements. msolve vs Singular unit verdicts: 0 disagreements.
- Inequality families evaluated on Danzer's true 9-gon (both orientations): all strictly positive.
- Independent numeric re-solve (Singular solve.lib) of 40 zero-dim cases: no convex real root.

## Known issues / caveats
- msolve 0.7.5 on NON-radical inputs (degenerate solutions present) gave non-reproducible real-root counts (e.g. #3732: 28/33/34)
  and occasional hangs. The cause is the random separating form plus multiplicities. No verdict in the ledger relies on msolve alone.
- Trust base: correctness of Singular 4.4.1 (std, slimgb, sat, radical), python-flint 0.9.0 / FLINT / Arb, sympy 1.14.0
  (exact Sturm count and expansion), Python 3.13.5 Fractions, gcc 14.2 for the C enumerators. numpy 2.5.3 / scipy 1.18.1
  are used only to FIND LP certificates (verified exactly afterwards). The mod-32003 steps only choose factors (hints), never decide.
- All of this was done by one agent, so the "independent" checks are independent code, not independent people.
  The enumeration's completeness rests on the soundness proofs of the pruning rules plus agreement of two enumerators.
- Not formalised (no Lean). Hand proofs should be re-read by a human.

## Reproduce
enum8.c / enum_b.c → s8.txt; lp_filter.py, lp_cert.py → cert8.jsonl; audit/audit_cert.py; alg/hint/sat scripts;
unit_sing.py, unit_slow.py, unit_alt.jsonl; cert0.py, cert0b.py, c3090.py; ledger.py → ledger8.tsv.

## 2026-10-10 ~09:25 CST — after AUDIT4
- AUDIT4 passed the corrected weak argument. n_3 = 9 holds for strictly convex polygons and for weakly convex polygons
  (computer-assisted, not peer-reviewed).
- audit2_code/rescued461.json was re-verified with our checker (audit_cert rows; strict rows = Q(ab,cd) and OBT): 461/461 ok, none in wbad.
  A copy is in weak/rescued461.json. 33,103 + 461 = 33,564 LP certificates are weak-valid.