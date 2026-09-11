# Proof attempt: \(S(6)=2\)

**Status: incomplete.** This document does **not** prove Dósa–Lángi–Tuza Conjecture 1.1.
It records the strongest argument we can currently close, and isolates a precise
unproved lemma. Numerics in [`RESULTS.md`](RESULTS.md) are supporting evidence
only; they are never used as a proof step.

---

## 中文摘要

目标：证明六个单位正方形无法覆盖边长严格大于 \(2\) 的正方形，即 \(S(6)=2\)。

已完成的部分：

- 从直径 \(\sqrt{2}\) 推出：边长 \(a>2\) 时，四个顶点必须由四个不同的单位正方形覆盖；四个边中点同样如此；顶点与中心不能同属一个单位正方形；没有单位正方形能同时碰到大正方形的一组对边。
- 组合分类完全：记 \(k\) 为“既盖顶点又盖中点”的单位正方形个数，则 \(k\in\{2,3,4\}\)。\(k=0,1\) 不可能。\(k=4\) 时顶点–中点匹配在 \(C_4\) 上只有顺时针、逆时针两种，且二者关于反射等价。
- 两个不盖顶点的“额外正方形”若都不碰边界，则周长不够（用 DLT 的 \(L\) 形引理）。因此额外正方形必须参与边界。
- 在最接近 Januszewski / DLT \(S(5)=2\) 的 **Case 2** 构型中：三角形面积论证仍然有效；第六个正方形与象限 \(R\) 的交（若非空）被直径限制在靠近中心的细条里。进一步，当 \(a>\sqrt{5}\) 时，\(R\) 落在大正方形边界上的那条边出现一个 \(L\) 形缺口，而其余四个单位正方形都够不到这个缺口——**该子构型在 \(a>\sqrt{5}\) 时被排除**。
- \(a\in(2,\sqrt{5}]\) 的同一子构型、以及 \(k=2\) 对边中点、\(k=3\)、\(k=4\) 仍未排除。

**未完成的瓶颈：** 对 \(a\in(2,\sqrt{5}]\)，三个受约束的单位正方形能否盖住象限 \(R\)；以及其余组合类型。因为 \(\lambda < S(3)=\sqrt{\varphi}\)，没有三个单位正方形的一般性禁止。

因此：本仓库给出的是一个**部分证明 + 一条干净的剩余引理**，不是 \(S(6)=2\) 的完整证明。边界覆盖的数值例子（\(s=2.33\)）说明 \(S_{\mathrm{bd}}(6)>2\) 很可能成立，证明不能走“边界盖不住”这条路，必须处理内部。

---

## 0. Scoreboard

| Claim | Status |
|---|---|
| \(S(6)\ge 2\) (trivial \(2\times 2\) tiling) | proved, classical |
| \(S(6)\le\sqrt{6}\) (area) | proved, classical |
| \(S(5)=2\) | proved by Januszewski; alternative proof by Dósa–Lángi–Tuza |
| Conjecture \(S(6)=2\) | **open** (this document) |
| Distance / capacity lemmas below (Lemmas D1–D6) | **proved here** |
| Combinatorial types \(k\in\{2,3,4\}\); \(k=4\) matching is chiral | **proved here** |
| Two extras missing \(\mathrm{bd}(S)\) is impossible | **proved here** |
| DLT Case-2 triangle: \(V_3\) misses \([c,m_3]\) | **proved here** |
| Diameter sliver for \(F\cap R_4\) | **proved here** |
| Case-2 subfamily, \(a>\sqrt{5}\): L-gap on \(\mathrm{bd}(S)\cap R_4\) | **proved here** (Lemma T8) |
| Case-2 subfamily, \(a\in(2,\sqrt{5}]\): three constrained squares cannot cover \(R_4\) | **OPEN** — Remaining Lemma RL-A_adj |
| Sister types \(k=2\) opposite, \(k=3\), \(k=4\) | reduced to RL-A_opp, RL-B1/B2, RL-C; **open** |

A complete proof of \(S(6)=2\) would be: Lemmas D1–D6 + the census + RL-A_adj + RL-A_opp + RL-B1 + RL-B2 + RL-C, or a single lemma that covers all five.

---

## 1. Notation and standing hypotheses

Let a *unit square* be a closed square of side \(1\) in the Euclidean plane, subject
to rigid motions (translations and rotations). Overlaps are allowed.

Following Friedman–Paterson and Dósa–Lángi–Tuza (DLT),
\[
S(n)=\sup\{\,a\ge 0:\ \text{a square of side \(a\) can be covered by \(n\) unit squares}\,\}.
\]
The supremum is a maximum: a decreasing sequence of coverable sides has a
coverable limit by compactness of \(\mathrm{SE}(2)^n\). So \(S(n)\) is attained.

The *boundary* analogue \(S_{\mathrm{bd}}(n)\) is the largest side whose *perimeter*
can be covered by \(n\) unit squares. Always \(S(n)\le S_{\mathrm{bd}}(n)\).

