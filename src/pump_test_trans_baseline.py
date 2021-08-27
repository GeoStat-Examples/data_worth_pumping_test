# -*- coding: utf-8 -*-
import numpy as np
import welltestpy as wtp
import seaborn as sns
import pandas as pd

from anaflow import thiem
from ogs5py import specialrange
from matplotlib import pyplot as plt
#from gstools import SRF, Gaussian
from project import get_srf, ogs_2d, priors
from scipy.optimize import curve_fit
from pathlib import Path

# discretization and parameters
time = specialrange(0, 7200, 50, typ="cub")
rad = specialrange(0, 1000, 100, typ="cub")
angles = 32
#storage = 1e-3
T_const = 1e-5
rate = -1e-3
well_pos = rad[[0, 6, 11, 16, 21, 31, 41, 51, 61, 71, 81]]
pwell_pos = np.array([well_pos[0], 0.0])
owell_pos = well_pos[1:]
    

def run_ogs_project(model):
    model.write_input()
    success = model.run_model()
    return success


def import_ogs_results(model, owell_name = "owell"):
    point = model.readtec_point(pcs="GROUNDWATER_FLOW")
    time = point[owell_name]["TIME"]
    head = point[owell_name]["HEAD"]
    return head, time
    

if __name__ == '__main__':
    
    owell_pos = [[1, 0], [3, 2], [5, 2], [0, -10], [-30, 0], [0, 50], [100, 0], [0, -250], [-500, 0]]
    owell_pos = np.array(owell_pos)
    
    field = wtp.FieldSite(name="Pump test data worth", coordinates=[51.353839, 12.431385])
    campaign = wtp.Campaign(name="Transient-multi", fieldsite=field)
    
    campaign.add_well(name="pwell", radius=0.1, coordinates=(0.0, 0.0))
    campaign.add_well(name="owell_0", radius=0.1, coordinates=(1.0, 0.0))
    campaign.add_well(name="owell_1", radius=0.1, coordinates=(3.0, 2.0))
    campaign.add_well(name="owell_2", radius=0.1, coordinates=(5.0, 2.0))
    campaign.add_well(name="owell_3", radius=0.1, coordinates=(0, -10.0))
    campaign.add_well(name="owell_4", radius=0.1, coordinates=(-30, 0.0))
    campaign.add_well(name="owell_5", radius=0.1, coordinates=(0, 50.0))
    campaign.add_well(name="owell_6", radius=0.1, coordinates=(100, 0.0))
    campaign.add_well(name="owell_7", radius=0.1, coordinates=(0, -250))
    campaign.add_well(name="owell_8", radius=0.1, coordinates=(-500, 0))
    
#    campaign.plot_wells()
    
    model = ogs_2d.init_ogs_project(rad, task_root="pump_2d_trans")
    T_field = get_srf.get_srf_2d(model, 
                                 mean = -5, var = 1.1, len_scale = 100, seed = 1)
    model = ogs_2d.write_ogs_project(model, owell_pos, T_field, time=time)
    succes = run_ogs_project(model)
    
    head_0, time_0 = import_ogs_results(model, owell_name = "owell_0")
    head_1, time_1 = import_ogs_results(model, owell_name = "owell_1")
    head_2, time_2 = import_ogs_results(model, owell_name = "owell_2")
    head_3, time_3 = import_ogs_results(model, owell_name = "owell_3")
    head_4, time_4 = import_ogs_results(model, owell_name = "owell_4")
    head_5, time_5 = import_ogs_results(model, owell_name = "owell_5")
    head_6, time_6 = import_ogs_results(model, owell_name = "owell_6")
    head_7, time_7 = import_ogs_results(model, owell_name = "owell_7")
    head_8, time_8 = import_ogs_results(model, owell_name = "owell_8")
    
    pumptest = wtp.PumpingTest(
        name="pwell",
        pumpingwell="pwell",
        pumpingrate=rate,
        description="Virtual transient 2d pumping test",
    )
    
    pumptest.add_transient_obs("owell_0", time_0, head_0)
    pumptest.add_transient_obs("owell_1", time_1, head_1)
    pumptest.add_transient_obs("owell_2", time_2, head_2)
    pumptest.add_transient_obs("owell_3", time_3, head_3)
    pumptest.add_transient_obs("owell_4", time_4, head_4)
    pumptest.add_transient_obs("owell_5", time_5, head_5)
    pumptest.add_transient_obs("owell_6", time_6, head_6)
    pumptest.add_transient_obs("owell_7", time_7, head_7)
    pumptest.add_transient_obs("owell_8", time_8, head_8)
    
    campaign.addtests(pumptest)
    campaign.save(path = "../data/")
    
    plt.plot(time_0, head_0)
    plt.plot(time_1, head_1)
    plt.plot(time_2, head_2)
    plt.plot(time_3, head_3)
    plt.plot(time_4, head_4)
    plt.plot(time_5, head_5)
    plt.plot(time_6, head_6)
    plt.plot(time_7, head_7)
    plt.plot(time_8, head_8)
    plt.show()
    
    
#    print(head_0)
