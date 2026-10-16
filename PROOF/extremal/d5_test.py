"""Test 'Lemma D(5)': for 5 unit squares and a>2, diam(S_a minus union) > sqrt2 ? (stronger than S(6)=2).
Refutation attempt from a=2 covers (families.jsonl) rescaled to a=2.001, removing each tile in turn. Float/shapely only."""
import json, numpy as np
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
def sq(cx, cy, th):
    c, s = np.cos(th), np.sin(th); pts = []
    for u, v in [(-.5, -.5), (.5, -.5), (.5, .5), (-.5, .5)]:
        pts.append((cx + c*u - s*v, cy + s*u + c*v))
    return Polygon(pts)
def diam(g):
    if g.is_empty: return 0.0
    pts = []
    for p in getattr(g, 'geoms', [g]):
        pts += list(p.exterior.coords)
    P = np.array(pts); return float(np.max(np.linalg.norm(P[:, None]-P[None], axis=2)))
def main():
  best = 9; rows = []
  for line in open('../rigidity/families.jsonl'):
      r = json.loads(line)
      if r[2] > 1e-9: continue
      x = np.array(r[3]).reshape(6, 3)
      for a in [2.001, 2.01]:
          T = [sq(cx*a/2, cy*a/2, th) for cx, cy, th in x]
          S = box(0, 0, a, a)
          for i in range(6):
              U = S.difference(unary_union([T[j] for j in range(6) if j != i]))
              U = U.buffer(0)
              d = diam(U) if U.area > 1e-12 else 0.0
              rows.append((a, i, d, U.area)); best = min(best, d) if U.area > 1e-12 else best
  print('covers tested:', len(rows)//12)
  print('min diam(U5) over all (a,tile) with nonempty U5:', best, ' sqrt2=', 2**.5)
  print(sorted(rows, key=lambda t: t[2])[:8])

if __name__ == "__main__":
  main()
