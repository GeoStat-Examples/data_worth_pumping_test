# -*- coding: utf-8 -*-
import numpy as np
#from anaflow import thiem
from ogs5py import OGS, by_id, show_vtk, specialrange, generate_time
#from matplotlib import pyplot as plt
##from gstools import SRF, Gaussian
#from project import get_srf
    
# discretization and parameters
angles = 64
storage = 1e-4
rate = -1e-3

def init_ogs_project(rad, task_root=None):
    
    # model setup
    model = OGS(task_root="pump_3d_steady", task_id="model", output_dir="out")
    model.pcs.add_block(  # set the process type
        PCS_TYPE="GROUNDWATER_FLOW", NUM_TYPE="NEW", TIM_TYPE="STEADY"
    )

    # generate a radial 3D mesh and conductivity field
    model.msh.generate(
        "radial", dim=3, angles=angles, rad=rad, z_arr=-np.arange(11)
    )
    
    return model


def write_ogs_project(model, owell_pos, K_field, time=None):
    
    model.mpd.add(name="conductivity")
    model.mpd.add_block(  # edit recent mpd file
        MSH_TYPE="GROUNDWATER_FLOW",
        MMP_TYPE="PERMEABILITY",
        DIS_TYPE="ELEMENT",
        DATA=by_id(K_field),
    )
    model.mmp.add_block(  # permeability, storage and porosity
        GEOMETRY_DIMENSION=3, PERMEABILITY_DISTRIBUTION=model.mpd.file_name
    )
    model.gli.generate("radial", dim=3, angles=64, rad_out=100, z_size=-10)
    model.gli.add_polyline("pwell", [[0, 0, 0], [0, 0, -10]])
#    model.gli.add_polyline("owell", [[owell_pos, 0.0, 0.0], 
#                                     [owell_pos, 0, -10]])
    for srf in model.gli.SURFACE_NAMES:  # set boundary     ition
        model.bc.add_block(
            PCS_TYPE="GROUNDWATER_FLOW",
            PRIMARY_VARIABLE="HEAD",
            GEO_TYPE=["SURFACE", srf],
            DIS_TYPE=["CONSTANT", 0.0],
        )
    model.st.add_block(  # set pumping condition at the pumpingwell
        PCS_TYPE="GROUNDWATER_FLOW",
        PRIMARY_VARIABLE="HEAD",
        GEO_TYPE=["POLYLINE", "pwell"],
        DIS_TYPE=["CONSTANT_NEUMANN", rate],
    )
    model.num.add_block(  # numerical solver
        PCS_TYPE="GROUNDWATER_FLOW",
        LINEAR_SOLVER=[2, 5, 1.0e-14, 1000, 1.0, 100, 4],
    )
    model.out.add_block(  # set the outputformat
        PCS_TYPE="GROUNDWATER_FLOW",
        NOD_VALUES="HEAD",
        GEO_TYPE="DOMAIN",
        DAT_TYPE="VTK",
    )
    
    return model
