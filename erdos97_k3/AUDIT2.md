# AUDIT2: independent skeptical audit of the claim n_3 = 9 (2026-10-10, ~06:30 CST)
Auditor: a separate agent session. It reused none of the pipeline code except where stated below, and it edited none of the existing files.
My scripts are in audit2_code/ (copied from /workspace/audit2).
**Caveat: this is still an AI audit, not a human referee.**

## Verdict summary
| # | Item | Verdict |
|---|---|---|
| 1 | Problem formulation | OK, with one stated convention: strictly convex polygon, "at least 3". A weakly convex reading (180° vertices allowed) is NOT covered. |
| 2 | Pruning soundness + enumeration completeness | OK. My own enumerator reproduces exactly the 40,096 D_8 classes. |
| 3 | LP / Singular / cert0 re-verification | OK. 300/300 LP certificates, 50/50 raw-unit, 55/55 cert0-unit, 5/5 cert0 zero-dim. No disagreements. |
| 4 | Hand proofs, translate lemma, Fact (D) | Mostly OK. The #2547 write-up is too compressed to check as written (see below). |
| 5 | Polynomial encoding / Danzer test | OK |
| 6 | Literature | Still open publicly: forum thread #97 says n_3 ∈ {8,9}. No n_3 = 9 claim found. |

**Overall:** I found no error. The claim "n_3 = 9" is supported as a **computer-assisted result**, conditional on:
- the correctness of Singular, FLINT/Arb and sympy;
- the strict-convexity convention;
- an expanded write-up of the #2547 hand proof.

It is not yet suitable to announce as a theorem without a human check of the hand proofs and of the full-population cert0 runs, which I only sampled.

## 1. Formulation
Erdős's question, as quoted in the erdosproblems.com #97 thread ([Er75f, p.100]), asks for the smallest n_k such that some convex n-gon has every vertex with k other vertices equidistant from it.

