#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pm4py.objects.log.importer.xes import factory as xes_factory
from DataPreprocess import dataPreprocess



#try to curve fit in the first dimention
import scipy
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

def calculateDistributions(timeData):
    y=np.array(timeData)
    size=len(y)
    y_df=pd.DataFrame(y,columns=['Data'])
    y_df.describe()
    
    #transform using standard scaler
    sc=StandardScaler() 
    yy = y.reshape (-1,1)
    sc.fit(yy)
    y_std =sc.transform(yy)
    del yy
    
    import warnings
    warnings.filterwarnings("ignore")
    dist_names = sorted(
         [k for k in scipy.stats._continuous_distns.__all__ if not (
             (k.startswith('rv_') or k.endswith('_gen') or (k == 'levy_stable') ))])
    chi_square = []
    p_values = []
    percentile_bins = np.linspace(0,100,41)
    percentile_cutoffs = [round(i,7) for i in np.percentile(y_std, percentile_bins)]
    observed_frequency, bins = np.histogram(y_std, bins=percentile_cutoffs)
    cum_observed_frequency = np.cumsum(observed_frequency)
    
    for index,distribution in enumerate(list(dist_names)):
        # Set up distribution and get fitted distribution parameters
        dist = getattr(scipy.stats, distribution)
        param = dist.fit(y_std)
        #cannotResolve=[]
        # Obtain the KS test P statistic, round it to 5 decimal places
        try:
            p = scipy.stats.kstest(y_std, distribution, args=param)
            p = np.around(p[1], 5)
            p_values.append(p) 
        except Exception  :
            try:
                print(distribution)
                p_values.append(0.0) 
                #cannotResolve.append(distribution)
                #continue
            except:
                return ["non",0,0]
   
        
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
        chi_square.append(ss)
        #dist_names=[i for i in dist_names if i not in cannotResolve]
    try:   
        results = pd.DataFrame()
        results['Distribution'] = dist_names
        results['chi_square'] = chi_square
        #results['p_value'] = p_values
        results.sort_values(['chi_square'], inplace=True)
        return results
    except:
        return ["non",0,0]

log=xes_factory.apply("BPI_Challenge_2012.xes")
results,statsTimes=dataPreprocess(log)
timeToSeconds=[[i.total_seconds() for i in j] for j in statsTimes] #transform to seconds
dists=[]
for index,i in enumerate(timeToSeconds):
    print(index)
    k=calculateDistributions(i)
    try:
        dists.append([index,k.iloc[1]['Distribution'],k.iloc[1]['chi_square']])
    except:
        dists.append(k)
        
temp=[timeToSeconds[3]]
k=None
for index,i in enumerate(temp):
    k=calculateDistributions(i)

f=open("distributions.txt","w")
for dist in dists:
    f.write(str(dist[0])+" "+str(dist[1])+" "+str(dist[2])+"\n")
f.close()

