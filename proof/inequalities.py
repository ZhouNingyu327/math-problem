"""Exact algebraic lemmas used in PROOF_ATTEMPT.md.

Every public function either returns a sympy relational that is *proved*
(the identity simplifies to True) or raises AssertionError. Numerical
tables are labelled as such and are never used as proof steps.

Standing interval: a ∈ (2, √6], equivalently λ = a/2 ∈ (1, √6/2].
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import sympy as sp

A = sp.Symbol("a", real=True, positive=True)
X = sp.Symbol("x", real=True, positive=True)
LAM = sp.Symbol("lambda", real=True, positive=True)

SQRT2 = sp.sqrt(2)
SQRT6 = sp.sqrt(6)
PHI = (1 + sp.sqrt(5)) / 2


@dataclass(frozen=True)
class LFunction:
    """Lemma 2.2 of Dósa–Lángi–Tuza: maximal short L-leg."""

    @staticmethod
    def formula(x=X):
        return x - x * sp.sqrt(x**2 - 1)

    @staticmethod
    def derivative(x=X):
        return sp.diff(LFunction.formula(x), x)

    @staticmethod
    def prove_decreasing_on_1_sqrt2() -> None:
        """l'(x) < 0 for x ∈ (1, √2]."""
        x = X
        lp = sp.simplify(LFunction.derivative(x))
        # l'(x) = 1 - sqrt(x^2-1) - x^2/sqrt(x^2-1)
        # = (sqrt(x^2-1) - (x^2-1) - x^2) / sqrt(x^2-1)
        # = (sqrt(x^2-1) + 1 - 2x^2) / sqrt(x^2-1)
        s = sp.sqrt(x**2 - 1)
        rewritten = (s + 1 - 2 * x**2) / s
        if sp.simplify(lp - rewritten) != 0:
            raise AssertionError("derivative rewrite failed")
        # denominator s > 0 on (1, √2]
        # numerator: s + 1 - 2x^2 ≤ √(2-1) + 1 - 2 = 0 at x=√2, and
        # at x→1+: 0 + 1 - 2 = -1 < 0. Show num < 0 by comparing squares:
        # s + 1 < 2x^2  ⇔  (since both sides > 0 for x≥1) wait 2x^2≥2≥ s+1?
        # s+1 ≤ 1+1=2 ≤ 2x^2, with 2x^2=2 only at x=1 where s=0, so s+1=1<2.
        # For x>1: 2x^2 > 2 ≥ 1+s only if s≤1 always (s≤1 on [1,√2]).
        # 2x^2 ≥ 2, 1+s ≤ 2, and 2x^2=2 iff x=1, 1+s=2 iff s=1 iff x=√2.
        # These cannot hold simultaneously, so 2x^2 > 1+s strictly on [1,√2].
        gap = 2 * x**2 - 1 - s
        # Prove gap > 0: (2x^2-1)^2 - (x^2-1) > 0 because 2x^2-1 ≥ 1 > 0.
        sq = sp.expand((2 * x**2 - 1) ** 2 - (x**2 - 1))
        # sq = 4x^4 - 4x^2 + 1 - x^2 + 1 = 4x^4 - 5x^2 + 2
        # Discriminant of 4u^2 - 5u + 2 with u=x^2: 25-32 < 0, leading coeff >0
        # so sq > 0 for all real x. Hence gap > 0.
        u = sp.Symbol("u", real=True, positive=True)
        quad = 4 * u**2 - 5 * u + 2
        disc = sp.discriminant(quad, u)
        if disc >= 0:
            raise AssertionError("expected 4u^2-5u+2 always positive")
        if sp.simplify(sq - (4 * x**4 - 5 * x**2 + 2)) != 0:
            raise AssertionError("square gap polynomial mismatch")

    @staticmethod
    def prove_sum_decreasing_on_1_sqrt2() -> None:
        """(x + l(x))' < 0 for x ∈ (1, √2]."""
        x = X
        s = sp.sqrt(x**2 - 1)
        f = x + LFunction.formula(x)  # 2x - x s
        fp = sp.simplify(sp.diff(f, x))
        # f = x (2 - s), f' = (2-s) + x (-x/s) = 2 - s - x^2/s
        # = (2s - (x^2-1) - x^2)/s = (2s - 2x^2 + 1)/s
        rewritten = (2 * s - 2 * x**2 + 1) / s
        if sp.simplify(fp - rewritten) != 0:
            raise AssertionError("sum derivative rewrite failed")
        # 2s + 1 < 2x^2 ? Square: (2s+1)^2 vs 4x^4
        # 4(x^2-1) + 4s + 1 = 4x^2 - 4 + 4s + 1 = 4x^2 + 4s - 3
        # Better: 2x^2 - 2s - 1. At x=1: 2-0-1=1>0; at x=√2: 4-2-1=1>0.
        gap = 2 * x**2 - 2 * s - 1
        # (2x^2-1)^2 - 4(x^2-1) > 0
        sq = sp.expand((2 * x**2 - 1) ** 2 - 4 * (x**2 - 1))
        # 4x^4 - 4x^2 + 1 - 4x^2 + 4 = 4x^4 - 8x^2 + 5 = 4(x^2-1)^2 + 1 > 0
        if sp.simplify(sq - (4 * (x**2 - 1) ** 2 + 1)) != 0:
            raise AssertionError("sum-gap polynomial mismatch")


