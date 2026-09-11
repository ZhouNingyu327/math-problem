"""Unit-square poses: center + rotation, local coordinates, vertices."""

from __future__ import annotations

import numpy as np

# A unit square has diameter sqrt(2); rotation by pi/2 is a symmetry.
THETA_PERIOD = np.pi / 2


def rotation_matrix(theta: float) -> np.ndarray:
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def unit_square_vertices(cx: float, cy: float, theta: float) -> np.ndarray:
    """Return (4, 2) CCW vertices of a side-1 square with given center and rotation."""
    local = np.array(
        [[-0.5, -0.5], [0.5, -0.5], [0.5, 0.5], [-0.5, 0.5]],
        dtype=float,
    )
    return local @ rotation_matrix(theta).T + np.array([cx, cy], dtype=float)


def poses_from_vector(x: np.ndarray, n: int | None = None) -> np.ndarray:
    """Reshape a flat parameter vector to (n, 3) array of (cx, cy, theta)."""
    x = np.asarray(x, dtype=float).reshape(-1)
    if n is None:
        if x.size % 3 != 0:
            raise ValueError(f"pose vector length {x.size} is not a multiple of 3")
        n = x.size // 3
    return x.reshape(n, 3)


def vector_from_poses(poses: np.ndarray) -> np.ndarray:
    return np.asarray(poses, dtype=float).reshape(-1)


def wrap_theta(theta: np.ndarray | float) -> np.ndarray | float:
    """Wrap angles into [0, pi/2)."""
    return np.mod(theta, THETA_PERIOD)


def local_coords(points: np.ndarray, cx: float, cy: float, theta: float) -> np.ndarray:
    """Map world points into the local frame of a posed unit square.

    Local axes are aligned with the square; the square is the box
    [-0.5, 0.5] x [-0.5, 0.5] in this frame.
    """
    pts = np.asarray(points, dtype=float)
    if pts.ndim == 1:
        pts = pts.reshape(1, 2)
    c, s = np.cos(theta), np.sin(theta)
    dx = pts[:, 0] - cx
    dy = pts[:, 1] - cy
    lx = c * dx + s * dy
    ly = -s * dx + c * dy
    return np.column_stack([lx, ly])


def outside_amount(points: np.ndarray, cx: float, cy: float, theta: float) -> np.ndarray:
    """Signed Chebyshev distance to the unit square; negative means inside."""
    local = local_coords(points, cx, cy, theta)
    return np.maximum(np.abs(local[:, 0]), np.abs(local[:, 1])) - 0.5


def min_outside(points: np.ndarray, poses: np.ndarray) -> np.ndarray:
    """For each point, min over squares of the outside amount (negative = covered)."""
    pts = np.asarray(points, dtype=float)
    if pts.ndim == 1:
        pts = pts.reshape(1, 2)
    poses = np.asarray(poses, dtype=float).reshape(-1, 3)
    best = np.full(pts.shape[0], np.inf, dtype=float)
    for cx, cy, theta in poses:
        best = np.minimum(best, outside_amount(pts, cx, cy, theta))
    return best


def points_covered(
    points: np.ndarray, poses: np.ndarray, *, eps: float = 1e-12
) -> np.ndarray:
    return min_outside(points, poses) <= eps


def target_corners(s: float) -> np.ndarray:
    return np.array([[0.0, 0.0], [s, 0.0], [s, s], [0.0, s]], dtype=float)


def target_midpoints(s: float) -> np.ndarray:
    h = s / 2.0
    return np.array([[h, 0.0], [s, h], [h, s], [0.0, h]], dtype=float)


def sample_grid(s: float, n: int) -> np.ndarray:
    xs = np.linspace(0.0, s, n)
    xx, yy = np.meshgrid(xs, xs, indexing="xy")
    return np.column_stack([xx.ravel(), yy.ravel()])


def sample_boundary(s: float, n_per_edge: int) -> np.ndarray:
    t = np.linspace(0.0, s, n_per_edge)
    bottom = np.column_stack([t, np.zeros_like(t)])
    right = np.column_stack([np.full_like(t, s), t])
    top = np.column_stack([t[::-1], np.full_like(t, s)])
    left = np.column_stack([np.zeros_like(t), t[::-1]])
    # Drop duplicate corners between consecutive edges.
    return np.vstack([bottom[:-1], right[:-1], top[:-1], left[:-1]])


def pose_bounds(s: float, n: int, *, margin: float = 0.6) -> list[tuple[float, float]]:
    """Box bounds for (cx, cy, theta) of n squares covering [0,s]^2.

    A unit square whose center is more than 0.5*sqrt(2)+eps outside the
    target cannot cover any target point. The default margin is slightly
    larger than 0.5 so axis-aligned squares may sit flush with the border.
    """
    lo, hi = -margin, s + margin
    bounds: list[tuple[float, float]] = []
    for _ in range(n):
        bounds.extend([(lo, hi), (lo, hi), (0.0, THETA_PERIOD)])
    return bounds


def rotate_around(point: np.ndarray, origin: np.ndarray, angle: float) -> np.ndarray:
    rel = np.asarray(point, dtype=float) - origin
    return origin + rel @ rotation_matrix(angle).T
