# Proof attempt for \(S(6)=2\)

**Status: incomplete.** This is not a proof of Dósa–Lángi–Tuza Conjecture 1.1.
Precise remaining statements live in [`GAPS.md`](GAPS.md). Numerics are never
a proof step.

Notation in this folder matches the case tree below, **not** the older index
in which \(k\) counted vertex-hosted midpoints.

---

## 0. Standing hypotheses

Let \(S=[0,a]^2\) with \(a\in(2,\sqrt{6}]\), \(\lambda=a/2\in(1,\sqrt{6}/2]\).
A family \(\{V_1,V_2,V_3,V_4,C,F\}\) of unit squares covers \(S\), where
\(v_i\in V_i\) are the four vertices (counterclockwise from the origin) and
\(c\in C\) is the centre. Write \(m_i\) for the midpoint of \([v_i,v_{i+1}]\).
The extras are \(C\) and \(F\).

**Midpoint type**
\[
k=\bigl|\{m_1,m_2,m_3,m_4\}\cap(C\cup F)\bigr|\in\{0,1,2\}.
\]
(Capacity: four midpoints, no unit square contains two of them, extras host at
most two, so \(k\ge 0\) and \(4-k\le 4\) with \(k\le 2\). The values \(k=3,4\)
are impossible.)

**Obstruction.** \(S_{\mathrm{bd}}(6)>2\) (a verified perimeter covering exists
at side \(2.33\); a DLT-style \(n\mapsto n+4\) extrapolation would even suggest
\(S_{\mathrm{bd}}(6)\ge 1+\sqrt{2}\)). Perimeter-only arguments cannot finish
the conjecture. The sixth square also blocks DLT’s two-item quarter reductions
that prove \(S(5)=2\). Interior constraints are required.

---

## 1. Done (used as axioms below)

These are proved in the appendices / [`../proof/inequalities.py`](../proof/inequalities.py)
and in Dósa–Lángi–Tuza arXiv:2601.16535.

| Tag | Statement |
|---|---|
| D1–D6 | Diameter \(\sqrt{2}\): no two vertices; no vertex+centre; no two midpoints; no opposite sides of \(S\); a vertex meets at most one incident midpoint. |
| \(\ell(x)\) | DLT Lemma 2.1: max short L-leg \(\ell(x)=x-x\sqrt{x^2-1}\) on \([1,\sqrt{2}]\), strictly decreasing, as is \(x+\ell(x)\le 2\). |
| P | If \(C\cup F\) misses \(\partial S\), four vertex L-shapes of long-leg \(\ge\lambda\) cover at most \(4(\lambda+\ell(\lambda))<4a\). Contradiction. So extras **must** meet \(\partial S\). |
| Q2 | \(S_{\mathrm{bd}}(2)=1\): two unit squares cannot cover the boundary of a square of side \(>1\). |
| T3 | Triangle / parallelogram fact: a unit square containing \([m_2,v_3]\) cannot meet \([c,m_3]\). |
| Match | For \(k=0\), the vertex–midpoint matching on \(C_4\) is only clockwise or counterclockwise (one \(D_4\)-orbit). |

Case tree:

```
covering by 6 unit squares, a > 2
├── extras miss ∂S                         DONE (P)
├── k = 0, extras meet ∂S                  G1
│     ├── 0-meet (four leftovers)          DONE all a>2   Lemma FarPair
│     ├── 1-meet (three leftovers)         DONE all a>2   FarPair
│     ├── 4-meet (no leftovers)            DONE all a>2   Lemma CycleSum
│     ├── 2-adj / 3-meet                   DONE a>a_φ     Lemma Cascade
│     ├── 2-opp leftovers                  DONE a>a_♦     Lemma OppFar
│     └── residual                         meet deep-δ (2,a_φ]; Open B (2,a_top], (2,a_cr]; razor (2,a_ψ]
├── k = 1                                  G2  (eject F from the critical quarter)
│     └── C hosts the extra midpoint
│           closed for a > 2^{5/4}         Lemma G2.large
│           open on (2, 2^{5/4}]
│     └── F hosts the extra midpoint       open
├── k = 2, extra-midpoints opposite        G3  open
├── k = 2, extra-midpoints adjacent        G4
│     └── DLT Case-2 representative
│           closed for a > √5              Lemma T8
│           open on (2, √5]
│     └── sister orbits                    open
└── c ∈ C ∩ F                              G5  (flag on every k)
      reduced for a > 2^{5/4}              Lemma G5.large
      open on (2, 2^{5/4}]
```

