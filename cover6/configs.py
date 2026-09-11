"""Named constructions and random / symmetric initializations."""

from __future__ import annotations

import math

import numpy as np

from cover6.geometry import THETA_PERIOD, rotate_around, wrap_theta

PHI = (1.0 + math.sqrt(5.0)) / 2.0
S3_DUDENEY = math.sqrt(PHI)  # S(3) = sqrt(phi) ≈ 1.27202
S7_GREEN = 1.5 + 0.5 * math.sqrt(2.0)  # side of Trevor Green's n=7 covering
S7_GREEN_AREA = S7_GREEN**2  # 11/4 + 3/sqrt(2)


def trivial_grid(s: float = 2.0, n: int = 6) -> np.ndarray:
    """Axis-aligned 2x2 covering of a side-2 square, plus unused extras.

    For s=2 this is a valid covering whenever n >= 4. Extra squares are
    stacked at the center (they do not hurt coverage).
    """
    if n < 4:
        raise ValueError("trivial 2x2 covering needs n >= 4")
    base = [
        (0.5, 0.5, 0.0),
        (1.5, 0.5, 0.0),
        (0.5, 1.5, 0.0),
        (1.5, 1.5, 0.0),
    ]
    extras = []
    for i in range(n - 4):
        extras.append((1.0, 1.0, (i * THETA_PERIOD / max(n - 4, 1))))
    poses = np.array(base + extras, dtype=float)
    if abs(s - 2.0) > 1e-15:
        # Shift the 2x2 block to the lower-left of a larger target; extras
        # sit on the remaining cross. This is *not* a covering for s>2.
        scale_shift = s - 2.0
        poses[:4, 0] += 0.0
        poses[:4, 1] += 0.0
        if n >= 5:
            poses[4] = (s / 2.0, 0.5 + scale_shift / 2.0, 0.0)
        if n >= 6:
            poses[5] = (s / 2.0, s - 0.5, 0.0)
        if n >= 7:
            poses[6] = (0.5, s / 2.0, 0.0)
    return poses


def corner_squares(s: float, n: int = 6, *, inset: float = 0.5) -> np.ndarray:
    """One square near each corner of [0,s]^2, remaining at the center."""
    if n < 4:
        raise ValueError("corner initialization needs n >= 4")
    d = min(inset, s / 2.0)
    base = [
        (d, d, 0.0),
        (s - d, d, 0.0),
        (s - d, s - d, 0.0),
        (d, s - d, 0.0),
    ]
    extras = []
    for i in range(n - 4):
        extras.append((s / 2.0, s / 2.0, i * math.pi / 8.0))
    return np.array(base + extras, dtype=float)


def rotated_corners_plus_center(s: float, n: int = 6, *, theta: float = math.pi / 8) -> np.ndarray:
    """C4-symmetric corner squares (rotated) plus extras at the center / sides."""
    origin = np.array([s / 2.0, s / 2.0])
    # Prototype near the lower-left corner of the *target*, then orbit.
    proto_c = np.array([0.5, 0.5])
    proto_theta = theta
    poses = []
    for k in range(4):
        ang = k * math.pi / 2.0
        c = rotate_around(proto_c, origin, ang)
        poses.append((c[0], c[1], wrap_theta(proto_theta + ang)))
    remaining = n - 4
    if remaining >= 1:
        poses.append((s / 2.0, s / 2.0, math.pi / 4.0))
    if remaining >= 2:
        poses.append((s / 2.0, 0.45, 0.0))
    if remaining >= 3:
        poses.append((s - 0.45, s / 2.0, math.pi / 4.0))
    for i in range(max(0, remaining - 3)):
        poses.append((s / 2.0, s / 2.0, (i + 1) * math.pi / 10.0))
    return np.array(poses[:n], dtype=float)


def type_i_bent_strip(s: float, n: int, *, block: int = 2) -> np.ndarray:
    """Type-I style: axis-aligned k x k block in the lower left, rest along an L.

    Friedman's Type I (used for n=7, 14, 23, ...) places a large untilted
    block in one corner and covers the remaining bent strip with tilted
    squares. For n=7 the published side is 3/2 + 1/sqrt(2) ≈ 2.207.
    """
    poses = []
    for iy in range(block):
        for ix in range(block):
            poses.append((0.5 + ix, 0.5 + iy, 0.0))
    n_block = block * block
    n_strip = n - n_block
    if n_strip < 0:
        return np.array(poses[:n], dtype=float)
    # Distribute remaining squares along the top and right strips.
    w = max(s - block, 0.15)
    top_count = (n_strip + 1) // 2
    right_count = n_strip - top_count
    theta = math.pi / 4.0
    for i in range(top_count):
        x = (i + 0.5) * s / max(top_count, 1)
        y = block + w / 2.0
        poses.append((min(x, s - 0.2), min(y, s - 0.2), theta))
    for i in range(right_count):
        y = (i + 0.5) * (block + w / 2.0) / max(right_count, 1)
        x = block + w / 2.0
        poses.append((min(x, s - 0.2), min(max(y, 0.2), s - 0.2), theta))
    return np.array(poses[:n], dtype=float)


