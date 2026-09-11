# Remaining gaps for \(S(6)=2\)

**None of G1–G5 is closed on the whole interval \((2,\sqrt{6}]\).** Until they
are, \(S(6)=2\) is not proved. Large-\(a\) fragments and the new G1 lemmas
(FarPair, CycleSum, Cascade, OppFar) proved in [`ATTEMPT.md`](ATTEMPT.md) are
recorded here so they are not rediscovered, and so the residual statements are
exact.

Throughout: \(S\) has side \(a\in(2,\sqrt{6}]\), \(\lambda=a/2\), extras \(C\ni c\)
and \(F\), and
\[
k=\bigl|\{m_1,m_2,m_3,m_4\}\cap(C\cup F)\bigr|.
\]

Thresholds (exact characterising equations; isolating brackets certified in
`proof/certificates.py` and written by `python3 -m proof`):

| symbol | value | role |
|---|---|---|
| \(a_\varphi\) | \(\approx 2.00910069\) | Cascade: \(\ell(a-\ell(\lambda))=a-\sqrt{2}\); adjacent meets die above |
| \(a_\diamond\) | \(\approx 2.09180768\) | OppFar: centre misses cascade leftover far-end |
| \(a_M\) | \(\approx 2.11195454\) | long+short vertex-meet limit \(\sqrt{2}+\ell(\lambda)=a\) |
| \(\sqrt{5}\) | \(\approx 2.236\) | T8 L-gap \(2\ell(\lambda)<\lambda\) |
| \(8\sqrt{2}/5\) | \(\approx 2.263\) | opposite stub escapes a \(\lambda\)-chord through \(c\) |
| \(2^{5/4}\) | \(\approx 2.378\) | far leftover outruns centre-reach; \(\lambda^4=2\) (G2/G5) |
| \(\sqrt{6}\) | \(\approx 2.449\) | area bound |

Local unpublished cuts (not proved in this repository): \(a_{\mathrm{top}}\approx 2.036\),
\(a_{\mathrm{cr}}\approx 2.0036\), \(a_B\approx 2.002\), and an Open C razor
\(a_\psi\). They are recorded only as targets; nothing below treats them as theorems.

---

## G1 — \(k=0\), extras meet \(\partial S\)

**Proved.**

- Extras miss \(\partial S\) is already impossible (perimeter bound P).
- **FarPair / NoMeet / OneMeet.** Adjacent leftover far-ends are at distance
  \(\lambda^2\sqrt{2}>\sqrt{2}\). 0-meet (four leftovers) and 1-meet (three)
  die for all \(a>2\). This includes the **bridge** (extra covering a leftover
  gap between two vertex L-legs on a non-meet side).
- **CycleSum.** Clockwise 4-meet dies for all \(a>2\)
  (\(\sum(x_i+\ell(x_i))\ge 4a>8\ge 4\max(x+\ell(x))\)).
- **Cascade.** Unique \(a_\varphi\); adjacent meets and 3-meet die for \(a>a_\varphi\).
- **OppFar.** Opposite-meet leftovers die for \(a>a_\diamond\) (centre cannot
  contain either cascade far-end; \(F\) takes at most one).
- G1.large centre-reach remains available for G2/G5 at \(a>2^{5/4}\).

G1 is therefore closed on \((a_\diamond,\sqrt{6}]\).

**Open (residual G1).** There is no covering with \(k=0\) and
\(a\in(2,a_\diamond]\) of one of the following types:

1. **2-opposite meets** (C-on-top / C-on-right) on the whole \((2,a_\diamond]\).
   Local work claims cuts at \(a_{\mathrm{top}}\approx 2.036\) and
   \(a_{\mathrm{cr}}\approx 2.0036\); this repository only reaches \(a_\diamond\).
2. **2-adjacent meets** on the meet band \((2,a_\varphi]\).
3. **3-meet** (one leftover side) on \((2,a_\varphi]\).

The meet band is blocked under MES of a forced \(C\)-set and under perimeter
reach bookkeeping: after several meets there is little or no leftover on
\(\partial S\), and the uncovered set is an interior hinge neighbourhood of
\(c\). CycleSum kills the 4-meet extreme of that picture. What remains is
2-meet/3-meet, for which a computer-assisted interior-witness plan is §CAP.

