"""Exact algebraic lemmas and the combinatorial census for the proof attempt."""

import math

import pytest
import sympy as sp

from proof.enumerate_types import all_assignments, census, orbit_representatives
from proof.inequalities import (
    LFunction,
    l_numeric,
    numeric_table,
    run_all_proofs,
)


def test_run_all_proofs():
    proved = run_all_proofs()
    assert len(proved) >= 13
    assert all(v == "proved" for v in proved.values())


def test_l_endpoints_and_monotonicity_samples():
    assert abs(l_numeric(1.0) - 1.0) < 1e-15
    assert abs(l_numeric(math.sqrt(2.0))) < 1e-15
    xs = [1.0 + i * 0.05 for i in range(9)]
    vals = [l_numeric(x) for x in xs]
    assert all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))
    sums = [x + l_numeric(x) for x in xs]
    assert all(sums[i] > sums[i + 1] for i in range(len(sums) - 1))
    assert 0.0 <= min(vals) <= max(vals) <= 1.0


def test_no_forced_middle_gap_on_standing_interval():
    # 2/λ ≥ λ on λ ≤ √2, and standing λ ≤ √6/2 < √2.
    assert math.sqrt(6) / 2 < math.sqrt(2)
    for a in (2.01, 2.2, math.sqrt(6)):
        lam = a / 2.0
        assert 2.0 / lam >= lam - 1e-12


def test_census_capacity_and_k4_matching():
    raw = all_assignments()
    # No assignment has k<2: capacity 4-k ≤ 2 extras.
    assert all(sum(v.startswith("V") for v in asn.values()) >= 2 for asn in raw)
    k4 = [asn for asn in raw if all(v.startswith("V") for v in asn.values())]
    # Only two perfect matchings on C4: clockwise Vi←mi and counterclockwise.
    assert len(k4) == 2
    cw = {"m1": "V1", "m2": "V2", "m3": "V3", "m4": "V4"}
    ccw = {"m1": "V2", "m2": "V3", "m3": "V4", "m4": "V1"}
    assert cw in k4 and ccw in k4


def test_census_d4_orbits_and_open_remaining():
    cen = census()
    assert cen["n_raw_assignments"] == len(all_assignments())
    # k=4 cw and ccw are D4-equivalent (reflection), so one orbit. This is G1.
    k4_orbs = [r for r in cen["orbits"] if r["k"] == 4]
    assert len(k4_orbs) == 1
    assert k4_orbs[0]["orbit_size"] == 2
    assert k4_orbs[0]["gap"] == "G1"
    assert k4_orbs[0]["k_extra"] == 0
    assert k4_orbs[0]["status"] == "partial"
    # Every raw assignment is accounted for in some orbit.
    assert sum(r["orbit_size"] for r in cen["orbits"] if True) == cen["n_raw_assignments"]
    gaps = {r["gap"] for r in cen["orbits"]}
    assert gaps == {"G1", "G2", "G3", "G4"}
    assert any(r["gap"] == "G3" and r["status"] == "open" for r in cen["orbits"])
    assert any(r["gap"] == "G4" and r["status"] == "partial" for r in cen["orbits"])
    g2 = [r for r in cen["orbits"] if r["gap"] == "G2"]
    assert any(r.get("t8_adjacent") and r["status"] == "partial" for r in g2)
    assert any(r["e_has_midpoint"] and not r["f_has_midpoint"] and not r.get("t8_adjacent") and r["status"] == "open" for r in g2)
    adj = [r for r in cen["orbits"] if r["k"] == 2 and r["vertex_midpoints_adjacent"] is True]
    opp = [r for r in cen["orbits"] if r["k"] == 2 and r["vertex_midpoints_adjacent"] is False]
    assert adj and opp
    assert all(r["gap"] == "G4" for r in adj)
    assert all(r["gap"] == "G3" for r in opp)


def test_l_formula_matches_dlt():
    x = sp.Symbol("x", positive=True)
    assert sp.simplify(LFunction.formula(x) - (x - x * sp.sqrt(x**2 - 1))) == 0


def test_numeric_table_deficit_positive():
    for row in numeric_table():
        if row["a"] > 2:
            assert row["deficit_k4"] > 0
            assert row["delta"] > 0


def test_g1_far_leftover_threshold():
    # λ⁴ = 2 at λ = 2^{1/4}, a = 2^{5/4}.
    a_star = 2.0 ** 1.25
    lam = a_star / 2.0
    leftover = lam - l_numeric(lam)
    reach = math.sqrt(2.0 - lam * lam)
    assert abs(leftover - reach) < 1e-9
    # Above the threshold, leftover outruns the centre-square.
    lam2 = (a_star + 0.02) / 2.0
    assert lam2 - l_numeric(lam2) > math.sqrt(2.0 - lam2 * lam2)
    assert a_star < math.sqrt(6.0)
    assert a_star > math.sqrt(5.0)


def test_sqrt5_left_gap_threshold():
    # 2 l(λ) = λ at a = √5; gap (2l < λ) for a > √5.
    a_star = math.sqrt(5.0)
    lam = a_star / 2.0
    assert abs(2.0 * l_numeric(lam) - lam) < 1e-12
    assert 2.0 * l_numeric((a_star + 0.05) / 2.0) < (a_star + 0.05) / 2.0
    assert 2.0 * l_numeric((a_star - 0.05) / 2.0) > (a_star - 0.05) / 2.0
    # V1 diameter √2 ends below the gap start λ + l(λ) throughout a ∈ (√5, √6].
    for a in (math.sqrt(5.0) + 1e-3, 2.3, math.sqrt(6.0)):
        lam = a / 2.0
        gap_start = lam + l_numeric(lam)
        assert gap_start > math.sqrt(2.0)
