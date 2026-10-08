# Six new-structure ideas: quick viability tests (2026-10-08)
(b) Halves / quarters: a 1 x a strip (a>2) needs >=3 unit squares, but this is just AREA (a>2). Squares crossing the midline
    contribute to both halves, and the total area slack is 6-a^2 ~ 2, so the halves bookkeeping reduces to area and forces nothing.
    The orthogonal midline adds the same slack again. VERDICT: not viable without a new per-half boundary lemma.
    Note: the strip lemma for w=1 IS rigorous (trapezoid area w*avg <= 1 gives avg <= 1/w = 1), but area already gives it.
(a) Cut-and-rescale to S(5): deleting a strip covered by one item and gluing does not keep the other items as unit squares
    (they get cut or sheared). No invariant survives. VERDICT: not viable.
(c) Minkowski / mixed area: covering implies no mixed-area inequality on the union beyond area and perimeter-type bounds
    (already covered by GridLen/S_bd). VERDICT: nothing new.
(d) Nerve / Euler characteristic: the nerve of a cover is combinatorial. The same nerves occur for side 2 and 2+eps (perturb the
    grid cover), so a purely combinatorial invariant cannot see a>2. VERDICT: provably insufficient alone.
(e) 3x3 grid witness set (spacing s=a/2>1): every unit square holds <=2 of the 9 points, and a pair must be grid-adjacent
    (collinear triples span 2s>sqrt2, diagonal pairs s*sqrt2>sqrt2, right triangles with legs s>1 do not fit). So >=5 squares are needed.
    That is the S(5)=2 bound again; with 6 squares the slack is the midpoint taxonomy already in use. VERDICT: reproduces known structure.
(f) Symmetrization (Steiner / reflection): the symmetral of a union of squares is not a union of unit squares. VERDICT: not viable.
Best lead remains the case-specific residual analysis (meet core), i.e. the big certified B&B.