Needed for a hand proof: a hinge / linking lemma that a unit square through
\(c\) covering one leftover tip cannot cover the interior pocket created by
two meeting L-legs at an adjacent vertex (or the 3-meet unique leftover plus
the diagonal gap of length \((a-2)\sqrt{2}\)).

---

## G2 — \(k=1\), three items on the critical quarter; eject \(F\)

**Proved.** If \(C\) hosts the unique extra-midpoint **and** the T8-adjacent
vertex hosts the next midpoint (\(m_3\in V_4\) when \(C\ni m_4\)), Lemma
G2.large closes that orbit for \(a>2^{5/4}\).

**Open (residual G2).**

1. That T8-adjacent \(C\)-midpoint orbit on \(a\in(2,2^{5/4}]\).
2. The \(C\)-midpoint orbit in which the weak vertex is adjacent to \(C\)'s
   midpoint (consecutive triple of vertex claims). The L-gap side then meets
   the weak vertex square, which can reach the gap without hosting a midpoint.
3. The subcase in which **\(F\)** hosts the extra-midpoint and \(C\) contains
   only \(c\) among important points. There is no full inner side in \(C\), so
   T8 does not start. Direct analogue of DLT Case 3 plus a midpoint-anchored
   sixth square; DLT’s arc leftover never restores after subtracting
   \(\sqrt{2}\) (Lemma L4). Need a new eject-\(F\) lemma.

---

## G3 — \(k=2\), extra-midpoints opposite

**Proved.** Nothing beyond the standing lemmas D1–D6, P, Match.

**Open (residual G3).** There is no covering in which \(C\) contains \(c\) and
one midpoint, \(F\) contains the opposite midpoint, and \(a\in(2,\sqrt{6}]\).

The DLT adjacent pair \((m_2\in V_3,\,m_3\in V_4)\) is absent, so T3+T8 do not
apply. Two opposite inner rays are fully extra-covered. A two-item quarter would
require ejecting both one vertex square and one extra from the same quarter
boundary — not established.

---

## G4 — \(k=2\), extra-midpoints adjacent

**Proved.** In the DLT Case-2 labeling \(C\ni c,m_4\), \(V_3\ni m_2\),
\(V_4\ni m_3\), \(F\ni m_1\), Lemma T8 closes the type for \(a>\sqrt{5}\).
The diameter sliver \(F\cap R\subset\) a neighbourhood of \(c\) is proved for
all \(a>2\).

**Open (residual G4).**

1. That same labeling on \(a\in(2,\sqrt{5}]\). The L-gap is absent
   (\(2\ell(\lambda)\ge\lambda\)). \(S_{\mathrm{bd}}(2)\) fails because \(V_1\)
   can meet the lower left of \(R\). Need: \(V_4\cup C\cup F\) cannot cover \(R\)
   (or \(\mathrm{bd}(R)\)) under the sliver constraint on \(F\).
2. The other adjacent orbits in the census (E/F swap; the vertex pair that is
   adjacent but not the T8 pair). Each needs a reduction to T8 or a parallel
   L-gap.

---

## G5 — \(c\in C\cap F\)

**Proved.** Both extras then lie in the closed disk of radius \(\sqrt{2}\) about
\(c\), so their traces on \(\partial S\) are midpoint-windows. For
\(a>2^{5/4}\) those windows miss the far leftovers of G1.large, and they miss
the top of a T8 gap; G5 does not resurrect types already killed at large \(a\).

**Open (residual G5).** On \(a\in(2,2^{5/4}]\), two complementary centre-squares
can meet all four sides near the midpoints. There is no WLOG reduction to
\(F\not\ni c\): both extras may contain \(c\) and (when \(k=2\)) one midpoint
each. Needed: show that a second square through \(c\) is redundant for
\(\partial S\) (so the type collapses to five items, contradicting \(S(5)=2\)),
or that it cannot cover the inner star complementary to \(C\).

A false shortcut: “pick the extra that contains more midpoints as \(C\)” does
not eliminate \(F\ni c\) when \(k=2\).

---

