"""Multi-start and differential-evolution search for coverings."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from scipy.optimize import dual_annealing, minimize

from cover6.configs import (
    c4_from_vector,
    c4_initial_vector,
    c4_vector_bounds,
    initializers,
    jitter,
)
from cover6.coverage import evaluate_covering, sampling_loss, shapely_loss
from cover6.geometry import pose_bounds, poses_from_vector, vector_from_poses, wrap_theta


@dataclass
class Trial:
    method: str
    seed: int
    s: float
    n: int
    loss: float
    poses: np.ndarray
    uncovered_area: float | None = None
    covered: bool = False
    notes: str = ""


@dataclass
class SearchLog:
    n: int
    s_targets: list[float]
    trials: list[Trial] = field(default_factory=list)
    best_covered_s: float | None = None
    best_covered_poses: np.ndarray | None = None
    best_attempt_s: float | None = None
    best_attempt_poses: np.ndarray | None = None
    best_attempt_area: float | None = None


def _clip_poses(poses: np.ndarray, s: float, n: int) -> np.ndarray:
    bounds = pose_bounds(s, n)
    x = vector_from_poses(poses).copy()
    for i, (lo, hi) in enumerate(bounds):
        x[i] = min(max(x[i], lo), hi)
    out = poses_from_vector(x, n)
    out[:, 2] = wrap_theta(out[:, 2])
    return out


def local_refine(
    s: float,
    poses: np.ndarray,
    *,
    n_grid: int = 64,
    maxiter: int = 250,
    use_shapely: bool = False,
) -> tuple[np.ndarray, float]:
    n = int(np.asarray(poses).reshape(-1, 3).shape[0])
    x0 = vector_from_poses(poses)
    bounds = pose_bounds(s, n)

    def fun(x: np.ndarray) -> float:
        p = poses_from_vector(x, n)
        if use_shapely:
            return shapely_loss(s, p)
        return sampling_loss(s, p, n_grid=n_grid)

    res = minimize(
        fun,
        x0,
        method="L-BFGS-B",
        bounds=bounds,
        options={"maxiter": maxiter, "ftol": 1e-12},
    )
    poses_out = _clip_poses(poses_from_vector(res.x, n), s, n)
    return poses_out, float(fun(vector_from_poses(poses_out)))


def _de_objective_factory(
    s: float, n: int, n_grid: int, decoder: Callable[[np.ndarray], np.ndarray]
) -> Callable[[np.ndarray], float]:
    def fun(x: np.ndarray) -> float:
        return sampling_loss(s, decoder(x), n_grid=n_grid)

    return fun


def differential_evolution_search(
    s: float,
    n: int,
    *,
    seed: int,
    maxiter: int = 80,
    popsize: int = 10,
    n_grid: int = 48,
    decoder: Callable[[np.ndarray], np.ndarray] | None = None,
    bounds: list[tuple[float, float]] | None = None,
    init: np.ndarray | None = None,
) -> tuple[np.ndarray, float]:
    """A compact DE-style search implemented with scipy dual_annealing + polish.

    Dual annealing is more reliable than a short DE run on this non-smooth
    covering loss, and does not require pickling worker functions.
    """
    rng = np.random.default_rng(seed)
    if decoder is None:
        decoder = lambda x: poses_from_vector(x, n)
    if bounds is None:
        bounds = pose_bounds(s, n)
    fun = _de_objective_factory(s, n, n_grid, decoder)
    x0 = init
    if x0 is None:
        x0 = np.array([(lo + hi) / 2.0 for lo, hi in bounds], dtype=float)
        x0 = x0 + rng.normal(0.0, 0.15, size=x0.shape)

    # Dual annealing uses bounds as a list of (low, high).
    res = dual_annealing(
        fun,
        bounds=bounds,
        maxiter=maxiter,
        seed=seed,
        x0=np.clip(x0, [b[0] for b in bounds], [b[1] for b in bounds]),
        no_local_search=False,
    )
    poses = decoder(res.x)
    poses = _clip_poses(poses, s, n)
    poses, loss = local_refine(s, poses, n_grid=max(n_grid, 64), maxiter=200)
    return poses, loss


def try_seed(
    s: float,
    poses: np.ndarray,
    *,
    method: str,
    seed: int,
    n_grid: int = 56,
    polish_shapely: bool = True,
) -> Trial:
    n = int(np.asarray(poses).reshape(-1, 3).shape[0])
    poses = _clip_poses(poses, s, n)
    poses, loss = local_refine(s, poses, n_grid=n_grid, maxiter=180)
    if polish_shapely:
        poses, loss = local_refine(
            s, poses, n_grid=n_grid, maxiter=80, use_shapely=True
        )
    report = evaluate_covering(s, poses)
    return Trial(
        method=method,
        seed=seed,
        s=s,
        n=n,
        loss=loss,
        poses=poses,
        uncovered_area=report.uncovered_area,
        covered=report.covered,
        notes=report.notes,
    )


def search_at_s(
    s: float,
    n: int,
    *,
    seed: int = 0,
    budget: str = "default",
    log: SearchLog | None = None,
) -> list[Trial]:
    """Multi-start search for a covering of a side-s square by n unit squares."""
    rng = np.random.default_rng(seed)
    budgets = {
        "tiny": dict(n_random=2, de=1, de_iter=15, n_grid=36, anneal=False),
        "default": dict(n_random=6, de=3, de_iter=40, n_grid=48, anneal=True),
        "serious": dict(n_random=10, de=5, de_iter=70, n_grid=56, anneal=True),
    }
    cfg = budgets.get(budget, budgets["default"])
    trials: list[Trial] = []

    seeds = initializers(s, n, rng)
    # Always try the structured seeds first (local polish only).
    for name, poses in seeds:
        trial = try_seed(
            s, poses, method=f"local:{name}", seed=seed, n_grid=cfg["n_grid"]
        )
        trials.append(trial)

    for i in range(cfg["n_random"]):
        poses = jitter(seeds[0][1], rng, pos=0.25, ang=0.4)
        trial = try_seed(
            s,
            poses,
            method=f"local:jitter{i}",
            seed=seed + 17 * (i + 1),
            n_grid=cfg["n_grid"],
        )
        trials.append(trial)

    if cfg["anneal"]:
        for i in range(cfg["de"]):
            poses, loss = differential_evolution_search(
                s,
                n,
                seed=seed + 1000 + i,
                maxiter=cfg["de_iter"],
                n_grid=cfg["n_grid"],
            )
            report = evaluate_covering(s, poses)
            trials.append(
                Trial(
                    method=f"anneal:{i}",
                    seed=seed + 1000 + i,
                    s=s,
                    n=n,
                    loss=loss,
                    poses=poses,
                    uncovered_area=report.uncovered_area,
                    covered=report.covered,
                    notes=report.notes,
                )
            )
            # Reduced C4 parameterization.
            if n >= 5:
                bounds = c4_vector_bounds(s, n)
                init = c4_initial_vector(s, n, rng)
                poses_c4, loss_c4 = differential_evolution_search(
                    s,
                    n,
                    seed=seed + 2000 + i,
                    maxiter=cfg["de_iter"],
                    n_grid=cfg["n_grid"],
                    decoder=lambda x, ss=s, nn=n: c4_from_vector(x, ss, nn),
                    bounds=bounds,
                    init=init,
                )
                report_c4 = evaluate_covering(s, poses_c4)
                trials.append(
                    Trial(
                        method=f"anneal_c4:{i}",
                        seed=seed + 2000 + i,
                        s=s,
                        n=n,
                        loss=loss_c4,
                        poses=poses_c4,
                        uncovered_area=report_c4.uncovered_area,
                        covered=report_c4.covered,
                        notes=report_c4.notes,
                    )
                )

    if log is not None:
        log.trials.extend(trials)
        _update_log_best(log, trials)
    return trials


def _update_log_best(log: SearchLog, trials: list[Trial]) -> None:
    for t in trials:
        if t.covered:
            if log.best_covered_s is None or t.s > log.best_covered_s + 1e-15:
                log.best_covered_s = t.s
                log.best_covered_poses = t.poses
        area = t.uncovered_area if t.uncovered_area is not None else np.inf
        if log.best_attempt_area is None or (
            t.s > (log.best_attempt_s or 0) + 1e-12 and area < 1e-6
        ):
            pass
        # Track the covering with largest s among near-covers, else smallest hole
        # at the largest attempted s that got close.
        if t.covered or (area < 1e-4):
            if log.best_attempt_s is None or t.s >= log.best_attempt_s - 1e-15:
                if t.s > (log.best_attempt_s or -1) + 1e-15 or area < (
                    log.best_attempt_area or np.inf
                ):
                    log.best_attempt_s = t.s
                    log.best_attempt_poses = t.poses
                    log.best_attempt_area = area


def binary_search_s(
    n: int,
    *,
    s_lo: float = 2.0,
    s_hi: float = 2.25,
    steps: int = 6,
    seed: int = 0,
    budget: str = "default",
    log: SearchLog | None = None,
) -> SearchLog:
    """Binary-search the largest s at which a covering appears to exist.

    This is a numerical probe, not a proof. Feasibility at a midpoint is
    declared only if ``evaluate_covering`` returns ``covered=True``.
    """
    if log is None:
        log = SearchLog(n=n, s_targets=[])
    # Always run the lower endpoint (expected feasible for n>=4 at s=2).
    for s in (s_lo,):
        log.s_targets.append(s)
        search_at_s(s, n, seed=seed, budget=budget, log=log)
    lo, hi = s_lo, s_hi
    for _ in range(steps):
        mid = 0.5 * (lo + hi)
        log.s_targets.append(mid)
        trials = search_at_s(mid, n, seed=seed, budget=budget, log=log)
        if any(t.covered for t in trials):
            lo = mid
        else:
            hi = mid
    # Probe a few explicit values above 2, useful even if binary search
    # already collapsed, so RESULTS.md can quote them.
    return log


def grow_from_trivial(
    n: int,
    *,
    s_start: float = 2.0,
    s_stop: float = 2.12,
    ds: float = 0.01,
    seed: int = 0,
) -> list[Trial]:
    """Adiabatic growth: start at the trivial covering and inch s upward."""
    from cover6.configs import trivial_grid

    poses = trivial_grid(s=2.0, n=n)
    trials: list[Trial] = []
    s = s_start
    while s <= s_stop + 1e-12:
        poses, loss = local_refine(s, poses, n_grid=72, maxiter=200)
        poses, loss = local_refine(s, poses, n_grid=72, maxiter=60, use_shapely=True)
        report = evaluate_covering(s, poses)
        trials.append(
            Trial(
                method="grow",
                seed=seed,
                s=s,
                n=n,
                loss=loss,
                poses=np.array(poses, copy=True),
                uncovered_area=report.uncovered_area,
                covered=report.covered,
                notes=report.notes,
            )
        )
        if not report.covered:
            break
        s = round(s + ds, 10)
    return trials


def best_trial(trials: list[Trial]) -> Trial:
    covered = [t for t in trials if t.covered]
    if covered:
        return max(covered, key=lambda t: t.s)
    return min(trials, key=lambda t: (t.uncovered_area if t.uncovered_area is not None else np.inf, -t.s))
