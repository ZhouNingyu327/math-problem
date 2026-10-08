"""SVG/PNG figures of a covering."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from cover6.coverage import uncovered_region
from cover6.geometry import unit_square_vertices

COLORS = [
    "#4C78A8",
    "#F58518",
    "#E45756",
    "#72B7B2",
    "#54A24B",
    "#EECA3B",
    "#B279A2",
    "#FF9DA6",
]


def plot_covering(
    s: float,
    poses: np.ndarray,
    path: Path | str,
    *,
    title: str | None = None,
    show_uncovered: bool = True,
) -> list[Path]:
    """Save PNG and SVG next to ``path`` (extension is ignored / replaced)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon as MplPolygon
    from matplotlib.patches import Rectangle
    from shapely.geometry import GeometryCollection, MultiPolygon, Polygon

    poses = np.asarray(poses, dtype=float).reshape(-1, 3)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    stem = path.with_suffix("")

    fig, ax = plt.subplots(figsize=(6.2, 6.2))
    pad = 0.75
    ax.set_xlim(-pad, s + pad)
    ax.set_ylim(-pad, s + pad)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    if title:
        ax.set_title(title)

    target = Rectangle(
        (0.0, 0.0),
        s,
        s,
        fill=False,
        edgecolor="black",
        linewidth=2.0,
        zorder=5,
        label="target",
    )
    ax.add_patch(target)

    for i, (cx, cy, theta) in enumerate(poses):
        verts = unit_square_vertices(cx, cy, theta)
        color = COLORS[i % len(COLORS)]
        patch = MplPolygon(
            verts,
            closed=True,
            facecolor=color,
            edgecolor=color,
            linewidth=1.2,
            alpha=0.38,
            zorder=2,
            label=f"sq{i+1}",
        )
        ax.add_patch(patch)
        ax.plot([cx], [cy], marker="+", color=color, markersize=8, zorder=4)

    if show_uncovered:
        region = uncovered_region(s, poses)
        geoms: list[Polygon] = []
        if region.is_empty:
            geoms = []
        elif isinstance(region, Polygon):
            geoms = [region]
        elif isinstance(region, MultiPolygon):
            geoms = list(region.geoms)
        elif isinstance(region, GeometryCollection):
            geoms = [g for g in region.geoms if isinstance(g, Polygon)]
        else:
            geoms = [region] if hasattr(region, "exterior") else []
        for g in geoms:
            if g.is_empty or g.area <= 0:
                continue
            xs, ys = g.exterior.xy
            ax.fill(xs, ys, facecolor="#d62728", edgecolor="#7f0000", alpha=0.85, zorder=3, label="uncovered")
            for hole in g.interiors:
                hx, hy = hole.xy
                ax.fill(hx, hy, facecolor="white", edgecolor="#7f0000", alpha=0.9, zorder=3)

    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=False, fontsize=8)
    fig.tight_layout()
    png = Path(str(stem) + ".png")
    svg = Path(str(stem) + ".svg")
    fig.savefig(png, dpi=160, bbox_inches="tight")
    fig.savefig(svg, bbox_inches="tight")
    plt.close(fig)
    return [png, svg]
