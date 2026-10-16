"""Parallel exact DFS: split at the root over the candidate sets of the rarest point (complete: that point must be covered
by some chosen set; at the root every family member is maximal, so all candidates are tried). Same _dfs as exactdfs.py.
usage: pardfs.py cert.json K slack nproc"""
import fps, exactdfs, numpy as np, json, sys, time
from multiprocessing import Pool
G = {}
def work(j):
    S, indptr, idx, compat, order, n, W = G['S'], G['indptr'], G['idx'], G['compat'], G['order'], G['n'], G['W']
    st = np.zeros(2, np.int64); t = time.time()
    found = exactdfs._dfs(S, indptr, idx, compat, order, S[j].copy(), 1, 6, n, W, st)
    return j, bool(found), int(st[0]), round(time.time() - t, 1)
if __name__ == '__main__':
    d = json.load(open(sys.argv[1])); K = int(sys.argv[2]); sl = float(sys.argv[3]); npr = int(sys.argv[4])
    P = np.array(d['P'], float); n = len(P)
    S, s = fps.family(P, K=K, slack=sl); W = S.shape[1]
    bits = fps.members(S, n); cnt = bits.sum(0)
    indptr = np.zeros(n + 1, np.int64); indptr[1:] = np.cumsum(cnt)
    idx = np.concatenate([np.nonzero(bits[:, p])[0] for p in range(n)]).astype(np.int64)
    B = bits.astype(np.float32); compat = (B.T @ B) > 0.5
    order = np.argsort(cnt, kind='stable').astype(np.int64)
    G.update(S=S, indptr=indptr, idx=idx, compat=compat, order=order, n=n, W=W)
    p = int(order[0]); cands = list(idx[indptr[p]:indptr[p+1]])
    print(f"a={d['a']} n={n} |F|={len(S)} s={s:.9f} root point {p} {P[p]} with {len(cands)} candidate sets", flush=True)
    t0 = time.time(); tot = 0; anyfound = False
    with Pool(npr) as pool:
        for k, (j, f, nodes, dt) in enumerate(pool.imap_unordered(work, cands)):
            tot += nodes; anyfound |= f
            print(f"  [{k+1}/{len(cands)}] set {j}: {'COVER FOUND' if f else 'no cover'} nodes={nodes} {dt}s", flush=True)
    print("EXACT PARALLEL DFS:", "A 6-COVER OF P EXISTS" if anyfound else "NO 6 SETS COVER P", f"total nodes {tot}, wall {time.time()-t0:.1f}s", flush=True)