def dudeney_three(s: float | None = None) -> np.ndarray:
    """Dudeney / Friedman covering realizing S(3)=sqrt(phi).

    Equality-case poses (Dósa–Lángi–Tuza Figure 1 / Friedman Figure 1, R=0):

    * T covers both top corners of the target. It has a vertex at the
      top-left target corner; the outward edge makes angle
      α = arccos(1/sqrt(phi)) with the top side.
    * One unit square is axis-aligned in the bottom-right corner.
    * The third square also has a vertex at the top-left target corner,
      with its first edge at angle 3π/2 − α (down the exterior of the
      left side), covering the remaining left/bottom region.

    These three polygons cover [0, sqrt(phi)]^2 up to floating-point error.
    """
    if s is None:
        s = S3_DUDENEY
    alpha = math.acos(1.0 / math.sqrt(PHI))
    v_tl = np.array([0.0, s], dtype=float)
    e_out = np.array([math.cos(alpha), math.sin(alpha)])
    e_in = np.array([math.sin(alpha), -math.cos(alpha)])
    center_t = v_tl + 0.5 * e_out + 0.5 * e_in
    theta_t = wrap_theta(math.atan2(e_in[1], e_in[0]))
    # Bottom-right axis-aligned unit square.
    br = (s - 0.5, 0.5, 0.0)
    # Third square: vertex at top-left, first-edge angle 3π/2 − α.
    theta_edge = 1.5 * math.pi - alpha
    e1 = np.array([math.cos(theta_edge), math.sin(theta_edge)])
    e2 = np.array([-e1[1], e1[0]])  # CCW
    center_bl = v_tl + 0.5 * e1 + 0.5 * e2
    bl = (float(center_bl[0]), float(center_bl[1]), float(wrap_theta(theta_edge)))
    top = (float(center_t[0]), float(center_t[1]), float(theta_t))
    return np.array([top, br, bl], dtype=float)


def green7_type_i(s: float | None = None) -> np.ndarray:
    """A Type-I initializer aimed at Trevor Green's n=7 covering.

    Exact published coordinates were not reconstructed; this is a
    geometrically faithful bent-strip seed for local/global polishing.
    The published side is 3/2 + 1/sqrt(2) ≈ 2.2071 (area 11/4 + 3/sqrt(2)).
    """
    if s is None:
        s = S7_GREEN
    return type_i_bent_strip(s, n=7, block=2)


def random_poses(s: float, n: int, rng: np.random.Generator) -> np.ndarray:
    cx = rng.uniform(-0.2, s + 0.2, size=n)
    cy = rng.uniform(-0.2, s + 0.2, size=n)
    th = rng.uniform(0.0, THETA_PERIOD, size=n)
    return np.column_stack([cx, cy, th])


def jitter(poses: np.ndarray, rng: np.random.Generator, *, pos: float = 0.15, ang: float = 0.25) -> np.ndarray:
    out = np.array(poses, dtype=float, copy=True)
    out[:, 0] += rng.normal(0.0, pos, size=out.shape[0])
    out[:, 1] += rng.normal(0.0, pos, size=out.shape[0])
    out[:, 2] = wrap_theta(out[:, 2] + rng.normal(0.0, ang, size=out.shape[0]))
    return out


def c4_expand(proto_cx: float, proto_cy: float, proto_theta: float, s: float) -> np.ndarray:
    """Four poses = C4 orbit of a prototype about the target center."""
    origin = np.array([s / 2.0, s / 2.0])
    proto = np.array([proto_cx, proto_cy])
    poses = []
    for k in range(4):
        ang = k * math.pi / 2.0
        c = rotate_around(proto, origin, ang)
        poses.append((c[0], c[1], wrap_theta(proto_theta + ang)))
    return np.array(poses, dtype=float)


def c4_from_vector(x: np.ndarray, s: float, n: int) -> np.ndarray:
    """Decode a reduced C4 parameterization into n poses.

    Layout:
      x[0:3]  = prototype corner square (cx, cy, theta)
      remaining squares are encoded as free (cx, cy, theta) triples,
      except we always replicate the prototype to 4 poses.
    """
    x = np.asarray(x, dtype=float).reshape(-1)
    core = c4_expand(x[0], x[1], x[2], s)
    extra_n = n - 4
    extras = []
    if extra_n > 0:
        rest = x[3:]
        extras = poses_from_rest(rest, extra_n, s)
    if extra_n <= 0:
        return core[:n]
    return np.vstack([core, extras])


def poses_from_rest(rest: np.ndarray, extra_n: int, s: float) -> np.ndarray:
    rest = np.asarray(rest, dtype=float).reshape(-1)
    need = extra_n * 3
    if rest.size < need:
        rest = np.pad(rest, (0, need - rest.size))
    extras = rest[:need].reshape(extra_n, 3)
    extras[:, 2] = wrap_theta(extras[:, 2])
    return extras


