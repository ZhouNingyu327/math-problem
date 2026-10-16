# Direction 1: classify a=2 covers + quantitative local non-extendability. Verdict (2026-10-08)

**Verdict: not viable as a separate route. It is equivalent in size to the full problem.**
* Qualitative compactness is trivial: if covers of side 2+eps_n exist, a subsequence converges to a cover of [0,2]^2. But a
  quantitative eta(eps) needs a lower bound on how far a non-cover is from covering, i.e. exactly the quantity S(6)=2 asserts is positive.
  By E2 (extremal/EXTREMAL.md) S(6)=2 iff no cover of the closed [0,2]^2 by six OPEN squares exists. So "no a=2 cover extends" is
  literally the conjecture restated at a=2.
* The a=2 cover set is positive-dimensional with many components: 13/48 random global searches gave exact covers with 1-4 tilted
  squares (rigidity/), plus the tilted-V3 family, and the grid family with two free spares. Local first/second-order analysis has to be done
  on each component, including the non-local motion of the spare squares (which can sit anywhere). There is no finite list of
  components available, and producing one is a global problem.
* The one family where local analysis works is the grid family with the V_i near grid quarters. There, the uncovered set contains a thin cross of total
  length ~4, and two unit squares cover at most 2*sqrt2 of a thin cross. This is sound and already noted in STATUS (rigidity round), but
  the premise (V_i near grid quarters) fails in general (tilted-V3 cover at a=2).
* E5/E6 (no self-stress, tension identity) give the first-order conditions. Classifying the tight-contact patterns is at least as large as the B&B.
Recommendation: replaced by the FPS certificates (fps/RESULTS.md), which are case-independent and monotone in a.
