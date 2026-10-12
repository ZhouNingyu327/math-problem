---
title: "No strictly convex octagon has three equidistant vertices from every vertex: $n_3 = 9$"
subtitle: "A computer-assisted note on a side question of Erdős Problem #97 (preprint-style; not peer-reviewed)"
date: "10 October 2026"
geometry: margin=2.3cm
fontsize: 10pt
---

**Rigor labels.** Each claim carries one of these labels:
**[P]** proved by hand in this note;
**[C]** computer-verified by exact arithmetic (rational / Gröbner bases over $\mathbb{Q}$ / certified intervals), with a stated trust base;
**[N]** numerical or heuristic evidence only;
**[L]** taken from the literature or from the forum, not re-proved here.

## 1. Problem and history

Erdős [Er46b] conjectured that every convex polygon has a vertex with no three other vertices at one common distance from it.
Danzer disproved this with a convex 9-gon in which every vertex has three others at one common distance (the distance depends on the vertex) [Er87b, p.175] **[L]**.
Erdős [Er75f, p.100] asked for the least $n_k$ such that some convex $n$-gon has every vertex with $k$ other vertices equidistant from it.
Fishburn–Reeds [FiRe92] gave a 20-gon with one uniform distance **[L]**.
The main open question in #97 (erdosproblems.com) is now $k=4$.

For $k=3$, the forum thread on #97 establishes the following **[L]**:

- explicit coordinates for Danzer's nonagon, so $n_3\le 9$;
- impossibility for $n\le 6$;
- impossibility for $n=7$: sallerk, Sep 2026, using SMT-solver verdicts.

This left $n_3\in\{8,9\}$.
The pattern constraints C1–C3 used below go back to veljjanoski's $k=4$ enumeration on the forum, and constraint O to sallerk.

**Convention.** "Strictly convex": the vertices are corners (every interior angle $<180^\circ$), so no three vertices are collinear.
This is the convention of the forum work, and Danzer's nonagon satisfies it.

**Main result.** No strictly convex octagon has every vertex with at least three other vertices at a common distance from it.
Hence $n_3=9$ for strictly convex polygons.
This is **[C]+[P]**, computer-assisted, and the $n=7$ case is re-done independently here **[C]**.

## 2. Reduction to witness patterns

Label the vertices $p_0,\dots,p_7$ counter-clockwise.
For each vertex $i$, choose a witness triple $T_i$ of three other vertices with $d(i,j)=d(i,k)=d(i,l)$.
The data $(T_0,\dots,T_7)$ is a *pattern*.
The necessary conditions below are each proved **[P]**:

- **E (equalities).** The equalities generate classes of equal distances (union-find).
- **C1.** $|T_i\cap T_j|\le 2$: two distinct circles meet in at most 2 points.
- **C2.** No pair $\{a,b\}$ lies in three triples. Otherwise three centres would lie on the perpendicular bisector of $ab$, i.e. be collinear.
- **C3.** If $\{a,b\}\subseteq T_i\cap T_j$, then the line $p_ip_j$ is the perpendicular bisector of $ab$. So $a$ and $b$ lie strictly on opposite sides of it, and $\{a,b\}$ separates $\{i,j\}$ in cyclic order.
- **O (obtuse middle).** Let $T_i=\{j,k,l\}$ in ccw order after $i$. Then $i$ and $k$ lie on opposite sides of chord $jl$. So the inscribed angle at $k$, on the circle centred at $p_i$, is $>90^\circ$. This gives $d(j,l)>d(j,k)$, $d(j,l)>d(k,l)$, and $d(j,l)>\tfrac{1}{\sqrt2}\,(d(j,k)+d(k,l))$.
- **Q (classical).** For a convex quadrilateral $abcd$: $|ac|+|bd|>|ab|+|cd|$ and $|ac|+|bd|>|ad|+|bc|$. The diagonals cross; apply the triangle inequality at the crossing point.
- **TRI.** The strict triangle inequality holds, since no three vertices are collinear.
- **Symmetry.** Patterns are taken up to the dihedral group $D_8$ (rotation, and reflection with relabelling).

As a soundness test, all inequality rows were evaluated on the true Danzer nonagon, in both orientations. All are strictly positive **[N]**.

## 3. Enumeration