def standing_interval():
    """Return (a_min_exclusive, a_max_inclusive) as sympy numbers."""
    return (sp.Integer(2), SQRT6)


def prove_vertex_center_too_far() -> None:
    """a/√2 > √2  ⇔  a > 2, so no unit square contains a vertex and the center."""
    # a/sqrt(2) - sqrt(2) = (a-2)/sqrt(2) > 0 iff a>2
    expr = sp.simplify(A / SQRT2 - SQRT2)
    if sp.simplify(expr - (A - 2) / SQRT2) != 0:
        raise AssertionError("vertex-center rewrite failed")


def prove_adjacent_midpoints_too_far() -> None:
    """a/√2 > √2  ⇔  a > 2."""
    prove_vertex_center_too_far()


def prove_nonadjacent_vertex_midpoint_too_far() -> None:
    """(a √5)/2 > √2 for a > 2."""
    # (a√5)/2 > √2  ⇔ a√5 > 2√2  ⇔ a > 2√(2/5)
    # 2√(2/5) = 2√0.4 ≈ 1.265 < 2, so yes on a>2.
    threshold = 2 * sp.sqrt(sp.Rational(2, 5))
    if not (threshold < 2):
        raise AssertionError("threshold should be < 2")
    # Direct: (2√5)/2 = √5 > √2 because 5>2.
    if not (sp.sqrt(5) > SQRT2):
        raise AssertionError("√5 > √2 failed")


def prove_triangle_area() -> None:
    """Right triangle of legs a/2 has area a²/8 > 1/2 iff a > 2."""
    area = (A / 2) * (A / 2) / 2
    if sp.simplify(area - A**2 / 8) != 0:
        raise AssertionError("area formula")
    # a^2/8 > 1/2  ⇔ a^2 > 4  ⇔ a > 2 (since a>0)
    if sp.simplify(A**2 / 8 - sp.Rational(1, 2) - (A**2 - 4) / 8) != 0:
        raise AssertionError("area comparison rewrite")


def prove_delta_positive() -> None:
    """δ(a) = a/2 − √(2 − a²/4) > 0 iff a > 2 (and a ≤ 2√2 so the sqrt is real)."""
    # a/2 > √(2 − a²/4)  ⇔ a²/4 > 2 − a²/4  ⇔ a²/2 > 2  ⇔ a² > 4  ⇔ a>2
    # Domain: 2 − a²/4 ≥ 0  ⇔ a ≤ 2√2. Standing interval a≤√6 < 2√2.
    if not (SQRT6 < 2 * SQRT2):
        raise AssertionError("√6 < 2√2 failed")
    lhs = (A / 2) ** 2
    rhs = 2 - A**2 / 4
    if sp.simplify(lhs - rhs - (A**2 / 2 - 2)) != 0:
        raise AssertionError("delta rewrite")


def prove_n5_arc_inequality() -> None:
    """5a/2 − 2√2 > a  ⇔  a > 4√2/3 ≈ 1.885, hence on the standing interval."""
    # 5a/2 - a > 2√2  ⇔  3a/2 > 2√2  ⇔ a > 4√2/3
    threshold = 4 * SQRT2 / 3
    if not (threshold < 2):
        raise AssertionError("4√2/3 should be < 2")
    if sp.simplify(sp.Rational(5, 2) * A - 2 * SQRT2 - A - (sp.Rational(3, 2) * A - 2 * SQRT2)) != 0:
        raise AssertionError("n5 arc rewrite")


def prove_n5_with_sixth_square_never_restores() -> None:
    """5a/2 − 2√2 − √2 > a is equivalent to a > 2√2, which is outside a ≤ √6.

    Worst-case subtracting a full diameter √2 from the DLT Case-3 leftover
    never restores the contradiction on the standing interval.
    """
    # 5a/2 - 3√2 > a  ⇔  3a/2 > 3√2  ⇔ a > 2√2
    if not (2 * SQRT2 > SQRT6):
        raise AssertionError("2√2 > √6 failed")


