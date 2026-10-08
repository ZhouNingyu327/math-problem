# Local / repo sync

**\(S(6)=2\) is not proved.** This file is a ledger between unpublished local
work and what [`ATTEMPT.md`](ATTEMPT.md) / [`GAPS.md`](GAPS.md) record. It is
not a proof.

## Local lemmas newly recorded

| Lemma | Statement | Lowers \(a_{\mathrm{top}}\) / \(a_{\mathrm{cr}}\)? |
|---|---|---|
| **OpenB-R2TopDiam** | \(\lvert p^\ast-r^\ast\rvert^2=2\mu^4>2\) (\(\mu=\lambda\); same polynomial as FarPair) | No |
| **OpenB-FHeight** | \(F\cap R_2\subseteq(\mu,Y_b]\) with \(Y_b<\mu+g_0\) (analytic) | No |

In-repo check: `prove_openb_r2_top_diam`. FHeight is recorded as a local
analytic statement; the repo does not re-derive \(g_0\).

## Retracted

- \(a_{\mathrm{top}}^F\approx 2.0265\). The hypothesis \(\delta\ge 2g_0\) is
  invalid under R1Exclusive. Do not cite this cut.

## Local cuts (authoritative for remaining G1)

| Cut | Value | Residual interval |
|---|---|---|
| \(a_{\mathrm{cr}}\) | \(2.0036185600\) | Open B C-on-right \((2,a_{\mathrm{cr}}]\) |
| \(a_\varphi\) | \(\approx 2.00910069\) | meet deep-\(\delta\) \((2,a_\varphi]\) |
| \(a_{\mathrm{top}}\) | \(2.0361747746\) | Open B C-on-top \((2,a_{\mathrm{top}}]\) |
| \(a_\psi\) | local, decimal not copied | Open C razor \((2,a_\psi]\) |

In-repo OppFar still closes 2-opp leftovers for \(a>a_\diamond\approx 2.0918\),
which is weaker than the local Open B cuts.

## CAP / moduli (stalled)

- Point-MES on meet deep-\(\delta\): stalled, ~0.072% under \(\delta_{\mathrm{force}}\).
- Pose-space B&B: ~95% product kill; joint \(+0.03\%\).
- Survivors: fat non-rigid \(C\)-moduli lobes. No clean one-pose lemma.
- \(V_3\) couple / moduli \(U(\theta,s)\) sampling certificates: failed to empty cells.

**CLobeFat** (in-repo): on \(a<a_\ast=(\sqrt{2}+\sqrt{10})/2\approx 2.288\), a
unit square through \(c\) and a leftover tip still reaches past the
height-bound inner edge of an opposite vertex square. The moduli stay fat.
This explains the stall; it does **not** kill meet deep-\(\delta\).

A future kill needs a second contact (rigidify) or a two-point / joint
\((C,F)\) witness, not a θ-independent MES.

## Sharpest remaining

1. Meet deep-\(\delta\) on \((2,a_\varphi]\).
2. Open B C-on-top on \((2,a_{\mathrm{top}}]\).
3. Open B C-on-right on \((2,a_{\mathrm{cr}}]\).
4. Open C razor on \((2,a_\psi]\).

G2–G5 are unchanged (open down to \(a=2^+\) except the large-\(a\) fragments
already in ATTEMPT).
