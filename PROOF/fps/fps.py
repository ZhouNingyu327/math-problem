"""Finite point-set (FPS) obstruction for S(6): lazy point generation + exact set-cover.

Certificate semantics (rigorous part):
  For angle frames theta_k=(k+1/2)*D, k=0..K-1 (D=90deg/K), any unit square with orientation in
  [theta_k-D/2, theta_k+D/2] (mod 90) lies in a frame-theta_k axis box of side s=cos(D/2)+sin(D/2) with
  the same centre. Hence every subset of P coverable by a unit square is contained in one of the
  'candidate box sets' {p: u_p in [u_i,u_i+s'], v_p in [v_j,v_j+s']} (s'=s+1e-9 slack, absorbs float error).
  The family F of these sets is a SUPERSET (up to inclusion) of all unit-square-coverable subsets.
  If no 6 members of F cover P, then no 6 unit squares cover P, so no 6 unit squares cover [0,a]^2.
"""
import numpy as np, math, time, json, sys
from numba import njit

@njit(cache=True)
def _angle_sets(x, y, c, sn, s, W, out, cnt0):
    n = x.shape[0]
    u = x * c + y * sn
    v = -x * sn + y * c
    ou = np.argsort(u)
    cnt = cnt0
    tmpidx = np.empty(n, np.int64)
    for ii in range(n):
        i = ou[ii]
        # window in u
        m = 0
        for jj in range(ii, n):
            j = ou[jj]
            if u[j] <= u[i] + s:
                tmpidx[m] = j; m += 1
            else:
                break
        # also points with equal u before ii (ties) - include points with u >= u[i]-0 handled by sort; ties earlier:
        jj = ii - 1
        while jj >= 0 and u[ou[jj]] >= u[i]:
            tmpidx[m] = ou[jj]; m += 1; jj -= 1
        # sort window by v
        vv = np.empty(m)
        for t in range(m):
            vv[t] = v[tmpidx[t]]
        ov = np.argsort(vv)
        end = 0
        prev_end = -1
        for st in range(m):
            if end < st:
                end = st
            while end < m and vv[ov[end]] <= vv[ov[st]] + s:
                end += 1
            if end > prev_end:
                # emit set ov[st:end]
                for w in range(W):
                    out[cnt, w] = 0
                for t in range(st, end):
                    p = tmpidx[ov[t]]
                    out[cnt, p >> 6] |= np.uint64(1) << np.uint64(p & 63)
                cnt += 1
                prev_end = end
    return cnt

def family(P, K=900, slack=1e-9):
    P = np.asarray(P, float)
    n = len(P); W = (n + 63) // 64
    D = (math.pi / 2) / K
    s = math.cos(D / 2) + math.sin(D / 2) + slack
    allsets = []
    buf = np.zeros((n * n + 8, W), np.uint64)
    for k in range(K):
        th = (k + 0.5) * D
        cnt = _angle_sets(P[:, 0].copy(), P[:, 1].copy(), math.cos(th), math.sin(th), s, W, buf, 0)
        allsets.append(np.unique(buf[:cnt], axis=0))
    S = np.unique(np.concatenate(allsets), axis=0)
    S = remove_dominated(S)
    return S, s

def popcount64(a):
    a = a.astype(np.uint64)
    c = np.zeros(a.shape, np.int64)
    for sh in range(0, 64, 8):
        c += np.array([bin(i).count('1') for i in range(256)])[((a >> np.uint64(sh)) & np.uint64(255)).astype(np.int64)]
    return c

@njit(cache=True)
def _dom(S, order):
    m, W = S.shape
    keep = np.ones(m, np.bool_)
    kept = np.empty(m, np.int64); nk = 0
    for oi in range(m):
        i = order[oi]
        dom = False
        for t in range(nk):
            j = kept[t]
            sub = True
            for w in range(W):
                if (S[i, w] & ~S[j, w]) != 0:
                    sub = False; break
            if sub:
                dom = True; break
        if dom:
            keep[i] = False
        else:
            kept[nk] = i; nk += 1
    return keep

def remove_dominated(S):
    pc = popcount64(S).sum(axis=1)
    order = np.argsort(-pc, kind='stable')
    keep = _dom(S, order)
    return S[keep]

def members(S, n):
    """list of point-index arrays for each set"""
    bits = np.unpackbits(S.view(np.uint8), axis=1, bitorder='little')[:, :n]
    return bits.astype(bool)

def solve_cover(M, m=6, time_limit=600, workers=8):
    """M: bool matrix sets x points. Return list of set indices (len<=m) covering all, or None if infeasible.
    Returns 'unknown' on timeout."""
    from ortools.sat.python import cp_model
    ns, n = M.shape
    mdl = cp_model.CpModel()
    xs = [mdl.NewBoolVar(f"x{i}") for i in range(ns)]
    cols = [np.nonzero(M[:, p])[0] for p in range(n)]
    for p in range(n):
        if len(cols[p]) == 0:
            return None
        mdl.AddBoolOr([xs[i] for i in cols[p]])
    mdl.Add(sum(xs) <= m)
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = time_limit
    sol.parameters.num_workers = workers
    st = sol.Solve(mdl)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return [i for i in range(ns) if sol.Value(xs[i])]
    if st == cp_model.INFEASIBLE:
        return None
    return 'unknown'

def solve_highs(M, m=6, tl=600, threads=4):
    """min set cover via HiGHS. Returns (status, opt, dualbound, chosen_indices)."""
    import highspy
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('time_limit', float(tl))
    h.setOptionValue('threads', threads)
    ns, n = M.shape
    inf = highspy.kHighsInf
    h.addVars(ns, np.zeros(ns), np.ones(ns))
    h.changeColsIntegrality(ns, np.arange(ns, dtype=np.int32), np.array([highspy.HighsVarType.kInteger]*ns))
    h.changeColsCost(ns, np.arange(ns, dtype=np.int32), np.ones(ns))
    for p in range(n):
        idx = np.nonzero(M[:, p])[0].astype(np.int32)
        h.addRow(1, inf, len(idx), idx, np.ones(len(idx)))
    h.run()
    info = h.getInfo()
    st = str(h.getModelStatus())
    chosen = None
    try:
        x = np.array(h.getSolution().col_value)
        if len(x) == ns:
            chosen = [int(i) for i in np.nonzero(x > 0.5)[0]]
    except Exception:
        pass
    return st, info.objective_function_value, info.mip_dual_bound, chosen

def cover_status(M, m=6, tl=600):
    """'CERT' if min cover > m proven, list of chosen if a cover with <=m found, 'unknown' otherwise"""
    st, obj, db, ch = solve_highs(M, m, tl)
    if db > m + 0.5:
        return 'CERT', obj, db
    if ch is not None and len(ch) <= m and obj < m + 0.5:
        return ch, obj, db
    return 'unknown', obj, db