**Standing hypotheses.** Let \(S\subset\mathbb{R}^2\) be a closed square of side
\(a\in(2,\sqrt{6}]\), and let \(\mathcal{F}=\{U_1,\dots,U_6\}\) be a family of
unit squares with \(S\subseteq\bigcup\mathcal{F}\). Write \(\lambda=a/2\in(1,\sqrt{6}/2]\).
(If \(a>\sqrt{6}\) the area of \(S\) exceeds \(6\), which is already impossible.)

Label \(S=[0,a]^2\) with vertices counterclockwise
\[
v_1=(0,0),\quad v_2=(a,0),\quad v_3=(a,a),\quad v_4=(0,a),
\]
midpoints
\[
m_1=\bigl(\tfrac a2,0\bigr),\ 
m_2=\bigl(a,\tfrac a2\bigr),\ 
m_3=\bigl(\tfrac a2,a\bigr),\ 
m_4=\bigl(0,\tfrac a2\bigr),
\]
and centre \(c=(a/2,a/2)\). These nine points are the *important points*, as in DLT §3.
Indices of vertices and midpoints are taken modulo \(4\). The *quadrant*
\[
R_i=\mathrm{conv}\{c,\,m_{i-1},\,v_i,\,m_i\}
\]
is a square of side \(\lambda\).

A unit square has diameter \(\sqrt{2}\). Consequently a single unit square contains
at most one pair of important points at distance \(>\sqrt{2}\).

---

## 2. Literature used as black boxes

We use the following published theorems as axioms. We do **not** re-prove them.

### 2.1 Friedman–Paterson

