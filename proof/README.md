# `proof/` — computer checks for the S(6)=2 attempt

This package does **not** prove \(S(6)=2\). It verifies algebraic identities
used as lemmas and enumerates combinatorial types of important-point coverings.

The mathematical write-up is

> [`../PROOF/ATTEMPT.md`](../PROOF/ATTEMPT.md)
> [`../PROOF/GAPS.md`](../PROOF/GAPS.md)

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest
python3 -m proof          # lemmas + D4 census + figures → artifacts/proof/
```
