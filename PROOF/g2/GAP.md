# G2-G5: the exact gap (2026-10-08 evening). Read off /workspace/square-cover-6/proof/ATTEMPT.md §4-§6

Notation as in ATTEMPT.md: S=[0,a]^2, mu=a/2, v1=(0,0), v2=(a,0), v3=(a,a), v4=(0,a); m1=(mu,0), m2=(a,mu), m3=(mu,a), m4=(0,mu); c=(mu,mu);
Q4=conv{v4,m3,c,m4}=[0,mu]x[mu,a]. Prop L: if bd(Q4) is covered by TWO unit squares then a<=2 (S_bd(2)=1).

## The step that fails (same in G2-main §5, G3 §4, G4 Type A §6)
The draft claims  (*)  bd(Q4) ⊂ V4 ∪ C  and then applies Prop L. Its four sides:
* [m4,c] ⊂ C and [m3,v4] ⊂ V4: correct (convexity, both endpoints inside).
* [c,m3]: the draft says "C covers distance <= 2/a up from c (CR-mid) and V4 covers <= 2/a down from m3 (CR); 4/a >= mu, so they meet".
  But CR gives **upper bounds on reach**, so it cannot give coverage. What is true: every point of [c,m3] lies in some item; V1, V2 are
  too far (|p-v1|,|p-v2| >= a/sqrt2 > sqrt2); V3 is excluded by the area-1/2 triangle argument (claimed in §6, not re-audited here);
  so [c,m3] ⊂ C ∪ V4 ∪ F. Nothing excludes F.
* [v4,m4] (left side, y in [mu,a]): for a<=a_* the reach zones of V4 (down to a-l(mu)) and C (up to mu+2/a) overlap. Again this is only
  "nothing else is NEEDED", not "nothing else is THERE". The covering items are V4, C, F, and also **V1** on y in [mu, sqrt2]
  (V1 ∋ v1 reaches height sqrt2 > mu on the left side). So [v4,m4] ⊂ V4 ∪ C ∪ F ∪ V1.
So what is actually proved is bd(Q4) ⊂ V4 ∪ C ∪ F ∪ V1 (∪V3 if the triangle argument fails). That is four items, while S_bd(3)=sqrt(phi)≈1.272 > mu
already allows three items to cover bd(Q4). Prop L does not apply.
Extra gaps: G3 applies CR-mid to F ∋ m2, but CR-mid needs c ∈ F, so F need not lie in the midline strip. G5 (c ∈ C∩F) has no argument for
a<=2^{5/4}. The large-a parts (forced gap Γ nonempty, a>a_*) are fine, because there an explicit point is shown to be uncovered.

## Exact missing statement
(EJ) In the G2/G3/G4 labellings with a in (2, 2.04): (F ∪ V1 ∪ V3) ∩ bd(Q4) ⊂ V4 ∪ C,
i.e. the other items contribute nothing to bd(Q4) that V4 ∪ C does not already cover. (EJ) plus Prop L closes the case.
The strong form "F ∩ bd(Q4) = ∅" is more than is needed.

## Is (EJ) true? Result: it cannot be proved by any argument that survives the limit a->2+ (explicit configuration)
**G2 is sharp at a=2.** The grid cover V1=[0,1]^2, V2=[1,2]x[0,1], V3=[1,2]^2, V4=[0,1]x[1,2], C=[0,1]x[0.4,1.4] covers [0,2]^2 and satisfies
all closed G2 incidences (v_i ∈ V_i, m1 ∈ V1, m2 ∈ V3, m3 ∈ V4, c, m4 ∈ C). So every valid G2 argument must be tight at a=2.
**(EJ) fails at a=2** (a2_G2.py, a2_G2_check.py/.log; shapely, floating point). Keep V1, V2, V3, C as above. Take
V4 = unit square centred (0.553609, 1.653758) rotated 8.292° (it contains v4=(0,2) and m3=(1,2)), and
F = unit square centred (-0.318034, 1.600000) rotated 21.885°.
F stays at Chebyshev distance >= 0.175 from every midpoint, so F holds no midpoint (strictly).
The six squares cover [0,2]^2 (uncovered area 0.0). The segment {0} x [1.400, 1.985] of bd(Q4), of length 0.585, lies in **no item except F**.
So "bd(Q4) ⊂ V4 ∪ C", and even "bd(Q4) ⊂ V1∪V2∪V3∪V4∪C", is false for limits of G2 configurations. Any proof of (EJ)
on (2, 2+δ) must use a > 2 quantitatively. Every closed-condition or compactness-stable argument (reach bounds, CR, L-bounds, diameter windows) fails.
Numerical near-cover search at a=2.01/2.02 with strict incidences (near_G2.py): the penalised Powell search did not converge (penalties stayed
large), so there is no quantitative near-cover statement yet.

## What weaker statement suffices
Three items easily cover bd(Q4) under the local constraints (S_bd(3)=1.272 > mu), so no purely local statement about Q4 can work. A
sufficient statement has to tie F to a second place where it is needed:
(EJ') for a in (2, 2.04), in the G2/G4 labellings, F cannot meet bd(Q4) \ (V4 ∪ C) and also cover the part of S that V1,V2,V3,V4,C miss outside Q4.
In the a=2 example the five-item leftover lies entirely in Q4 (F is needed only there). So (EJ') too must exploit the eps-strips that appear only for a>2,
for example the vertical/horizontal mid-strips of width a-2 that the near-grid vertex items cannot cover. This is the same sharpness
obstruction as in the open G1 cases. Status: **(EJ) is not proved. It is refuted as a limit-stable lemma, and G2-G5 remain open on (2, 2.04).**