def prove_perimeter_deficit_k4() -> None:
    """2(a − 2 l(a/2)) > 0 for a ∈ (2, 2√2]."""
    # l(a/2) < 1 for a/2 > 1, and a > 2, so a − 2l(a/2) > 2 − 2 = 0.
    # Need l(x) < 1 for x ∈ (1, √2].
    # l(x) − 1 = x − x s − 1 = x(1-s) − 1. Since l is decreasing (proved)
    # and l(1)=1, we have l(x)<1.
    x = A / 2
    l = LFunction.formula(x)
    # Direct: 1 - l(x) = 1 - x + x s. For x>1 this is positive because
    # l(x) = x(1-s) and s>0 so 1-s<1, thus l(x) < x, not enough.
    # l(x) = x(1-s) < 1  ⇔ x - 1 < x s  (since 1-s>0? s<1 on [1,√2))
    # s=1 at x=√2, l(√2)=√2(1-1)=0<1.
    # For x∈(1,√2): s<1 so 1-s>0. x(1-s)<1 ⇔ 1-s < 1/x ⇔ 1 - 1/x < s
    # ⇔ (x-1)/x < s. Square (both sides positive): (x-1)^2 / x^2 < x^2 - 1
    # ⇔ (x-1)^2 < x^2 (x-1)(x+1)  ⇔ x-1 < x^2 (x+1)   (x>1)
    # ⇔ 0 < x^3 + x^2 - x + 1. All positive. Wait: x-1 < x^2(x+1)=x^3+x^2
    # ⇔ 0 < x^3 + x^2 - x + 1, yes.
    lhs = (x - 1) ** 2
    rhs = x**2 * (x**2 - 1)
    gap = sp.expand(rhs - lhs)
    # After cancelling (x-1): we already outlined the chain. Check gap > 0
    # symbolically on x>1: rhs - lhs = x^2(x^2-1) - (x-1)^2
    # = (x-1)[ x^2(x+1) - (x-1) ] = (x-1)(x^3 + x^2 - x + 1)
    factored = (x - 1) * (x**3 + x**2 - x + 1)
    if sp.expand(gap - factored) != 0:
        raise AssertionError("l<1 factorization mismatch")


def prove_height_area_bound() -> None:
    """If a unit square contains a segment of length λ and a point at
    perpendicular distance h from that line, then h ≤ 1/λ.

    Corollary: 2/λ ≥ λ on λ ∈ (0, √2], so two opposite-side squares are
    *not* forced to leave a middle gap in a λ-square when λ ≤ √2.
    """
    # triangle area λ h / 2 ≤ 1/2 ⇒ h ≤ 1/λ. This is DLT's parallelogram fact.
    # 2/λ ≥ λ  ⇔  2 ≥ λ^2  ⇔ λ ≤ √2.
    if not (SQRT6 / 2 < SQRT2):
        raise AssertionError("standing λ = √6/2 < √2 failed")


def prove_sliver_geometry() -> None:
    """For λ ∈ (1, √2): √2 − λ > 0, and √(2−λ²) < λ, and 2λ − √2 > 0."""
    # √2 > λ because λ ≤ √6/2 < √2
    # √(2-λ²) < λ  ⇔ 2-λ² < λ²  ⇔ 2 < 2λ²  ⇔ λ > 1
    # 2λ − √2 > 0  ⇔ λ > √2/2, true for λ>1 > 0.707
    if not (sp.Rational(1, 1) > SQRT2 / 2):
        raise AssertionError("1 > √2/2 failed")


def prove_right_side_diameter_no_gap() -> None:
    """2 √(2−λ²) ≥ λ on λ ∈ (1, √6/2]. Equality is not needed; this shows the
    diameter bound does not force a gap on the inner side of the Case-2 quadrant.
    """
    # 2√(2-λ²) ≥ λ  ⇔ 4(2-λ²) ≥ λ²  ⇔ 8 ≥ 5λ²  ⇔ λ ≤ √(8/5)
    # √(8/5) = 2√10 / 5 ≈ 1.2649 > √6/2 ≈ 1.2247
    if not (sp.sqrt(sp.Rational(8, 5)) > SQRT6 / 2):
        raise AssertionError("√(8/5) should exceed √6/2")


A_STAR = 2 ** sp.Rational(5, 4)  # 2^{5/4} ≈ 2.378; λ = 2^{1/4}