A complete proof is: G1 + G2 + G3 + G4 + G5, each on the whole interval \((2,\sqrt{6}]\).
Combinatorial G1 is closed on \((a_\diamond,\sqrt{6}]\); local Open B already
cuts 2-opp leftovers at \(a_{\mathrm{top}}\) / \(a_{\mathrm{cr}}\). Sharpest
remaining: meet deep-\(\delta\) \((2,a_\varphi]\), C-on-top \((2,a_{\mathrm{top}}]\),
C-on-right \((2,a_{\mathrm{cr}}]\), razor \((2,a_\psi]\). \(S(6)=2\) is **not**
proved.

---

## 2. Lemma G1.large (\(k=0\), \(a>2^{5/4}\))

Assume \(k=0\): every midpoint lies in a vertex square. W.l.o.g. clockwise:
\([v_i,m_i]\subset V_i\). Then on side \(E_i=[v_i,v_{i+1}]\),

- \(V_i\) covers at least \([v_i,m_i]\) (length \(\lambda\));
- \(V_{i+1}\) has long-leg \(\ge\lambda\) on the next side, hence covers at most
  \(\ell(\lambda)\) of \(E_i\) from \(v_{i+1}\).

The leftover on \(E_i\) is a segment of length at least
\(\lambda-\ell(\lambda)=\lambda\sqrt{\lambda^2-1}\), lying strictly past \(m_i\)
toward \(v_{i+1}\). (If \(V_i\) extends past \(m_i\), the leftover starts even
farther from \(c\).)

**Centre reach.** \(C\ni c\) has distance \(\lambda\) to \(E_i\). Any point of
\(C\cap E_i\) lies within \(\sqrt{2-\lambda^2}\) of \(m_i\) (diameter from \(c\),
foot of the perpendicular). The same holds for \(F\) if \(c\in F\).

**Algebra.** \(\lambda\sqrt{\lambda^2-1}>\sqrt{2-\lambda^2}\) iff \(\lambda^4>2\)
iff \(\lambda>2^{1/4}\) iff \(a>2^{5/4}\). Checked in
`prove_centre_cannot_cover_far_leftover`.

Thus for \(a>2^{5/4}\), neither extra that contains \(c\) can cover the far end
of any leftover. An extra that does *not* contain \(c\) still cannot contain a
vertex or a midpoint (\(k=0\)), so it meets at most two adjacent sides, hence
covers at most two leftovers.

Four leftovers, at most two covered by a non-central \(F\), none covered at the
far end by a central extra: at least two leftovers remain. Contradiction.

This closes G1 on \((2^{5/4},\sqrt{6}]\) by centre-reach. Lemma FarPair below
closes the *no-meet* subcase on the whole interval \((2,\sqrt{6}]\), so G1.large
is now a G2/G5 tool rather than the bottleneck for G1.

---

## 2A. Refined G1: FarPair, Cascade, Open B, CLobeFat

Clockwise matching. On side \(E_i\), write \(x_i\) for the long-leg of \(V_i\)
(\(\ge\lambda\), since \(m_i\in V_i\)) and \(\ell(x_{i+1})\) for the maximal short-leg
of \(V_{i+1}\) on \(E_i\). A **meet** on \(E_i\) means \(V_i\cup V_{i+1}\) covers
\(E_i\), equivalently \(x_i+\ell(x_{i+1})\ge a\). Otherwise \(E_i\) has a leftover
segment whose far end (from \(m_i\)) is the inner tip of \(V_{i+1}\)'s short leg.

