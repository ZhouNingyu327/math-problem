"""Interval-certificate hooks for residual G1 configurations.

This module does **not** prove S(6)=2. It (1) certifies the cascade / diamond
/ meet-limit thresholds with mpmath interval arithmetic so CI can re-check the
brackets in PROOF/GAPS.md, and (2) records the schema of a computer-assisted
covering certificate for the residual 2-meet and 3-meet boxes on (2, a_♦].

A covering certificate, once produced, is a JSON list of boxes in configuration
space, each carrying a witness point of S that every unit-square tuple in the
box misses. Verification is a finite arithmetic check: interval evaluation of
the four vertex squares and two extras on that witness, confirming the point
lies outside every square.
"""

from __future__ import annotations

from typing import Any

from mpmath import iv

from proof.inequalities import (
    a_diamond_numeric,
    a_meet_max_numeric,
    a_phi_numeric,
)

# Published brackets: each named root is the unique zero of the corresponding
# function on (2, 2√2), and the function takes opposite strict signs at the
# two endpoints (certified below by interval arithmetic).
A_PHI_BRACKET = ("2.00910069", "2.00910070")
A_DIAMOND_BRACKET = ("2.09180768", "2.09180769")
A_MEET_MAX_BRACKET = ("2.11195453", "2.11195454")

# Local Open B cuts (not isolating roots of a repo-proved equation).
# Do not invent a_top^F ≈ 2.0265; that cut is retracted (δ≥2g0 invalid
# under R1Exclusive). These values do not move after OpenB-R2TopDiam / FHeight.
A_TOP_LOCAL = 2.0361747746
A_CR_LOCAL = 2.0036185600

RESIDUAL_TYPES = (
    "G1-2adj",   # two adjacent vertex-meets, leftovers on the other two sides
    "G1-2opp",   # two opposite vertex-meets (C-on-top / C-on-right)
    "G1-3meet",  # three vertex-meets, one leftover side
)


def _ell_iv(x):
    return x - x * iv.sqrt(x * x - 1)


def cascade_gap_iv(a):
    lam = a / 2
    alpha = a - _ell_iv(lam)
    return _ell_iv(alpha) - (a - iv.sqrt(iv.mpf(2)))


def cascade_far_centre_iv(a):
    lam = a / 2
    alpha = a - _ell_iv(lam)
    p0 = _ell_iv(alpha)
    d2 = (p0 - lam) ** 2 + (a - lam) ** 2
    return iv.sqrt(d2) - iv.sqrt(iv.mpf(2))


def meet_max_iv(a):
    return iv.sqrt(iv.mpf(2)) + _ell_iv(a / 2) - a


def _strict_positive(x) -> bool:
    return x.a > 0


def _strict_negative(x) -> bool:
    return x.b < 0


def certify_published_brackets(dps: int = 40) -> dict[str, dict[str, str]]:
    """Interval-arithmetic sign certificates for a_φ, a_♦, a_M.

    Each function is continuous and strictly monotone on the isolating
    interval (proved in `proof.inequalities`), so a strict sign change at
    the published endpoints pins the unique root inside the bracket.
    """
    iv.dps = dps
    out: dict[str, dict[str, str]] = {}
    checks = (
        ("a_phi", cascade_gap_iv, A_PHI_BRACKET, True),       # + then −
        ("a_diamond", cascade_far_centre_iv, A_DIAMOND_BRACKET, False),  # − then +
        ("a_meet_max", meet_max_iv, A_MEET_MAX_BRACKET, True),
    )
    for name, f, (lo_s, hi_s), pos_then_neg in checks:
        lo, hi = iv.mpf(lo_s), iv.mpf(hi_s)
        flo, fhi = f(lo), f(hi)
        if pos_then_neg:
            if not _strict_positive(flo):
                raise AssertionError(f"{name}: f({lo_s}) not strictly positive ({flo})")
            if not _strict_negative(fhi):
                raise AssertionError(f"{name}: f({hi_s}) not strictly negative ({fhi})")
        else:
            if not _strict_negative(flo):
                raise AssertionError(f"{name}: f({lo_s}) not strictly negative ({flo})")
            if not _strict_positive(fhi):
                raise AssertionError(f"{name}: f({hi_s}) not strictly positive ({fhi})")
        out[name] = {"lo": lo_s, "hi": hi_s, "sign": "+-" if pos_then_neg else "-+"}
    return out


def brackets_contain_numeric_roots() -> None:
    """Float bisection roots lie in the published brackets."""
    checks = (
        (a_phi_numeric(), A_PHI_BRACKET),
        (a_diamond_numeric(), A_DIAMOND_BRACKET),
        (a_meet_max_numeric(), A_MEET_MAX_BRACKET),
    )
    for root, (lo, hi) in checks:
        if not (float(lo) <= root <= float(hi)):
            raise AssertionError(f"{root} not in [{lo}, {hi}]")


def covering_certificate_schema() -> dict[str, Any]:
    """Informal schema for a residual-configuration covering certificate.

    Configuration of one vertex square: (x, y, theta) for the centre of the
    unit square and the angle of an edge, each an interval. Six squares give
    an 18-dimensional box. A certificate row is:

        {
          "type": "G1-2opp" | "G1-2adj" | "G1-3meet",
          "a": [a_lo, a_hi],          # side-length interval inside (2, a_♦]
          "box": 18 × [lo, hi],       # pose intervals
          "witness": [x, y],          # point of [0, a_hi]^2
          "reason": "point-miss" | "far-pair" | "triangle" | "diameter"
        }

    Verification for "point-miss": interval-evaluate the six rotated unit
    squares on the witness; each square's interval hull misses the point
    (the point is outside the Minkowski sum of the square with the pose
    uncertainty). Union of boxes must cover the compact configuration
    space of the named type (boundary of the type is a lower-dimensional
    set, handled by a separate closed-face list).

    This is the MES-free / reach-bookkeeping-free plan for the meet band:
    the witness is typically an *interior* point (hinge vertex of two
    meeting L-legs, or a diagonal-gap point), not a MES of a forced
    leftover on ∂S.
    """
    return {
        "residual_types": list(RESIDUAL_TYPES),
        "a_interval": "(2, a_diamond]",
        "pose_dim": 18,
        "witness_dim": 2,
        "reasons": ["point-miss", "far-pair", "triangle", "diameter"],
        "ci": "python3 -m proof  # certifies a_φ, a_♦ brackets; checks schema if file present",
        "certificate_path": "artifacts/proof/meet_band_certificates.json",
    }


def load_and_check_optional_certificates(path) -> dict[str, Any]:
    """If a certificate file exists, check the schema. Missing file is OK."""
    import json
    from pathlib import Path

    p = Path(path)
    if not p.exists():
        return {"present": False, "schema": covering_certificate_schema()}
    data = json.loads(p.read_text())
    if not isinstance(data, list):
        raise AssertionError("certificate file must be a JSON list")
    allowed = set(RESIDUAL_TYPES)
    a_hi_max = float(A_DIAMOND_BRACKET[1]) + 1e-6
    for i, row in enumerate(data):
        if row.get("type") not in allowed:
            raise AssertionError(f"row {i}: bad type")
        if "a" not in row or "witness" not in row:
            raise AssertionError(f"row {i}: missing a or witness")
        _a_lo, a_hi = row["a"]
        if not (2.0 < float(a_hi) <= a_hi_max):
            raise AssertionError(f"row {i}: a-interval not inside (2, a_♦]")
    return {"present": True, "n": len(data), "schema": covering_certificate_schema()}
