"""Numerical experiments on covering a square by n unit squares.

S(n) is the largest edge length of a square that can be covered by n
axis-length-1 squares, allowing rigid motions (translation + rotation)
and overlaps.
"""

from cover6.coverage import CoverageReport, evaluate_covering
from cover6.geometry import poses_from_vector, unit_square_vertices, vector_from_poses

__version__ = "0.1.0"

__all__ = [
    "CoverageReport",
    "evaluate_covering",
    "poses_from_vector",
    "unit_square_vertices",
    "vector_from_poses",
    "__version__",
]