Friedman–Paterson, *Covering squares with unit squares*, Geombinatorics 15(3) (2006)
([HTML](https://erich-friedman.github.io/papers/covering/covering.html)):

- \(S(2)=1\), by an unavoidable-corner argument: two unit squares covering a
  square of side \(>1\) must each take two corners, and then a pair of opposite
  sides cannot be finished.
- Sketch that “the same method” yields \(S(5)=2\) and \(S(10)=3\).
- \(S(3)=\sqrt{\varphi}\) with \(\varphi=(1+\sqrt{5})/2\), via a one-parameter
  family of perimeter-maximal placements.

They explicitly leave \(n=6\) open; their table of best-known constructions has
the trivial side-\(2\) covering for \(n=6\).

### 2.2 Januszewski

Januszewski, *A note on covering a square of side length \(2+\varepsilon\) with
unit squares*, Amer. Math. Monthly 116 (2009), 174–178, supplies complete proofs
of \(S(5)=2\) and \(S(10)=3\). We could not obtain the PDF in this environment.
Everything below that needs \(S(5)=2\) uses DLT’s alternative proof (Theorem 1.3)
instead of Januszewski’s text.

### 2.3 Dósa–Lángi–Tuza, arXiv:2601.16535

DLT introduce \(S_{\mathrm{bd}}\) and prove:

**Lemma 2.1 (DLT; \(L\)-shape).** Let \(X\) be an L-shape (two orthogonal segments
meeting at an endpoint) maximally embedded in a unit square, with legs \(x\) and
\(l(x)\), \(x>1\). Then \(l(x)<1\), the far endpoint of the long leg is a vertex of
the unit square, and
\[
l(x)=x-x\sqrt{x^2-1},\qquad x\in[1,\sqrt{2}].
\]
The map \(l\) is a strictly decreasing bijection \([1,\sqrt{2}]\to[0,1]\), and
\(x+l(x)\) is strictly decreasing, with \(\sqrt{2}\le x+l(x)\le 2\), the upper
bound \(2\) if and only if the item is homothetic to the target (axis-aligned
\(1\times 1\) L). We re-check the calculus of \(l\) in
[`proof/inequalities.py`](proof/inequalities.py); that is a verification of DLT’s
formula, not an independent existence proof of maximal embeddings.

**Parallelogram fact (DLT §3).** No parallelogram of area \(1\) contains a
triangle of area \(>1/2\). In particular no unit square does.

**Theorem 1.2 (DLT).** \(S_{\mathrm{bd}}(2)=S(2)=1\) and
\(S_{\mathrm{bd}}(3)=S(3)=\sqrt{\varphi}\). Moreover: a unit square that is not a
translate of a \(\lambda\)-square with \(\lambda\ge 1\) covers a *connected* arc of
that \(\lambda\)-square’s boundary of length **strictly less than** \(2\lambda\).
(This is the computation after DLT (2).)

**Theorem 1.3 (DLT).** \(S(5)=2\). The proof is a three-case analysis on a
central item \(S_5\ni c\):

1. \(S_5\) meets \(\mathrm{bd}(S)\) in at most one point: four vertex items cover
   the perimeter, each an L of length \(\le 2\), total \(\le 8=4a\) only if \(a=2\)
   and all four are homothetic.
2. \(S_5\) contains a midpoint, w.l.o.g. \(m_4\). A triangle argument shows that
   the item at \(v_3\) cannot meet \([c,m_3]\). Then
   \(\mathrm{bd}(\mathrm{conv}\{v_4,m_4,c,m_3\})\) is covered by two unit squares,
   contradicting \(S_{\mathrm{bd}}(2)=1\) since the quadrant has side \(a/2>1\).
3. \(S_5\) meets the boundary in a positive-length segment but contains only \(c\).
   Each vertex item contains the vertex and one adjacent midpoint (a chiral
   matching). One vertex item is then forced to cover a connected arc of a
   quadrant-boundary of length \(>5a/2-2\sqrt{2}>a=2\cdot(a/2)\), contradicting
   the \(n=2\) arc bound.

**Theorem 1.4 (DLT).** \(S_{\mathrm{bd}}(4)=2\),
\(S_{\mathrm{bd}}(n+4)=S_{\mathrm{bd}}(n)+\sqrt{2}\) for \(n\ge 4\), and
\(S_{\mathrm{bd}}(5)\approx 2.072>2=S(5)\). For boundary coverings with
\(a>\sqrt{2}\), no unit square meets opposite sides; after a rearrangement,
intersections with the perimeter are connected L-shapes or \(\sqrt{2}\)-chords.

**Conjecture 1.1 (DLT).** \(S(6)=2\), equivalently Soifer’s \(\Pi(2)=7\).

The inequality \(S(5)<S_{\mathrm{bd}}(5)\) is the structural warning for \(n=6\):
a proof of \(S(6)=2\) **cannot** proceed by showing that the boundary of a
square of side \(>2\) is uncoverable by six unit squares. Numerically we have a
boundary covering at side \(2.33\) ([`RESULTS.md`](RESULTS.md)); that is
consistent with Theorem 1.4’s recurrence suggesting \(S_{\mathrm{bd}}(6)\) is
well above \(2\). The obstruction, if the conjecture is true, is interior.

---

## 3. Distance lemmas

Throughout, \(a>2\). Diameter of a unit square is \(\sqrt{2}\).

**Lemma D1 (vertices).** No unit square contains two vertices of \(S\).
Adjacent vertices are distance \(a>2>\sqrt{2}\); opposite vertices are farther.

**Lemma D2 (vertex and centre).** No unit square contains a vertex and \(c\).
Distance \(a/\sqrt{2}>\sqrt{2}\) iff \(a>2\). Algebra: \(a/\sqrt{2}-\sqrt{2}=(a-2)/\sqrt{2}\).

**Lemma D3 (midpoints).** No unit square contains two midpoints.
Adjacent midpoints are distance \(a/\sqrt{2}>\sqrt{2}\); opposite midpoints are
distance \(a>2\).

**Lemma D4 (vertex and midpoint).** A unit square may contain a vertex and an
*incident* midpoint (distance \(\lambda\in(1,\sqrt{2}]\)). It cannot contain a
vertex and a non-incident midpoint: that distance is \((a\sqrt{5})/2>\sqrt{2}\)
already at \(a=2\) because \(\sqrt{5}>\sqrt{2}\).

**Lemma D5 (midpoint and centre).** Distance \(\lambda\in(1,\sqrt{2}]\), so a
unit square *may* contain \(c\) and one midpoint.

**Lemma D6 (opposite sides).** No unit square meets two opposite sides of \(S\),
because those sides are distance \(a>\sqrt{2}\) apart.

The algebraic identities behind D2–D5 are checked exactly in
[`proof/inequalities.py`](proof/inequalities.py) (`run_all_proofs`).

**Corollary D7.** There are exactly four *vertex squares* \(V_1,V_2,V_3,V_4\),
with \(v_i\in V_i\) and \(V_i\neq V_j\) for \(i\neq j\). There are exactly four
*midpoint squares*, pairwise distinct. The remaining two members of \(\mathcal{F}\)
are the *extras*, written \(E,F\). By D2, \(c\notin V_1\cup V_2\cup V_3\cup V_4\),
so without loss of generality \(c\in E\).

**Corollary D8 (no 7-point diameter packing).** There is no 6-point subset of
\(\{v_i,m_j,c\}\) with all pairwise distances \(>\sqrt{2}\). The five points
\(\{v_1,v_2,v_3,v_4,c\}\) *do* have min-distance \(>\sqrt{2}\), which is DLT’s
\(n=5\) unavoidable set; a sixth important point always lies at distance
\(\le\sqrt{2}\) from one of those five. In particular \(S(6)=2\) cannot be proved
by a 6-point “one point per item” counting argument of the DLT \(n=5\) kind.

---

## 4. Combinatorial types

Each midpoint is hosted by exactly one of \(\{V_1,V_2,V_3,V_4,E,F\}\), and the
host is geometrically allowed by D1–D5:
\[
\begin{align*}
m_1&\in\{V_1,V_2,E,F\},\\
m_2&\in\{V_2,V_3,E,F\},\\
m_3&\in\{V_3,V_4,E,F\},\\
m_4&\in\{V_4,V_1,E,F\}.
\end{align*}
\]
No square hosts two midpoints (D3). Let
\[
k=\#\{i: V_i\text{ hosts a midpoint}\}=\bigl|\{V_1,V_2,V_3,V_4\}\cap\{\text{midpoint squares}\}\bigr|.
\]
The two extras host at most two midpoints, so \(4-k\le 2\), hence \(k\ge 2\).
Trivially \(k\le 4\). Thus \(k\in\{2,3,4\}\).

**Lemma T1.** Types \(k=0\) and \(k=1\) are impossible. In particular the
axis-aligned four-corner placement (each \(V_i\) a homothetic copy of a
\(1\times 1\) corner square) leaves all four midpoints to the two extras, which
cannot host them.

**Lemma T2 (\(k=4\) matching).** If \(k=4\), each \(V_i\) hosts exactly one
incident midpoint, and each midpoint is hosted by a vertex square. Viewing the
sides of \(S\) as the edges of \(C_4\), this is an assignment of each edge to
exactly one of its endpoints with each vertex claiming exactly one edge. The only
such assignments on \(C_4\) are the two cyclic orientations:

- *clockwise:* \(m_i\in V_i\) for all \(i\), equivalently \([v_i,m_i]\subset V_i\);
- *counterclockwise:* \(m_i\in V_{i+1}\) for all \(i\).

There is no mixed matching: a 2+2 split of orientations repeats an edge or leaves
a vertex with claim-degree \(0\) or \(2\). Reflection of the picture swaps the
two orientations, so under the dihedral group \(D_4\) there is a single orbit.
We work with the clockwise representative.

A brute-force enumeration of all injective allowed assignments
([`proof/enumerate_types.py`](proof/enumerate_types.py)) finds **74** assignments,
in **11** orbits under \(D_4\) (rotations and reflections of \(S\), with \(E\)
fixed as the extra that contains \(c\)):

| \(k\) | #assignments | # \(D_4\)-orbits | remaining lemma |
|---:|---:|---:|---|
| 2 | 40 | 6 | RL-A_adj (3 orbits, 24 asns) and RL-A_opp (3 orbits, 16 asns) |
| 3 | 32 | 4 | RL-B1 (E also hosts a midpoint) and RL-B2 (F hosts it) |
| 4 | 2 | 1 | RL-C |
| **total** | **74** | **11** | all **open** as covering problems |

The census is regenerated by `python3 -m proof`. The table of orbit
representatives is [`artifacts/proof/case_table.md`](artifacts/proof/case_table.md).
The enumerator only classifies *which* squares contain *which* important points;
it does not claim any type is geometrically unrealisable. That is the job of
Sections 6–10.

Figures: [`artifacts/proof/important_points.svg`](artifacts/proof/important_points.svg),
[`artifacts/proof/type_k4_chiral.svg`](artifacts/proof/type_k4_chiral.svg).

---

## 5. Closed geometric lemmas (all types)

**Lemma L1 (extras must meet the boundary).** Suppose \(E\cup F\) meets
\(\mathrm{bd}(S)\) in at most finitely many points. Then \(\mathrm{bd}(S)\) is
covered by the four vertex squares. Each vertex square covers a connected L-shape
(DLT rearrangement is not even needed: the intersection of a convex set with
\(\mathrm{bd}(S)\) is a union of arcs, and the vertex forces an L or a one-sided
segment through \(v_i\)). By DLT Lemma 2.1 the total length of an L in a unit
square is at most \(x+l(x)\le 2\).

If the vertex square also hosts a midpoint then one leg has length \(\ge\lambda>1\),
so the maximal total is \(\lambda+l(\lambda)<2\) because \(x+l(x)\) is strictly
decreasing on \([1,\sqrt{2}]\) and \(\lambda>1\). For \(k\ge 2\) at least two
vertex squares are of this kind, and the other two contribute at most \(2\) each.
The covered perimeter is therefore at most
\[
2\bigl(\lambda+l(\lambda)\bigr)+4=a+2l(a/2)+4.
\]
Compare with \(4a\): the inequality \(a+2l(a/2)+4\ge 4a\) rearranges to
\(2l(a/2)+4\ge 3a\). The left side is \(<6\) because \(l(a/2)<1\) for \(a>2\),
and the right side is \(>6\). Contradiction.

(The identity \(l(x)<1\) for \(x\in(1,\sqrt{2}]\) is the algebraic content of
`prove_perimeter_deficit_k4` in [`proof/inequalities.py`](proof/inequalities.py).)

**Lemma L2 (inner star, diameter).** Let
\[
\delta(a)=\frac a2-\sqrt{2-\frac{a^2}4}>0\qquad(a\in(2,2\sqrt{2}]).
\]
On each segment \([c,m_i]\), the open stub of length \(\delta(a)\) adjacent to
\(c\) lies at distance \(>\sqrt{2}\) from every vertex. Hence no vertex square
meets those stubs. (Proof: a point \(p\) on \([c,m_1]\) at distance \(t\) from
\(c\) has \(\|p-v_1\|=\|p-v_2\|=\sqrt{t^2+\lambda^2}\), which is \(>\sqrt{2}\)
precisely when \(t<\delta(a)\); \(v_3,v_4\) are farther.) Therefore the four
stubs are covered by \(E\cup F\).

This is *not* yet a contradiction: a unit square containing \(c\), rotated
\(45^\circ\) and centred, extends \(\sqrt{2}/2\approx 0.707\) along each axis,
and \(\delta(\sqrt{6})\approx 0.518<0.707\). The inner star can be swallowed by
a single diamond at \(c\). Lemma L2 only constrains *where* the extras must act.

**Lemma L3 (height from a chord, area).** If a unit square contains a segment of
length \(\lambda\) and a point at perpendicular distance \(h\) from the line of
that segment, the triangle they span has area \(\lambda h/2\le 1/2\), hence
\(h\le 1/\lambda\). On the standing interval \(\lambda\le\sqrt{6}/2<\sqrt{2}\)
one has \(2/\lambda\ge\lambda\), so two unit squares containing a pair of
opposite sides of a \(\lambda\)-square are **not** forced by this bound to leave
an uncovered middle strip. (Equality \(2/\lambda=\lambda\) occurs at
\(\lambda=\sqrt{2}\), which is outside the area bound for \(S\).)

**Lemma L4 (the \(n=5\) Case-3 leftover does not survive a sixth square).**
DLT Case 3 produces a connected arc of length \(>5a/2-2\sqrt{2}>a\) covered by
one unit square inside a quadrant of side \(\lambda\), contradicting the \(n=2\)
arc bound. With a sixth square \(F\) that arc is shortened by at most the
diameter \(\sqrt{2}\). The inequality \(5a/2-3\sqrt{2}>a\) is equivalent to
\(a>2\sqrt{2}>\sqrt{6}\), so it never holds on the standing interval. *The
tightness of DLT Case 3 is destroyed by one extra square.*

---

## 6. Type \(k=2\): reduction toward Remaining Lemma A

Here both extras host a midpoint, and exactly two vertex squares host midpoints.
Up to \(D_4\) there are two geometric families: the two vertex-hosted midpoints
are adjacent on \(C_4\) (RL-A_adj) or opposite (RL-A_opp).

### 6.1 The DLT Case-2 representative (a subfamily of A_adj)

Fix, as in DLT Theorem 1.3 Case 2,

- \(E\ni c,m_4\), hence \([c,m_4]\subset E\) (the bottom side of \(R_4\));
- \(V_3\ni v_3,m_2\), hence \([m_2,v_3]\subset V_3\);
- the remaining vertex-hosted midpoint is \(m_3\), necessarily in \(V_4\) or in
  \(F\) (it cannot lie in \(E\): \(\|m_4-m_3\|=a/\sqrt{2}>\sqrt{2}\); it cannot
  lie in \(V_3\) by D3).

**Lemma T3 (triangle).** \(V_3\) does not meet \([c,m_3]\).
If it did, convexity would put the right triangle
\(\mathrm{conv}\{v_3,m_2,p\}\) for some \(p\in[c,m_3]\) inside \(V_3\). Taking a
unit-length subsegment of \([m_2,v_3]\) (legal because \(\lambda>1\)) and using
that the horizontal distance from the line \(x=a\) to the line \(x=a/2\) is
\(\lambda>1\), one obtains a triangle of base \(1\) and height \(>1\), area
\(>1/2\), contradicting the parallelogram fact. Equivalently, the full triangle
\(\mathrm{conv}\{v_3,m_2,c\}\) has area \(a^2/8>1/2\).

**Corollary T4.** \(V_1\) and \(V_2\) also miss \([c,m_3]\): the nearest point of
that segment to \(v_1\) or \(v_2\) is \(c\), at distance \(a/\sqrt{2}>\sqrt{2}\).
Thus \([c,m_3]\subset V_4\cup E\cup F\).

**Subcase \(m_3\in V_4\).** Then \([v_4,m_3]\subset V_4\), so the top side of
\(R_4\) is in \(V_4\). The leftover midpoint is \(m_1\in F\).

**Remark (why \(S_{\mathrm{bd}}(2)\) does not finish the subcase).** If one
could show \(\mathrm{bd}(R_4)\subset V_4\cup E\), Theorem 1.2 would give an
immediate contradiction. This is DLT’s \(n=5\) Case 2. For \(n=6\) the square
\(V_1\ni v_1\) can still meet the lower part of the left side of \(R_4\)
(points \((0,y)\) with \(\lambda\le y\le\sqrt{2}\)), so three unit squares may
meet \(\mathrm{bd}(R_4)\) and \(S_{\mathrm{bd}}(2)\) does not apply. We do
**not** claim that \(F\) must meet \(R_4\).

**Lemma T6 (diameter sliver).** If \(F\ni m_1=(a/2,0)\) *and* \(F\) meets
\(R_4=[0,\lambda]\times[\lambda,a]\), then any point of \(F\cap R_4\) satisfies
\(\|p-m_1\|\le\sqrt{2}\), hence
\[
F\cap R_4\ \subseteq\
\bigl[\lambda-\sqrt{2-\lambda^2},\,\lambda\bigr]\times\bigl[\lambda,\,\sqrt{2}\bigr]\cap R_4.
\]
In particular, for \(\lambda>1\):

- \(F\) does not meet the top of \(R_4\) (height \(a=2\lambda>\sqrt{2}\));
- \(F\) does not meet the left of \(R_4\) (the sliver’s left edge is
  \(\lambda-\sqrt{2-\lambda^2}>0\) iff \(\lambda>1\)).

So even if \(F\) enters \(R_4\), it cannot help cover the left side of \(R_4\),
which is part of \(\mathrm{bd}(S)\). Figure:
[`artifacts/proof/case2_quadrant.svg`](artifacts/proof/case2_quadrant.svg).

**Lemma T7 (no diameter gap on the inner side).** The right side of \(R_4\) has
length \(\lambda\). Diameter from \(m_3\) lets \(V_4\) reach at most
\(\sqrt{2-\lambda^2}\) down that side; diameter from \(m_4\) lets \(E\) reach at
most \(\sqrt{2-\lambda^2}\) up that side. One has \(2\sqrt{2-\lambda^2}\ge\lambda\)
on the whole standing interval, because this is equivalent to
\(\lambda\le\sqrt{8/5}\approx 1.265\) and \(\sqrt{6}/2\approx 1.225<\sqrt{8/5}\).
Thus diameter considerations **do not** force a hole on \([c,m_3]\). Combined
with L3, \(V_4\) and \(E\) may overlap in the interior of \(R_4\).

**Lemma T8 (L-gap for \(a>\sqrt{5}\), this subcase closed).**
The set \([v_4,m_3]\) of length \(\lambda>1\) lies in \(V_4\), so any downward
vertical L-leg of \(V_4\) at \(v_4\) has length at most \(l(\lambda)\)
(DLT Lemma 2.1). Likewise \([c,m_4]\subset E\), so any upward vertical L-leg of
\(E\) at \(m_4\) has length at most \(l(\lambda)\). Therefore on the left side
of \(R_4\),
\[
V_4\cap[v_4,m_4]\ \subseteq\ [v_4,\,v_4-l(\lambda)\,e_y],\qquad
E\cap[v_4,m_4]\ \subseteq\ [m_4,\,m_4+l(\lambda)\,e_y].
\]
These two segments fail to cover \([v_4,m_4]\) precisely when
\(2l(\lambda)<\lambda\), i.e. \(\lambda>\sqrt{5}/2\), i.e. \(a>\sqrt{5}\).
(Algebra: \(2l(\lambda)-\lambda=\lambda\bigl(1-2\sqrt{\lambda^2-1}\bigr)\).)

Let \(G\) be the resulting open gap, a subsegment of \(\mathrm{bd}(S)\). No
other member of \(\mathcal{F}\) meets \(G\):

- \(F\) misses the left side of \(R_4\) (T6, even without assuming \(F\) meets
  \(R_4\): the same diameter computation shows that every point of the left
  side of \(R_4\) is at distance \(\ge\lambda\) from \(m_1\), and more strongly
  a point \((0,y)\) with \(y\ge\lambda+l(\lambda)\) has
  \(\|(0,y)-m_1\|=\sqrt{\lambda^2+y^2}>\sqrt{2}\) once \(y>\sqrt{2-\lambda^2}\);
  since \(\lambda+l(\lambda)>\sqrt{2}\) for \(\lambda<\sqrt{2}\), already
  \(y>\sqrt{2}\) so \(\|\,\cdot\,-m_1\|>\sqrt{2}\));
- \(V_1\ni v_1=(0,0)\): a point of \(V_1\) is at distance \(\le\sqrt{2}\) from
  \(v_1\), so \(V_1\) meets the left side of \(S\) at most in
  \(\{0\}\times[0,\sqrt{2}]\). The gap starts at height
  \(\lambda+l(\lambda)\). The sum \(x+l(x)\) is strictly decreasing from \(2\)
  to \(\sqrt{2}\) on \([1,\sqrt{2}]\), hence \(\lambda+l(\lambda)>\sqrt{2}\) on
  the standing interval. Thus \(V_1\) ends strictly below \(G\);
- \(V_2\ni v_2=(a,0)\) and \(V_3\ni v_3=(a,a)\) are at distance \(\ge a>\sqrt{2}\)
  from the left side of \(S\).

Hence \(G\) is uncovered. This subcase cannot occur for \(a>\sqrt{5}\).

**This is the end of what we can prove in this subcase for all \(a>2\).**
For \(a\in(2,\sqrt{5}]\) there is no L-gap on the left side, and three unit
squares (\(V_4\), \(E\), and possibly \(V_1\) or \(F\)) may cover a
\(\lambda\)-square because \(\lambda\le\sqrt{5}/2\approx 1.118<S(3)\). That
range is Remaining Lemma RL-A_adj.

The other A_adj orbits are the same picture up to rotation, or the swap of which
extra hosts which leftover midpoint (`V1,V2,E,F` versus `V1,V2,F,E` in the census).
The swap is geometrically different (the centre-square’s midpoint may sit on a
side adjacent to the two vertex-claimed midpoints, or opposite them after
labelling). We bundle them as RL-A_adj rather than pretend every orbit inherits
T8 without a separate check.

### 6.2 Opposite vertex-midpoints (A_opp)

Census representatives: `V1,E,V3,F`, `V1,E,V4,F`, `V1,F,V4,E`.
Here the two vertex-hosted midpoints are opposite, so the extras host the other
opposite pair, and \(E\) contains \(c\) together with one of those. One obtains
two opposite half-sides of \(S\) covered by vertex squares and a centre-square
that already contains a full inner ray \([c,m_E]\). We did not find a reduction
of this family to a *single* quadrant with a two-item boundary covering (the
DLT triangle+quadrant trick uses an adjacent pair \(m_2\in V_3\), \(m_3\in V_4\)).
This family remains open as RL-A_opp.

---

## 7. Type \(k=3\): Remaining Lemma B

Three vertex squares host midpoints; exactly one extra hosts a midpoint.

- **B1.** That extra is \(E\), so \(E\) contains \(c\) and a midpoint (DLT Case 2
  with a *free* sixth square \(F\) that contains no important point). The
  \(n=5\) \(S_{\mathrm{bd}}(2)\) squeeze does not apply, because \(F\) is
  unconstrained except by D1–D6: it may meet every quadrant.
- **B2.** That extra is \(F\), so \(E\) contains only \(c\) among the important
  points (DLT Case 3 with a sixth square that *does* contain a midpoint).
  Lemma L4 shows that the Case-3 arc-length contradiction does not survive.

Both are open. B1 looks strictly harder than A_adj (one extra is freer). B2 looks
closest to DLT Case 3, but L4 is a proof that the *same* quantitative estimate
cannot work.

---

## 8. Type \(k=4\): Remaining Lemma C

Each vertex square contains exactly one adjacent midpoint; w.l.o.g. clockwise,
\([v_i,m_i]\subset V_i\). The extras contain **no** important point except
\(c\in E\). By L1 they must meet the boundary. By L2 they must cover the inner
star.

The perimeter leftover after four maximal vertex L-shapes of long-leg
\(\lambda\) is
\[
\Delta(a)=4a-4\bigl(\lambda+l(\lambda)\bigr)=2\bigl(a-2l(a/2)\bigr)>0.
\]
The extras, containing no vertex, cannot form an L at a corner of \(S\). Each
meets \(\mathrm{bd}(S)\) in at most two segments on adjacent open sides (D6), of
total length at most \(2\sqrt{2}\). Near \(a=2^+\) one has \(\Delta(a)\) small
and \(2\sqrt{2}\) large, so perimeter arithmetic does not finish the case.

Each quadrant \(R_i\) has two outer sides covered by \(V_{i}\) and \(V_{i-1}\)
and two inner sides that the vertex squares cannot cover near \(c\) (Lemma L2).
Three squares meet each quadrant (\(V_{i-1}\), \(V_i\), and at least one extra),
which is permitted by \(S(3)=\sqrt{\varphi}>\lambda\). This is the \(n=6\)
relaxation of DLT Case 3, and it is open.

---

## 9. Remaining lemmas (what is actually unproved)

We state the gaps as standalone claims. None of them is proved in this repository.

### Remaining Lemma RL-A_adj

Let \(a\in(2,\sqrt{5}]\) and \(\lambda=a/2\). Let \(S=[0,a]^2\) and
\(R=[0,\lambda]\times[\lambda,a]\). Suppose \(V_4,E,F\) are unit squares such that

1. \(v_4,m_3\in V_4\) (hence the top side of \(R\) lies in \(V_4\));
2. \(c,m_4\in E\) (hence the bottom side of \(R\) lies in \(E\));
3. \(m_1\in F\);
4. \(V_3\ni v_3,m_2\), and the remaining two unit squares are the vertex
   squares at \(v_1\) and \(v_2\).

Then \(S\not\subset V_1\cup V_2\cup V_3\cup V_4\cup E\cup F\).

(For \(a>\sqrt{5}\) this representative is already excluded by Lemma T8.)

### Remaining Lemma RL-A_opp

No covering of type \(k=2\) exists in which the two vertex-hosted midpoints are
opposite.

### Remaining Lemma RL-B1

No covering of type \(k=3\) exists in which \(E\) contains \(c\) and a midpoint
(and \(F\) contains no midpoint).

### Remaining Lemma RL-B2

No covering of type \(k=3\) exists in which \(E\) contains \(c\) but no midpoint
(and \(F\) contains one midpoint).

### Remaining Lemma RL-C

No covering of type \(k=4\) exists. Equivalently: there is no covering in which
each vertex square contains the clockwise (or counterclockwise) adjacent midpoint.

### One-sentence bottleneck

The single most plausible “crowning” statement, of which RL-A_adj is the
sharpest special case, is:

> **RL (quadrant form).** A square \(R\) of side \(\lambda\in(1,\sqrt{5}/2]\)
> cannot be covered by three unit squares if two of them contain a pair of
> opposite sides of \(R\) and the third contains a point at distance \(\lambda\)
> from \(R\).

Closing RL-A_adj would finish the DLT Case-2 representative for all \(a>2\)
(T8 already handles \(a>\sqrt{5}\)). It would **not** by itself finish the
other A_adj orbits, A_opp, \(k=3\), or \(k=4\).

---

## 10. Dead ends (arguments that look promising and fail)

These are recorded so they are not rediscovered as “proofs”.

1. **Unavoidable 6-point set of min-distance \(>\sqrt{2}\).** Impossible among
   the important points (D8). Adding non-important points does not help: any
   point far from \(c\) is close to a vertex.
2. **Boundary-only obstruction.** False in spirit and numerically:
   \(S_{\mathrm{bd}}(5)>S(5)\), and six unit squares cover the perimeter of a
   square of side \(2.33\) in
   [`artifacts/boundary_n6/best_boundary.json`](artifacts/boundary_n6/best_boundary.json).
3. **Quadrant + \(S(3)\).** Each quadrant has side \(\lambda\le\sqrt{6}/2<S(3)\),
   so three unit squares *can* cover a quadrant. One would need
   \(a>2\sqrt{\varphi}\approx 2.544>\sqrt{6}\), which is already excluded by area.
4. **DLT Case-3 arc with a sixth square subtracted.** Lemma L4: the leftover
   never exceeds \(2\lambda\) on \(a\le\sqrt{6}\).
5. **Middle strip in the Case-2 quadrant.** Lemmas L3 and T7: both the
   area-height bound and the endpoint-diameter bound fail to force a gap on
   \((1,\sqrt{6}/2]\).
6. **Inner star vs. two extras.** A centred diamond at \(c\) covers all four
   stubs throughout the standing interval (L2).
7. **Perimeter deficit for \(k=4\) with extras allowed on the boundary.** The
   extras can contribute up to \(2\sqrt{2}\) each, which swamps \(\Delta(a)\)
   near \(a=2\).

---

## 11. Computer algebra and the census

Re-run:

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest
python3 -m proof
```

| Artifact | Role |
|---|---|
| [`proof/inequalities.py`](proof/inequalities.py) | Exact rewrites: \(l'(x)<0\), \((x+l(x))'<0\), \(\delta(a)>0\), triangle area, sliver inequalities, “Case-3 leftover never restores”. Each identity is a polynomial comparison or a discriminant, not a floating-point check. |
| [`proof/enumerate_types.py`](proof/enumerate_types.py) | Exhaustive injective assignments of midpoints to allowed hosts; \(D_4\) orbits; tags RL-A/B/C. |
| [`artifacts/proof/case_table.md`](artifacts/proof/case_table.md) | The 11 orbits. |
| [`artifacts/proof/numeric_table.json`](artifacts/proof/numeric_table.json) | Decimal illustrations of \(\delta,\Delta,l(\lambda)\). **Not proof.** |
| [`tests/test_proof_inequalities.py`](tests/test_proof_inequalities.py) | Guards the identities and the census counts. |

If a future argument claims “\(2\sqrt{2-\lambda^2}<\lambda\) on the standing
interval” or “\(k=4\) has a third matching”, those tests will fail.

---

## 12. What a complete proof would still have to do

Assume Lemmas D1–D6, T1–T2, L1–L4, T3–T8. Then \(S\subseteq\bigcup\mathcal{F}\)
with \(a>2\) forces one of the 11 orbits. The DLT Case-2 representative is
already impossible for \(a>\sqrt{5}\). To finish:

1. Prove RL-A_adj (the sliver-quadrant covering). Extend by \(D_4\) and the
   E/F-swap to all 24 A_adj assignments.
2. Prove RL-A_opp, or reduce it to RL-A_adj by a triangle/quadrant argument we
   do not currently have.
3. Prove RL-B1 and RL-B2. B2 is the natural home for a *new* Case-3 estimate
   that uses the midpoint in \(F\); B1 is Case 2 with a free sixth square.
4. Prove RL-C. This is the most populated *geometric* case (the extras are
   interior/boundary helpers with no important-point anchors except \(c\in E\)).

Until every orbit is closed, **do not assert \(S(6)=2\)**.

The strongest statement this repository currently supports is:

> **Partial theorem.** Let \(S\) be a square of side \(a\in(2,\sqrt{6}]\) and
> \(\mathcal{F}\) a covering by six unit squares. Then the covering is of one
> of the 11 \(D_4\)-orbits in [`artifacts/proof/case_table.md`](artifacts/proof/case_table.md),
> and the extras meet \(\mathrm{bd}(S)\). In the DLT Case-2 representative
> (\(E\ni c,m_4\), \(V_3\ni m_2\), \(V_4\ni m_3\), \(F\ni m_1\)) one has
> \(a\le\sqrt{5}\). No covering with \(a>2\) has been ruled out in the other
> orbits, nor in that representative for \(a\in(2,\sqrt{5}]\).

---

## References

1. E. Friedman, D. Paterson, *Covering squares with unit squares*, Geombinatorics 15(3) (2006). [erich-friedman.github.io/papers/covering](https://erich-friedman.github.io/papers/covering/covering.html)
2. J. Januszewski, *A note on covering a square of side length \(2+\varepsilon\) with unit squares*, Amer. Math. Monthly 116 (2009), 174–178.
3. G. Dósa, Zs. Lángi, Zs. Tuza, *Covering a square by congruent squares*, arXiv:2601.16535, 2026. Conjecture 1.1, Theorems 1.2–1.4, Lemma 2.1.
4. H. E. Dudeney, *Puzzles and Curious Problems*, 1931, Problem 219 (\(n=3\)).
5. A. Soifer, *Covering a square of side \(n+\varepsilon\) with unit squares*, J. Combin. Theory Ser. A 113 (2006), 380–383. \(\Pi(n)\); Conjecture 1.1 is \(\Pi(2)=7\).
