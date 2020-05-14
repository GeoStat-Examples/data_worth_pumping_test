import pandas
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns
from scipy import stats
from statsmodels.nonparametric.kde import KDEUnivariate
from scipy.optimize import curve_fit

def kde_statsmodels_u(x, x_grid, bandwidth=0.2, **kwargs):
    """Univariate Kernel Density Estimation with Statsmodels"""
    kde = KDEUnivariate(x)
    kde.fit(bw=bandwidth, **kwargs)
    return kde.evaluate(x_grid)

def func(x, mu, sigma):
    return 1/(sigma*np.sqrt(2*np.pi)) * np.exp(-0.5 *((x-mu)/sigma)**2)

def func_2(x, mu_1, sigma_1, mu_2, sigma_2, theta):
    func_1 = 1/(sigma_1*np.sqrt(2*np.pi)) * np.exp(-0.5 *((x-mu_1)/sigma_1)**2)
    func_2 = 1/(sigma_2*np.sqrt(2*np.pi)) * np.exp(-0.5 *((x-mu_2)/sigma_2)**2)
    return theta*func_1 + (1-theta)*func_2

def get_data():
    df = pandas.read_csv('priors_lambda.csv')

    x = np.log(np.array(df["lambda_horizontal"]))
    x = x[~np.isnan(x)]
    x = x.reshape((-1, 1))
    y = np.log(np.array(df["scale_horizontal"]))
    y = y[~np.isnan(y)]

    reg = LinearRegression()
    reg.fit(x, y)
#    r_sq = reg.score(x, y)

    y_reg = x[:,0]*reg.coef_ + reg.intercept_
    y_res = y - y_reg
    y_grid = np.linspace(-4.0, 4.0, 1000)
    k2, p = stats.normaltest(y_reg)
    
    return y_res, y_grid

def fit_data(y_res, y_grid):
    #popt, pcov = curve_fit(func, 
    #                       y_grid, 
    #                       kde_statsmodels_u(y_res, y_grid, bandwidth=0.5), 
    #                       p0=[0, 1])
    popt, pcov = curve_fit(func_2, 
                           y_grid, 
                           kde_statsmodels_u(y_res, y_grid, bandwidth=0.5), 
                           p0=[-0.5, 1, 0.5, 1, 0.5])
    return popt

def get_random_sample(popt, sample_no):
    
    import random
    
    sample = np.zeros((sample_no))
    
    for i in range(sample_no):
        rand = random.uniform(0, 1)
        if rand < popt[4]:
            sample[i] = random.gauss(popt[0], popt[1])
        else:
            sample[i] = random.gauss(popt[2], popt[3])
#    print()
    return sample


if __name__ == '__main__':
    
    y_res, y_grid = get_data()
    popt = fit_data(y_res, y_grid)
    sample = get_random_sample(popt, 1000)

    #print(y_res)

    #print(reg.summary())

    #plt.scatter(x, y)
    #plt.plot(x, x*reg.coef_ + reg.intercept_)
    #plt.scatter(x, y_res)
#    sns.distplot(y_res, hist=False, rug=True)
#    plt.plot(y_grid, kde_statsmodels_u(y_res, y_grid, bandwidth=0.5))
    #plt.plot(y_grid, func(y_grid, popt[0], popt[1]))
    plt.plot(y_grid, func_2(y_grid, popt[0], popt[1], popt[2], popt[3], popt[4]))
    sns.distplot(sample, hist=False, rug=True)

    plt.show()
