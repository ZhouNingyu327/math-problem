# Hand proofs for the n=8, k=3 classes #28, #366, #2547, #2550, #4190 and the hand reduction for #3090
(Expanded in response to AUDIT2.md. Convention: p_0..p_7 are the vertices of a STRICTLY convex octagon in ccw order, i.e. every
vertex is a corner with interior angle < 180°. A polygon traversed clockwise is reflected; reflection preserves the pattern.)

## Notation and Fact (D)
e_k = p_{k+1} − p_k (indices mod 8). Choose lifted directions φ_k of e_k with φ_0 < φ_1 < … < φ_7 < φ_0 + 360°. This is possible,
and each step φ_{k+1} − φ_k (the exterior angle at p_{k+1}) lies in (0°,180°): strict convexity makes every exterior angle positive
and < 180°, and the exterior angles sum to 360°.
**Fact (D2).** The two-step chord p_k→p_{k+2} = e_k + e_{k+1} has a direction θ(k,k+2) that can be chosen in the open interval (φ_k, φ_{k+1}).
Proof: two nonzero vectors whose directions differ by an angle in (0°,180°) have a sum whose direction lies strictly between them. ∎
Consequence: θ(k,k+2) < φ_{k+1} < θ(k+1,k+3), and all of θ(0,2) < θ(1,3) < … < θ(7,1) lie in one turn (φ_0, φ_0+360°).
**Lift rule.** If a direction is known mod 360° to equal α + c, and it also lies in an open interval J ⊂ (α, α+360°), then its lifted
value is the unique representative of α + c (mod 360°) in (α, α+360°). This is used below to turn mod-360 identities into real equalities.

## Forced linear relations (each derived by hand from the pattern; each also confirmed by Singular slimgb over Q, forced_sing.log)
Generic step R: if |p_a p_x| = |p_a p_y| = |p_x p_y| = r and |p_z p_x| = |p_z p_y| = r with p_z ≠ p_a,
then p_z is the reflection of p_a in the line p_x p_y, i.e. p_z = p_x + p_y − p_a (two circles of radius r about p_x and p_y meet in exactly
those two points).
- #2547, T=[(1,2,6),(0,3,7),(0,4,6),(1,5,7),(2,5,6),(3,4,7),(0,2,4),(1,3,5)].
  T0: |01|=|02|=|06|; T6: |60|=|62|=|64|; T2: |20|=|24|=|26|. So 0,2,6 is equilateral (side |01|=1) and, by R, p4 = p2+p6−p0.
  T1: |10|=|13|=|17|; T7: |71|=|73|=|75|; T3: |31|=|35|=|37|. So 1,3,7 is equilateral (side 1) and p5 = p3+p7−p1. T4: |42|=|45| ⇒ |p4p5| = 1.
- #2550: p5 = p2+p6−p0 and p4 = p3+p7−p1 (same scheme). #4190: p5 = p2+p7−p0 and p4 = p3+p6−p1.
- #28: p3 = p0+p2−p1 and p7 = p4+p6−p5. #366: p4 = p0+p2−p1. #3090: p5 = p3+p7−p1.
Singular check (I + {t_q f_q − 1} + {s(Δx²+Δy²) − 1} is the unit ideal; f_q are the squared distances needed for "p_z ≠ p_a"):
all 11 relations give DIM −1. Every control (a false relation) gives DIM ≥ 1.

## #2547 (expanded)
Orientation: the triangle 0,2,6 inherits the ccw order of the polygon, so p6 − p0 is p2 − p0 rotated by +60°. Likewise p7 − p1 is p3 − p1
rotated by +60°. Write a = θ(0,2) (= direction of p2 − p0) and b = θ(1,3). Then, mod 360°:
 θ(2,4) = dir(p6−p0) = a+60, θ(4,6) = dir(p0−p2) = a+180, θ(3,5) = dir(p7−p1) = b+60, θ(7,1) = dir(p1−p7) = b+240.
Lifting with (D2) and the lift rule (all intervals are inside (a, a+360°) or (b, b+360°)):
 a ∈ (φ0,φ1), b ∈ (φ1,φ2) ⇒ a < b.
 θ(2,4) ∈ (φ2,φ3) ⊂ (a, a+360) ⇒ θ(2,4) = a+60 > φ2 > b. Hence t := b − a ∈ (0°, 60°).
 θ(3,5) ∈ (φ3,φ4) ⊂ (b, b+360) ⇒ θ(3,5) = b+60 < φ4.
 θ(4,6) ∈ (φ4,φ5) ⊂ (a, a+360) ⇒ θ(4,6) = a+180 > φ4.
 θ(7,1) ∈ (φ7, φ0+360) ⊂ (b, b+360) ⇒ θ(7,1) = b+240 < φ0+360, i.e. φ0 > b − 120.
