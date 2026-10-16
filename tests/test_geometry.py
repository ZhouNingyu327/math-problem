"""Geometry unit tests."""

import numpy as np

from cover6.coverage import evaluate_covering, uncovered_area
from cover6.geometry import min_outside, points_covered, unit_square_vertices
from cover6.configs import trivial_grid


def test_vertices_axis_aligned():
    v = unit_square_vertices(0.5, 0.5, 0.0)
    assert v.shape == (4, 2)
    assert np.allclose(np.min(v, axis=0), [0.0, 0.0], atol=1e-12)
    assert np.allclose(np.max(v, axis=0), [1.0, 1.0], atol=1e-12)


def test_rotated_45_bounding_box():
    v = unit_square_vertices(0.0, 0.0, np.pi / 4)
    # Vertices of a 45-degree unit square sit on the axes at distance sqrt(2)/2.
    r = np.sqrt(2) / 2
    radii = np.linalg.norm(v, axis=1)
    assert np.allclose(radii, r, atol=1e-12)


def test_point_inside_and_outside():
    poses = np.array([[0.5, 0.5, 0.0]])
    inside = np.array([[0.5, 0.5], [0.0, 0.0], [1.0, 1.0]])
    outside = np.array([[1.1, 0.5], [-0.1, 0.5], [0.5, 1.2]])
    assert points_covered(inside, poses).all()
    assert not points_covered(outside, poses).any()
    assert (min_outside(inside, poses) <= 1e-12).all()
    assert (min_outside(outside, poses) > 0).all()