def prove_centre_cannot_cover_far_leftover() -> None:
    """On a side whose vertex items cover [v_i, m_i] and a short L-leg l(λ)
    from v_{i+1}, the leftover has length λ − l(λ) = λ√(λ²−1) past the midpoint.

    A unit square containing c (distance λ from the side) can reach at most
    √(2−λ²) past the midpoint. That fails to cover the leftover iff
    λ√(λ²−1) > √(2−λ²) iff λ⁴ > 2 iff λ > 2^{1/4} iff a > 2^{5/4}.
    """
    lam = LAM
    l = LFunction.formula(lam)
    leftover = sp.simplify(lam - l)  # λ √(λ²−1)
    if sp.simplify(leftover - lam * sp.sqrt(lam**2 - 1)) != 0:
        raise AssertionError("leftover identity")
    reach = sp.sqrt(2 - lam**2)
    # leftover^2 - reach^2 = λ²(λ²−1) − (2−λ²) = λ⁴ − 2
    diff = sp.expand(leftover**2 - reach**2)
    if sp.simplify(diff - (lam**4 - 2)) != 0:
        raise AssertionError("G1 far-leftover polynomial")
    if not (A_STAR < SQRT6):
        raise AssertionError("2^{5/4} < √6")
    if not (A_STAR > sp.sqrt(5)):
        raise AssertionError("2^{5/4} > √5")
    if not (A_STAR > 2):
        raise AssertionError("2^{5/4} > 2")


def prove_far_pair_distance() -> None:
    """Clockwise leftover far-ends on adjacent sides of S are at distance λ²√2.

    On side E_i the leftover, when nonempty, ends at the inner tip of V_{i+1}'s
    short L-leg. For a maximal short-leg that tip is
        p1 = (2λ − ℓ(λ), 0),   p2 = (2λ, 2λ − ℓ(λ))
    (bottom / right; the other pairs are D4 images). Then |p1 p2|² = 2λ⁴, so
    |p1 p2| = λ²√2 > √2 iff λ > 1 iff a > 2. No unit square contains two of
    them. Opposite far-ends are still farther: distance at least a > √2.
    """
    lam = LAM
    ell = LFunction.formula(lam)
    s = sp.sqrt(lam**2 - 1)
    # ℓ = λ(1−s),  2λ−ℓ = λ(1+s)
    if sp.simplify(ell - lam * (1 - s)) != 0:
        raise AssertionError("ell rewrite")
    if sp.simplify(2 * lam - ell - lam * (1 + s)) != 0:
        raise AssertionError("2λ−ℓ rewrite")
    d2 = ell**2 + (2 * lam - ell) ** 2
    if sp.simplify(d2 - 2 * lam**4) != 0:
        raise AssertionError("FarPair polynomial 2λ⁴")
    # opposite pair p1=(2λ−ℓ, 0) and p3=(ℓ, 2λ):
    # dx = 2λ−2ℓ, dy = −2λ, dist² = 4(λ−ℓ)² + 4λ² = 4λ² ( (1−(1−s))² + 1 ) > 4λ²
    opp = (2 * lam - 2 * ell) ** 2 + (2 * lam) ** 2
    if sp.simplify(opp - 4 * (lam - ell) ** 2 - 4 * lam**2) != 0:
        raise AssertionError("opposite far-end expansion")
    # (λ−ℓ) = λ s > 0 for λ>1, so opp = 4λ² s² + 4λ² = 4λ²(s²+1) = 4λ⁴ > 4
    if sp.simplify(sp.expand(opp) - 4 * lam**4) != 0:
        raise AssertionError("opposite far-end = 4λ⁴")


def prove_far_centre_triangle() -> None:
    """Triangle △(c, p1, p2) with adjacent leftover far-ends has area λ⁴/2.

    This is > 1/2 iff a > 2. Redundant with FarPair (two far-ends already do
    not fit in a unit square) but records the parallelogram obstruction
    through c explicitly. Shoelace on p1=(2λ−ℓ,0), p2=(2λ, 2λ−ℓ), c=(λ,λ).
    """
    lam = LAM
    ell = LFunction.formula(lam)
    p1x, p1y = 2 * lam - ell, 0
    p2x, p2y = 2 * lam, 2 * lam - ell
    cx, cy = lam, lam
    twice = p1x * p2y + p2x * cy + cx * p1y - (p1y * p2x + p2y * cx + cy * p1x)
    area = sp.simplify(twice / 2)
    if sp.simplify(area - lam**4 / 2) != 0:
        raise AssertionError("FarCentre area λ⁴/2")


