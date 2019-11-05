#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import math 
import threading
import time
import scipy

from pm4py.algo.filtering.log.attributes import attributes_filter as log_attributes_filter
def dataPreprocess(log):
    activities_all = log_attributes_filter.get_attribute_values(log, "concept:name")
    activities=list(activities_all.keys())
    results=[]
    for trace in log:
        k=[0 for i in range(len(activities))]
        times=[[] for i in range(len(activities))]
        previousTime=trace.attributes["REG_DATE"]
        for index,event in enumerate(trace):
            indexActivity=activities.index(event["concept:name"])
            k[indexActivity]+=1
            times[indexActivity].append(event["time:timestamp"]-previousTime)
            previousTime=event["time:timestamp"]
            timesSeconds=[[i.total_seconds() for i in x] for x in times]
        results.append(timesSeconds)
    return results


def calculateRMSE(originalData:np.ndarray,valuesFromDistribution:np.ndarray):
    originalData.sort()
    valuesFromDistribution.sort()
    sum=0
    for index,i in enumerate(originalData):
        sum+=pow(i-valuesFromDistribution[index],2)
    return math.sqrt(sum/len(originalData))


def perDistribution(distribution,y_std,rmse,rmseLocker):
    print(distribution)
    dist = getattr(scipy.stats, distribution)
    param = dist.fit(y_std)
    try:
        valuesFromDistribution=np.array([round(i,7) for i in dist.rvs(*param[:-2],loc=param[-2],scale=param[-1], size=len(y_std))])
        originalData=np.array([i[0] for i in y_std])
        rmseValue=calculateRMSE(originalData,valuesFromDistribution)
        while rmseLocker.locked():
           continue
        rmseLocker.acquire()
        rmse.append(round(rmseValue,7)) 
        rmseLocker.release()
    except:
        while rmseLocker.locked():
           continue
        rmseLocker.acquire()
        rmse.append(np.Inf) 
        rmseLocker.release()
    

def calculateDistributions(timeData):
    y=np.array(timeData)#create the dataFrame
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
    
    rmseLocker=threading.Lock()
    rmse=[]
    threads=[]
    for index,distribution in enumerate(list(dist_names)):
        t = threading.Thread(target=perDistribution,args=(distribution,y_std,rmse,rmseLocker))
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
        results['RMSE'] = rmse
        results.sort_values(['RMSE'], inplace=True)
        return results
    except Exception as e:
        print('Failed error with pdDataframe: '+ str(e))

def getDistributionsFitting(results):
    timeToSeconds=[[k  for i in [x[index] for x in results] for k in i] for index in range(len(results[0]))] #get data per activity
    dists=[]
    for index,i in enumerate(timeToSeconds):
        print(index)
        k=calculateDistributions(i)
        distributions=[str(k.iloc[x]["Distribution"])+"-"+str(k.iloc[x]["RMSE"]) for x in range(len(k))]
        try:           
            dists.append([index,distributions])
        except:
            dists.append(k)
    f=open("distributions.txt","w")
    for dist in dists:
        f.write(str(dist[0])+", ")
        for distribution in dist[1]:
            f.write(distribution+", ")
        f.write("\n")
    f.close()

from pm4py.objects.log.importer.xes import factory as xes_factory
log=xes_factory.apply("BPI_Challenge_2012.xes")
results=dataPreprocess(log)
getDistributionsFitting(results)
