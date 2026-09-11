"""python -m proof  — re-run exact lemmas, census, and diagrams."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "artifacts" / "proof"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="S(6)=2 proof-attempt checks (not a completed proof)")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = p.parse_args(argv)
    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)

    from proof.inequalities import numeric_table, run_all_proofs
    from proof.enumerate_types import census, markdown_table
    from proof.diagrams import write_all

    proved = run_all_proofs()
    table = numeric_table()
    cen = census()
    md = markdown_table()

    (out / "proved_lemmas.json").write_text(json.dumps(proved, indent=2) + "\n")
    (out / "numeric_table.json").write_text(json.dumps(table, indent=2) + "\n")
    # orbits include assignment dicts; JSON dump
    slim = {
        "n_raw_assignments": cen["n_raw_assignments"],
        "n_orbits": cen["n_orbits"],
        "by_k": cen["by_k"],
        "by_status": cen["by_status"],
        "by_k_status": cen["by_k_status"],
        "orbits": cen["orbits"],
    }
    (out / "census.json").write_text(json.dumps(slim, indent=2) + "\n")
    (out / "case_table.md").write_text(md + "\n")
    figs = write_all(out)

    print(json.dumps({"proved_lemmas": len(proved), "n_orbits": cen["n_orbits"],
                      "n_raw": cen["n_raw_assignments"], "figures": [str(f) for f in figs]}, indent=2))
    print("STATUS: combinatorial census complete; Remaining Lemmas A/B/C are OPEN.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
