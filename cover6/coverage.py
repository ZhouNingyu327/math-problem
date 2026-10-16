"""Coverage tests: dense sampling and polygon (shapely) uncovered measure."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
from shapely import union_all
from shapely.geometry import LineString, Polygon, box

from cover6.geometry import (
    min_outside,
    poses_from_vector,
    sample_boundary,
    sample_grid,
    target_corners,
    unit_square_vertices,
)


@dataclass
class CoverageReport:
    s: float
    n: int
    uncovered_area: float
    uncovered_boundary: float
    sample_uncovered_frac: float
    sample_n_points: int
    sample_n_uncovered: int
    boundary_sample_uncovered: int
    corners_uncovered: int
    max_outside: float
    covered: bool
    covered_strict: bool
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def covering_polygons(poses: np.ndarray) -> list[Polygon]:
    poses = np.asarray(poses, dtype=float).reshape(-1, 3)
    polys = []
    for cx, cy, theta in poses:
        verts = unit_square_vertices(cx, cy, theta)
        polys.append(Polygon(verts))
    return polys


def covering_union(poses: np.ndarray) -> Polygon:
    return union_all(covering_polygons(poses))


def uncovered_region(s: float, poses: np.ndarray) -> Polygon:
    target = box(0.0, 0.0, float(s), float(s))
    return target.difference(covering_union(poses))


def uncovered_area(s: float, poses: np.ndarray) -> float:
    region = uncovered_region(s, poses)
    if region.is_empty:
        return 0.0
    return float(region.area)


def uncovered_boundary_length(s: float, poses: np.ndarray) -> float:
    boundary = box(0.0, 0.0, float(s), float(s)).boundary
    leftover = boundary.difference(covering_union(poses))
    if leftover.is_empty:
        return 0.0
    return float(leftover.length)


def sample_coverage_stats(
    s: float,
    poses: np.ndarray,
    *,
    n_grid: int = 160,
    n_boundary: int = 400,
    eps: float = 1e-10,
) -> dict[str, float | int]:
    grid = sample_grid(s, n_grid)
    boundary = sample_boundary(s, n_boundary)
    corners = target_corners(s)
    grid_out = min_outside(grid, poses)
    bnd_out = min_outside(boundary, poses)
    cor_out = min_outside(corners, poses)
    n_grid_uncovered = int(np.count_nonzero(grid_out > eps))
    n_bnd_uncovered = int(np.count_nonzero(bnd_out > eps))
    n_cor_uncovered = int(np.count_nonzero(cor_out > eps))
    all_out = np.concatenate([grid_out, bnd_out, cor_out])
    return {
        "sample_n_points": int(grid.shape[0]),
        "sample_n_uncovered": n_grid_uncovered,
        "sample_uncovered_frac": n_grid_uncovered / max(grid.shape[0], 1),
        "boundary_sample_uncovered": n_bnd_uncovered,
        "corners_uncovered": n_cor_uncovered,
        "max_outside": float(np.max(all_out)),
    }


def evaluate_covering(
    s: float,
    poses: np.ndarray,
    *,
    n_grid: int = 160,
    n_boundary: int = 400,
    area_tol: float = 1e-8,
    boundary_tol: float = 1e-6,
    sample_eps: float = 1e-8,
) -> CoverageReport:
    """Evaluate coverage of [0,s]^2 by the given unit-square poses.

    ``covered`` uses polygon uncovered area/boundary plus sampling.
    ``covered_strict`` additionally requires a slightly shrunken target
    (negative buffer) to lie in the union, which rejects razor-thin
    numerical "covers".
    """
    poses = np.asarray(poses, dtype=float).reshape(-1, 3)
    area = uncovered_area(s, poses)
    blen = uncovered_boundary_length(s, poses)
    stats = sample_coverage_stats(
        s, poses, n_grid=n_grid, n_boundary=n_boundary, eps=sample_eps
    )
    sample_ok = (
        stats["sample_n_uncovered"] == 0
        and stats["boundary_sample_uncovered"] == 0
        and stats["corners_uncovered"] == 0
    )
    covered = (
        area <= area_tol
        and blen <= boundary_tol
        and bool(sample_ok)
    )
    # Conservative: interior slightly inside the target must be covered.
    target_eroded = box(0.0, 0.0, float(s), float(s)).buffer(-1e-9)
    leftover_strict = target_eroded.difference(covering_union(poses))
    strict_area = 0.0 if leftover_strict.is_empty else float(leftover_strict.area)
    covered_strict = covered and strict_area <= area_tol
    notes = []
    if area > area_tol:
        notes.append(f"uncovered_area={area:.3e}")
    if blen > boundary_tol:
        notes.append(f"uncovered_boundary={blen:.3e}")
    if not sample_ok:
        notes.append(
            f"sample_uncovered={stats['sample_n_uncovered']}/"
            f"{stats['sample_n_points']}"
        )
    return CoverageReport(
        s=float(s),
        n=int(poses.shape[0]),
        uncovered_area=float(area),
        uncovered_boundary=float(blen),
        sample_uncovered_frac=float(stats["sample_uncovered_frac"]),
        sample_n_points=int(stats["sample_n_points"]),
        sample_n_uncovered=int(stats["sample_n_uncovered"]),
        boundary_sample_uncovered=int(stats["boundary_sample_uncovered"]),
        corners_uncovered=int(stats["corners_uncovered"]),
        max_outside=float(stats["max_outside"]),
        covered=bool(covered),
        covered_strict=bool(covered_strict),
        notes="; ".join(notes),
    )


def sampling_loss(
    s: float,
    poses: np.ndarray,
    *,
    n_grid: int = 56,
    n_boundary: int = 80,
    corner_weight: float = 40.0,
    boundary_weight: float = 8.0,
    important_weight: float = 50.0,
) -> float:
    """Smooth-ish penalty for local/global optimization at fixed s.

    Uses a squared hinge on the Chebyshev outside-amount of sample points,
    with extra weight on the boundary, the four corners, the four side
    midpoints, and the center. Midpoints matter for s>2: no unit square
    can cover two of them, so they are a useful obstruction probe.
    """
    from cover6.geometry import target_midpoints

    poses = np.asarray(poses, dtype=float).reshape(-1, 3)
    grid = sample_grid(s, n_grid)
    # Half-cell offset grid so thin plus-shaped gaps near s=2 are less likely
    # to slip between sample lines.
    if n_grid >= 8:
        xs = np.linspace(0.0, s, n_grid, endpoint=False) + 0.5 * s / n_grid
        xx, yy = np.meshgrid(xs, xs, indexing="xy")
        grid = np.vstack([grid, np.column_stack([xx.ravel(), yy.ravel()])])
    boundary = sample_boundary(s, n_boundary)
    corners = target_corners(s)
    important = np.vstack([corners, target_midpoints(s), [[s / 2.0, s / 2.0]]])
    g = np.maximum(min_outside(grid, poses), 0.0)
    b = np.maximum(min_outside(boundary, poses), 0.0)
    imp = np.maximum(min_outside(important, poses), 0.0)
    return float(
        np.mean(g * g)
        + boundary_weight * np.mean(b * b)
        + (corner_weight + important_weight) * 0.5 * np.sum(imp * imp)
    )


def shapely_loss(s: float, poses: np.ndarray, *, boundary_weight: float = 0.25) -> float:
    """Exact polygonal uncovered area + weighted uncovered boundary length."""
    return uncovered_area(s, poses) + boundary_weight * uncovered_boundary_length(s, poses)


def loss_from_vector(
    x: np.ndarray,
    s: float,
    n: int,
    *,
    n_grid: int = 56,
    use_shapely: bool = False,
) -> float:
    poses = poses_from_vector(x, n)
    if use_shapely:
        return shapely_loss(s, poses)
    return sampling_loss(s, poses, n_grid=n_grid)


def target_boundary_lines(s: float) -> list[LineString]:
    return [
        LineString([(0.0, 0.0), (s, 0.0)]),
        LineString([(s, 0.0), (s, s)]),
        LineString([(s, s), (0.0, s)]),
        LineString([(0.0, s), (0.0, 0.0)]),
    ]