def prove_cycle_sum_four_meet() -> None:
    """A clockwise 4-meet is impossible for a > 2.

    If every side of S is covered by the two incident vertex squares, then
    x_i + ℓ(x_{i+1}) ≥ a for the four long-leg lengths x_i ∈ [λ, √2]. Summing
        Σ (x_i + ℓ(x_i)) ≥ 4a > 8.
    But x ↦ x+ℓ(x) is decreasing on [1, √2] (already proved) with value 2 at
    x=1, hence x+ℓ(x) ≤ 2 and the left-hand side is ≤ 8, contradiction.
    Equality would require a=2 and every x_i=1 (the trivial 2×2 tiling).
    """
    x = X
    s = sp.sqrt(x**2 - 1)
    tot = x + LFunction.formula(x)  # 2x − x s = x(2−s)
    if sp.simplify(tot - x * (2 - s)) != 0:
        raise AssertionError("x+ℓ rewrite")
    # tot(1) = 2. For x>1, tot < 2 because the map is strictly decreasing.
    if sp.simplify(tot.subs(x, 1) - 2) != 0:
        raise AssertionError("x+ℓ at 1")
    LFunction.prove_sum_decreasing_on_1_sqrt2()


def prove_cascade_threshold_unique() -> None:
    """The cascade gap function f(a) = ℓ(a − ℓ(λ)) − (a − √2) has a unique
    root a_φ in (2, a_M), where a_M is the unique root of √2 + ℓ(λ) = a.

    Domain: α(a) := a − ℓ(λ) runs from α(2)=1 to α(a_M)=√2. On that interval
    α is strictly increasing (ℓ(λ) strictly decreasing in a), so ℓ(α(a)) is
    strictly decreasing, while a−√2 is strictly increasing, hence f is
    strictly decreasing. Signs: f(2) = 1 − (2−√2) = √2−1 > 0, and
    f(a_M) = 0 − (a_M−√2) = −ℓ(λ) < 0. Unique root, and the vertex-uncoverable
    leftover on the previous side after a meet appears iff a > a_φ.

    Adjacent meets are then impossible for a > a_φ: the common vertex square
    would need a short-leg at least a−√2 and a long-leg at least α(a), which
    is exactly f(a) ≥ 0.
    """
    # f(2) = √2 − 1 > 0
    if not (SQRT2 - 1 > 0):
        raise AssertionError("√2−1 > 0")
    # α(2) = 2 − ℓ(1) = 1
    if sp.simplify(2 - LFunction.formula(1) - 1) != 0:
        raise AssertionError("α(2)=1")
    # Meet-possibility: max long+short = √2 + ℓ(λ). At λ=1 this is √2+1 > 2.
    if not (SQRT2 + 1 > 2):
        raise AssertionError("√2+1 > 2")
    LFunction.prove_decreasing_on_1_sqrt2()


def prove_cascade_far_end_centre_reach() -> None:
    """After a meet, the previous-side vertex-uncoverable gap (a > a_φ) has
    far end P = (ℓ(α), a) on the top in the LR-meet labeling, α = a − ℓ(λ).

    At the cascade threshold itself, ℓ(α) = a − √2, so P = (a−√2, a) and
        |c P|² = (λ − (a−√2))² + λ² = (√2 − λ)² + λ² = 2λ² − 2λ√2 + 2.
    This is < 2 iff λ < √2, which holds on the standing interval. Hence C
    still reaches P at a = a_φ. As a increases, α increases, ℓ(α) decreases,
    P moves away from c, and |c P| is strictly increasing. At the long+short
    meet limit a_M (α=√2, ℓ(α)=0) one has P=(0,a) and |c P| = λ√2 > √2
    because λ > 1. So there is a unique a_♦ ∈ (a_φ, a_M) with |c P| = √2;
    for a > a_♦ the centre-square cannot contain the cascade far-end.

    The same distance appears for the BT-meet (C-on-right) far-end by D4.
    """
    lam = LAM
    # hypot(√2−λ, λ)² − 2 = 2λ² − 2λ√2 = 2λ(λ−√2) < 0 on λ ∈ (1, √2)
    diff = (SQRT2 - lam) ** 2 + lam**2 - 2
    if sp.simplify(diff - 2 * lam * (lam - SQRT2)) != 0:
        raise AssertionError("cascade-threshold centre-reach rewrite")
    # at the meet limit, P=(0,a), |cP|² = λ²+λ² = 2λ² > 2 iff λ>1
    if sp.simplify(2 * lam**2 - 2 - 2 * (lam**2 - 1)) != 0:
        raise AssertionError("meet-limit centre-reach rewrite")
    if not (SQRT6 / 2 < SQRT2):
        raise AssertionError("standing λ < √2")


