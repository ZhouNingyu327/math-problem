import fps, numpy as np, time, highspy, sys
def solve_highs(M, m=6, tl=300):
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('time_limit', float(tl))
    h.setOptionValue('threads', 4)
    ns, n = M.shape
    inf = highspy.kHighsInf
    h.addVars(ns, np.zeros(ns), np.ones(ns))
    h.changeColsIntegrality(ns, np.arange(ns, dtype=np.int32), np.array([highspy.HighsVarType.kInteger]*ns))
    h.changeColsCost(ns, np.arange(ns, dtype=np.int32), np.ones(ns))
    for p in range(n):
        idx = np.nonzero(M[:, p])[0].astype(np.int32)
        h.addRow(1, inf, len(idx), idx, np.ones(len(idx)))
    h.run()
    st = h.getModelStatus()
    info = h.getInfo()
    return str(st), info.objective_function_value, info.mip_dual_bound
a=float(sys.argv[1]); k=int(sys.argv[2])
g=np.linspace(0,a,k); P=np.array([(x,y) for x in g for y in g])
S,s=fps.family(P,K=360); M=fps.members(S,len(P)); print(S.shape)
t=time.time(); print(solve_highs(M, tl=float(sys.argv[3])), time.time()-t)
