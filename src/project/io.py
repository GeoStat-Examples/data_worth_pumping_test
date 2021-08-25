# -*- coding: utf-8 -*-
import numpy as np
from scipy.spatial import distance
import pandas as pd
from pathlib import Path
#from anaflow import thiem
#from ogs5py import OGS, MSH
#from matplotlib import pyplot as plt
##from gstools import SRF, Gaussian
#from project import get_srf


def save_posteriors(path, data=[], my_priors=[], init=True):
    
#    data_no = 9
    data_no = len(data)
    columns=['mu','sigma', 'len_scale']
    for i in range(data_no):
        columns.append('data_' + str(i))
    df = pd.DataFrame(columns=columns)
    my_file = Path(path)
    if not my_file.is_file():
        df.to_csv(path)
    if not init:
        row = {'mu' : my_priors[0][0], 
               'sigma' : my_priors[1][0], 
               'len_scale' : my_priors[2][0]}
        for i in range(data_no):
            row['data_' + str(i)] = data[i]
        df = df.append(row, ignore_index=True)
        df.to_csv(path, mode = 'a', header=False)
        #del df
    return df

def import_ss_ogs_results(model, well_pos, owell_pos, pwell_pos):
    
    well_no = len(well_pos)
    owell_no = well_no - 1
    owell_rad = np.zeros((owell_no))
    head = np.zeros((owell_no))
    
    n = 0
    for i in range(well_no):
        if owell_pos[i]:
            owell_rad[n] = distance.euclidean(well_pos[pwell_pos[0]], 
                                              well_pos[i])
            n = n+1
    
    point = model.readtec_point(pcs="GROUNDWATER_FLOW")
#    print(owell_rad)
#    print(point)
    for i in range(owell_no):
        head[i] = point["well_" + str(i+1)]["HEAD"][1]
    return head, owell_rad
