# -*- coding: utf-8 -*-
import numpy as np
import welltestpy as wtp
import seaborn as sns

from ogs5py import specialrange
from matplotlib import pyplot as plt
#from gstools import SRF, Gaussian
from project import get_srf, ogs_2d, priors, io

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

def campaign(model, T_field, owell_pos, pwell_pos):
    
    owell_pos = np.array(owell_pos)
    
    model = ogs_2d.write_ogs_project(model, owell_pos, T_field, pwell_pos)
    succes = run_ogs_project(model)
    head = import_ogs_results(model, owell_pos)
    
    return head


def get_glue(model, my_priors, head_1, head_2, head_3, head_4):
    
    cmp = wtp.load_campaign("Cmp_Steady-multi_1.cmp")
    head_base_1 = np.zeros((9))
    for i in range(9):
        head_base_1[i] = cmp.tests["pwell"].observations["owell_" + str(i)].observation
    cmp = wtp.load_campaign("Cmp_Steady-multi_2.cmp")
    head_base_2 = np.zeros((9))
    for i in range(9):
        head_base_2[i] = cmp.tests["pwell"].observations["owell_" + str(i)].observation
    cmp = wtp.load_campaign("Cmp_Steady-multi_3.cmp")
    head_base_3 = np.zeros((9))
    for i in range(9):
        head_base_3[i] = cmp.tests["pwell"].observations["owell_" + str(i)].observation
    cmp = wtp.load_campaign("Cmp_Steady-multi_4.cmp")
    head_base_4 = np.zeros((9))
    for i in range(9):
        head_base_4[i] = cmp.tests["pwell"].observations["owell_" + str(i)].observation

    glue = np.sum((head_1 - head_base_1)**2)
    glue = glue + np.sum((head_2 - head_base_2)**2)
    glue = glue + np.sum((head_3 - head_base_3)**2)
    glue = glue + np.sum((head_4 - head_base_4)**2)  

#    plt.plot(head_base_1)
#    plt.plot(head_base_2)
#    plt.plot(head_base_3)
#    plt.plot(head_base_4)
#    plt.plot(head_1)
#    plt.plot(head_2)
#    plt.plot(head_3)
#    plt.plot(head_4)
#    plt.show()
    
    return glue
    

if __name__ == '__main__':
    
    pwell_pos_1 = [[0, 0]]
    owell_pos_1 = [[1, 0], [3, 2], [5, 2], [0, -10], [-30, 0], [0, 50], [100, 0], [0, -250], [-500, 0]]
    pwell_pos_2 = [[1, 0]]
    owell_pos_2 = [[0, 0], [3, 2], [5, 2], [0, -10], [-30, 0], [0, 50], [100, 0], [0, -250], [-500, 0]]
    pwell_pos_3 = [[3, 2]]
    owell_pos_3 = [[1, 0], [0, 0], [5, 2], [0, -10], [-30, 0], [0, 50], [100, 0], [0, -250], [-500, 0]]
    pwell_pos_4 = [[5, 2]]
    owell_pos_4 = [[1, 0], [3, 2], [0, 0], [0, -10], [-30, 0], [0, 50], [100, 0], [0, -250], [-500, 0]]
    
    i_no = 1000000
    glue = np.zeros(i_no)
    my_path = '../results/posterior_steady_multi.csv'
    io.save_posteriors(path=my_path)
    
    for i in range(i_no):
        # initialize aquifer system
        model = ogs_2d.init_ogs_project(rad, task_root="pump_2d_steady_multi")
        my_priors = priors.get_priors(sample_no=1)
        T_field = get_srf.get_srf_2d(model, 
                                     mean=my_priors[0], var=my_priors[1],
                                     len_scale=my_priors[2])
    
        # run pumping test on aquifer system
        head_1 = campaign(model, T_field, owell_pos_1, pwell_pos_1)
        head_2 = campaign(model, T_field, owell_pos_2, pwell_pos_2)
        head_3 = campaign(model, T_field, owell_pos_3, pwell_pos_3)
        head_4 = campaign(model, T_field, owell_pos_4, pwell_pos_4)
        
    
        glue[i] = get_glue(model, my_priors, head_1, head_2, head_3, head_4)
        
        if glue[i] < 4*250:
            head = np.zeros((4*9))
            head[0:9] = head_1
            head[9:18] = head_2
            head[18:27] = head_3
            head[27:36] = head_4
            df = io.save_posteriors(path=my_path, data=head,
                                    my_priors=my_priors, init=False)
    
    sns.distplot(glue, hist=False, rug=True)
    