- **"At least 3" vs "exactly 3".** The pattern approach picks 3 witnesses out of possibly more, so it covers "at least 3". Since n_3 = 9 is attained by Danzer's nonagon, where all counts are exactly 3 (sallerk's exact coordinates), the answer is the same under either reading.
- **Distance may depend on the vertex.** This is handled: the equalities are per vertex only.
- **Convexity.** The pipeline assumes vertices in strictly convex position, ccw. Strictness is used essentially:
  - C2 (no 3 collinear);
  - strict TRI;
  - C3 (a, b not on the line p_i p_j);
  - Rabinowitsch factors (orientations ≠ 0).

  The forum (mysticflounder; veljjanoski's k = 4 enumeration) uses the same "strict convex position" convention. However, an 8-gon with some 180° vertices is NOT excluded by this work. It should be stated as a convention, or handled separately.
- **Degenerate cases.** Coincident points are excluded by the Rabinowitsch factors (squared distances ≠ 0), which is legitimate.

## 2. Pruning rules and enumeration
**Each rule re-derived:**
- E: definition.
- C1: |T_i ∩ T_j| ≤ 2, because the circumcentre is unique.
- C2: a pair in 3 triples puts 3 centres on its perpendicular bisector, so they are collinear.
- C3: line p_i p_j is the perpendicular bisector of ab, so a and b are strictly on opposite sides, hence cyclically separated by i and j.
- O: the 3 witnesses lie in an angular window < π at p_i, so the inscribed angle at the middle witness is > 90°.
- Q: the diagonals of a convex quadrilateral cross; then apply the strict triangle inequality.
- The order-cycle check is a consequence of O + E.
- D_8 symmetry: the constraints are invariant under rotation, and under reflection + relabelling (O keeps the middle element).
- DFS prunes partial assignments. All rules are monotone, so this is sound.

**My own enumerator** (audit2_code/my.c) was written from scratch with different data structures:
- per-pair witness lists;
- class merging by repeated relabelling;
- Floyd–Warshall closure of the strict order on a char matrix;
- no canonical pruning in the DFS.

Canonicalisation under D_8 was done separately in Python (canon.py).

**Result:** 639,162 labelled survivors (identical to enum_b's count), giving **40,096 D_8 classes, equal as a set to the ledger's 40,096** (0 missing, 0 extra). Every survivor maps to a ledger class.

**Limitation:** my enumerator applies the same rule set. It confirms the implementation of the rules, not that they are the only consequences one could use. That is fine, since extra rules would only prune more.

## 3. Re-verification with my own code
- **LP** (lpv.py): 300 random certificates from cert8.jsonl. I rebuilt the classes (own union-find) and the rows (same documented row order: Q, TRI, obtuse with c = 7071/10000, and I checked 2c² < 1). Result: **300/300 valid** (y > 0, all combined coefficients ≤ 0). Validity of each row as a strict inequality was re-derived by hand.
- **Singular raw-unit** (sg.py): 50 random "how: I" cases, with my own encoding (p0 = (0,0), p1 = (1,0), squared-distance differences) and Singular std over Q. Result: **50/50 unit**.
- **cert0 / cert0b** (sg2.py): 60 random cases, rebuilt with my own encoding and ONE Rabinowitsch variable t·∏f_q − 1 (instead of the pipeline's one t per factor), then slimgb + std.
  - **55/55 CERT-UNIT reproduce the unit ideal.**
  - **5/5 CERT-NONCONVEX reproduce dim 0 with the same vdim D** (16, 16, 4, 12, 4).
  - For these 5 I solved with msolve and tested all 56 orientations numerically. **No strictly convex real solution** (real-root counts 12, 0, 0, 4, 0).
  - (My first run had a missing-parenthesis bug that gave false "non-unit" results. It was found and fixed, and all results above come from the corrected run.)
- **#3090:** I re-ran c3090.py. It reproduced: original equations in the reduced ideal = True; vdim 14, radical vdim 8 = deg w; 8 real roots, all certified nonconvex. I re-checked the hand reduction by hand:
  - 0,2,6 equilateral, with both rotation signs kept;
  - 1,3,7 equilateral, from T1, T3 and T7;
  - p5 = p3 + p7 − p1, the second circle intersection, since p5 ≠ p1;
  - the remaining equations are listed correctly.
- **Not done by me:** a population-wide re-run of the 3,860 C, 1,077 C′ and 192 C″ verdicts. The C″ tier (old sequential saturation) was not sampled by me at all.

## 4. Hand proofs
- **Fact (D)** (chord directions increase monotonically in a strictly convex ccw polygon, lifted to one turn): a correct classical fact. The write-up should include a short proof.
- **Translate lemma:** correct. conv(A) ⊕ [0,u] for a triangle A has ≤ 5 vertices, but 6 distinct points in strictly convex position are all vertices.
- **#28:** correct. Interior angles of 60°/120° at 1, 2, 5, 6 give exterior angles summing to 360°, leaving 0 for the other four vertices.
- **#366:** correct. The convex order 0,2,3,4 forces φ ∈ (60°, 120°), while (D) forces θ(1,3) ∈ (120°, 180°).
- **#4190:** correct, given the two parallelogram relations (derivation checked: reflection in line p2p7, since p5 ≠ p0).
- **#2550:** correct. The parallelogram lemma for convex quadrilaterals with equal opposite sides is valid, and (D) gives θ02 < θ13.
- **#2547:** the trig argument is plausible, but the step "γ ∈ (60+t, 300−t)" is asserted without justification in NOTES. Needs a written proof. The class is also covered only by the hand tier in the ledger.
- The forced linear relations for 2547/2550/4190/28/366 were checked by the pipeline with msolve only (rhombus_forced.py). I did not re-derive them with Singular.

## 5. Encoding
- The polynomial system (2 equations per vertex, gauge p0 = (0,0), p1 = (1,0)) loses no information, since similarity transformations are free.
- Rabinowitsch factors (squared distances, orientations ≠ 0) are true for every strictly convex realisation, so they only enlarge the set of solutions.
- **Danzer test** (own check, audit2_code/my9.c + dz.txt): on the exact-structure Danzer 9-gon data:
  - strictly convex (min orientation 0.213);
  - equidistance error 4e-16;
  - my N = 9 port of the full rule set (E, O, C1–C3, Q, order) **accepts** its pattern.

## 6. Literature (checked 10 Oct 2026)
- erdosproblems.com/forum/thread/97: sallerk (17 Sep 2026) says that "for k = 3 the smallest n is 8 or 9" (n = 7 excluded by z3/Gröbner solver verdicts). No later post on k = 3 (latest posts concern k = 4).
- A web search found nothing claiming n_3 = 8 or 9.
- I did not exhaustively search arXiv 2025–26, nor sallerk's GitHub commits after 17 Sep. **Re-check both before any announcement.**