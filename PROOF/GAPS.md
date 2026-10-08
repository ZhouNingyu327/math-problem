# Remaining gaps for \(S(6)=2\)

**None of G1–G5 is closed on the whole interval \((2,\sqrt{6}]\).** Until they
are, \(S(6)=2\) is not proved. Fragments in [`ATTEMPT.md`](ATTEMPT.md) include
FarPair, CycleSum, Cascade, OppFar, OpenB-R2TopDiam, OpenB-FHeight, and
CLobeFat. Local Open A/B/C cuts are recorded so they are not rediscovered.

Throughout: \(S\) has side \(a\in(2,\sqrt{6}]\), \(\lambda=a/2\), extras \(C\ni c\)
and \(F\), and
\[
k=\bigl|\{m_1,m_2,m_3,m_4\}\cap(C\cup F)\bigr|.
\]

Thresholds (exact characterising equations; isolating brackets certified in
`proof/certificates.py` and written by `python3 -m proof`):

| symbol | value | role |
|---|---|---|
| \(a_{\mathrm{cr}}\) | \(\approx 2.0036185600\) | local Open B C-on-right; **not** lowered by R2TopDiam/FHeight |
| \(a_\varphi\) | \(\approx 2.00910069\) | Cascade: \(\ell(a-\ell(\lambda))=a-\sqrt{2}\); adjacent meets die above |
| \(a_{\mathrm{top}}\) | \(\approx 2.0361747746\) | local Open B C-on-top; **not** lowered by R2TopDiam/FHeight |
| \(a_\diamond\) | \(\approx 2.09180768\) | in-repo OppFar: centre misses cascade leftover far-end |
| \(a_M\) | \(\approx 2.11195454\) | long+short vertex-meet limit \(\sqrt{2}+\ell(\lambda)=a\) |
| \(\sqrt{5}\) | \(\approx 2.236\) | T8 L-gap \(2\ell(\lambda)<\lambda\) |
| \(8\sqrt{2}/5\) | \(\approx 2.263\) | opposite stub escapes a \(\lambda\)-chord through \(c\) |
| \(2^{5/4}\) | \(\approx 2.378\) | far leftover outruns centre-reach; \(\lambda^4=2\) (G2/G5) |
| \(\sqrt{6}\) | \(\approx 2.449\) | area bound |

Retracted: \(a_{\mathrm{top}}^F\approx 2.0265\) (\(\delta\ge 2g_0\) is invalid under
R1Exclusive). Local \(a_\psi\) (Open C razor) is not given a decimal here.

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
- **OpenB-R2TopDiam.** \(\lvert p^\ast-r^\ast\rvert^2=2\mu^4>2\) on \(R_2\)
  (`prove_openb_r2_top_diam`). **OpenB-FHeight** (local analytic):
  \(F\cap R_2\subseteq(\mu,Y_b]\) with \(Y_b<\mu+g_0\). These do **not** lower
  \(a_{\mathrm{top}}\) or \(a_{\mathrm{cr}}\).
- **CLobeFat.** Remaining room past \(c\) still reaches the height-bound hole
  on \(a<a_\ast\approx 2.288\), so deep-\(\delta\) \(C\)-moduli stay fat
  (`prove_clobe_fat_remaining_room`). Explains the MES/B&B stall; not a kill.
- G1.large centre-reach remains available for G2/G5 at \(a>2^{5/4}\).

In-repo combinatorial G1 is closed on \((a_\diamond,\sqrt{6}]\). Local Open B
already cuts C-on-top at \(a_{\mathrm{top}}\) and C-on-right at \(a_{\mathrm{cr}}\).

**Open (sharpest remaining).** \(S(6)=2\) is not proved. Residual G1:

1. **Meet deep-\(\delta\)** on \((2,a_\varphi]\). Point-MES stalled (~0.072%
   under \(\delta_{\mathrm{force}}\)). Pose-space B&B ~95% product kill, joint
   \(+0.03\%\); survivors are fat non-rigid \(C\)-moduli lobes. \(V_3\)-couple /
   \(U(\theta,s)\) sampling certificates failed to empty cells. CLobeFat shows
   why a one-pose lemma is not available.
2. **Open B C-on-top** on \((2,a_{\mathrm{top}}]\). R2TopDiam + FHeight do not
   shrink this interval.
3. **Open B C-on-right** on \((2,a_{\mathrm{cr}}]\). Same.
4. **Open C razor** on \((2,a_\psi]\).

Needed for a hand proof of (1): a hinge / linking lemma that cuts the fat
\(C\)-moduli by a second contact (leftover tip plus an inward meet-hypotenuse)
so the pose set becomes rigid, *or* a pair of interior witnesses that no
single lobe pose and \(F\) can split. CLobeFat rules out θ-independent
one-point MES.

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

## CAP — interval certificates (stalled on fat \(C\)-moduli)

Hand lemmas do **not** close meet deep-\(\delta\) or Open B below
\(a_{\mathrm{top}}\) / \(a_{\mathrm{cr}}\). Local computer-assisted attempts:

| Attempt | Outcome |
|---|---|
| Point-MES, deep small-\(\delta\) | STALLED (~0.072% under \(\delta_{\mathrm{force}}\)) |
| Pose-space B&B | ~95% product kill; joint \(+0.03\%\) |
| Survivors | fat non-rigid \(C\)-moduli lobes — no clean one-pose lemma |
| \(V_3\) couple / \(U(\theta,s)\) sampling | failed to empty cells |

CLobeFat is the structural reason: remaining room past \(c\) still covers the
height-bound hole, so \(\{C\ni c\}\cap\{\text{leftover tip}\}\) is a fat body.
A future certificate must use **two** interior witnesses per box, or a joint
\((C,F)\) predicate, not a single MES point. Schema remains in
`proof/certificates.py`; `meet_band_certificates.json` is still absent.

**CI.** `certify_published_brackets` pins \(a_\varphi,a_\diamond,a_M\). Local
decimals \(a_{\mathrm{top}},a_{\mathrm{cr}}\) are constants, not isolating
brackets. Do not check in a fake \(a_{\mathrm{top}}^F\).

Until a covering-certificate file exists and verifies, meet deep-\(\delta\)
and Open B below the local cuts remain **open**.

---

## Success criterion

A finished proof in this folder would close: meet deep-\(\delta\) on
\((2,a_\varphi]\), Open B C-on-top on \((2,a_{\mathrm{top}}]\), C-on-right on
\((2,a_{\mathrm{cr}}]\), Open C razor on \((2,a_\psi]\), plus residual G2, G3,
G4, and G5, with every inequality classical, checked in `python3 -m proof`, or
a verified interval certificate. Until then: **gaps**. \(S(6)=2\) is **not**
proved.