Thresholds (unique roots, isolating brackets in
`artifacts/proof/threshold_brackets.json`):

| symbol | equation | value |
|---|---|---|
| \(a_\varphi\) | \(\ell\bigl(a-\ell(\lambda)\bigr)=a-\sqrt{2}\) | \(\approx 2.00910069\) |
| \(a_{\mathrm{cr}}\) | local Open B C-on-right cut (not lowered by R2TopDiam/FHeight) | \(\approx 2.0036185600\) |
| \(a_{\mathrm{top}}\) | local Open B C-on-top cut (not lowered by R2TopDiam/FHeight) | \(\approx 2.0361747746\) |
| \(a_\diamond\) | \(\lvert c-P\rvert=\sqrt{2}\) for cascade far-end \(P=(\ell(\alpha),a)\), \(\alpha=a-\ell(\lambda)\) | \(\approx 2.09180768\) |
| \(a_M\) | \(\sqrt{2}+\ell(\lambda)=a\) (long+short vertex-meet limit) | \(\approx 2.11195454\) |

**Lemma FarPair.** Adjacent leftover far-ends
\(p_1=(2\lambda-\ell(\lambda),0)\), \(p_2=(2\lambda,\,2\lambda-\ell(\lambda))\)
satisfy \(\lvert p_1 p_2\rvert=\lambda^2\sqrt{2}>\sqrt{2}\) for \(a>2\). Opposite
far-ends are at distance \(2\lambda^2>2\). No unit square contains two leftover
far-ends. (Identity: `prove_far_pair_distance`. The triangle \(\triangle(c,p_1,p_2)\)
has area \(\lambda^4/2>1/2\), `prove_far_centre_triangle`; that is redundant with
the diameter statement.)

This is **not** a MES of a forced \(C\)-set and **not** perimeter-reach
bookkeeping: it is a pairwise diameter on the leftover tips.

**Lemma NoMeet / OneMeet.** If there are four leftovers (0-meet) or three
(1-meet), at least three (resp. two) leftover far-ends must be covered by
\(\{C,F\}\). FarPair says each extra contains at most one. Contradiction for
all \(a>2\). Non-incident vertex squares cannot reach a leftover tip (distance
\(\ge a>\sqrt{2}\)).

In particular the **bridge** pattern — an extra covering a leftover gap between
two vertex L-legs on a side that is not a meet — is exactly 0-meet or 1-meet
leftover covering, and is dead for all \(a>2\).

**Lemma CycleSum (4-meet).** If every side is a vertex-meet, then
\(x_i+\ell(x_{i+1})\ge a\) for \(i=1,2,3,4\). Summing gives
\(\sum(x_i+\ell(x_i))\ge 4a>8\). But \(x+\ell(x)\le 2\) on \([1,\sqrt{2}]\),
equality only at \(x=1\). Contradiction for \(a>2\). (`prove_cycle_sum_four_meet`.)
This is an interior/L-cycle identity, not a reach argument: there is no leftover
on \(\partial S\) to take a MES of.

**Lemma Cascade.** Let \(\alpha(a)=a-\ell(\lambda)\) and
\(f(a)=\ell(\alpha(a))-(a-\sqrt{2})\). Then \(f\) is strictly decreasing on
\([2,a_M]\) with \(f(2)=\sqrt{2}-1>0\) and \(f(a_M)<0\), hence a unique root
\(a_\varphi\). For \(a>a_\varphi\), a meet on one side forces a
vertex-uncoverable leftover on the previous side (the common vertex square
cannot supply both the stretched long-leg \(\ge\alpha\) and the short-leg
\(\ge a-\sqrt{2}\)). Adjacent meets are therefore impossible, and 3-meet
(which contains an adjacent pair) dies with them. (`prove_cascade_threshold_unique`.)

