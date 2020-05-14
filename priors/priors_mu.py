import pandas
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import seaborn as sns

def func(x, mu, sigma):
    fact = 1/(sigma*np.sqrt(2*np.pi))
    return fact * np.exp(-0.5 *((x-mu)/sigma)**2)

def get_data():
    df = pandas.read_csv('priors_mu.csv')
    df_sand = df.loc[df["rock_type"] == "Sand"]
    return df_sand

def fit_data(df_sand):
    popt, pcov = curve_fit(func, df_sand["mu_log10_K"], 
                           df_sand["p_mu_log10_K"], p0=[-5, 2])
    return popt

def get_random_sample(popt, sample_no):
    
    import random 
    sample = np.zeros((sample_no))
    
    for i in range(sample_no):
        sample[i] = random.gauss(popt[0], popt[1])
    return sample

#print(df)
#print(popt)
    
if __name__ == '__main__':
    
    df_sand = get_data()
    popt = fit_data(df_sand)
    sample = get_random_sample(popt, 1000)

    plt.plot(df_sand["mu_log10_K"], df_sand["p_mu_log10_K"])
    plt.plot(df_sand["mu_log10_K"], 
             func(df_sand["mu_log10_K"], popt[0], popt[1]))
    sns.distplot(sample, hist=False, rug=True)
    plt.show()
