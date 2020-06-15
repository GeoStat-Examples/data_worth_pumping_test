# -*- coding: utf-8 -*-
import numpy as np
#from anaflow import thiem
from ogs5py import OGS, by_id, show_vtk, specialrange, generate_time
#from matplotlib import pyplot as plt
##from gstools import SRF, Gaussian
from project import get_srf
    
# discretization and parameters
angles = 64
storage = 1e-4
rate = -1e-3

def init_ogs_project(rad, task_root=None):
    
    model = OGS(task_root=task_root, task_id="model", output_dir="out")
    if task_root=="pump_2d_steady":
        model.pcs.add_block(PCS_TYPE="GROUNDWATER_FLOW", 
                            NUM_TYPE="NEW",
                            TIM_TYPE="STEADY")
    else:
        model.pcs.add_block(PCS_TYPE="GROUNDWATER_FLOW", 
                            NUM_TYPE="NEW")

    # generate a radial mesh and geometry ("boundary" polyline)
    model.msh.generate("radial", dim=2, rad=rad, angles=angles)
    model.gli.generate("radial", dim=2, rad_out=rad[-1], angles=angles)
    
    return model

def write_ogs_project(model, owell_pos, transmissivity, time=None):
      
    model.bc.add_block(  # boundary condition
        PCS_TYPE="GROUNDWATER_FLOW",
        PRIMARY_VARIABLE="HEAD",
        GEO_TYPE=["POLYLINE", "boundary"],
        DIS_TYPE=["CONSTANT", 0.0],
    )
    model.st.add_block(  # source term
        PCS_TYPE="GROUNDWATER_FLOW",
        PRIMARY_VARIABLE="HEAD",
        GEO_TYPE=["POINT", "pwell"],
        DIS_TYPE=["CONSTANT_NEUMANN", rate],
    )
    model.num.add_block(  # numerical solver
        PCS_TYPE="GROUNDWATER_FLOW",
        LINEAR_SOLVER=[2, 5, 1e-14, 1000, 1.0, 100, 4]
    )
    
    if isinstance(transmissivity, float):
        model.mmp.add_block(  # medium properties
            GEOMETRY_DIMENSION=2,
            STORAGE=[1, storage],
            PERMEABILITY_TENSOR=["ISOTROPIC", transmissivity],
        )
    else:
        model.mpd.add(name="conductivity")
        model.mpd.add_block(  # edit recent mpd file
            MSH_TYPE="GROUNDWATER_FLOW",
            MMP_TYPE="PERMEABILITY",
            DIS_TYPE="ELEMENT",
            DATA=by_id(transmissivity),
        )
        model.mmp.add_block(  # permeability, storage and porosity
            GEOMETRY_DIMENSION=2, 
            STORAGE=[1, storage],
            PERMEABILITY_DISTRIBUTION=model.mpd.file_name
        )
    
    if model.task_root=="pump_2d_steady":
        model = add_steady_files(model, owell_pos, transmissivity)
    else:
        model = add_trans_files(model, owell_pos, transmissivity, time)
    
    return model


def add_steady_files(model, owell_pos, transmissivity):
        
    model.gli.add_points([0.0, 0.0, 0.0], "pwell")
    for i in range(len(owell_pos)):
        model.gli.add_points([owell_pos[i], 0.0, 0.0], "owell_" + str(i))

    for i in range(len(owell_pos)):
        model.out.add_block(  # point observation
        PCS_TYPE="GROUNDWATER_FLOW",
        NOD_VALUES="HEAD",
        GEO_TYPE=["POINT", "owell_" + str(i)],
        DAT_TYPE="TECPLOT",
        )
   
    return model

def add_trans_files(model, owell_pos, transmissivity, time):
        
    model.gli.add_points([0.0, 0.0, 0.0], "pwell")
    model.gli.add_points([owell_pos, 0.0, 0.0], "owell")
        
    model.ic.add_block(  # initial condition
        PCS_TYPE="GROUNDWATER_FLOW",
        PRIMARY_VARIABLE="HEAD",
        GEO_TYPE="DOMAIN",
        DIS_TYPE=["CONSTANT", 0.0],
    )
    model.out.add_block(  # point observation
        PCS_TYPE="GROUNDWATER_FLOW",
        NOD_VALUES="HEAD",
        GEO_TYPE=["POINT", "owell"],
        DAT_TYPE="TECPLOT",
    )
    model.tim.add_block(  # set the timesteps
        PCS_TYPE="GROUNDWATER_FLOW",
        **generate_time(time)  # generate input from time-series
    )
    
    return model

