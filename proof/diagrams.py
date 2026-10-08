"""Figures for PROOF_ATTEMPT.md (combinatorial geometry, not coverings)."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle


def _save(fig, path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".png"), dpi=140, bbox_inches="tight")
    plt.close(fig)
    return path


def important_points(path: Path) -> Path:
    a = 2.2
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    ax.add_patch(Rectangle((0, 0), a, a, fill=False, lw=2, color="black"))
    verts = {
        "v1": (0, 0),
        "v2": (a, 0),
        "v3": (a, a),
        "v4": (0, a),
    }
    mids = {
        "m1": (a / 2, 0),
        "m2": (a, a / 2),
        "m3": (a / 2, a),
        "m4": (0, a / 2),
    }
    c = (a / 2, a / 2)
    for name, p in verts.items():
        ax.plot(*p, "o", color="#E45756", ms=9, zorder=5)
        ax.annotate(name, p, textcoords="offset points", xytext=(6, 6), fontsize=11)
    for name, p in mids.items():
        ax.plot(*p, "s", color="#4C78A8", ms=8, zorder=5)
        offset = {
            "m1": (0, -16),
            "m2": (8, 0),
            "m3": (0, 8),
            "m4": (-22, 0),
        }[name]
        ax.annotate(name, p, textcoords="offset points", xytext=offset, fontsize=11)
    ax.plot(*c, "D", color="#54A24B", ms=8, zorder=5)
    ax.annotate("c", c, textcoords="offset points", xytext=(8, 4), fontsize=12)
    # inner cross
    ax.plot([0, a], [a / 2, a / 2], color="#54A24B", ls=":", lw=1)
    ax.plot([a / 2, a / 2], [0, a], color="#54A24B", ls=":", lw=1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-0.35, a + 0.45)
    ax.set_ylim(-0.4, a + 0.4)
    ax.set_title("Important points on a square of side $a>2$")
    return _save(fig, path)


def type_k4_chiral(path: Path) -> Path:
    a = 2.2
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.6))
    for ax, title, cw in zip(axes, ["clockwise matching", "counterclockwise matching"], [True, False]):
        ax.add_patch(Rectangle((0, 0), a, a, fill=False, lw=2, color="black"))
        verts = [(0, 0), (a, 0), (a, a), (0, a)]
        mids = [(a / 2, 0), (a, a / 2), (a / 2, a), (0, a / 2)]
        labels_v = ["v1", "v2", "v3", "v4"]
        labels_m = ["m1", "m2", "m3", "m4"]
        for p, lab in zip(verts, labels_v):
            ax.plot(*p, "o", color="#E45756", ms=8)
            ax.annotate(lab, p, textcoords="offset points", xytext=(4, 4), fontsize=9)
        for p, lab in zip(mids, labels_m):
            ax.plot(*p, "s", color="#4C78A8", ms=7)
        pairs = (
            [(0, 0, a / 2, 0), (a, 0, a, a / 2), (a, a, a / 2, a), (0, a, 0, a / 2)]
            if cw
            else [(0, 0, 0, a / 2), (a, 0, a / 2, 0), (a, a, a, a / 2), (0, a, a / 2, a)]
        )
        for x0, y0, x1, y1 in pairs:
            ax.annotate(
                "",
                xy=(x1, y1),
                xytext=(x0, y0),
                arrowprops=dict(arrowstyle="->", color="#F58518", lw=2),
            )
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-0.3, a + 0.35)
        ax.set_ylim(-0.3, a + 0.35)
        ax.set_title(title)
    fig.suptitle("Type $k=4$: the only two vertex–midpoint matchings", y=0.02)
    fig.tight_layout()
    return _save(fig, path)


def case2_quadrant(path: Path) -> Path:
    lam = 1.12
    a = 2 * lam
    fig, ax = plt.subplots(figsize=(6.0, 6.0))
    ax.add_patch(Rectangle((0, 0), a, a, fill=False, lw=2, color="black"))
    # quadrant R = [0,λ]×[λ,2λ]
    ax.add_patch(
        Rectangle((0, lam), lam, lam, facecolor="#4C78A8", alpha=0.18, edgecolor="#4C78A8", lw=2)
    )
    ax.annotate("R", (lam / 2, lam + lam / 2), ha="center", va="center", fontsize=14, color="#4C78A8")
    # F-sliver near c, from m1
    import math

    sliver = Polygon(
        [
            (lam - math.sqrt(max(2 - lam * lam, 0)), lam),
            (lam, lam),
            (lam, min(a, math.sqrt(2))),
            (lam - 0.15, min(a, math.sqrt(2))),
        ],
        closed=True,
        facecolor="#E45756",
        alpha=0.35,
        edgecolor="#E45756",
        lw=1,
        label="diameter-feasible $F\\cap R$",
    )
    ax.add_patch(sliver)
    # labels
    pts = {
        "v1": (0, 0),
        "v2": (a, 0),
        "v3": (a, a),
        "v4": (0, a),
        "m1": (lam, 0),
        "m2": (a, lam),
        "m3": (lam, a),
        "m4": (0, lam),
        "c": (lam, lam),
    }
    for name, p in pts.items():
        ax.plot(*p, "o", color="black", ms=5)
        ax.annotate(name, p, textcoords="offset points", xytext=(5, 5), fontsize=10)
    ax.annotate(
        "E contains $[c,m_4]$\n(bottom of $R$)",
        (lam / 2, lam),
        textcoords="offset points",
        xytext=(8, -28),
        fontsize=9,
        color="#54A24B",
    )
    ax.annotate(
        "$S_4$ contains $[v_4,m_3]$\n(top of $R$)",
        (lam / 2, a),
        textcoords="offset points",
        xytext=(8, 8),
        fontsize=9,
        color="#F58518",
    )
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-0.35, a + 0.55)
    ax.set_ylim(-0.45, a + 0.55)
    ax.set_title(
        "Case-2 quadrant $R$ and the diameter sliver of $F$ (near $c$)\n"
        f"illustrated at $\\lambda={lam}$  (not a covering)"
    )
    return _save(fig, path)


def write_all(out_dir: Path) -> list[Path]:
    out_dir = Path(out_dir)
    return [
        important_points(out_dir / "important_points"),
        type_k4_chiral(out_dir / "type_k4_chiral"),
        case2_quadrant(out_dir / "case2_quadrant"),
    ]
