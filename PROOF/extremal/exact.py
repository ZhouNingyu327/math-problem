"""Exact minimum covering depth min_{x in S_a} max_i d_i(x) for 6 unit squares (floating point, exact enumeration
of candidate vertices of the piecewise-linear depth landscape). d_i(x)=min_k (1/2 - n_ik.(x-c_i))."""
import numpy as np, itertools

def pieces(P):
    N = []; B = []; T = []
    for i, (cx, cy, th) in enumerate(P):
        for k in range(4):
            ang = th + k*np.pi/2; n = np.array([np.cos(ang), np.sin(ang)])
            N.append(n); B.append(0.5 + n @ np.array([cx, cy])); T.append(i)
    return np.array(N), np.array(B), np.array(T)  # L(x) = B - N.x

def mdepth(P, X):
    N, B, T = pieces(P)
    L = B[None, :] - X @ N.T            # (M,24)
    D = L.reshape(len(X), 6, 4).min(2)  # (M,6)
    return D.max(1), D.argmax(1)

def candidates(P, a):
    N, B, T = pieces(P)
    # side lines as pieces with 'L' = distance constraint: x=0,x=a,y=0,y=a represented as lines n.x=b
    sides = [(np.array([1., 0]), 0.), (np.array([1., 0]), a), (np.array([0., 1]), 0.), (np.array([0., 1]), a)]
    pts = [np.array([0., 0]), np.array([a, 0]), np.array([0, a]), np.array([a, a])]
    idx = range(24)
    # triples: L_p = L_q = L_r  -> (N_p - N_q).x = B_p - B_q, (N_p - N_r).x = B_p - B_r
    tri = np.array(list(itertools.combinations(idx, 3)))
    A1 = N[tri[:, 0]] - N[tri[:, 1]]; A2 = N[tri[:, 0]] - N[tri[:, 2]]
    b1 = B[tri[:, 0]] - B[tri[:, 1]]; b2 = B[tri[:, 0]] - B[tri[:, 2]]
    det = A1[:, 0]*A2[:, 1] - A1[:, 1]*A2[:, 0]
    ok = np.abs(det) > 1e-12
    x = (b1*A2[:, 1] - b2*A1[:, 1])[ok]/det[ok]; y = (A1[:, 0]*b2 - A2[:, 0]*b1)[ok]/det[ok]
    X = [np.stack([x, y], 1)]
    pair = np.array(list(itertools.combinations(idx, 2)))
    for (sn, sb) in sides:
        A1 = N[pair[:, 0]] - N[pair[:, 1]]; b1 = B[pair[:, 0]] - B[pair[:, 1]]
        det = A1[:, 0]*sn[1] - A1[:, 1]*sn[0]; ok = np.abs(det) > 1e-12
        x = (b1*sn[1] - sb*A1[:, 1])[ok]/det[ok]; y = (A1[:, 0]*sb - sn[0]*b1)[ok]/det[ok]
        X.append(np.stack([x, y], 1))
    X.append(np.array(pts))
    X = np.concatenate(X)
    e = 1e-12
    X = X[(X[:, 0] >= -e) & (X[:, 0] <= a+e) & (X[:, 1] >= -e) & (X[:, 1] <= a+e)]
    return np.clip(X, 0, a)

def min_depth(P, a, k=1):
    X = candidates(P, a)
    m, am = mdepth(P, X)
    o = np.argsort(m)
    return m[o[0]], X[o[:k]], m[o[:k]]
