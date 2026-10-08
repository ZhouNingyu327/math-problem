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