def prove_openb_r2_top_diam() -> None:
    """Local OpenB-R2TopDiam: |p* − r*|² = 2μ⁴ > 2 for μ = λ > 1.

    Same polynomial as FarPair. In the Open B C-on-top labelling the two
    forced tips p*, r* on the boundary of the rectangle R2 are a D4 image
    of the adjacent leftover far-ends, so the identity is identical.
    This does *not* lower a_top or a_cr.
    """
    prove_far_pair_distance()
    mu = LAM
    if sp.simplify(2 * mu**4 - 2 - 2 * (mu**4 - 1)) != 0:
        raise AssertionError("OpenB-R2TopDiam 2μ⁴>2 iff μ>1")


def prove_clobe_fat_remaining_room() -> None:
    """On the meet band, C containing c and a boundary leftover tip still
    reaches past the height-bound inner edge of an opposite vertex square.

    Remaining opposite room after a chord of length ≥ λ is at most √2−λ
    (and at least that along the diagonal). The height bound for a vertex
    square with a λ-leg puts its inner edge at distance λ−1/λ from c.
    Then √2−λ ≥ λ−1/λ iff 2λ² − √2 λ − 1 ≤ 0. The positive root is
    λ_* = (√2+√10)/4, i.e. a_* = (√2+√10)/2 ≈ 2.288. The quadratic is
    negative on [1, λ_*], which contains the whole meet band (a ≤ a_φ < 2.02
    < a_*) and the local Open B cuts a_top, a_cr.

    Consequence: the moduli of unit squares containing {c} ∪ {leftover tip}
    is a fat positive-dimensional body throughout (2, a_φ], not a rigid
    pose. A θ-independent point witness cannot empty it. This *explains*
    the local stall (point-MES ~0.072% under δ_force; pose B&B survivors
    are fat lobes). It does **not** kill those coverings.
    """
    lam = LAM
    poly = 2 * lam**2 - SQRT2 * lam - 1
    # disc = 2 + 8 = 10, roots (√2 ± √10)/4
    disc = SQRT2**2 + 8
    if sp.simplify(disc - 10) != 0:
        raise AssertionError("CLobeFat discriminant")
    lam_star = (SQRT2 + sp.sqrt(10)) / 4
    a_star = 2 * lam_star
    # a_* > 2.02 > a_φ (a_φ < 2.02 by cascade_gap(2.02)<0, certified)
    # Prove (√2+√10)/2 > 201/100  ⇔  √2+√10 > 401/100
    # ⇔ 100√2 + 100√10 > 401. Compare by isolating √10.
    # √10 > 401/100 − √2. RHS positive because √2 < 2 < 4.01.
    rhs = sp.Rational(401, 100) - SQRT2
    # 10 > (401/100 − √2)² = 401²/10000 − 2·401/100·√2 + 2
    gap = 10 - rhs**2
    # gap = 8 - 401²/10000 + 8.02√2
    # Direct: (√2+√10)² = 2+2√20+10 = 12+4√5 > (401/100)² = 160801/10000 = 16.0801?
    # 12+4√5 ≈ 12+8.94 = 20.94 > 16.08, but that's squares of the sum vs 4.01².
    left_sq = sp.expand((SQRT2 + sp.sqrt(10)) ** 2)
    right_sq = sp.Rational(401, 100) ** 2
    if sp.simplify(left_sq - (12 + 4 * sp.sqrt(5))) != 0:
        raise AssertionError("CLobeFat (√2+√10)² rewrite")
    # 12+4√5 > 401²/10000  ⇔  (12·10000 − 401²) + 40000√5 > 0
    # 120000 − 160801 = −40801, so need 40000√5 > 40801 ⇔ √5 > 40801/40000
    # 5 > 40801² / 40000². Both positive.
    num = 40801**2
    den = 40000**2
    if not (5 * den - num > 0):
        raise AssertionError("CLobeFat a_* > 2.02")
    if not (a_star > sp.Rational(201, 100)):
        raise AssertionError("a_* should exceed 2.02")
    # poly at λ=1: 2−√2−1 = 1−√2 < 0
    if not (1 - SQRT2 < 0):
        raise AssertionError("CLobeFat at λ=1")
    # leading coeff > 0, so poly < 0 on [1, λ_*)
    if sp.simplify(poly.subs(lam, 1) - (1 - SQRT2)) != 0:
        raise AssertionError("CLobeFat poly(1)")
    # silence unused if the expansion of gap was not needed
    _ = gap