A C depth-first search (`enum8.c`) yields **40,096** $D_8$-classes of patterns satisfying E, C1–C3, O and Q. The enumerator does not use TRI; TRI enters only in the LP tier.
A second, independently written enumerator (`enum_b.c`) uses bitsets, Warshall closure and a different canonical form. It produces the identical set **[C]**.
Completeness rests on the soundness of the rules above and on the correctness of the C code.

## 4. Refutation of every class

| Tier | Method | Classes |
|---|---|---|
| A | Exact LP (Gordan) certificate | 34,962 |
| B | Hand proof | 5 |
| C | Singular Gröbner basis over $\mathbb{Q}$: unit ideal | 3,860 |
| C$'$ | Certified zero-dimensional: all real solutions nonconvex | 1,077 |
| C$''$ | Singular saturation over $\mathbb{Q}$: unit ideal | 192 |
| | **Total** (ledger `ledger8.tsv`, coverage asserted) | **40,096** |

**Tier A [C].** The linear consequences of E/O/Q/TRI are inequalities $L_r>0$ in the distance classes.
A certificate is a vector $y\ge 0$, $y\ne 0$, with $\sum_r y_rL_r\equiv 0$ (or $\le 0$ identically).
This contradicts strict positivity.
The certificates were found with floating-point LP, then verified in exact rational arithmetic. A second, independently written checker re-verified all 34,962.

**Tier C [C].** Fix the gauge $p_0=(0,0)$, $p_1=(1,0)$. The pattern gives the polynomial system $I$.
Adding the Rabinowitsch variables $t\,f-1$ forces $f\neq 0$; here $f$ is a squared distance or an orientation determinant, and both are nonzero on every strictly convex realisation.
A Singular `slimgb`/`std` computation over $\mathbb{Q}$ returning $\{1\}$ shows there are no solutions at all.
Fifteen classes instead use the **translate lemma [P]**: if $A$ and $A+u$ are disjoint subsets of a strictly convex set, then $|A|\le 2$. The reason is that $\mathrm{conv}(A\cup(A+u))=\mathrm{conv}A\oplus[0,u]$ has at most $|A|+2$ vertices.

**Tier C$'$ [C].** These classes have finitely many complex solutions. The steps are:

1. Compute the number $D$ of solutions as the vdim of the (radical) ideal over $\mathbb{Q}$, in Singular.
2. Obtain a rational parametrisation $x_i=g_i(\vartheta)/w'(\vartheta)$, $w(\vartheta)=0$ from msolve.
3. Re-verify the parametrisation exactly in FLINT: $w$ is squarefree, $\deg w=D$, every generator vanishes modulo $w$, and the separating form is consistent.
4. Isolate the real roots of $w$ in Arb balls, cross-checked by an exact Sturm count.
5. Certify, with interval arithmetic, an orientation sign violating strict convexity at every real root.

msolve is used only as an *untrusted oracle*: its output is checked exactly.

**Tier B [P].** Classes #28, #366, #2547, #2550 and #4190 are refuted by hand; full proofs are in `HANDPROOFS.md`.
The tools are the exterior-angle sum, Fact (D), and a parallelogram lemma.
Fact (D) (two-step form, written D2 in `HANDPROOFS.md`): the two-step chord $p_kp_{k+2}$ has a direction strictly between those of edges $k$ and $k+1$.
The forced linear relations used, such as $p_4=p_2+p_6-p_0$, follow by hand from the elementary rule "equilateral triangle plus a second apex gives a reflection". They were re-derived with Singular over $\mathbb{Q}$ on the full systems; every false control relation is non-unit **[C]**.
The last class, #3090, was reduced by hand to a 19-variable system with exactly 8 solutions, all real and all certified nonconvex **[P]+[C]**.

## 5. Verification and audits

- Two independent enumerators agree **[C]**.
- All LP certificates were re-verified by independent code **[C]**.
- msolve versus Singular unit verdicts on samples: 0 disagreements. `slimgb` versus `std`: 49/50 identical, 1 timeout, 0 disagreements **[C]**.
- A numerical re-solve of 40 zero-dimensional cases found no convex real root **[N]**.
- An internal audit (AUDIT2) found no error but three gaps: the #2547 write-up, the Singular re-derivation of forced relations, and the convexity convention. All three are addressed.
- **Known issue:** on non-radical inputs, msolve 0.7.5 gave non-reproducible real-root counts. For this reason no verdict relies on msolve alone.

