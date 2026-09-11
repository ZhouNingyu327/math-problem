"""Command-line entry: python -m cover6 <command>."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACTS = ROOT / "artifacts"


def _cmd_baseline(args: argparse.Namespace) -> int:
    from cover6.configs import trivial_grid
    from cover6.coverage import evaluate_covering
    from cover6.io_util import save_covering
    from cover6.visualize import plot_covering

    out = Path(args.out)
    n = args.n
    s = args.s
    poses = trivial_grid(s=s, n=n)
    report = evaluate_covering(s, poses)
    payload = save_covering(
        out / "baseline.json",
        s,
        poses,
        extra={"construction": "trivial_2x2_plus_extras", "command": "baseline"},
    )
    plot_covering(
        s,
        poses,
        out / "baseline",
        title=f"Trivial covering  n={n}  s={s}  uncovered={report.uncovered_area:.2e}",
    )
    print(json.dumps(payload["coverage"], indent=2))
    if s <= 2.0 + 1e-12 and n >= 4:
        return 0 if report.covered else 1
    return 0


def _cmd_verify(args: argparse.Namespace) -> int:
    from cover6.coverage import evaluate_covering
    from cover6.io_util import load_json, poses_from_dict

    data = load_json(args.path)
    s, poses = poses_from_dict(data)
    report = evaluate_covering(s, poses)
    print(json.dumps(report.to_dict(), indent=2))
    return 0 if report.covered else 1


def _cmd_plot(args: argparse.Namespace) -> int:
    from cover6.io_util import load_json, poses_from_dict
    from cover6.visualize import plot_covering

    data = load_json(args.path)
    s, poses = poses_from_dict(data)
    title = args.title or f"n={data.get('n')}  s={s}"
    paths = plot_covering(s, poses, args.out, title=title)
    for p in paths:
        print(p)
    return 0


def _cmd_search(args: argparse.Namespace) -> int:
    from cover6.coverage import evaluate_covering
    from cover6.io_util import covering_to_dict, save_json
    from cover6.optimize import SearchLog, best_trial, binary_search_s, grow_from_trivial, search_at_s
    from cover6.visualize import plot_covering

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    n = args.n
    seed = args.seed
    budget = args.budget
    log = SearchLog(n=n, s_targets=[])

    grow_trials = []
    if n >= 4:
        grow_trials = grow_from_trivial(n, s_start=2.0, s_stop=args.s_hi, ds=0.01, seed=seed)
        log.trials.extend(grow_trials)

    if args.binary:
        binary_search_s(
            n,
            s_lo=args.s_lo,
            s_hi=args.s_hi,
            steps=args.steps,
            seed=seed,
            budget=budget,
            log=log,
        )
    else:
        for s in args.s_list:
            log.s_targets.append(s)
            search_at_s(s, n, seed=seed, budget=budget, log=log)

    best = best_trial(log.trials)
    best_report = evaluate_covering(best.s, best.poses)
    covered_trials = [t for t in log.trials if t.covered]
    best_covered_s = max((t.s for t in covered_trials), default=None)

    summary = {
        "n": n,
        "seed": seed,
        "budget": budget,
        "s_targets": log.s_targets,
        "n_trials": len(log.trials),
        "best_covered_s": best_covered_s,
        "best_trial": covering_to_dict(
            best.s,
            best.poses,
            report=best_report,
            extra={"method": best.method, "seed": best.seed, "loss": best.loss},
        ),
        "trials": [
            {
                "method": t.method,
                "s": t.s,
                "loss": t.loss,
                "uncovered_area": t.uncovered_area,
                "covered": t.covered,
                "notes": t.notes,
            }
            for t in sorted(log.trials, key=lambda t: (-t.s, t.uncovered_area or 1e9))
        ],
        "grow": [
            {"s": t.s, "uncovered_area": t.uncovered_area, "covered": t.covered}
            for t in grow_trials
        ],
    }
    save_json(out / "search_log.json", summary)
    save_json(out / "best.json", summary["best_trial"])
    plot_covering(
        best.s,
        best.poses,
        out / "best",
        title=(
            f"n={n}  s={best.s:.6f}  uncovered={best_report.uncovered_area:.3e}"
            f"  covered={best_report.covered}"
        ),
    )
    # Also dump the best strictly-covered trial if it differs.
    if covered_trials:
        bc = max(covered_trials, key=lambda t: t.s)
        bc_report = evaluate_covering(bc.s, bc.poses)
        save_json(
            out / "best_covered.json",
            covering_to_dict(
                bc.s,
                bc.poses,
                report=bc_report,
                extra={"method": bc.method, "seed": bc.seed},
            ),
        )
        plot_covering(
            bc.s,
            bc.poses,
            out / "best_covered",
            title=f"n={n}  best covered s={bc.s:.6f}",
        )
    print(
        json.dumps(
            {
                "n": n,
                "best_covered_s": best_covered_s,
                "best_trial_s": best.s,
                "best_trial_uncovered_area": best_report.uncovered_area,
                "best_trial_covered": best_report.covered,
                "n_trials": len(log.trials),
            },
            indent=2,
        )
    )
    return 0


def _cmd_experiment(args: argparse.Namespace) -> int:
    from cover6.experiment import run_experiment

    return run_experiment(Path(args.out), budget=args.budget, seed=args.seed)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="cover6",
        description="Numerical search for S(6): largest square coverable by 6 unit squares.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("baseline", help="Verify the trivial s=2 covering.")
    b.add_argument("--n", type=int, default=6)
    b.add_argument("--s", type=float, default=2.0)
    b.add_argument("--out", type=Path, default=DEFAULT_ARTIFACTS / "baseline")
    b.set_defaults(func=_cmd_baseline)

    v = sub.add_parser("verify", help="Re-evaluate a saved JSON covering.")
    v.add_argument("path", type=Path)
    v.set_defaults(func=_cmd_verify)

    pl = sub.add_parser("plot", help="Render a saved JSON covering.")
    pl.add_argument("path", type=Path)
    pl.add_argument("--out", type=Path, required=True)
    pl.add_argument("--title", type=str, default=None)
    pl.set_defaults(func=_cmd_plot)

    s = sub.add_parser("search", help="Numerical search at one or several s values.")
    s.add_argument("--n", type=int, default=6)
    s.add_argument("--seed", type=int, default=0)
    s.add_argument("--budget", choices=["tiny", "default", "serious"], default="default")
    s.add_argument("--out", type=Path, default=DEFAULT_ARTIFACTS / "search_n6")
    s.add_argument("--s-lo", type=float, default=2.0)
    s.add_argument("--s-hi", type=float, default=2.15)
    s.add_argument("--steps", type=int, default=4)
    s.add_argument("--binary", action="store_true")
    s.add_argument(
        "--s-list",
        type=float,
        nargs="+",
        default=[2.0, 2.02, 2.05, 2.10],
    )
    s.set_defaults(func=_cmd_search)

    e = sub.add_parser("experiment", help="Run the full paper-oriented experiment suite.")
    e.add_argument("--out", type=Path, default=DEFAULT_ARTIFACTS)
    e.add_argument("--budget", choices=["tiny", "default", "serious"], default="default")
    e.add_argument("--seed", type=int, default=0)
    e.set_defaults(func=_cmd_experiment)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
