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
│     └── closed for a > 2^{5/4}           Lemma G1.large
│     └── open on (2, 2^{5/4}]             GAPS §G1
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

This closes G1 on \((2^{5/4},\sqrt{6}]\). It does **not** close G1 on
\((2,2^{5/4}]\), where a centre-square *can* reach the whole leftover on each
side it meets, and two extras on complementary adjacent-side pairs can cover
all four leftovers. That is GAPS §G1.

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
> - if \(k=0\), then \(a\le 2^{5/4}\);
> - if \(k=1\) and \(C\) hosts the extra midpoint, then \(a\le 2^{5/4}\);
> - if \(k=2\) adjacent in the T8 labeling, then \(a\le\sqrt{5}\).
>
> Coverings on \((2,\sqrt{5}]\) are not ruled out in any type. Coverings on
> \((\sqrt{5},2^{5/4}]\) are not ruled out in G1, G2-\(F\), G3, G4-sisters, or G5.

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
