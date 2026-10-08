"""Full experiment suite used to populate artifacts/ and RESULTS.md."""

from __future__ import annotations

import json
import time
from pathlib import Path

from cover6.configs import (
    S3_DUDENEY,
    S7_GREEN,
    corner_squares,
    dudeney_three,
    green7_type_i,
    trivial_grid,
)
from cover6.coverage import evaluate_covering
from cover6.io_util import covering_to_dict, save_covering, save_json
from cover6.optimize import (
    SearchLog,
    Trial,
    best_trial,
    grow_from_trivial,
    local_refine,
    search_at_s,
)
from cover6.visualize import plot_covering


def _save_trial(out: Path, name: str, s: float, poses: np.ndarray, extra: dict) -> dict:
    report = evaluate_covering(s, poses)
    payload = save_covering(out / f"{name}.json", s, poses, extra=extra)
    plot_covering(
        s,
        poses,
        out / name,
        title=(
            f"{name}  n={poses.shape[0]}  s={s:.6f}  "
            f"uncovered={report.uncovered_area:.3e}  covered={report.covered}"
        ),
    )
    return payload


def run_experiment(out: Path, *, budget: str = "default", seed: int = 0) -> int:
    t0 = time.time()
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    summary: dict = {
        "seed": seed,
        "budget": budget,
        "checks": {},
        "searches": {},
    }

    # ------------------------------------------------------------------
    # 1. Baseline: trivial s=2 with n=6
    # ------------------------------------------------------------------
    base_dir = out / "baseline"
    poses2 = trivial_grid(s=2.0, n=6)
    summary["checks"]["baseline_n6_s2"] = _save_trial(
        base_dir,
        "n6_s2_trivial",
        2.0,
        poses2,
        extra={"construction": "trivial_2x2_plus_two_extras"},
    )["coverage"]

    # Negative control: same 2x2 block on a slightly larger square.
    poses_gap = trivial_grid(s=2.05, n=6)
    summary["checks"]["trivial_n6_s2p05_should_fail"] = _save_trial(
        base_dir,
        "n6_s2p05_trivial_gap",
        2.05,
        poses_gap,
        extra={"construction": "2x2_block_on_larger_square", "expect_covered": False},
    )["coverage"]

    # n=4 at s=2 must work; at s=2.02 must fail.
    summary["checks"]["baseline_n4_s2"] = _save_trial(
        base_dir,
        "n4_s2_trivial",
        2.0,
        trivial_grid(s=2.0, n=4),
        extra={"construction": "trivial_2x2"},
    )["coverage"]
    summary["checks"]["n4_s2p02_should_fail"] = evaluate_covering(
        2.02, trivial_grid(s=2.02, n=4)
    ).to_dict()

    # ------------------------------------------------------------------
    # 2. Known n=3 covering S(3)=sqrt(phi)
    # ------------------------------------------------------------------
    known_dir = out / "known"
    d_poses = dudeney_three()
    d_poses, _ = local_refine(S3_DUDENEY, d_poses, n_grid=80, maxiter=250, use_shapely=True)
    d_report = evaluate_covering(S3_DUDENEY, d_poses)
    if not d_report.covered:
        # Fall back to a short search at the known optimum side length.
        log3 = SearchLog(n=3, s_targets=[S3_DUDENEY])
        search_at_s(S3_DUDENEY, 3, seed=seed, budget="tiny", log=log3)
        bt = best_trial(log3.trials)
        d_poses = bt.poses
        d_report = evaluate_covering(S3_DUDENEY, d_poses)
    summary["checks"]["dudeney_n3"] = _save_trial(
        known_dir,
        "n3_dudeney",
        S3_DUDENEY,
        d_poses,
        extra={"construction": "dudeney", "theory_s": S3_DUDENEY},
    )["coverage"]

    # ------------------------------------------------------------------
    # 3. n=7 Type-I seed polished at the published Green side length
    # ------------------------------------------------------------------
    g_poses = green7_type_i()
    g_poses, _ = local_refine(S7_GREEN, g_poses, n_grid=72, maxiter=250)
    g_poses, _ = local_refine(S7_GREEN, g_poses, n_grid=72, maxiter=80, use_shapely=True)
    summary["checks"]["green7_seed"] = _save_trial(
        known_dir,
        "n7_green_seed",
        S7_GREEN,
        g_poses,
        extra={
            "construction": "type_i_seed_for_green",
            "theory_s": S7_GREEN,
            "theory_area": S7_GREEN**2,
        },
    )["coverage"]

    # ------------------------------------------------------------------
    # 4. Adiabatic growth from the n=6 trivial covering
    # ------------------------------------------------------------------
    grow_dir = out / "search_n6"
    grow_trials = grow_from_trivial(6, s_start=2.0, s_stop=2.12, ds=0.01, seed=seed)
    grow_payload = [
        {"s": t.s, "uncovered_area": t.uncovered_area, "covered": t.covered, "method": t.method}
        for t in grow_trials
    ]
    save_json(grow_dir / "grow.json", {"trials": grow_payload})
    last = grow_trials[-1]
    _save_trial(
        grow_dir,
        "grow_last",
        last.s,
        last.poses,
        extra={"construction": "adiabatic_growth", "covered": last.covered},
    )
    max_grow_covered = max((t.s for t in grow_trials if t.covered), default=None)
    summary["searches"]["n6_grow"] = {
        "max_covered_s": max_grow_covered,
        "last_s": last.s,
        "last_uncovered_area": last.uncovered_area,
        "last_covered": last.covered,
        "n_steps": len(grow_trials),
    }

    # ------------------------------------------------------------------
    # 5. n=6 multi-start at several s > 2
    # ------------------------------------------------------------------
    n6_log = SearchLog(n=6, s_targets=[])
    n6_targets = [2.0, 2.02, 2.05, 2.10]
    for s in n6_targets:
        n6_log.s_targets.append(s)
        search_at_s(s, 6, seed=seed, budget=budget, log=n6_log)
    n6_best = best_trial(n6_log.trials)
    n6_best_report = evaluate_covering(n6_best.s, n6_best.poses)
    covered6 = [t for t in n6_log.trials if t.covered]
    best_covered6 = max((t.s for t in covered6), default=None)
    n6_summary = {
        "n": 6,
        "s_targets": n6_targets,
        "n_trials": len(n6_log.trials),
        "best_covered_s": best_covered6,
        "any_s_gt_2_covered": bool(best_covered6 is not None and best_covered6 > 2.0 + 1e-12),
        "best_trial": covering_to_dict(
            n6_best.s,
            n6_best.poses,
            report=n6_best_report,
            extra={"method": n6_best.method, "seed": n6_best.seed},
        ),
        "trials": [
            {
                "method": t.method,
                "s": t.s,
                "uncovered_area": t.uncovered_area,
                "covered": t.covered,
                "notes": t.notes,
            }
            for t in sorted(n6_log.trials, key=lambda t: (-int(t.covered), -t.s, t.uncovered_area or 1e9))
        ],
    }
    save_json(grow_dir / "search_log.json", n6_summary)
    save_json(grow_dir / "best.json", n6_summary["best_trial"])
    plot_covering(
        n6_best.s,
        n6_best.poses,
        grow_dir / "best",
        title=(
            f"n=6 best trial  s={n6_best.s:.6f}  "
            f"uncovered={n6_best_report.uncovered_area:.3e}  covered={n6_best_report.covered}"
        ),
    )
    if covered6:
        bc = max(covered6, key=lambda t: t.s)
        _save_trial(
            grow_dir,
            "best_covered",
            bc.s,
            bc.poses,
            extra={"method": bc.method, "seed": bc.seed},
        )
    # Representative hole at s=2.05 (best uncovered among those trials).
    t205 = [t for t in n6_log.trials if abs(t.s - 2.05) < 1e-12]
    if t205:
        hole = min(t205, key=lambda t: t.uncovered_area or 1e9)
        _save_trial(
            grow_dir,
            "best_at_s2p05",
            hole.s,
            hole.poses,
            extra={"method": hole.method, "expect_s_gt_2": True},
        )
    summary["searches"]["n6"] = {
        "best_covered_s": best_covered6,
        "any_s_gt_2_covered": n6_summary["any_s_gt_2_covered"],
        "n_trials": n6_summary["n_trials"],
        "best_trial_s": n6_best.s,
        "best_trial_uncovered_area": n6_best_report.uncovered_area,
        "best_trial_covered": n6_best_report.covered,
        "min_uncovered_by_s": {
            str(s): min(
                (t.uncovered_area for t in n6_log.trials if abs(t.s - s) < 1e-12 and t.uncovered_area is not None),
                default=None,
            )
            for s in n6_targets
        },
    }

    # ------------------------------------------------------------------
    # 6. n=7 positive control: can the same pipeline find s>2?
    # ------------------------------------------------------------------
    n7_dir = out / "search_n7"
    n7_log = SearchLog(n=7, s_targets=[])
    n7_targets = [2.0, 2.05, 2.10]
    for s in n7_targets:
        n7_log.s_targets.append(s)
        search_at_s(s, 7, seed=seed, budget=budget, log=n7_log)
    # Also polish the Green seed at a few s values near 2.10.
    for s in (2.05, 2.10, 2.15):
        p = green7_type_i(s)
        p, _ = local_refine(s, p, n_grid=64, maxiter=220)
        p, _ = local_refine(s, p, n_grid=64, maxiter=80, use_shapely=True)
        report = evaluate_covering(s, p)
        n7_log.trials.append(
            Trial(
                method="green_seed_polish",
                seed=seed,
                s=s,
                n=7,
                loss=report.uncovered_area,
                poses=p,
                uncovered_area=report.uncovered_area,
                covered=report.covered,
                notes=report.notes,
            )
        )
        n7_log.s_targets.append(s)

    n7_best = best_trial(n7_log.trials)
    n7_best_report = evaluate_covering(n7_best.s, n7_best.poses)
    covered7 = [t for t in n7_log.trials if t.covered]
    best_covered7 = max((t.s for t in covered7), default=None)
    n7_summary = {
        "n": 7,
        "s_targets": n7_targets,
        "n_trials": len(n7_log.trials),
        "best_covered_s": best_covered7,
        "any_s_gt_2_covered": bool(best_covered7 is not None and best_covered7 > 2.0 + 1e-12),
        "best_trial": covering_to_dict(
            n7_best.s,
            n7_best.poses,
            report=n7_best_report,
            extra={"method": n7_best.method, "seed": n7_best.seed},
        ),
        "trials": [
            {
                "method": t.method,
                "s": t.s,
                "uncovered_area": t.uncovered_area,
                "covered": t.covered,
                "notes": t.notes,
            }
            for t in sorted(n7_log.trials, key=lambda t: (-int(t.covered), -t.s, t.uncovered_area or 1e9))
        ],
    }
    save_json(n7_dir / "search_log.json", n7_summary)
    save_json(n7_dir / "best.json", n7_summary["best_trial"])
    plot_covering(
        n7_best.s,
        n7_best.poses,
        n7_dir / "best",
        title=(
            f"n=7 best trial  s={n7_best.s:.6f}  "
            f"uncovered={n7_best_report.uncovered_area:.3e}  covered={n7_best_report.covered}"
        ),
    )
    if covered7:
        bc = max(covered7, key=lambda t: t.s)
        _save_trial(
            n7_dir,
            "best_covered",
            bc.s,
            bc.poses,
            extra={"method": bc.method, "seed": bc.seed},
        )
    summary["searches"]["n7"] = {
        "best_covered_s": best_covered7,
        "any_s_gt_2_covered": n7_summary["any_s_gt_2_covered"],
        "n_trials": n7_summary["n_trials"],
        "best_trial_s": n7_best.s,
        "best_trial_uncovered_area": n7_best_report.uncovered_area,
        "best_trial_covered": n7_best_report.covered,
        "published_green_s": S7_GREEN,
    }

    # Corner-only picture at s=2.05 for illustration of the plus-shaped hole.
    plus = corner_squares(2.05, 6, inset=0.5)
    summary["checks"]["corners_n6_s2p05"] = _save_trial(
        grow_dir,
        "corners_s2p05_plus_hole",
        2.05,
        plus,
        extra={"construction": "four_corners_plus_center_on_s_gt_2"},
    )["coverage"]

    summary["elapsed_sec"] = time.time() - t0
    save_json(out / "experiment_summary.json", summary)
    print(json.dumps(
        {
            "elapsed_sec": summary["elapsed_sec"],
            "baseline_covered": summary["checks"]["baseline_n6_s2"]["covered"],
            "n6_best_covered_s": summary["searches"]["n6"]["best_covered_s"],
            "n6_any_s_gt_2": summary["searches"]["n6"]["any_s_gt_2_covered"],
            "n7_best_covered_s": summary["searches"]["n7"]["best_covered_s"],
            "n7_any_s_gt_2": summary["searches"]["n7"]["any_s_gt_2_covered"],
            "dudeney_covered": summary["checks"]["dudeney_n3"]["covered"],
        },
        indent=2,
    ))
    return 0 if summary["checks"]["baseline_n6_s2"]["covered"] else 1
