# stat_inference.py: Statistical Inference in Python.
from __future__ import division

import numpy as np
import scipy as sp 
import pandas as pd

import scipy.stats as st

def rates_ratio_test(numA=None, numB=None, pos_numA=None, pos_numB=None, 
                     ratio_hypo=[None, 2.7], alpha=0.05):
    """Hypothesis Testing for Rates Ratio.
    
    To apply hypothesis testing for rates ratio of controlled group A over treatment group B, 
    which is derived from the `Union-Intersection Test`,
          H0: O_B / O_A = r, or
              r1 < O_B / O_A < r2, or 
              O_B / O_A < r2, or 
              O_B / O_A > r1,
      vs. H1: otherwise,
    where O_A and O_B are Overall Evaluation Criterion (OEC) in rate 
    calculated by vectors of Bernoulli r.v.'s.
    
    Args:
      numA: int, number of examples in group A.
      numB: int, number of examples in group B.
      pos_numA: int, number of positive examples in group A.
      pos_numB: int, number of positive examples in group B.
      ratio_hypo: array-like, r or [r1, r2], with r, r1 and r2 are scalars. 
        Null hypotheses for testing rates ratio.
        - if r: H0: OEC_B / OEC_A = r,
        - if [r1, r2]: H0: r1 < OEC_B / OEC_A < r2,
        - if [None, r2]: H0: OEC_B / OEC_A < r2. Default.
        - if [r1, None]: H0: OEC_B / OEC_A > r1.
      alpha: A float. Type I error with Pr(H1|H0) = alpha. Defaults to 0.05.

    Returns:
      infer_dict: A dict. Information dict.
        - infer_dict['oec_a']: OEC for group A,
        - infer_dict['oec_b']: OEC for group B,
        - infer_dict['oec_ratio']: Observed rates ratio.
        - infer_dict['ratio_hypo']: Null hypothesis.
        - infer_dict['ratio_ci']: ratio's confidence interval with lower and upper bounds, 
          [ci_l, ci_u].
        - infer_dict['reject']:
          * True: if the hypothesis is rejected,
          * False: if the hypothesis is not rejecteted.
    
    Raises:
      ValueError: Inputs are missing.
      TypeError: Null hypothesis type is incorrect.
      ValueError: Null hypothesis's both values are missing.
      ValueError: Null hypothesis is incorrect.
      ValueError: Left null hypothesis should be smaller than the right.
    """

    if ((numA is not None) & (numB is not None) & 
        (pos_numA is not None) & (pos_numB is not None)):
        pass
    else:
        raise ValueError("Inputs are missing.")

    if isinstance(ratio_hypo, list) is False:
        r1 = ratio_hypo
        r2 = ratio_hypo
    elif len(ratio_hypo) == 2:
        r1 = ratio_hypo[0]
        r2 = ratio_hypo[1]
        if (r1 is None) and (r2 is None):
            raise ValueError("Null hypothesis's both values are missing.")    
        if (r1 is not None) and (r2 is not None):
            if r1 > r2:
                raise ValueError("Left null hypothesis should be smaller than the right.")
    else:
        raise TypeError("Null hypothesis type is incorrect.")
    
    oecA = pos_numA / numA
    oecB = pos_numB / numB
    
    if (numA >= 100) and (numA >= 100) and (pos_numA >= 5) and (pos_numB >= 5):
        oec_ratio = oecB / oecA
        or_var = (1 - oecB) / (numB * oecB) + (1 - oecA) / (numA * oecA)
        or_stdev = np.power(or_var, 0.5)
    
        if (r1 is not None) and (r2 is not None):
            z = st.norm.ppf(1 - alpha / 2)
            ci_l = np.exp(np.log(r1) - z * or_stdev)
            ci_u = np.exp(np.log(r2) + z * or_stdev)
        elif (r1 is None) and (r2 is not None):
            z = st.norm.ppf(1 - alpha)
            ci_l = -np.inf
            ci_u = np.exp(np.log(r2) + z * or_stdev)
        elif (r1 is not None) and (r2 is None):
            z = st.norm.ppf(1 - alpha)
            ci_l = np.exp(np.log(r1) - z * or_stdev)
            ci_u = np.inf
        else:
            pass
        
        if (oec_ratio < ci_l) | (oec_ratio > ci_u):
            reject = True
        else:
            reject = False
    else:
        oec_ratio = None
        ratio_ci = None
        reject = False
   
    rates_ratio_test_d = {
        'oec_a': oecA,
        'oec_b': oecB,
        'oec_ratio': oec_ratio,
        'ratio_hypo': str(ratio_hypo),
        'ratio_ci': str([ci_l, ci_u]),
        'reject': reject
    }

    return rates_ratio_test_d
