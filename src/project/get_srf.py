# -*- coding: utf-8 -*-
import numpy as np
from gstools import SRF, Gaussian


def get_srf_2d(model, mean = None, var = None, len_scale = None, seed=None):
    
    #init field
    T_field = np.zeros((len(model.msh.centroids_flat[:,0])))
    
    # covariance model for conductivity field
    mean = mean/np.log10(2.71828)
    cov_model = Gaussian(dim=3, var=var, len_scale=len_scale, anis=[1, 1])
    srf = SRF(model=cov_model, mean=mean, seed=seed)
#    print(np.mean(srf.mesh(model.msh)))
#    T_field = np.exp(srf.mesh(model.msh))
    for i in range(10):
        incr = 1
        T_field = T_field + np.exp(srf((model.msh.centroids_flat[:,0],
                                        model.msh.centroids_flat[:,1],
                                        model.msh.centroids_flat[:,2]+i*incr), 
                                       mesh_type='unstructured'))
#    print(np.mean(T_field))
    return T_field

def get_srf_3d(model, mean = None, var = None, len_scale = None):
    
    # covariance model for conductivity field
#    print(mean)
    mean = mean/np.log10(2.71828)
#    print(mean)
    cov_model = Gaussian(dim=3, var=2, len_scale=10, anis=[1, 0.2])
    srf = SRF(model=cov_model, mean=-9, seed=1000)
#    print(np.mean(srf.mesh(model.msh)))
    cond = np.exp(srf.mesh(model.msh))
#    print(np.mean(cond))
    return cond
