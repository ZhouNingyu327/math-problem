"""Exact, solver-independent check that no m sets of a family cover all points (bitset DFS).
Complete branching: the chosen uncovered point p must lie in some chosen set; among sets containing p only those
maximal on the uncovered points are tried (a dominated choice can be swapped for its dominator). Pruning:
greedy set of pairwise-incompatible uncovered points (no family member contains two of them) needs that many
more sets."""
import numpy as np
from numba import njit

@njit(cache=True)
def _popc(x):
    c = 0
    while x:
        x &= x - np.uint64(1); c += 1
    return c

@njit(cache=True)
def _has(mask, p):
    return (mask[p >> 6] >> np.uint64(p & 63)) & np.uint64(1)

@njit(cache=True)
def _dfs(S, indptr, idx, compat, order, covered, depth, m, n, W, stats):
    stats[0] += 1
    # uncovered list
    U = np.empty(n, np.int64); nu = 0
    for t in range(n):
        p = order[t]
        if not _has(covered, p):
            U[nu] = p; nu += 1
    if nu == 0:
        return True
    if depth == m:
        return False
    # incompatibility lower bound (greedy)
    I = np.empty(nu, np.int64); ni = 0
    for t in range(nu):
        p = U[t]; ok = True
        for r in range(ni):
            if compat[p, I[r]]:
                ok = False; break
        if ok:
            I[ni] = p; ni += 1
            if ni > m - depth:
                stats[1] += 1
                return False
    # choose point with fewest candidate sets
    best = -1; bc = 1 << 60
    for t in range(nu):
        p = U[t]; c = indptr[p+1] - indptr[p]
        if c < bc:
            bc = c; best = p
    p = best
    nc = indptr[p+1] - indptr[p]
    R = np.empty((nc, W), np.uint64); pc = np.empty(nc, np.int64)
    for j in range(nc):
        sid = idx[indptr[p] + j]; c = 0
        for w in range(W):
            R[j, w] = S[sid, w] & ~covered[w]; c += _popc(R[j, w])
        pc[j] = c
    ordc = np.argsort(-pc)
    keep = np.zeros(nc, np.bool_)
    kept = np.empty(nc, np.int64); nk = 0
    for jj in range(nc):
        j = ordc[jj]; dom = False
        for r in range(nk):
            q = kept[r]; sub = True
            for w in range(W):
                if (R[j, w] & ~R[q, w]) != 0:
                    sub = False; break
            if sub:
                dom = True; break
        if not dom:
            kept[nk] = j; nk += 1
    newc = np.empty(W, np.uint64)
    for r in range(nk):
        j = kept[r]
        for w in range(W):
            newc[w] = covered[w] | R[j, w]
        if _dfs(S, indptr, idx, compat, order, newc.copy(), depth + 1, m, n, W, stats):
            return True
    return False

def no_cover(S, n, m=6):
    """True iff no m members of S (bitset rows) cover points 0..n-1. Exact."""
    W = S.shape[1]
    bits = np.unpackbits(S.view(np.uint8), axis=1, bitorder='little')[:, :n].astype(bool)
    cnt = bits.sum(0)
    if (cnt == 0).any():
        return True, np.zeros(2, np.int64)
    indptr = np.zeros(n + 1, np.int64); indptr[1:] = np.cumsum(cnt)
    idx = np.concatenate([np.nonzero(bits[:, p])[0] for p in range(n)]).astype(np.int64)
    B = bits.astype(np.float32)
    compat = (B.T @ B) > 0.5
    order = np.argsort(cnt, kind='stable').astype(np.int64)   # rare points first in LB greedy
    stats = np.zeros(2, np.int64)
    found = _dfs(S, indptr, idx, compat, order, np.zeros(W, np.uint64), 0, m, n, W, stats)
    return (not found), stats
