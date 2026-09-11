"""Exhaustive combinatorial types for midpoint-to-square assignments.

Coordinates / labels follow Dósa–Lángi–Tuza:

    v1=(0,0), v2=(a,0), v3=(a,a), v4=(0,a)   (counterclockwise)
    m1 midpoint of [v1,v2]  (bottom)
    m2 midpoint of [v2,v3]  (right)
    m3 midpoint of [v3,v4]  (top)
    m4 midpoint of [v4,v1]  (left)
    c  centre

Squares: V1..V4 (the unique squares containing v1..v4) and extras E, F,
with the standing convention that c ∈ E.

A midpoint may only sit in a square that is geometrically allowed by the
diameter √2 (Lemma D in PROOF_ATTEMPT.md):

    m1 ∈ {V1, V2, E, F}
    m2 ∈ {V2, V3, E, F}
    m3 ∈ {V3, V4, E, F}
    m4 ∈ {V4, V1, E, F}

No square contains two midpoints. The script lists every injective
assignment, quotients by the D4 action that fixes E (the centre-square)
and records orbit representatives.

This is a complete *combinatorial* census. It does not by itself prove
that each type is geometrically unrealisable.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from itertools import product

MIDPOINTS = ("m1", "m2", "m3", "m4")
VERTEX_SQUARES = ("V1", "V2", "V3", "V4")
EXTRAS = ("E", "F")
SQUARES = VERTEX_SQUARES + EXTRAS

HOSTS: dict[str, tuple[str, ...]] = {
    "m1": ("V1", "V2", "E", "F"),
    "m2": ("V2", "V3", "E", "F"),
    "m3": ("V3", "V4", "E", "F"),
    "m4": ("V4", "V1", "E", "F"),
}

# D4 on midpoints / vertex-squares, fixing E and F.
_ROT = {"m1": "m2", "m2": "m3", "m3": "m4", "m4": "m1",
        "V1": "V2", "V2": "V3", "V3": "V4", "V4": "V1",
        "E": "E", "F": "F"}
_REF = {"m1": "m4", "m4": "m1", "m2": "m3", "m3": "m2",  # reflect across the rising diagonal v1–v3
        "V1": "V1", "V3": "V3", "V2": "V4", "V4": "V2",
        "E": "E", "F": "F"}


def _apply(perm: dict[str, str], assignment: dict[str, str]) -> dict[str, str]:
    """Push an assignment forward: host(m) ↦ perm(host)(perm(m))."""
    out = {}
    for m in MIDPOINTS:
        new_m = perm[m]
        new_host = perm[assignment[m]]
        out[new_m] = new_host
    return out


def _d4_images(assignment: dict[str, str]) -> list[dict[str, str]]:
    images = []
    rot = {k: k for k in _ROT}  # identity as a map on labels via successive rot
    # generate rotations of identity
    cur = {"m1": "m1", "m2": "m2", "m3": "m3", "m4": "m4",
           "V1": "V1", "V2": "V2", "V3": "V3", "V4": "V4", "E": "E", "F": "F"}
    for _ in range(4):
        images.append(_apply(cur, assignment))
        cur = {k: _ROT[cur[k]] for k in cur}
    # reflections: ref, then rotations of ref
    cur = dict(_REF)
    # fill identity for any missing
    for k in list(_ROT):
        cur.setdefault(k, k)
    for _ in range(4):
        images.append(_apply(cur, assignment))
        cur = {k: _ROT[cur[k]] for k in cur}
    return images


def _key(assignment: dict[str, str]) -> tuple[tuple[str, str], ...]:
    return tuple((m, assignment[m]) for m in MIDPOINTS)


@dataclass(frozen=True)
class TypeRecord:
    assignment: dict[str, str]
    k: int
    e_has_midpoint: bool
    f_has_midpoint: bool
    vertex_claimed: tuple[str, ...]
    extra_claimed: tuple[str, ...]
    vertex_midpoints_adjacent: bool | None
    chiral: str | None  # 'cw', 'ccw', or None
    orbit_size: int
    status: str
    note: str


def _chirality(assignment: dict[str, str]) -> str | None:
    """For k=4, detect the unique clockwise / counterclockwise matching."""
    if any(assignment[m] in EXTRAS for m in MIDPOINTS):
        return None
    # clockwise: Vi contains m_i  (v_i claims the side [v_i, v_{i+1}])
    cw = all(assignment[f"m{i}"] == f"V{i}" for i in range(1, 5))
    # counterclockwise: V_{i+1} contains m_i
    ccw = all(assignment[f"m{i}"] == f"V{(i % 4) + 1}" for i in range(1, 5))
    if cw:
        return "cw"
    if ccw:
        return "ccw"
    return "other"


def _vertex_midpoints_adjacent(assignment: dict[str, str]) -> bool | None:
    """True iff the two midpoints hosted by vertex squares are adjacent on C4."""
    claimed = [m for m in MIDPOINTS if assignment[m] in VERTEX_SQUARES]
    if len(claimed) != 2:
        return None
    i, j = (int(m[1]) for m in claimed)
    return abs(i - j) % 2 == 1  # differ by 1 or 3 ⇒ adjacent; by 2 ⇒ opposite


def classify(assignment: dict[str, str]) -> dict:
    hosts = [assignment[m] for m in MIDPOINTS]
    k = sum(1 for h in hosts if h in VERTEX_SQUARES)
    e_has = "E" in hosts
    f_has = "F" in hosts
    vertex_claimed = tuple(m for m in MIDPOINTS if assignment[m] in VERTEX_SQUARES)
    extra_claimed = tuple(m for m in MIDPOINTS if assignment[m] in EXTRAS)
    chiral = _chirality(assignment)
    adj = _vertex_midpoints_adjacent(assignment)
    return {
        "k": k,
        "e_has_midpoint": e_has,
        "f_has_midpoint": f_has,
        "vertex_claimed": vertex_claimed,
        "extra_claimed": extra_claimed,
        "vertex_midpoints_adjacent": adj,
        "chiral": chiral,
    }


def _status_note(info: dict) -> tuple[str, str]:
    """Proved / reduced / open, matching PROOF_ATTEMPT.md.

    Combinatorial types k=0,1 are absent from the census (capacity).
    k=4 extras-miss-boundary is a geometric lemma, not a type filter.
    """
    k = info["k"]
    e_has = info["e_has_midpoint"]
    f_has = info["f_has_midpoint"]
    chiral = info["chiral"]
    if k <= 1:
        return "closed", "capacity: 4-k extras cannot host 4-k midpoints"
    if k == 4:
        if chiral in {"cw", "ccw"}:
            return (
                "open",
                "Remaining Lemma C (k=4). One D4-orbit: cw and ccw are reflections.",
            )
        return "closed", "k=4 matching on C4 is only cw or ccw (proved)"
    if k == 3:
        if e_has and not f_has:
            return (
                "open",
                "Remaining Lemma B1: E hosts c and the leftover midpoint; F has no midpoint.",
            )
        if f_has and not e_has:
            return (
                "open",
                "Remaining Lemma B2: E hosts only c; F hosts the leftover midpoint.",
            )
        return "closed", "k=3 requires exactly one extra-midpoint"
    # k == 2
    if not (e_has and f_has):
        return "closed", "k=2 requires both extras to host a midpoint"
    if info["vertex_midpoints_adjacent"] is True:
        return (
            "open",
            "Remaining Lemma A_adj: vertex-squares host two adjacent midpoints.",
        )
    if info["vertex_midpoints_adjacent"] is False:
        return (
            "open",
            "Remaining Lemma A_opp: vertex-squares host two opposite midpoints.",
        )
    return "open", "k=2 unclassified"


def all_assignments() -> list[dict[str, str]]:
    keys = MIDPOINTS
    pools = [HOSTS[m] for m in keys]
    out = []
    for hosts in product(*pools):
        if len(set(hosts)) < 4:
            continue
        out.append(dict(zip(keys, hosts, strict=True)))
    return out


def orbit_representatives(assignments: list[dict[str, str]] | None = None) -> list[TypeRecord]:
    if assignments is None:
        assignments = all_assignments()
    seen: set[tuple] = set()
    records: list[TypeRecord] = []
    for asn in assignments:
        k = _key(asn)
        if k in seen:
            continue
        images = _d4_images(asn)
        orbit_keys = [_key(im) for im in images]
        for ok in orbit_keys:
            seen.add(ok)
        info = classify(asn)
        status, note = _status_note(info)
        records.append(
            TypeRecord(
                assignment=asn,
                orbit_size=len(set(orbit_keys)),
                status=status,
                note=note,
                **info,
            )
        )
    records.sort(key=lambda r: (r.k, r.status, r.note, _key(r.assignment)))
    return records


def census() -> dict:
    raw = all_assignments()
    orbs = orbit_representatives(raw)
    by_k: dict[int, int] = defaultdict(int)
    by_status: dict[str, int] = defaultdict(int)
    by_k_status: dict[str, int] = defaultdict(int)
    for r in orbs:
        by_k[r.k] += r.orbit_size
        by_status[r.status] += r.orbit_size
        by_k_status[f"k={r.k}:{r.status}"] += r.orbit_size
    return {
        "n_raw_assignments": len(raw),
        "n_orbits": len(orbs),
        "by_k": dict(by_k),
        "by_status": dict(by_status),
        "by_k_status": dict(by_k_status),
        "orbits": [
            {
                **asdict(r),
            }
            for r in orbs
        ],
    }


def markdown_table(records: list[TypeRecord] | None = None) -> str:
    if records is None:
        records = orbit_representatives()
    lines = [
        "| orbit rep (m1,m2,m3,m4) | k | |orb| | E has mid | F has mid | chiral / adj | status | remaining lemma |",
        "|---|---:|---:|:---:|:---:|---|---|---|",
    ]
    for r in records:
        asn = ",".join(r.assignment[m] for m in MIDPOINTS)
        if r.chiral:
            extra = r.chiral
        elif r.vertex_midpoints_adjacent is True:
            extra = "adj mids"
        elif r.vertex_midpoints_adjacent is False:
            extra = "opp mids"
        else:
            extra = "—"
        lines.append(
            f"| `{asn}` | {r.k} | {r.orbit_size} | {r.e_has_midpoint} | "
            f"{r.f_has_midpoint} | {extra} | {r.status} | {r.note} |"
        )
    return "\n".join(lines)
