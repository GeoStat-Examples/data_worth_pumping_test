# -*- coding: utf-8 -*-
import numpy as np
#import anaflow as ana
from ogs5py import OGS, by_id, show_vtk, specialrange
#from matplotlib import pyplot as plt
from gstools import SRF, Gaussian


# discretization and parameters
rad = specialrange(0, 1000, 100, typ="cub")
obs = rad[21]
angles = 32
storage = 1e-3
transmissivity = 1e-4
rate = -1e-3

# covariance model for conductivity field
cov_model = Gaussian(dim=2, var=2, len_scale=100, anis=[1])
srf = SRF(model=cov_model, mean=-9, seed=1000)

# model setup
model = OGS(task_root="pump_2d_steady", task_id="model", output_dir="out")
model.pcs.add_block(
        PCS_TYPE="GROUNDWATER_FLOW", NUM_TYPE="NEW", TIM_TYPE="STEADY")

# generate a radial mesh and geometry ("boundary" polyline)
model.msh.generate("radial", dim=2, rad=rad, angles=angles)
model.gli.generate("radial", dim=2, rad_out=rad[-1], angles=angles)
model.gli.add_points([0.0, 0.0, 0.0], "pwell")

# generate a 2D conductivity field
cond = np.exp(srf.mesh(model.msh))
model.mpd.add(name="conductivity")
model.mpd.add_block(  # edit recent mpd file
    MSH_TYPE="GROUNDWATER_FLOW",
    MMP_TYPE="PERMEABILITY",
    DIS_TYPE="ELEMENT",
    DATA=by_id(cond),
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
#model.mmp.add_block(  # medium properties
#    GEOMETRY_DIMENSION=2,
#    PERMEABILITY_TENSOR=["ISOTROPIC", transmissivity],
#)
model.num.add_block(  # numerical solver
    PCS_TYPE="GROUNDWATER_FLOW",
    LINEAR_SOLVER=[2, 5, 1e-14, 1000, 1.0, 100, 4]
)
model.out.add_block(  # set the outputformat
    PCS_TYPE="GROUNDWATER_FLOW",
    NOD_VALUES="HEAD",
    GEO_TYPE="DOMAIN",
    DAT_TYPE="VTK",
)

model.write_input()
success = model.run_model()

#model.msh.show(show_cell_data={"Conductivity": cond}, log_scale=True)
files = model.output_files(pcs="GROUNDWATER_FLOW", typ="VTK")
show_vtk(files[-1], log_scale=True)  # show the last time-step