**Lemma OppFar.** After opposite meets, the two leftover sides carry cascade
gaps for \(a>a_\varphi\). The far end \(P=(\ell(\alpha),a)\) (LR-meet / C-on-top
labelling; BT-meet / C-on-right is the D4 image) satisfies
\(\lvert cP\rvert<\sqrt{2}\) at \(a=a_\varphi\) and \(\lvert cP\rvert>\sqrt{2}\)
at \(a=a_M\), with unique crossing \(a_\diamond\). For \(a>a_\diamond\), \(C\)
contains neither leftover far-end (both are cascade-far from \(c\)). \(F\)
contains at most one (FarPair / opposite sides). At least one leftover tip is
uncovered. (`prove_cascade_far_end_centre_reach`.) Local Open B work already
cuts C-on-top at \(a_{\mathrm{top}}<a_\diamond\) and C-on-right at
\(a_{\mathrm{cr}}\); OppFar is the in-repo fallback, not the sharp cut.

**Lemma OpenB-R2TopDiam.** In the Open B C-on-top rectangle \(R_2\), the forced
tips \(p^\ast,r^\ast\) satisfy \(\lvert p^\ast-r^\ast\rvert^2=2\mu^4>2\) for
\(\mu=\lambda>1\). Same polynomial as FarPair (`prove_openb_r2_top_diam`).
**Lemma OpenB-FHeight (local analytic).** \(F\cap R_2\subseteq(\mu,Y_b]\) with
\(Y_b<\mu+g_0\). Together these constrain \(F\) in \(R_2\) but **do not** lower
\(a_{\mathrm{top}}\approx 2.0361747746\) or \(a_{\mathrm{cr}}\approx 2.0036185600\).

A claimed cut \(a_{\mathrm{top}}^F\approx 2.0265\) using \(\delta\ge 2g_0\) is
**retracted**: that hypothesis is invalid under R1Exclusive.

**Lemma CLobeFat.** On \((2,a_\varphi]\) (and through \(a_{\mathrm{top}}\)),
every unit square containing \(c\) and a leftover tip still reaches past the
height-bound inner edge of an opposite vertex square:
\(\sqrt{2}-\lambda\ge\lambda-1/\lambda\) iff \(a\le a_\ast=(\sqrt{2}+\sqrt{10})/2\approx 2.288\).
(`prove_clobe_fat_remaining_room`.) So the \(C\)-moduli covering a deep-\(\delta\)
leftover is a fat positive-dimensional body, not a rigid pose. This is why
point-MES on meet deep-\(\delta\) stalled (~0.072% under \(\delta_{\mathrm{force}}\))
and why pose-space B&B survivors are fat non-rigid lobes (~95% product kill,
joint \(+0.03\%\); \(V_3\)-couple / \(U(\theta,s)\) sampling failed to empty
cells). CLobeFat **explains** the stall; it does **not** kill the lobes.

**G1 / Open A–C summary.** In-repo combinatorial G1 is closed on
\((a_\diamond,\sqrt{6}]\). Matching **local** status (authoritative for what
remains):

| Local name | Closed on | Residual |
|---|---|---|
| Open A Cascade | \(a>a_\varphi\) | **meet deep-\(\delta\)** on \((2,a_\varphi]\) |
| Open B C-on-top | \(a>a_{\mathrm{top}}\) | \((2,a_{\mathrm{top}}]\) |
| Open B C-on-right | \(a>a_{\mathrm{cr}}\) | \((2,a_{\mathrm{cr}}]\) |
| Open C | \(a>a_\psi\) (local) | **razor** \((2,a_\psi]\) |
| Bridge | all \(a>2\) (FarPair) | — |

Sharpest remaining: meet deep-\(\delta\) \((2,a_\varphi]\); Open B C-on-top
\((2,a_{\mathrm{top}}]\); C-on-right \((2,a_{\mathrm{cr}}]\); razor
\((2,a_\psi]\). \(S(6)=2\) is **not** proved.

