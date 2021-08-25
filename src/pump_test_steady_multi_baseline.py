# -*- coding: utf-8 -*-
import numpy as np
import welltestpy as wtp

from ogs5py import specialrange
from matplotlib import pyplot as plt
#from gstools import SRF, Gaussian
from project import get_srf, ogs_2d

# discretization and parameters
#time = specialrange(0, 7200, 50, typ="cub")
rad = specialrange(0, 1000, 100, typ="cub")
angles = 32
#storage = 1e-3
T_const = 1e-5
rate = -1e-3
    

def run_ogs_project(model):
    model.write_input()
    success = model.run_model()
    return success


def import_ogs_results(model, owell_pos):
    point = model.readtec_point(pcs="GROUNDWATER_FLOW")
    head = np.zeros((len(owell_pos)))
    for i in range(len(owell_pos)):
        head[i] = point["owell_" + str(i)]["HEAD"][1]
    return head

def campaign(model, T_field, owell_pos, pwell_pos, campaign_id = 1):
    
    owell_pos = np.array(owell_pos)
    
    field = wtp.FieldSite(name = "Pump test data worth", coordinates=[0.0, 0.0])
    campaign = wtp.Campaign(name = "Steady-multi_" + str(campaign_id), 
                            fieldsite = field)
    
    campaign.add_well(name="pwell", radius=0.1, coordinates=(pwell_pos[0][0], 
                                                             pwell_pos[0][1]))
    campaign.add_well(name="owell_0", radius=0.1, coordinates=(owell_pos[0][0], 
                                                               owell_pos[0][1]))
    campaign.add_well(name="owell_1", radius=0.1, coordinates=(owell_pos[1][0], 
                                                               owell_pos[1][1]))
    campaign.add_well(name="owell_2", radius=0.1, coordinates=(owell_pos[2][0], 
                                                               owell_pos[2][1]))
    campaign.add_well(name="owell_3", radius=0.1, coordinates=(owell_pos[3][0], 
                                                               owell_pos[3][1]))
    campaign.add_well(name="owell_4", radius=0.1, coordinates=(owell_pos[4][0], 
                                                               owell_pos[4][1]))
    campaign.add_well(name="owell_5", radius=0.1, coordinates=(owell_pos[5][0], 
                                                               owell_pos[5][1]))
    campaign.add_well(name="owell_6", radius=0.1, coordinates=(owell_pos[6][0], 
                                                               owell_pos[6][1]))
    campaign.add_well(name="owell_7", radius=0.1, coordinates=(owell_pos[7][0], 
                                                               owell_pos[7][1]))
    campaign.add_well(name="owell_8", radius=0.1, coordinates=(owell_pos[8][0], 
                                                               owell_pos[8][1]))
    
    model = ogs_2d.write_ogs_project(model, owell_pos, T_field, pwell_pos)
    succes = run_ogs_project(model)
    head = import_ogs_results(model, owell_pos)
        
    pumptest = wtp.PumpingTest(
        name="pwell",
        pumpingwell="pwell",
        pumpingrate=rate,
        description="Virtual steady-state 2d pumping test with multiple wells",
    )
    
    pumptest.add_steady_obs("owell_0", head[0])
    pumptest.add_steady_obs("owell_1", head[1])
    pumptest.add_steady_obs("owell_2", head[2])
    pumptest.add_steady_obs("owell_3", head[3])
    pumptest.add_steady_obs("owell_4", head[4])
    pumptest.add_steady_obs("owell_5", head[5])
    pumptest.add_steady_obs("owell_6", head[6])
    pumptest.add_steady_obs("owell_7", head[7])
    pumptest.add_steady_obs("owell_8", head[8])
    
    campaign.addtests(pumptest)
    campaign.save()
    
    return head
    

if __name__ == '__main__':
    
    # initialize aquifer system
    model = ogs_2d.init_ogs_project(rad, task_root="pump_2d_steady_multi")
    T_field = get_srf.get_srf_2d(model, 
                                 mean = -5, var = 1.1, len_scale = 100, 
                                 seed = 1)
    
    # run pumping test on aquifer system
    pwell_pos = [[0, 0]]
    owell_pos = [[1, 0], [3, 2], [5, 2], [0, -10], [-30, 0], [0, 50], [100, 0], [0, -250], [-500, 0]]
    head_1 = campaign(model, T_field, owell_pos, pwell_pos, campaign_id = 1)
    
    pwell_pos = [[1, 0]]
    owell_pos = [[0, 0], [3, 2], [5, 2], [0, -10], [-30, 0], [0, 50], [100, 0], [0, -250], [-500, 0]]
    head_2 = campaign(model, T_field, owell_pos, pwell_pos, campaign_id = 2)

    pwell_pos = [[3, 2]]
    owell_pos = [[1, 0], [0, 0], [5, 2], [0, -10], [-30, 0], [0, 50], [100, 0], [0, -250], [-500, 0]]
    head_3 = campaign(model, T_field, owell_pos, pwell_pos, campaign_id = 3)
    
    pwell_pos = [[5, 2]]
    owell_pos = [[1, 0], [3, 2], [0, 0], [0, -10], [-30, 0], [0, 50], [100, 0], [0, -250], [-500, 0]]
    head_4 = campaign(model, T_field, owell_pos, pwell_pos, campaign_id = 4)
    
    # plotting the results from the pumping test
    plt.plot(head_1)
    plt.plot(head_2)
    plt.plot(head_3)
    plt.plot(head_4)

    plt.show()
    