## Why the sixth square blocks DLT’s \(S(5)=2\) reductions

DLT Theorem 1.3 has three cases for five items. Each breaks for six items in
exactly one place:

| DLT \(n=5\) | Why it dies for \(n=6\) |
|---|---|
| Case 1: central item misses \(\partial S\), four L-shapes of length \(\le 2\) | Still true that extras cannot *all* miss \(\partial S\) (P). The remaining \(k=0\) extras-*meeting*-boundary case is G1. |
| Case 2: two items cover a quarter boundary, \(S_{\mathrm{bd}}(2)=1\) | The sixth square meets the quarter (sliver about \(c\), or \(V_1\) on the lower outer side). G2/G4 are the eject-\(F\) problems. |
| Case 3: one vertex item covers a quarter-arc of length \(>5a/2-2\sqrt{2}>a\) | Subtracting a diameter \(\sqrt{2}\) for \(F\) never restores \(>2\lambda\) on \(a\le\sqrt{6}\) (L4). |

Perimeter-only is independently impossible: \(S_{\mathrm{bd}}(6)>2\).

---

## CAP — interval certificates for residual G1 (meet band and 2-opp)

Hand lemmas above do **not** close 2-meet/3-meet on \((2,a_\diamond]\). The
following is a computer-assisted plan whose output would be checked in CI
(`python3 -m proof` already certifies the threshold brackets and will load
`artifacts/proof/meet_band_certificates.json` if present).

**Configuration space.** For each residual type (`G1-2opp`, `G1-2adj`,
`G1-3meet`), a covering is a tuple of six unit squares. Parametrize each by
centre \((x,y)\) and edge-angle \(\theta\), so a pose is a point of
\([0,a]^2\times\mathbb{R}/(\pi/2)\) (square symmetry). With \(a\in(2,a_\diamond]\)
this is a compact 19-dimensional set (18 pose coordinates plus \(a\)). Type
constraints (which sides are vertex-meets, \(k=0\) matching, \(c\in C\)) cut
out a closed subset \(K_{\mathrm{type}}\).

**Predicate.** A box \(B\subset K_{\mathrm{type}}\) is *impossible* if there
exists a witness point \(p\in S\) such that the interval evaluation of every
square in \(B\) misses \(p\) (the Minkowski sum of a unit square with the pose
uncertainty does not contain \(p\)). Alternative cheap predicates, already
exact on a box: FarPair (two leftover tips in one square), triangle area
\(>1/2\), diameter \(>\sqrt{2}\).

**Search.** Branch-and-bound: subdivide \(K_{\mathrm{type}}\) until every leaf
is impossible or smaller than a declared \(\varepsilon\) (then fail, do not
claim a proof). Prefer interior witnesses — the hinge vertex of two meeting
L-legs, or a point on the diagonal gap of length \((a-2)\sqrt{2}\) — rather
than MES of a leftover on \(\partial S\).

**Certificate format.** JSON list of rows, schema in
`proof/certificates.py` / `artifacts/proof/cap_schema.json`:

```json
{
  "type": "G1-2opp",
  "a": [2.01, 2.02],
  "box": [[lo, hi], "... 18 pairs"],
  "witness": [x, y],
  "reason": "point-miss"
}
```

**CI.** `certify_published_brackets` already uses mpmath interval arithmetic
to pin \(a_\varphi,a_\diamond,a_M\). A covering-certificate file is optional;
when present, `load_and_check_optional_certificates` checks types and
\(a\)-intervals. A future verifier should interval-evaluate each witness
against each pose box (no floating-point search at check time).

**What this is not.** It is not a replacement for G2–G5. It is only proposed
for residual G1. Until a covering-certificate file exists and verifies, the
meet band and 2-opp on \((2,a_\diamond]\) remain **open**.

---

## Success criterion

A finished proof in this folder would be: residual G1 (2-meet/3-meet on
\((2,a_\diamond]\)), G2 (both subcases), G3, G4 (T8 remainder + sisters), and G5,
each closed on the interval where it is still listed as open, with every
inequality either classical, checked in `python3 -m proof`, or supplied as a
verified interval certificate. Until then the title of this file remains
accurate: **gaps**.
