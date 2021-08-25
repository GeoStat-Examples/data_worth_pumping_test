# -*- coding: utf-8 -*-
import numpy as np
#from anaflow import thiem
from ogs5py import OGS, MSH
#from matplotlib import pyplot as plt
##from gstools import SRF, Gaussian
from project import get_srf
    
# discretization and parameters
#angles = 64
#storage = 1e-4
#rate = -1e-3

def create_mesh(model):
    
    ###############################################################################
    # Generate mesh
    
    inner_mesh = MSH()
    inner_mesh.generate(
            "grid_adapter2D",  # adapter  generator
            out_dim=(500.0, 500.0),  # outer dimension
            in_dim=(100.0, 100.0),  # inner dimension
            out_res=(20.0, 20.0),  # outer x−y resolution
            in_res=(1.0, 1.0),  # inner x−y resolution
            out_pos=(-250.0, -250.0),  # outer  block  position
            in_pos=(-50.0, -50.0),  # inner  block  position
            out_mat=0,        # outer  material ID
            in_mat=0,        # inner  material ID
            fill=True,        # fill  the  inner  block
    )   
    model.msh.generate(
            "grid_adapter2D",  # adapter  generator
            out_dim=(5000.0, 5000.0),  # outer dimension
            in_dim=(500.0, 500.0),  # inner dimension
            out_res=(1000.0, 1000.0),  # outer x−y resolution
            in_res=(20.0, 20.0),  # inner x−y resolution
            out_pos=(-2500.0, -2500.0),  # outer  block  position
            in_pos=(-250.0, -250.0),  # inner  block  position
            out_mat=0,        # outer  material ID
            in_mat=0,        # inner  material ID
            fill=False,        # fill  the  inner  block
    )
    model.msh.combine_mesh(inner_mesh)
    #my_mesh = model.msh.centroids_flat
    
    return model