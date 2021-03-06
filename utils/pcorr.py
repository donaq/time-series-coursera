import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as sts
from scipy import stats, linalg

def pcorr(C):
    """
    Returns the sample linear partial correlation coefficients between pairs of variables in C, controlling 
    for the remaining variables in C.
    Parameters
    ----------
    C : array-like, shape (n, p)
        Array with the different variables. Each column of C is taken as a variable
    Returns
    -------
    P : array-like, shape (p, p)
        P[i, j] contains the partial correlation of C[:, i] and C[:, j] controlling
        for the remaining variables in C.
    """
    
    C = np.asarray(C)
    p = C.shape[1]
    P_corr = np.zeros((p, p), dtype=np.float)
    for i in range(p):
        P_corr[i, i] = 1
        for j in range(i+1, p):
            idx = np.ones(p, dtype=np.bool)
            idx[i] = False
            idx[j] = False
            beta_i = linalg.lstsq(C[:, idx], C[:, j])[0]
            beta_j = linalg.lstsq(C[:, idx], C[:, i])[0]

            res_j = C[:, j] - C[:, idx].dot( beta_i)
            res_i = C[:, i] - C[:, idx].dot(beta_j)
            
            corr = stats.pearsonr(res_i, res_j)[0]
            P_corr[i, j] = corr
            P_corr[j, i] = corr
        
    return P_corr

def acf_df(dat, mode="correlation", nlags=40):
    """returns acf,aconv,pacf dataframe"""
    if mode=="covariance":
        vals = sts.acovf(dat) # nlag arg does not exist in v0.9.0
    elif mode=="correlation":
        vals = sts.acf(dat, nlags=nlags)
    elif mode=="pacf":
        vals = sts.pacf(dat, nlags=nlags)

    else:
        raise Exception("wtf")

    return pd.DataFrame(np.array([np.array(range(len(vals))),vals]).T,columns=["lag","values"])