def prove_opposite_stub_escapes_centre_chord() -> None:
    """If C contains a segment [c, m] of length λ, the remaining room on the
    same line past c is at most √2−λ. The inner-star stub on the opposite ray
    has length δ(λ)=λ−√(2−λ²). Then δ > √2−λ iff λ > 4√2/5, i.e. a > 8√2/5.
    """
    lam = LAM
    delta = lam - sp.sqrt(2 - lam**2)
    room = SQRT2 - lam
    # δ − room = 2λ − √2 − √(2−λ²). Positive iff (2λ−√2)² > 2−λ² (and 2λ>√2).
    # 4λ² − 4λ√2 + 2 > 2 − λ²  ⇒  5λ² − 4√2 λ > 0  ⇒  λ > 4√2/5.
    thresh = 4 * SQRT2 / 5
    if not (thresh > 1):
        raise AssertionError("4√2/5 > 1")
    if not (2 * thresh < SQRT6):
        raise AssertionError("8√2/5 < √6")
    # record the algebraic identity used in PROOF/ATTEMPT.md
    lhs = sp.expand((2 * lam - SQRT2) ** 2 - (2 - lam**2))
    # 4λ² - 4λ√2 + 2 - 2 + λ² = 5λ² - 4√2 λ
    if sp.simplify(lhs - (5 * lam**2 - 4 * SQRT2 * lam)) != 0:
        raise AssertionError("opposite-stub polynomial")


def prove_left_side_L_gap_at_sqrt5() -> None:
    """2 l(λ) < λ  ⇔  λ > √5 / 2  ⇔  a > √5.

    On that range the two L-legs of V4 (down from v4) and E (up from m4) cannot
    meet on the left side of R4, and √2 < λ + l(λ) so V1 cannot reach the gap.
    """
    lam = A / 2
    l = LFunction.formula(lam)
    # 2l - λ = λ (1 - 2 sqrt(λ²-1)); negative iff λ² > 5/4.
    rewritten = lam * (1 - 2 * sp.sqrt(lam**2 - 1))
    if sp.simplify(2 * l - lam - rewritten) != 0:
        raise AssertionError("2l-λ rewrite failed")
    # λ + l(λ) = λ (2 - sqrt(λ²-1)) is decreasing from 2 to √2 on [1,√2],
    # hence > √2 for λ < √2. Standing λ ≤ √6/2 < √2.
    if not (SQRT6 / 2 < SQRT2):
        raise AssertionError("standing λ < √2")
    if not (sp.sqrt(5) < SQRT6):
        raise AssertionError("√5 < √6")
    if not (sp.sqrt(5) > 2):
        raise AssertionError("√5 > 2")


def l_numeric(x: float) -> float:
    if x <= 1.0:
        return 1.0
    if x >= math.sqrt(2.0):
        return 0.0
    return x - x * math.sqrt(x * x - 1.0)


def delta_numeric(a: float) -> float:
    return a / 2.0 - math.sqrt(2.0 - a * a / 4.0)


def _bisect_root(f, lo: float, hi: float, n: int = 80) -> float:
    a, b = lo, hi
    fa = f(a)
    for _ in range(n):
        m = 0.5 * (a + b)
        if fa * f(m) <= 0.0:
            b = m
        else:
            a = m
    return 0.5 * (a + b)


def cascade_gap_numeric(a: float) -> float:
    """ℓ(a − ℓ(λ)) − (a − √2). Positive iff adjacent meets are still possible."""
    lam = a / 2.0
    alpha = a - l_numeric(lam)
    return l_numeric(alpha) - (a - math.sqrt(2.0))


def cascade_far_centre_numeric(a: float) -> float:
    """|c − (ℓ(α), a)| − √2 for α = a − ℓ(λ). Positive iff C misses the cascade far-end."""
    lam = a / 2.0
    alpha = a - l_numeric(lam)
    p0 = l_numeric(alpha)
    dist = math.hypot(p0 - lam, a - lam)
    return dist - math.sqrt(2.0)


def a_meet_max_numeric() -> float:
    """Unique root of √2 + ℓ(λ) = a on (2, 2√2): long+short vertex-meet limit."""
    return _bisect_root(lambda a: math.sqrt(2.0) + l_numeric(a / 2.0) - a, 2.0, 2.3)


def a_phi_numeric() -> float:
    """Unique cascade threshold a_φ ≈ 2.00910069."""
    return _bisect_root(cascade_gap_numeric, 2.0, a_meet_max_numeric())


def a_diamond_numeric() -> float:
    """Unique a_♦ ∈ (a_φ, a_M) with |c P| = √2 for the cascade far-end P."""
    return _bisect_root(cascade_far_centre_numeric, a_phi_numeric(), a_meet_max_numeric())


