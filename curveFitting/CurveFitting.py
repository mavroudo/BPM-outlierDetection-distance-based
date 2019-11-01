#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#try to curve fit in the first dimention
import scipy
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import threading
import time


def perDistribution(distribution,y_std,size,p_values,chi_values,pvalueLocker,chivalueLocker):
    # Set up distribution and get fitted distribution parameters
    print(distribution)
    dist = getattr(scipy.stats, distribution)
    param = dist.fit(y_std)
    # Obtain the KS test P statistic, round it to 5 decimal places
    try:
        p = scipy.stats.kstest(y_std, distribution, args=param) #memory might broke
        p = np.around(p[1], 5)
        while pvalueLocker.locked():
            continue
        pvalueLocker.acquire()
        p_values.append(p) 
        pvalueLocker.release()
    except Exception  :
        try:
            p_values.append(0.0)
            #continue
        except Exception as e:
            print('Failed error with kp test: '+ str(e))
            return ["non",0,0]
    #number_of_bins=int(len(timeData)/250) #fix it
    percentile_bins = np.linspace(0,100,41) #calculate chi_with 41 bins 
    percentile_cutoffs = [round(i,7) for i in np.percentile(y_std, percentile_bins)]
    observed_frequency, bins = np.histogram(y_std, bins=percentile_cutoffs)
    cum_observed_frequency = np.cumsum(observed_frequency)
    # Get expected counts in percentile bins
    # This is based on a 'cumulative distrubution function' (cdf)
    cdf_fitted = dist.cdf(percentile_cutoffs, *param[:-2], loc=param[-2], 
                          scale=param[-1])
    expected_frequency = []
    for bin in range(len(percentile_cutoffs)-1):
        expected_cdf_area = cdf_fitted[bin+1] - cdf_fitted[bin]
        expected_frequency.append(expected_cdf_area)
    # calculate chi-squared
    expected_frequency = np.array(expected_frequency) * size
    cum_expected_frequency = np.cumsum(expected_frequency)
    ss = sum (np.nan_to_num(((cum_expected_frequency - cum_observed_frequency) ** 2) / cum_observed_frequency))
    while chivalueLocker.locked():
       continue
    chivalueLocker.acquire()
    chi_values.append(ss) 
    chivalueLocker.release()



def calculateDistributions(timeData):
    y=np.array(timeData)#create the dataFrame
    size=len(y)
    y_df=pd.DataFrame(y,columns=['Data'])
    y_df.describe()   
   
    sc=StandardScaler() #transform using standard scaler
    yy = y.reshape (-1,1)
    sc.fit(yy)
    y_std =sc.transform(yy)
    del yy  
    
    import warnings #mute the warning from the getattr
    warnings.filterwarnings("ignore")
    dist_names = sorted(
         [k for k in scipy.stats._continuous_distns.__all__ if not (
             (k.startswith('rv_') or k.endswith('_gen') or (k == 'levy_stable') ))])
    
    p_values = [] # Calculate p values 
    chi_square = []
    pvalueLocker=threading.Lock()
    chivalueLocker=threading.Lock()
    threads=[]
    for index,distribution in enumerate(list(dist_names)):
        t = threading.Thread(target=perDistribution,args=(distribution,y_std,size,p_values,chi_square,pvalueLocker,chivalueLocker))
        threads.append(t)
        t.start()
        while True:
            active=0
            for thread in threads:
                if thread.isAlive() : 
                    active+=1
            if active<8:
                break
            else:
                time.sleep(2)
            
            
        
    [thread.join() for thread in threads]
    try:   
        results = pd.DataFrame()
        results['Distribution'] = dist_names
        results['chi_square'] = chi_square
        #results['p_value'] = p_values
        results.sort_values(['chi_square'], inplace=True)
        return results
    except Exception as e:
        print('Failed error with pdDataframe: '+ str(e))


def getDistributionsFitting(allTimes):
    timeToSeconds=[[i.total_seconds() for i in j] for j in allTimes] #transform to seconds
    dists=[]
    for index,i in enumerate(timeToSeconds):
        print(index)
        k=calculateDistributions(i)
        distributions=[str(k.iloc[x]["Distribution"])+"-"+str(k.iloc[x]["chi_square"]) for x in range(len(k)) if k.iloc[x]["chi_square"] != np.Inf]
        try:           
            dists.append([index,distributions])
        except:
            dists.append(k)
    f=open("distributions.txt","w")
    for dist in dists:
        f.write(str(dist[0])+" ")
        for distribution in dist[1]:
            f.write(distribution+" ")
        f.write("\n")
    f.close()


from pm4py.objects.log.importer.xes import factory as xes_factory
from DataPreprocess import dataPreprocess
log=xes_factory.apply("BPI_Challenge_2012.xes")
results,statsTimes=dataPreprocess(log)
getDistributionsFitting(statsTimes)