Set e = p1 − p0 (direction φ0, length 1) and e' = p5 − p4 (direction φ4, length 1). Let γ = φ4 − φ0. From the lines above:
 γ > (b+60) − a = 60 + t  and  γ < (a+180) − (b−120) = 300 − t.   (*)
This justifies the step γ ∈ (60+t, 300−t).
Now e' − e = (p5 − p1) − (p4 − p0) = D_B − D_A, where D_A = (p2−p0)+(p6−p0) = √3·u(a+30) and D_B = √3·u(b+30). Hence
 |e' − e| = 2√3 sin(t/2)   (two vectors of length √3 at angle t),
 |e' − e| = 2 |sin(γ/2)|   (two unit vectors at angle γ).
By (*), γ/2 ∈ (30 + t/2, 150 − t/2). This interval lies in (0°,180°) and is symmetric about 90°, so sin(γ/2) > sin(30° + t/2) > 0. Therefore
 √3 sin(t/2) > sin(30° + t/2) = ½cos(t/2) + (√3/2) sin(t/2) ⇒ (√3/2) sin(t/2) > ½ cos(t/2) ⇒ tan(t/2) > 1/√3 ⇒ t > 60°,
contradicting t < 60°. ∎

## #4190
p7 − p5 = p0 − p2 and p6 − p4 = p1 − p3, so mod 360°: θ(5,7) = a+180 and θ(4,6) = b+180. With a = θ(0,2), b = θ(1,3), we have a < b (D2).
Lift: θ(4,6) ∈ (φ4,φ5) ⊂ (b, b+360) ⇒ θ(4,6) = b+180. θ(5,7) ∈ (φ5,φ6) ⊂ (a, a+360) ⇒ θ(5,7) = a+180.
(D2) gives θ(4,6) < θ(5,7), so b < a. Contradiction. ∎

## #2550
The quadrilateral p0 p1 p4 p5 is strictly convex (a subsequence of the polygon) with |p0p1| = |p4p5| = 1 and |p1p4| = |p0p5| = √3
(the long rhombus diagonals). Lemma: a convex quadrilateral ABCD with AB = CD and BC = DA is a parallelogram.
Proof: triangles ABC and CDA are congruent (SSS, common side AC). The isometry exchanging A and C and taking B to D is either the point
reflection in the midpoint of AC (giving a parallelogram) or the reflection in the perpendicular bisector of AC. In the second case B and D
lie on the same side of line AC, so ABCD is not convex. ∎
So p5 − p0 = p4 − p1, i.e. √3·u(a+30) = √3·u(b+30) with a = θ(0,2), b = θ(1,3), so a ≡ b mod 360. But a < b < φ2 < φ0+360 < a+360. Contradiction. ∎

## #366
T0, T2: |01|=|02|=|04|, |20|=|21|=|24|. So 0,1,2 is equilateral, and by R (p4 ≠ p1) p4 = p0+p2−p1. In the gauge p0=(0,0), p1=(1,0), ccw:
p2 = (1/2, √3/2), p4 = (−1/2, √3/2). T1: |p1p3| = |p1p0| = 1, so p3 = p1 + u(ψ).
The points 0,2,3,4 are in strictly convex position in this order, so p3 and p0 lie strictly on opposite sides of line p2p4 (y = √3/2).
Hence sin ψ > √3/2, i.e. ψ ∈ (60°,120°) mod 360. But p1→p3 is a two-step chord: by (D2) its direction lies in (φ1, φ2) with φ1 = 120°
(direction of p2 − p1) and φ2 < φ1 + 180 = 300°. No representative of (60°,120°) mod 360 lies in (120°,300°). Contradiction. ∎

## #28
T0, T2, T3 ⇒ 0,1,2 and 0,2,3 are equilateral. T4–T7 ⇒ 4,5,6 and 4,6,7 are equilateral. The vertices 0,1,2,3 and 4,5,6,7 are consecutive,
so the interior angles are ∠1 = ∠p0p1p2 = 60°, ∠2 = ∠p1p2p3 = 120°, ∠5 = 60°, ∠6 = 120°. The exterior angles at 1, 2, 5, 6 then sum to
120+60+120+60 = 360°, leaving 0° for vertices 0, 3, 4, 7, whose exterior angles must be > 0. Contradiction. ∎

## #3090 (hand reduction; then exact certification, c3090.py)
Relations p6 = rot_{+60}(p2) about p0 and p7 − p1 = rot_{±60}(p3 − p1), p5 = p3+p7−p1, as above. The sign of the rotation is left as a
variable (r² = 3), so both orientations are covered. The reduced system is zero-dimensional with 8 distinct solutions, all real, all
certified nonconvex.