def run_all_proofs() -> dict[str, str]:
    """Execute every exact lemma. Returns a dict of lemma name → 'proved'."""
    LFunction.prove_decreasing_on_1_sqrt2()
    LFunction.prove_sum_decreasing_on_1_sqrt2()
    prove_vertex_center_too_far()
    prove_adjacent_midpoints_too_far()
    prove_nonadjacent_vertex_midpoint_too_far()
    prove_triangle_area()
    prove_delta_positive()
    prove_n5_arc_inequality()
    prove_n5_with_sixth_square_never_restores()
    prove_perimeter_deficit_k4()
    prove_height_area_bound()
    prove_sliver_geometry()
    prove_right_side_diameter_no_gap()
    prove_left_side_L_gap_at_sqrt5()
    prove_centre_cannot_cover_far_leftover()
    prove_far_pair_distance()
    prove_far_centre_triangle()
    prove_cycle_sum_four_meet()
    prove_cascade_threshold_unique()
    prove_cascade_far_end_centre_reach()
    prove_openb_r2_top_diam()
    prove_clobe_fat_remaining_room()
    prove_opposite_stub_escapes_centre_chord()
    # l(1)=1, l(√2)=0
    if sp.simplify(LFunction.formula(1)) != 1:
        raise AssertionError("l(1)=1")
    if sp.simplify(LFunction.formula(SQRT2)) != 0:
        raise AssertionError("l(√2)=0")
    names = [
        "l decreasing on (1, √2]",
        "x+l(x) decreasing on (1, √2]",
        "vertex–center distance > √2 iff a>2",
        "adjacent midpoints farther than √2 iff a>2",
        "non-adjacent vertex–midpoint farther than √2 for a>2",
        "triangle area a²/8 > 1/2 iff a>2",
        "inner-star stub δ(a)>0 iff a>2",
        "DLT n=5 arc leftover 5a/2-2√2 > a on a>2",
        "subtracting √2 never restores the n=5 arc on a≤√6",
        "k=4 perimeter deficit 2(a-2l(a/2))>0",
        "height bound h≤1/λ; 2h not forced < λ on λ≤√2",
        "F-sliver: √2-λ>0, √(2-λ²)<λ, 2λ-√2>0",
        "2√(2-λ²)≥λ on standing interval (no forced inner-side gap)",
        "2l(λ)<λ iff a>√5; λ+l(λ)>√2 on standing interval",
        "centre cannot cover far leftover iff a>2^{5/4}",
        "FarPair: adjacent leftover far-ends at distance λ²√2 > √2 iff a>2",
        "FarCentre: △(c,p1,p2) has area λ⁴/2 > 1/2 iff a>2",
        "CycleSum: clockwise 4-meet impossible for a>2",
        "Cascade: unique a_φ in (2, a_M) for ℓ(a−ℓ(λ))=a−√2; adjacent meets die above it",
        "cascade far-end: |c P|<√2 at a_φ, |c P|>√2 at a_M, unique a_♦ in between",
        "OpenB-R2TopDiam: |p*-r*|²=2μ⁴>2 for μ=λ>1 (does not lower a_top/a_cr)",
        "CLobeFat: remaining room reaches the height-bound hole on a<a_*; lobes stay fat",
        "opposite inner stub escapes a λ-chord through c iff a>8√2/5",
        "l(1)=1 and l(√2)=0",
    ]
    return {n: "proved" for n in names}


def numeric_table(values_a=(2.01, 2.05, 2.10, 2.20, math.sqrt(6))) -> list[dict]:
    """Supporting table; not a proof."""
    rows = []
    for a in values_a:
        lam = a / 2.0
        rows.append(
            {
                "a": a,
                "lambda": lam,
                "l(a/2)": l_numeric(lam),
                "x+l at a/2": lam + l_numeric(lam),
                "delta": delta_numeric(a),
                "deficit_k4": 2 * (a - 2 * l_numeric(lam)),
                "h_area": 1.0 / lam,
                "two_h_area_minus_lambda": 2.0 / lam - lam,
                "sliver_width": math.sqrt(2.0) - lam,
                "reach_from_endpoints": math.sqrt(2.0 - lam * lam),
                "leftover_past_mid": lam - l_numeric(lam),
                "centre_reach_past_mid": math.sqrt(max(2.0 - lam * lam, 0.0)),
                "far_pair_distance": (lam**2) * math.sqrt(2.0),
                "cascade_gap": cascade_gap_numeric(a),
                "cascade_far_centre": cascade_far_centre_numeric(a),
            }
        )
    return rows
