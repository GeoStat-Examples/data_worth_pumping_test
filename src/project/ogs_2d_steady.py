# -*- coding: utf-8 -*-
import numpy as np
#from anaflow import thiem
from ogs5py import OGS, by_id, show_vtk, specialrange
#from matplotlib import pyplot as plt
##from gstools import SRF, Gaussian
from project import get_srf
    
# discretization and parameters
rad = specialrange(0, 1000, 100, typ="cub")
angles = 32
#storage = 1e-3
transmissivity = 1e-4
rate = -1e-3
owell_pos = [6, 11, 16, 21, 31, 41, 51, 61, 71, 81]
#owell_pos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def init_ogs_project():
    
    # model setup
    model = OGS(task_root="pump_2d_steady", task_id="model", output_dir="out")
    model.pcs.add_block(PCS_TYPE="GROUNDWATER_FLOW", 
                        NUM_TYPE="NEW", 
                        TIM_TYPE="STEADY")

    # generate a radial mesh and geometry ("boundary" polyline)
    model.msh.generate("radial", dim=2, rad=rad, angles=angles)
    model.gli.generate("radial", dim=2, rad_out=rad[-1], angles=angles)
    model.gli.add_points([0.0, 0.0, 0.0], "pwell")
    for i in range(len(owell_pos)):
        model.gli.add_points([rad[owell_pos[i]], 0.0, 0.0], "owell_" + str(i))
    
    return model


def write_ogs_project(model, transmissivity):

    
    if isinstance(transmissivity, float):
        model.mmp.add_block(  # medium properties
                GEOMETRY_DIMENSION=2,
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
    model.mmp.add_block(  # permeability, storage and porosity
            GEOMETRY_DIMENSION=2, PERMEABILITY_DISTRIBUTION=model.mpd.file_name
    )
    model.num.add_block(  # numerical solver
            PCS_TYPE="GROUNDWATER_FLOW",
            LINEAR_SOLVER=[2, 5, 1e-14, 1000, 1.0, 100, 4]
    )
    #model.out.add_block(  # set the outputformat
    #    PCS_TYPE="GROUNDWATER_FLOW",
    #    NOD_VALUES="HEAD",
    #    GEO_TYPE="DOMAIN",
    #    DAT_TYPE="VTK",
    #)
    for i in range(len(owell_pos)):
        model.out.add_block(  # point observation
        PCS_TYPE="GROUNDWATER_FLOW",
        NOD_VALUES="HEAD",
        GEO_TYPE=["POINT", "owell_" + str(i)],
        DAT_TYPE="TECPLOT",
        )
    
    return model
