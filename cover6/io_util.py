"""JSON serialization of coverings and search logs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from cover6.coverage import CoverageReport, evaluate_covering
from cover6.geometry import wrap_theta


def covering_to_dict(
    s: float,
    poses: np.ndarray,
    *,
    report: CoverageReport | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    poses = np.asarray(poses, dtype=float).reshape(-1, 3)
    payload: dict[str, Any] = {
        "s": float(s),
        "n": int(poses.shape[0]),
        "area": float(s * s),
        "poses": [
            {
                "cx": float(cx),
                "cy": float(cy),
                "theta": float(wrap_theta(th)),
                "theta_deg": float(np.degrees(wrap_theta(th))),
            }
            for cx, cy, th in poses
        ],
    }
    if report is not None:
        payload["coverage"] = report.to_dict()
    if extra:
        payload.update(extra)
    return payload


def poses_from_dict(data: dict[str, Any]) -> tuple[float, np.ndarray]:
    s = float(data["s"])
    poses = np.array(
        [[p["cx"], p["cy"], p["theta"]] for p in data["poses"]],
        dtype=float,
    )
    return s, poses


def save_json(path: Path | str, data: dict[str, Any]) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path


def load_json(path: Path | str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_covering(
    path: Path | str,
    s: float,
    poses: np.ndarray,
    *,
    extra: dict[str, Any] | None = None,
    evaluate: bool = True,
) -> dict[str, Any]:
    report = evaluate_covering(s, poses) if evaluate else None
    payload = covering_to_dict(s, poses, report=report, extra=extra)
    save_json(path, payload)
    return payload