See [`LOCAL_SYNC.md`](LOCAL_SYNC.md) for the local/repo ledger.

---

## 3. Lemma G2.large (\(k=1\), \(C\) hosts the extra midpoint, \(a>2^{5/4}\))

Assume \(C\ni c,m_4\), so \([c,m_4]\subset C\), and \(F\) hosts no midpoint.
Three vertex squares host the other midpoints. This lemma assumes in addition
the T8-adjacent labeling \(m_3\in V_4\) (so \([v_4,m_3]\subset V_4\)). The
orbit in which the weak vertex is the one adjacent to \(C\)'s midpoint is
**not** included; see GAPS §G2. Let
\(R=\mathrm{conv}\{v_4,m_3,c,m_4\}=[0,\lambda]\times[\lambda,a]\).

**L-gap (Lemma T8).** On the left side \([v_4,m_4]\) of \(R\) (which is in
\(\partial S\)): \(V_4\) has long-leg \(\ge\lambda\) on the top, hence a downward
L-leg at most \(\ell(\lambda)\); \(C\) has long-leg \(\lambda\) along the bottom
of \(R\), hence an upward L-leg at most \(\ell(\lambda)\). These fail to meet
iff \(2\ell(\lambda)<\lambda\) iff \(a>\sqrt{5}\). The resulting open gap \(G\)
is missed by \(V_1\) because \(\lambda+\ell(\lambda)>\sqrt{2}\) (the highest
\(V_1\) can climb the left side). Missed by \(V_2,V_3\) by diameter.

**Opposite stub.** \(C\) contains a chord of length \(\lambda\) ending at \(c\),
so it extends at most \(\sqrt{2}-\lambda\) past \(c\) along the same line (toward
\(m_2\)). The inner-star stub on that ray has length
\(\delta=\lambda-\sqrt{2-\lambda^2}\). Then \(\delta>\sqrt{2}-\lambda\) iff
\(\lambda>4\sqrt{2}/5\) iff \(a>8\sqrt{2}/5\approx 2.263\). Vertex squares miss
the stub (distance from any vertex to \(c\) is \(>\sqrt{2}\)). Hence \(F\) must
cover the opposite stub.

**F cannot fill the top of \(G\).** A point of the opposite stub is near \(c\).
Any unit square containing such a point meets the left side of \(S\) at most in
the window \(y\in[\lambda-\sqrt{2-\lambda^2},\,\lambda+\sqrt{2-\lambda^2}]\).
The top of \(G\) is at height \(2\lambda-\ell(\lambda)\). The comparison
\[
2\lambda-\ell(\lambda)\;\stackrel{?}{>}\;\lambda+\sqrt{2-\lambda^2}
\]
rearranges to \(\lambda-\ell(\lambda)>\sqrt{2-\lambda^2}\), which is the G1.large
polynomial \(\lambda^4>2\), i.e. \(a>2^{5/4}\). So \(F\) may enter the *bottom*
of \(G\) but cannot reach the *top*. Combined with T8, the top of \(G\) is
uncovered. This closes the \(C\)-midpoint subcase of G2 on \((2^{5/4},\sqrt{6}]\).

The subcase in which **\(F\)** hosts the unique extra-midpoint (so \(C\) contains
only \(c\) among important points) is not covered by this argument: there is no
full inner side \([c,m]\subset C\) on which to hang the L-gap. That is GAPS §G2.

---

## 4. Lemma T8 (\(k=2\) adjacent, one representative, \(a>\sqrt{5}\))

This is the DLT Case-2 analogue: \(C\ni c,m_4\), \(V_3\ni v_3,m_2\),
\(V_4\ni v_4,m_3\), \(F\ni m_1\). Triangle T3 ejects \(V_3\) from \([c,m_3]\).
The L-gap of §3 on \([v_4,m_4]\) appears for \(a>\sqrt{5}\). Here \(F\ni m_1\)
is confined by diameter to a sliver about \(c\) in \(R\) and **misses** the left
side of \(R\) for \(\lambda>1\) (the sliver’s left edge is
\(\lambda-\sqrt{2-\lambda^2}>0\)). Combined with \(V_1\) missing \(G\), the gap
is uncovered.

