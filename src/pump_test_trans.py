# -*- coding: utf-8 -*-
import numpy as np
import welltestpy as wtp
import seaborn as sns
import pandas as pd

from anaflow import thiem
from ogs5py import specialrange
from matplotlib import pyplot as plt
#from gstools import SRF, Gaussian
from project import get_srf, ogs_2d, priors, io
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


def get_glue(model, my_priors):
    
    head = np.zeros((9*50))
    
    head_0, time_0 = import_ogs_results(model, owell_name = "owell_0")
    head_1, time_1 = import_ogs_results(model, owell_name = "owell_1")
    head_2, time_2 = import_ogs_results(model, owell_name = "owell_2")
    head_3, time_3 = import_ogs_results(model, owell_name = "owell_3")
    head_4, time_4 = import_ogs_results(model, owell_name = "owell_4")
    head_5, time_5 = import_ogs_results(model, owell_name = "owell_5")
    head_6, time_6 = import_ogs_results(model, owell_name = "owell_6")
    head_7, time_7 = import_ogs_results(model, owell_name = "owell_7")
    head_8, time_8 = import_ogs_results(model, owell_name = "owell_8")
    
    cmp = wtp.load_campaign("../data/Cmp_Transient-multi.cmp")
    head_base_0 = cmp.tests["pwell"].observations["owell_0"].observation
    head_base_1 = cmp.tests["pwell"].observations["owell_1"].observation
    head_base_2 = cmp.tests["pwell"].observations["owell_2"].observation
    head_base_3 = cmp.tests["pwell"].observations["owell_3"].observation
    head_base_4 = cmp.tests["pwell"].observations["owell_4"].observation
    head_base_5 = cmp.tests["pwell"].observations["owell_5"].observation
    head_base_6 = cmp.tests["pwell"].observations["owell_6"].observation
    head_base_7 = cmp.tests["pwell"].observations["owell_7"].observation
    head_base_8 = cmp.tests["pwell"].observations["owell_8"].observation
    
    glue = np.sum((head_0 - head_base_0)**2)
    glue = glue + np.sum((head_1 - head_base_1)**2)
    glue = glue + np.sum((head_2 - head_base_2)**2)
    glue = glue + np.sum((head_3 - head_base_3)**2)
    glue = glue + np.sum((head_4 - head_base_4)**2)
    glue = glue + np.sum((head_5 - head_base_5)**2)
    glue = glue + np.sum((head_6 - head_base_6)**2)
    glue = glue + np.sum((head_7 - head_base_7)**2)
    glue = glue + np.sum((head_8 - head_base_8)**2)
    
    head[0:50] = head_0
    head[50:100] = head_1
    head[100:150] = head_2
    head[150:200] = head_3
    head[200:250] = head_4
    head[250:300] = head_5
    head[300:350] = head_6
    head[350:400] = head_7
    head[400:450] = head_8
    
    my_path = '../results/posterior_trans.csv'
    if glue < 9*250:
        df = io.save_posteriors(path=my_path, data=head,
                                my_priors=my_priors, init=False)
    
#    plt.plot(time_0, head_0)
#    plt.plot(time_1, head_1)
#    plt.plot(time_2, head_2)
#    plt.plot(time_3, head_3)
#    plt.plot(time_4, head_4)
#    plt.plot(time_5, head_5)
#    plt.plot(time_6, head_6)
    
#    plt.plot(time_0, head_base_0)
#    plt.plot(time_1, head_base_1)
#    plt.plot(time_2, head_base_2)
#    plt.plot(time_3, head_base_3)
#    plt.plot(time_4, head_base_4)
#    plt.plot(time_5, head_base_5)
#    plt.plot(time_6, head_base_6)
    
#    plt.show()
    
    return glue
    

def my_fit_func(xdata, T_const):
    return thiem(xdata, 1000, T_const, rate = -1e-3, h_ref=0.0)


def fit_results(xdata, ydata):
    popt, pcov = curve_fit(my_fit_func, xdata, ydata, bounds=([0],[1]))
    return popt

#def save_posteriors(path, data=[], my_priors=[], init=True):
#    
#    columns=['mu','sigma', 'len_scale']
#    for i in range(10):
#        columns.append('data_' + str(i))
#    df = pd.DataFrame(columns=columns)
#    my_file = Path(path)
#    if not my_file.is_file():
#        df.to_csv(path)
#    if not init:
#        row = {'mu' : my_priors[0][0], 
#               'sigma' : my_priors[1][0], 
#               'len_scale' : my_priors[2][0]}
#        for i in range(10):
#            row['data_' + str(i)] = data[i]
#        df = df.append(row, ignore_index=True)
#        df.to_csv(my_path, mode = 'a', header=False)
#        #del df
#    return df
    


if __name__ == '__main__':
    
    owell_pos = [[1, 0], [3, 2], [5, 2], [0, -10], [-30, 0], [0, 50], [100, 0], [0, -250], [-500, 0]]
    owell_pos = np.array(owell_pos)
    
    i_no = 100000
    glue = np.zeros(i_no)
    my_path = '../results/posterior_trans.csv'
    io.save_posteriors(path=my_path)
    
    for i in range(i_no):
        my_priors = priors.get_priors(sample_no=1)
        model = ogs_2d.init_ogs_project(rad, task_root="pump_2d_trans")
        T_field = get_srf.get_srf_2d(model, mean=my_priors[0], var=my_priors[1],
                                     len_scale=my_priors[2])
        model = ogs_2d.write_ogs_project(model, owell_pos, T_field, time=time)
        succes = run_ogs_project(model)
    
        glue[i] = get_glue(model, my_priors)
    
    sns.distplot(glue, hist=False, rug=True)
    
