"""Baseline covering checks: trivial s=2 works; slightly larger does not."""

import math

import numpy as np

from cover6.configs import S3_DUDENEY, dudeney_three, trivial_grid
from cover6.coverage import evaluate_covering, uncovered_area


def test_trivial_n6_s2_covered():
    poses = trivial_grid(s=2.0, n=6)
    report = evaluate_covering(2.0, poses)
    assert report.covered, report.notes
    assert report.covered_strict
    assert report.uncovered_area < 1e-12
    assert report.corners_uncovered == 0


def test_trivial_n4_s2_covered():
    poses = trivial_grid(s=2.0, n=4)
    report = evaluate_covering(2.0, poses)
    assert report.covered, report.notes
    assert report.uncovered_area < 1e-12


def test_trivial_n6_s2p05_not_covered():
    poses = trivial_grid(s=2.05, n=6)
    report = evaluate_covering(2.05, poses)
    assert not report.covered
    assert report.uncovered_area > 1e-4


def test_area_upper_bound_not_claimed_feasible():
    # Area says S(6) <= sqrt(6) ≈ 2.449. A side this large cannot be covered
    # by the trivial construction, and we treat it as a sanity bound only.
    s = math.sqrt(6)
    poses = trivial_grid(s=2.0, n=6)
    assert uncovered_area(s, poses) > 0.5


def test_dudeney_n3_covers_theory_side():
    poses = dudeney_three()
    report = evaluate_covering(S3_DUDENEY, poses, n_grid=120)
    assert report.uncovered_area < 1e-8, report.notes
    assert report.corners_uncovered == 0
    assert report.covered, report.notes
