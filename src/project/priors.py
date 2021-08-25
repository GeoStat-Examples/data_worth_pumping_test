import numpy as np
import seaborn as sns
import random 

def get_random_sample(popt, sample_no, seed = None):
    
    sample = np.zeros((sample_no))
    
    for i in range(sample_no):
        sample[i] = random.gauss(popt[0], popt[1])
    return sample

def get_correlation_sample(popt, sample_no, seed = None):
    
    sample = np.zeros((sample_no))
    
    for i in range(sample_no):
        rand = random.uniform(0, 1)
        if rand < popt[4]:
            sample[i] = random.gauss(popt[0], popt[1])
        else:
            sample[i] = random.gauss(popt[2], popt[3])
    
    sample = np.exp(0.99722*np.log(2000) - 2.2173 + sample)

    return sample

def get_priors(sample_no, seed = None):
    
    sample = np.zeros((3, sample_no))
    
    popt = [-4.81374, 2.05843]
    sample[0,:] = get_random_sample(popt, sample_no, seed = seed)
    
    popt = [1.09815, 0.0232984]
    sample[1,:] = get_random_sample(popt, sample_no, seed = seed)
    
#    popt = [-0.750524, 0.709014, 0.895672, 0.742894, 0.545689]
    popt = [-1.40243, 0.783084, 0.41414, 0.895658, 0.226714]
    sample[2,:] = get_correlation_sample(popt, sample_no, seed = seed) 
#    print(np.exp( 0.99722*np.log(1000) - 2.2173 ))
    
    return sample
    

#print(df)
#print(popt)
    
if __name__ == '__main__':
    

    sample = get_priors(1000)  
    
    sns.distplot(sample[2,:], hist=False, rug=True)