## 6. Software and trust base

- **Trusted for verdicts:** Singular 4.4.1 (`std`, `slimgb`, `sat`, `radical`, `vdim`); python-flint 0.9.0 (FLINT/Arb); sympy 1.14.0; Python `fractions`; gcc 14.2 (enumerators).
- **Untrusted search only:** numpy and scipy (finding LP certificates); msolve 0.7.5 (parametrisations, hints).
- Modular (mod 32003) computations only choose hints; they never decide a case.

## 7. Caveats

1. The proof is computer-assisted and **not peer-reviewed**. All work, including the "independent" checks, was done by one automated agent, so independence means independent code, not independent people. Nothing is formalised.
2. The result holds under the **strict convexity** convention. Erdős wrote only "convex polygon".
3. **Weakly convex polygons** (some $180^\circ$ vertices): settled in the appendix **[C]**, after an audit correction (AUDIT3); the corrected argument passed an independent re-audit (AUDIT4).
4. The $n=7$ input is re-done here **[C]**. For $n\le6$ the enumerator itself outputs no classes **[C]**, consistent with the forum **[L]**.

## Appendix: weakly convex polygons (corrected after audit AUDIT3, passed by audit AUDIT4)

Allowing $180^\circ$ vertices (distinct points in convex position, not all collinear):

- E, C1–C3, O and Q(ab,cd) stay valid and strict **[P]**.
- **Q(ad,bc) is only non-strict**: with four collinear vertices, $|ac|+|bd|=|ad|+|bc|$.
- TRI is non-strict, and orientation non-vanishing is lost.
- The enumerator's use of Q stays sound: with distinct points, $|ac|\le|ad|$ and $|bd|\le|bc|$ cannot both hold in the equality case. So the 40,096 classes are unchanged.

**Octagons [C].** An independent audit (AUDIT3) found that 1,398 Gordan certificates get their strictness only from Q(ad,bc) rows. Of the 1,859 certificates that use such rows, 461 were replaced by the auditor with certificates using a genuinely strict row. These are re-verified with our own checker and stored in `weak/rescued461.json` **[C]**. It also found that 9 classes were carried over on the translate lemma, which needs strict convexity. The weak octagon case is therefore **reduced to 1,407 classes**. All other classes are refuted for weakly convex octagons. **Closing the 1,407 [C].** A Q(ad,bc)-equality forces four *consecutive* collinear vertices $p_{i-1},p_i,p_{i+1},p_{i+2}$. Parametrising them on one segment, with all ratios distinct and in neither endpoint, gives a unit ideal over $\mathbb{Q}$ for all $1{,}398\times 8=11{,}184$ cases. The 9 translate classes are split by a single $180^\circ$ vertex: all 72 cases are unit. Positive controls (dropping equations) give positive-dimensional ideals.

**Independent nonconvexity check [C].** Every finite-case "nonconvex" verdict used in the weak argument was re-certified by a second method: msolve real-root isolation plus exact rational interval arithmetic. The box counts match the certified real-root counts. All 156 PASS; for the two n=7 cases all 8 boxes each are nonconvex.

**$n\le7$ [C].** Two independently written enumerators give 0 classes for $n\le 6$ and the same 27 classes for $n=7$. All 27 are refuted with saturation by distances only: 25 have no solutions, 2 are certified nonconvex. Hence **$n_3=9$ also for weakly convex polygons [C]+[P]** (computer-assisted; the corrected weak argument passed audit AUDIT4).

## References

- [Er46b] P. Erdős, On sets of distances of n points, Amer. Math. Monthly 53 (1946).
- [Er75f] P. Erdős, On some problems of elementary and combinatorial geometry, Ann. Mat. Pura Appl. 103 (1975), p.100.
- [Er87b] P. Erdős, Some combinatorial and metric problems in geometry, Intuitive Geometry (Siófok 1985), p.175.
- [FiRe92] P. Fishburn, J. Reeds, Unit distances between vertices of a convex polygon, Comput. Geom. 2 (1992).
- T. Bloom, Erdős Problem #97, erdosproblems.com/97, and its forum thread (posts by sallerk, veljjanoski, mysticflounder).