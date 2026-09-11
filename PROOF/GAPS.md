# Remaining gaps for \(S(6)=2\)

**None of G1–G5 is closed on the whole interval \((2,\sqrt{6}]\).** Until they
are, \(S(6)=2\) is not proved. Large-\(a\) fragments proved in
[`ATTEMPT.md`](ATTEMPT.md) are recorded here so they are not rediscovered, and
so the residual statements are exact.

Throughout: \(S\) has side \(a\in(2,\sqrt{6}]\), \(\lambda=a/2\), extras \(C\ni c\)
and \(F\), and
\[
k=\bigl|\{m_1,m_2,m_3,m_4\}\cap(C\cup F)\bigr|.
\]

Thresholds (exact, see `proof/inequalities.py`):

| symbol | value | role |
|---|---|---|
| \(\sqrt{5}\) | \(\approx 2.236\) | T8 L-gap \(2\ell(\lambda)<\lambda\) |
| \(8\sqrt{2}/5\) | \(\approx 2.263\) | opposite stub escapes a \(\lambda\)-chord through \(c\) |
| \(2^{5/4}\) | \(\approx 2.378\) | far leftover outruns centre-reach; \(\lambda^4=2\) |
| \(\sqrt{6}\) | \(\approx 2.449\) | area bound |

---

## G1 — \(k=0\), extras meet \(\partial S\)

**Proved.** Extras miss \(\partial S\) is already impossible (perimeter bound P).
For \(a>2^{5/4}\), four far leftovers on \(\partial S\) cannot be covered:
centre-squares cannot reach them, a non-central extra meets at most two sides
(Lemma G1.large).

**Open (residual G1).** There is no covering with \(k=0\) and
\(a\in(2,2^{5/4}]\).

On this range a square through \(c\) *can* cover an entire leftover on each
side it meets. Two extras, each meeting at most two adjacent sides, can cover
all four leftovers by taking complementary pairs (SW vs NE, or SE vs NW).
The two-item quarter kill via \(S_{\mathrm{bd}}(2)=1\) fails: each quarter
boundary meets at least one extra *and* two vertex squares, and \(C\) contains
no midpoint so no inner side of a quarter is fully in \(C\).

Needed: a surplus argument that complementary leftover-coverers cannot also
cover the inner star, or a genuine two-item reduction after ejecting one vertex
square from a quarter.

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

## Success criterion

A finished proof in this folder would be: residual G1, G2 (both subcases), G3,
G4 (T8 remainder + sisters), and G5, each closed on the interval where it is
still listed as open, with every inequality either classical or checked in
`python3 -m proof`. Until then the title of this file remains accurate:
**gaps**.
