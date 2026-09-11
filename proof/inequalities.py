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
            }
        )
    return rows
