# AUDIT4: re-audit of the corrected weak-convexity argument (2026-10-10, ~09:50 CST)
Written by the same auditor as AUDIT2 and AUDIT3. I edited none of their files. My new code is audit2_code/sp.py and relp_save.py,
plus the stored certificates in audit2_code/rescued461.json.

## Verdicts
| Item | Verdict |
|---|---|
| Q(ad,bc) equality ⇒ 4 consecutive collinear vertices; split placement | **CORRECT**, covers all cases |
| LP-gap list = my wbad.json | **IDENTICAL** (1,398 classes, same list) |
| Split systems: own-encoding sample | **60/60 agree** (50 pair, 10 single), with a positive control |
| 9 translate classes | **CLOSED**: all 8 i-cases unit for each class, no duplicate entries |
| Tally 33,564 + 1,398 + 4,805 + 9 + 320 | **CORRECT per class**: disjoint, union = all 40,096 |
| #385 | Ledger verdict CERT-NONCONVEX (D = 8, 8 real) present; the independent indep_nc re-check is **not yet done** |
| Write-ups | **Mostly accurate now.** Three defects remain (listed below). |

**Overall:** I found no remaining logical gap in the weak-convexity octagon argument. "n_3 = 9 also for weakly convex polygons" is now supported as a computer-assisted result, with the same trust base as the strict case.

**Caveats:**
- The 461 rescued certificates were previously NOT stored anywhere in the project. AUDIT3 only printed a count. I have now saved them, with exact rationals, in audit2_code/rescued461.json. They were checked exactly inside relp_save.py, but have not been re-checked by a second program.
- The independent re-check of #385 is pending.

## 1. The collinearity lemma
**Claim:** in a weakly convex ccw labelling, |ac| + |bd| = |ad| + |bc| (a < b < c < d cyclically) forces 4 consecutive labels to be collinear.

**Equality forces a, b, c, d onto one supporting line:**
- Let X ∈ [a,c] ∩ [b,d]. Equality needs X ∈ [a,d] ∩ [b,c].
- If line ad meets int K, then b and c are strictly on one side of it, so [b,c] misses [a,d]. Hence line ad is a supporting line.
- If exactly one of b, c lies on line ad, then the intersection point is that vertex, say b. But X = b ∈ [a,c] puts b on line ac, so c is on line ad too.
- So all four are collinear, and they lie on the same side (segment) of K.

**Consecutive:** a line with ≥ 3 boundary points of a 2-dimensional K is a supporting line. Its intersection with K is a segment of ∂K. The boundary arc a→b→c→d lies on that segment, so every label between a and d is on it. That gives a block of ≥ 4 consecutive collinear labels, which contains i−1, i, i+1, i+2 for i = a+1.

**Placement used:** p_i = (1−l)p_{i−1} + l·p_{i+2} and p_{i+1} = (1−m)p_{i−1} + m·p_{i+2}, with l, m, 1−l, 1−m, m−l ≠ 0.
- This is a superset of the true placement 0 < l < m < 1, so it is sound.
- All 8 cyclic i are run, so wrap-around blocks are included.
- **Why the certificates are then valid:** a realisation without 4 collinear points makes every Q(ad,bc) row strict, so each of the 1,398 certificates is valid there. Realisations with 4 collinear points are killed by the split.

## 2. Lists and tally
- The list in straight3.py (audit2_code/wbad.json) is byte-equal to my /workspace/audit2/wbad.json: 1,398 classes.
- straight3.jsonl has 11,256 entries: 11,184 pair + 72 single. All are CERT-UNIT, with no duplicate (T, i, mode).
- Every one of the 1,398 classes has all i = 0..7. Each of the 9 translate classes has all i = 0..7.

**Per-class partition** (my own script):
| Part | Size |
|---|---|
| Weak-valid LP: (cert8 − my wfails) ∪ rescued461 | 33,564 |
| wbad | 1,398 |
| Carried-over algebra (LP survivors − weak_open − the 9 translate classes) | 4,805 |
| Translate classes | 9 |
| weak_open | 320 |

The parts sum to 40,096, their union has 40,096 elements, and it equals s8.txt. The 320: 273 are closed in weak_alg.jsonl, and 47 by the straight splits (checked in AUDIT3).

## 3. Own-encoding sample
I rebuilt the systems with my own polynomial strings (audit2_code/sp.py): Singular slimgb over Q, saturating by all 27 distances if not already unit.
- 50 random "pair" systems and 10 random "single" systems: **all unit (dim −1), matching the ledger.**
- Positive control: only 3 pattern equations plus the collinear placement gives dim 8, not unit.

## 4. Write-ups (dated 09:15)
- **report_zh.pdf caveat 3** still opens with "尚未完全解决…目前只是被约化到 1,407 类" ("not yet fully resolved… currently only reduced to 1,407 classes"). The update bullet in the same caveat then says the problem is closed. **This is internally inconsistent; the stale sentence should be removed.**
- **note_en.pdf appendix:**
  - the heading still says "(partial …)" while the text concludes n_3 = 9 for weak polygons;
  - there is a broken macro, "1,398𝑖𝑚𝑒𝑠8 cases" (should be 1,398 × 8 = 11,184).
- **Both write-ups** say every nonconvex verdict was independently re-certified "except one still running" (#385). This is accurate only as long as that qualifier stays in.
- **Both write-ups** omit that 461 of the 33,564 weak-valid LP certificates are new certificates, not the original ones. They should cite audit2_code/rescued461.json, and ideally re-verify those certificates with the project's own checker.
- **Earlier items fixed:** the TRI remark in §3, Fact (D)/D2, and the dual-enumerator statement for n ≤ 6.