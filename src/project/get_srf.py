# -*- coding: utf-8 -*-
import numpy as np
from gstools import SRF, Gaussian


def get_srf_2d(model, mean = None, var = None, len_scale = None):
    
    # covariance model for conductivity field
    cov_model = Gaussian(dim=2, var=var, len_scale=len_scale, anis=[1])
    srf = SRF(model=cov_model, mean=mean, seed=1000)
    cond = np.exp(srf.mesh(model.msh))
    
    return cond

