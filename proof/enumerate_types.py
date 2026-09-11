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
    k: int  # vertex-hosted midpoints (old index)
    k_extra: int  # |{midpoints} ∩ (C ∪ F)|, the G1–G4 index
    gap: str
    e_has_midpoint: bool
    f_has_midpoint: bool
    vertex_claimed: tuple[str, ...]
    extra_claimed: tuple[str, ...]
    vertex_midpoints_adjacent: bool | None
    chiral: str | None  # 'cw', 'ccw', or None
    t8_adjacent: bool | None
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


def _t8_adjacent(assignment: dict[str, str]) -> bool | None:
    """True if C's unique extra-midpoint m_i has V_i hosting m_{i-1}.

    That is the DLT Case-2 / Lemma T8 labeling (C ∋ m_i, V_i ∋ m_{i-1}).
    """
    extra_in_c = [m for m in MIDPOINTS if assignment[m] == "E"]
    if len(extra_in_c) != 1:
        return None
    i = int(extra_in_c[0][1])
    prev = f"m{((i - 2) % 4) + 1}"  # m_{i-1}
    return assignment[prev] == f"V{i}"


def classify(assignment: dict[str, str]) -> dict:
    hosts = [assignment[m] for m in MIDPOINTS]
    k = sum(1 for h in hosts if h in VERTEX_SQUARES)
    e_has = "E" in hosts
    f_has = "F" in hosts
    vertex_claimed = tuple(m for m in MIDPOINTS if assignment[m] in VERTEX_SQUARES)
    extra_claimed = tuple(m for m in MIDPOINTS if assignment[m] in EXTRAS)
    chiral = _chirality(assignment)
    adj = _vertex_midpoints_adjacent(assignment)
    k_extra = 4 - k
    if k_extra == 0:
        gap = "G1"
    elif k_extra == 1:
        gap = "G2"
    elif k_extra == 2 and adj is False:
        gap = "G3"
    elif k_extra == 2 and adj is True:
        gap = "G4"
    else:
        gap = "?"
    t8_adjacent = _t8_adjacent(assignment)
    return {
        "k": k,
        "k_extra": k_extra,
        "gap": gap,
        "e_has_midpoint": e_has,
        "f_has_midpoint": f_has,
        "vertex_claimed": vertex_claimed,
        "extra_claimed": extra_claimed,
        "vertex_midpoints_adjacent": adj,
        "chiral": chiral,
        "t8_adjacent": t8_adjacent,
    }


def _status_note(info: dict) -> tuple[str, str]:
    """partial / open / closed, matching PROOF/GAPS.md.

    k here is the number of vertex-hosted midpoints. The G-index is k_extra.
    G5 (c ∈ C ∩ F) is a geometric flag, not a midpoint assignment.
    """
    k = info["k"]
    gap = info["gap"]
    e_has = info["e_has_midpoint"]
    f_has = info["f_has_midpoint"]
    chiral = info["chiral"]
    if k <= 1:
        return "closed", "capacity: extras cannot host 4 or 3 midpoints"
    if gap == "G1":
        if chiral in {"cw", "ccw"}:
            return (
                "partial",
                "G1 (k_extra=0): 0-/1-/4-meet closed for all a>2 (FarPair, CycleSum); "
                "2-adj/3-meet closed for a>a_φ; 2-opp closed for a>a_♦≈2.0918; "
                "residual 2-meet/3-meet on (2, a_♦].",
            )
        return "closed", "k_extra=0 matching on C4 is only cw or ccw (proved)"
    if gap == "G2":
        if e_has and not f_has:
            if info.get("t8_adjacent"):
                return (
                    "partial",
                    "G2 (k_extra=1, C hosts extra midpoint, T8-adjacent). "
                    "Closed for a>2^{5/4}; open on (2, 2^{5/4}].",
                )
            return (
                "open",
                "G2 (k_extra=1, C hosts extra midpoint, weak vertex adjacent to C). "
                "L-gap side meets the weak vertex; open for all a>2.",
            )
        return (
            "open",
            "G2 (k_extra=1, F hosts the extra midpoint). Need to eject F from the critical quarter.",
        )
    if gap == "G3":
        return "open", "G3 (k_extra=2, opposite extra-midpoints)."
    if gap == "G4":
        return (
            "partial",
            "G4 (k_extra=2, adjacent extra-midpoints). DLT Case-2 representative "
            "closed for a>√5 (Lemma T8); remaining a∈(2,√5] and sister orbits.",
        )
    return "open", "unclassified"


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
    records.sort(key=lambda r: (r.k_extra, r.gap, r.status, r.note, _key(r.assignment)))
    return records


def census() -> dict:
    raw = all_assignments()
    orbs = orbit_representatives(raw)
    by_k: dict[int, int] = defaultdict(int)
    by_status: dict[str, int] = defaultdict(int)
    by_k_status: dict[str, int] = defaultdict(int)
    by_gap: dict[str, int] = defaultdict(int)
    for r in orbs:
        by_k[r.k] += r.orbit_size
        by_status[r.status] += r.orbit_size
        by_k_status[f"k={r.k}:{r.status}"] += r.orbit_size
        by_gap[r.gap] += r.orbit_size
    return {
        "n_raw_assignments": len(raw),
        "n_orbits": len(orbs),
        "by_k": dict(by_k),
        "by_k_extra": {str(4 - int(k)): n for k, n in by_k.items()},
        "by_gap": dict(by_gap),
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
        "| orbit (m1,m2,m3,m4) | k_extra | gap | |orb| | C mid | F mid | chiral/adj | status | note |",
        "|---|---:|---|---:|:---:|:---:|---|---|---|",
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
            f"| `{asn}` | {r.k_extra} | {r.gap} | {r.orbit_size} | {r.e_has_midpoint} | "
            f"{r.f_has_midpoint} | {extra} | {r.status} | {r.note} |"
        )
    return "\n".join(lines)