This closes **one** G4 representative for \(a>\sqrt{5}\). Sister G4 orbits and
the interval \((2,\sqrt{5}]\) remain. If \(c\in F\) as well, the sliver argument
must be replaced by the centre-reach of G1.large; that is G5, and is absorbed
for \(a>2^{5/4}\) by the same height comparison as in G2.large.

---

## 5. G3, G4 remainder, G5

**G3.** Extra-midpoints opposite: \(C\) contains \(c\) and one midpoint, \(F\)
the opposite midpoint. There is no DLT-adjacent pair \((m_2\in V_3,\,m_3\in V_4)\)
on which to hang T3+T8. Two opposite inner rays are fully extra-covered, which
is compatible with a Type-III “diamond at the centre” picture. No contradiction
on any subinterval is proved. See GAPS §G3.

**G4 remainder.** Adjacent extra-midpoints other than the T8 labeling, and
T8 itself on \((2,\sqrt{5}]\), need a two-item quarter after ejecting \(F\).
The diameter sliver of \(F\cap R\) is proved; \(S_{\mathrm{bd}}(2)\) still fails
because \(V_1\) can poke the lower left of \(R\) for \(a\le\sqrt{5}\). See GAPS §G4.

**G5.** If \(c\in C\cap F\), both extras lie in the disk of radius \(\sqrt{2}\)
about \(c\). Their intersections with \(\partial S\) are midpoint-windows of
half-width \(\sqrt{2-\lambda^2}\). For \(a>2^{5/4}\) those windows miss the far
leftovers of G1.large, so G5 does not save G1 (or the large-\(a\) parts of G2/G4).
On \((2,2^{5/4}]\) two complementary centre-squares *can* meet all four sides
near the midpoints; G5 does not reduce to “\(F\not\ni c\)”. See GAPS §G5.

---

## 6. What is not claimed

- \(S(6)=2\) is **not** proved.
- \(S_{\mathrm{bd}}(6)=1+\sqrt{2}\) is **not** proved (only \(S_{\mathrm{bd}}(6)>2\)).
- Closing a gap on a subinterval \((a_0,\sqrt{6}]\) does **not** yield
  \(S(6)\le a_0\), because other gaps remain open down to \(a=2^+\).

The strongest global statement:

> Any covering of a square of side \(a\in(2,\sqrt{6}]\) by six unit squares has
> type \(k\in\{0,1,2\}\) as above, extras meet \(\partial S\), and:
> - if \(k=0\), then the covering is a 2-meet or a 3-meet, and locally
>   \(a\le a_{\mathrm{top}}\) in C-on-top, \(a\le a_{\mathrm{cr}}\) in C-on-right,
>   and \(a\le a_\varphi\) in meet deep-\(\delta\) (0-meet, 1-meet, and 4-meet
>   are impossible for all \(a>2\));
> - if \(k=1\) in the T8-adjacent \(C\)-midpoint orbit, then \(a\le 2^{5/4}\);
> - if \(k=2\) adjacent in the T8 labeling, then \(a\le\sqrt{5}\).
>
> Coverings on \((2,a_{\mathrm{top}}]\) are not ruled out in Open B C-on-top,
> nor on \((2,a_{\mathrm{cr}}]\) in C-on-right, nor on \((2,a_\varphi]\) in meet
> deep-\(\delta\), nor in G2, G3, G4, or G5. \(S(6)=2\) is **not** proved.

---

## 7. Computer checks

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest
python3 -m proof
```

Census (74 assignments, 11 \(D_4\)-orbits) is tagged G1–G4 in
[`../artifacts/proof/case_table.md`](../artifacts/proof/case_table.md).
G5 is not a row of that table.
