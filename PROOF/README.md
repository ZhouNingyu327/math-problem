# `PROOF/`

Attempt to prove \(S(6)=2\) (six unit squares cannot cover a square of side
strictly greater than 2).

| File | Role |
|---|---|
| [`ATTEMPT.md`](ATTEMPT.md) | Case tree, standing lemmas, fragments that *are* proved |
| [`GAPS.md`](GAPS.md) | Residual G1 Open A/B/C and G2–G5, stated as unproved lemmas |
| [`LOCAL_SYNC.md`](LOCAL_SYNC.md) | Local cuts, retracted \(a_{\mathrm{top}}^F\), CAP stall |

**This folder does not contain a complete proof.** Machine checks:

```bash
python3 -m pytest
python3 -m proof
```
