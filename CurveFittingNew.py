#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import math 
import threading
import time
import scipy

from pm4py.algo.filtering.log.attributes import attributes_filter as log_attributes_filter
def dataPreprocess(log):
    activities_all = log_attributes_filter.get_attribute_values(log, "concept:name")
    activities=list(activities_all.keys())
    dataVectors=[]
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
        dataVectors.append(timesSeconds)
    return dataVectors


def calculateRMSE(originalData:np.ndarray,valuesFromDistribution:np.ndarray):
    originalData.sort()
    valuesFromDistribution.sort()
    sum=0
    for index,i in enumerate(originalData):
        sum+=pow(i-valuesFromDistribution[index],2)
    return math.sqrt(sum/len(originalData))
def calculateR2(originalData:np.ndarray,valuesFromDistribution:np.ndarray):
    return r2_score(originalData,valuesFromDistribution)


def perDistribution(distribution,y_std,rmse,rmseLocker,r2,r2Locker):
    dist = getattr(scipy.stats, distribution)
    param = dist.fit(y_std)
    try:
        valuesFromDistribution=np.array([round(i,7) for i in dist.rvs(*param[:-2],loc=param[-2],scale=param[-1], size=len(y_std))])
        originalData=np.array([i[0] for i in y_std])
        rmseValue=calculateRMSE(originalData,valuesFromDistribution)
        r2value=calculateR2(originalData,valuesFromDistribution)
        print(distribution,rmseValue,r2value)
        while rmseLocker.locked():
           continue
        rmseLocker.acquire()
        rmse.append(round(rmseValue,5)) 
        rmseLocker.release()
        while r2Locker.locked():
           continue
        r2Locker.acquire()
        r2.append(round(r2value,5)) 
        r2Locker.release()
    except:
        while rmseLocker.locked():
           continue
        rmseLocker.acquire()
        rmse.append(np.Inf) 
        rmseLocker.release()
        while r2Locker.locked():
           continue
        r2Locker.acquire()
        r2.append(0) 
        r2Locker.release()
    

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
             (k.startswith('rv_') or k.endswith('_gen') or (k == 'levy_stable') or (k=="wrapcauchy")))])
    
    rmseLocker=threading.Lock()
    r2Locker=threading.Lock()
    rmse=[]
    r2=[]
    threads=[]
    for index,distribution in enumerate(list(dist_names)):
        t = threading.Thread(target=perDistribution,args=(distribution,y_std,rmse,rmseLocker,r2,r2Locker))
        threads.append(t)
        t.start()
        while True:
            active=0
            for thread in threads:
                if thread.isAlive() : 
                    active+=1
            if active<4:
                break
            else:
                time.sleep(2)
            
            
        
    [thread.join() for thread in threads]
    try:   
        distributionsDF = pd.DataFrame()
        distributionsDF['Distribution'] = dist_names
        distributionsDF['RMSE'] = rmse
        distributionsDF["R2"]=r2
        distributionsDF.sort_values(['RMSE'], inplace=True)
        return distributionsDF
    except Exception as e:
        print('Failed error with pdDataframe: '+ str(e))

def getDistributionsFitting(dataVectors):
    timeToSeconds=[[k  for i in [x[index] for x in dataVectors] for k in i] for index in range(len(dataVectors[0]))] #get data per activity
    dists=[]
    for index,i in enumerate(timeToSeconds):
        print(index)
        distributionsDF=calculateDistributions(i)
        distributions=[str(distributionsDF.iloc[x]["Distribution"])+"-"+str(distributionsDF.iloc[x]["RMSE"])+"-"+str(distributionsDF.iloc[x]["R2"]) for x in range(len(distributionsDF))]
        try:           
            dists.append([index,distributions])
        except:
            dists.append(distributionsDF)
    f=open("distributions.txt","w")
    for dist in dists:
        f.write(str(dist[0])+", ")
        for distribution in dist[1]:
            f.write(distribution+", ")
        f.write("\n")
    f.close()

from pm4py.objects.log.importer.xes import factory as xes_factory
log=xes_factory.apply("BPI_Challenge_2012.xes")
dataVectors=dataPreprocess(log)
getDistributionsFitting(dataVectors)