def c4_vector_bounds(s: float, n: int, *, margin: float = 0.6) -> list[tuple[float, float]]:
    lo, hi = -margin, s + margin
    bounds = [(lo, hi), (lo, hi), (0.0, THETA_PERIOD)]
    extra_n = max(n - 4, 0)
    for _ in range(extra_n):
        bounds.extend([(lo, hi), (lo, hi), (0.0, THETA_PERIOD)])
    return bounds


def c4_initial_vector(s: float, n: int, rng: np.random.Generator | None = None) -> np.ndarray:
    proto = np.array([0.45, 0.45, math.pi / 8.0])
    extras = []
    extra_n = max(n - 4, 0)
    if extra_n >= 1:
        extras.extend([s / 2.0, s / 2.0, math.pi / 4.0])
    if extra_n >= 2:
        extras.extend([s / 2.0, 0.4, 0.0])
    for i in range(max(0, extra_n - 2)):
        extras.extend([s / 2.0, s / 2.0, (i + 1) * 0.2])
    vec = np.concatenate([proto, np.array(extras, dtype=float)]) if extras else proto
    if rng is not None:
        vec = vec + rng.normal(0.0, 0.05, size=vec.shape)
        vec[2] = wrap_theta(vec[2])
    return vec


def midpoint_squares(s: float, n: int) -> np.ndarray:
    """Corner squares plus extras parked on side midpoints (and the center)."""
    poses = corner_squares(s, n=min(n, 4))
    mids = [
        (s / 2.0, 0.40, 0.0),
        (s - 0.40, s / 2.0, 0.0),
        (s / 2.0, s - 0.40, 0.0),
        (0.40, s / 2.0, 0.0),
        (s / 2.0, s / 2.0, math.pi / 4.0),
    ]
    extra_n = max(n - 4, 0)
    extras = list(mids[:extra_n])
    if extra_n > len(mids):
        extras.extend((s / 2.0, s / 2.0, 0.2 * i) for i in range(extra_n - len(mids)))
    if extras:
        poses = np.vstack([poses, np.array(extras, dtype=float)])
    return poses[:n]


def rotated_corner_midpoint(s: float, n: int) -> np.ndarray:
    """Tilt corner squares so their axis-aligned bounding box exceeds side 1.

    For s slightly above 2 this is the natural attempt to cover both a
    corner and the nearby side midpoint with one square.
    """
    over = max(0.0, s / 2.0 - 1.0)
    theta = math.asin(min(0.5, over + 0.08))
    d = 0.5
    origin = np.array([s / 2.0, s / 2.0])
    proto = np.array([d, d])
    poses = []
    for k in range(4):
        ang = k * math.pi / 2.0
        c = rotate_around(proto, origin, ang)
        poses.append((c[0], c[1], wrap_theta(theta + ang)))
    extra_n = n - 4
    extras: list[tuple[float, float, float]] = []
    if extra_n >= 1:
        extras.append((s / 2.0, s / 2.0, math.pi / 4.0))
    if extra_n >= 2:
        extras.append((s / 2.0, 0.45, math.pi / 6.0))
    if extra_n >= 3:
        extras.append((s - 0.45, s / 2.0, math.pi / 6.0))
    for i in range(max(0, extra_n - 3)):
        extras.append((s / 2.0, s / 2.0, 0.15 * (i + 1)))
    if extras:
        poses = poses + extras
    return np.array(poses[:n], dtype=float)


def initializers(s: float, n: int, rng: np.random.Generator) -> list[tuple[str, np.ndarray]]:
    """A menu of seeds for multi-start search."""
    seeds: list[tuple[str, np.ndarray]] = []
    if n >= 4:
        seeds.append(("trivial_grid", trivial_grid(s=min(s, 2.0) if s <= 2.0 else s, n=n)))
        seeds.append(("corners", corner_squares(s, n)))
        seeds.append(("midpoints", midpoint_squares(s, n)))
        seeds.append(("rotated_corners", rotated_corners_plus_center(s, n)))
        seeds.append(("rotated_corners_steep", rotated_corners_plus_center(s, n, theta=math.pi / 5)))
        seeds.append(("rotated_corner_mid", rotated_corner_midpoint(s, n)))
        seeds.append(("type_i", type_i_bent_strip(s, n, block=2)))
        seeds.append(("corners_jitter", jitter(corner_squares(s, n), rng)))
        seeds.append(("rotated_jitter", jitter(rotated_corners_plus_center(s, n), rng)))
        seeds.append(("mid_jitter", jitter(midpoint_squares(s, n), rng)))
    if n == 3:
        seeds.append(("dudeney", dudeney_three(s if abs(s - S3_DUDENEY) < 0.2 else S3_DUDENEY)))
    if n == 7:
        seeds.append(("green7", green7_type_i(s)))
        seeds.append(("green7_at_s", type_i_bent_strip(s, 7, block=2)))
        seeds.append(("n7_midpoints", midpoint_squares(s, 7)))
    seeds.append(("random", random_poses(s, n, rng)))
    seeds.append(("random2", random_poses(s, n, rng)))
    return seeds
