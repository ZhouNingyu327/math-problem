"""Regression tests on committed covering artifacts."""

from pathlib import Path

from cover6.coverage import evaluate_covering
from cover6.io_util import load_json, poses_from_dict

ROOT = Path(__file__).resolve().parents[1]


def test_committed_baseline_json_covers():
    data = load_json(ROOT / "artifacts/baseline/n6_s2_trivial.json")
    s, poses = poses_from_dict(data)
    report = evaluate_covering(s, poses)
    assert s == 2.0
    assert report.covered
    assert report.uncovered_area == 0.0


def test_committed_dudeney_json_covers():
    data = load_json(ROOT / "artifacts/known/n3_dudeney.json")
    s, poses = poses_from_dict(data)
    report = evaluate_covering(s, poses)
    assert report.covered
    assert abs(s - 1.272019649514069) < 1e-9


def test_committed_boundary_n6_covers_perimeter_not_interior():
    data = load_json(ROOT / "artifacts/boundary_n6/best_boundary.json")
    s, poses = poses_from_dict(data)
    report = evaluate_covering(s, poses, n_grid=180, n_boundary=600)
    assert s > 2.0
    assert report.uncovered_boundary <= 1e-8
    assert report.corners_uncovered == 0
    assert report.boundary_sample_uncovered == 0
    assert report.uncovered_area > 1.0
    assert not report.covered
