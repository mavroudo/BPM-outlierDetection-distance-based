#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 11:50:36 2020

@author: mavroudo
"""

from pm4py.algo.filtering.log.attributes import attributes_filter as log_attributes_filter
from pm4py.objects.log.importer.xes import factory as xes_factory
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import threading
import scipy
import numpy as np
import math
import time
import pandas as pd
import os
import warnings
from statistics import mean


def dataPreprocess(log):
    """
        Transform every trace in the log file in a way that we will have direct
        access to every event in a trace and its time. Also returns a array
        with the initial sequence of events in a trace that will be used latter
        to create the pairs
    """
    activities_all = log_attributes_filter.get_attribute_values(log, "concept:name")
    activities=list(activities_all.keys())
    dataVectors=[]
    theIndex=[]
    for trace in log:
        k=[0 for i in range(len(activities))]
        times=[[] for i in range(len(activities))]
        previousTime=trace.attributes["REG_DATE"]
        aIndex=[]
        for index,event in enumerate(trace):
            indexActivity=activities.index(event["concept:name"])
            k[indexActivity]+=1
            times[indexActivity].append(event["time:timestamp"]-previousTime)
            aIndex.append([index,indexActivity,len(times[indexActivity])])
            previousTime=event["time:timestamp"]
        timesSeconds=[[i.total_seconds() for i in x] for x in times]
        dataVectors.append(timesSeconds)
        theIndex.append(aIndex)
    return dataVectors,theIndex

def readFromFile(log):
    """
        This functions will read the distribution evaluation from the file. 
        It will be used if we had already run the experiments, to save time.
    """
    dists=[]
    with open("distributions.txt","r") as f:
        for line in f:
           dists.append(line.split(", ")[1:-1])
           
    distributions=[[i.split("-") for i in d ] for d in dists]
    distributions=[]
    for index,d in enumerate(dists):
        distributions.append([])
        for i in d:
            k=i.split("-")
            if len(k)==4:
                k.remove("")
                k[2]="-"+k[2]
            distributions[index].append(k)
   
    p=[[[i[0],float(i[1]),float(i[2])]for i in dist]for dist in distributions]
    pSorted=[[sorted(i,key=lambda x:x[2],reverse=True)] for i in p]
    oneDist=[i[0][0] for i in pSorted]
    distributionsDF = pd.DataFrame()  
    activities_all = log_attributes_filter.get_attribute_values(log, "concept:name")
    activities=list(activities_all.keys())
    distributionsDF["Activity_Name"]=activities
    distributionsDF['Distribution'] = [i[0] for i in oneDist]
    distributionsDF['RMSE'] = [i[1] for i in oneDist]
    distributionsDF["R2"]=[i[2] for i in oneDist]
    return distributionsDF

def calculateRMSE(originalData:np.ndarray,valuesFromDistribution:np.ndarray):    
    originalData.sort()
    valuesFromDistribution.sort()
    sum=0
    for index,i in enumerate(originalData):
        sum+=pow(i-valuesFromDistribution[index],2)
    return math.sqrt(sum/len(originalData))

def calculateDistributions(timeData):
    """
        This function will use 8 threads to run for every distribution in parallel.
        So someone can test more than the 9 dstributions that were given in the 
        paper. The scipy supports up to 98 different distriburions for continuous
        values
    """
    y=np.array(timeData)#create the dataFrame
    sc=StandardScaler() #transform using standard scaler
    yy = y.reshape (-1,1)
    sc.fit(yy)
    y_std =sc.transform(yy)
    del yy    
    import warnings #mute the warning from the getattr
    warnings.filterwarnings("ignore")
    #the distributions that used in the paper
    dist_names=['beta','expon','norm','lognorm','gamma','uniform','weibull_max','weibull_min','t']
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
            if active<8:
                break
            else:
                time.sleep(2)
        
    [thread.join() for thread in threads]
    try:   
        distributionsDF = pd.DataFrame()
        distributionsDF['Distribution'] = dist_names
        distributionsDF['RMSE'] = rmse
        distributionsDF["R2"]=r2
        distributionsDF.sort_values(['R2'], inplace=True)
        return distributionsDF
    except Exception as e:
        print('Failed error with pdDataframe: '+ str(e))

def perDistribution(distribution,y_std,rmse,rmseLocker,r2,r2Locker):
    dist = getattr(scipy.stats, distribution)
    param = dist.fit(y_std)
    try:
        valuesFromDistribution=np.array([round(i,7) for i in dist.rvs(*param[:-2],loc=param[-2],scale=param[-1], size=len(y_std))])
        originalData=np.array([i[0] for i in y_std])
        rmseValue=calculateRMSE(originalData,valuesFromDistribution)
        r2value=r2_score(originalData,valuesFromDistribution)
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

def getDistributionsFitting(timeToSeconds,log):
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
    return readFromFile(log)

def outlierDetectionWithDistribution(log,dataVectors,threshold):
    """
    This function will return a array with the outliers based on their underlying
    distribution. For this it will read the distributions from the distributions.txt
    file if this exists. If not it will cal the CurveFitting method in order to 
    create it. This might take some time.
    
    traces: the trace from the log file after the have been preprocessed
    allTImes: contains in lists all the times that spoted in the trace for every activity
    threshold: contains a float number <1 that will determine when a time in the
        trace is outlier based on the probability density function
    return: an array with the outliers that will be in form [a,b] where a is the
        index of the trace and b the index of the activity that made it an outlier
    """
    timeToSeconds=[[k  for i in [x[index] for x in dataVectors] for k in i] for index in range(len(dataVectors[0]))]
    #standarize data
    standarized=[] #contains all the times standarized
    standarScalers=[] #contains all the scalers that have been fitting to the allTimesSeconds
    for index,i in enumerate(timeToSeconds):
        sc=StandardScaler()
        numpyArray=np.array(i)
        numpyArray = numpyArray.reshape (-1,1)
        sc.fit(numpyArray) #fit to the all of the times spend 
        standarScalers.append(sc)
        standarized.append(sc.transform(numpyArray)) #trnasform the values in the result
        
    print("Getting distributions")
    if not os.path.isfile("distributions.txt"): #check if the distributions exist
       distributionsDF=getDistributionsFitting(timeToSeconds) #calculate again
    else:
        distributionsDF=readFromFile(log) #read distrs from txt

    #get the distributions in a array
    warnings.filterwarnings("ignore")
    distributions=[]
    print("check how good they fit")
    for index in range(len(distributionsDF)):
        if distributionsDF.iloc[index]["R2"]>=0.9:
            dist = getattr(scipy.stats, distributionsDF.iloc[index]["Distribution"])
            param = dist.fit(standarized[index])
            distribution=dist(*param[:-2], loc=param[-2],scale=param[-1])
            distributions.append([distribution])
        else: 
            size=len(timeToSeconds[index])
            down=int(size*threshold)
            up=int(size-size*threshold)
            distributions.append([float(sorted(standarized[index])[down]),float(sorted(standarized[index])[up])])
    #perform outlier detection trace by trace
    print("finding  outliers")
    outliers=[]
    for traceIndex,dataVector in enumerate(dataVectors):
        for activityIndex,activity in enumerate(dataVector): # looping through the time events           
            if len(distributions[activityIndex])==1: #fit distribution
                dist=distributions[activityIndex][0]                             
                for eventIndex,event in enumerate(activity):
                    x=standarScalers[activityIndex].transform(np.array(event).reshape(1,-1))
                    predict=float(dist.pdf(x))
                    if predict<threshold:
                        outliers.append([traceIndex,activityIndex,eventIndex,event,float(x)])
            else:
                minValue,maxValue=distributions[activityIndex] #use min and max from given data
                for eventIndex,event in enumerate(activity):
                    x=standarScalers[activityIndex].transform(np.array(event).reshape(1,-1))
                    if x<minValue or x>maxValue:
                        outliers.append([traceIndex,activityIndex,eventIndex,event,float(x)])
    means=[mean(i) for i in timeToSeconds]
    return outliers,distributions,means


def createPairsFromOutliers(outliers,index,dataVectors,means):
    """
        After finding the outliers we can create the outlier pairs, using the 
        initlial sequence of events in every trace.
    """
    #get the indexes in their seq
    indexOfOutliers=[]
    for outlier in outliers:
        indexInTrace=int([index for index,event in enumerate(index[outlier[0]]) if event[1]==outlier[1] and event[2]==outlier[2]+1][0])
        indexOfOutliers.append([outlier[0],outlier[1],indexInTrace,dataVectors[outlier[0]][outlier[1]][outlier[2]]])
    #create the outlier pairs
    outlierPairs=[]
    outlierId=0
    while outlierId<len(indexOfOutliers):
        outlier=indexOfOutliers[outlierId]
        if outlier[2]>0: # it has a previous            
            thisIndex=index[outlier[0]][outlier[2]-1]
            timeA=dataVectors[outlier[0]][thisIndex[1]][thisIndex[2]-1]   
            timeB=outlier[3]
            if timeB>means[outlier[1]]:
                outlierPairs.append([outlier[0],thisIndex[1],outlier[1],timeA,timeB,"ok","over",outlier[2]-1])
            else:
                outlierPairs.append([outlier[0],thisIndex[1],outlier[1],timeA,timeB,"ok","under",outlier[2]-1])
        
        #that is for the next one
        try:
            outlierNext=indexOfOutliers[outlierId+1]
            if outlier[0]==outlierNext[0] and outlier[2]==outlierNext[2]-1: #both activities one next to another are outliers
                a1="under"
                a2="under"
                if outlier[3]>means[outlier[1]]:
                    a1="over"
                if outlierNext[3]>means[outlierNext[1]]:
                    a2="over"           
                outlierPairs.append([outlier[0],outlier[1],outlierNext[1],outlier[3],outlierNext[3],a1,a2,outlier[2]])
                outlierId+=2
            else:
                try:
                    nextActivity=index[outlier[0]][outlier[2]+1]
                    timeA=outlier[3]
                    timeB=dataVectors[outlier[0]][nextActivity[1]][nextActivity[2]-1]
                    a1="under"
                    if outlier[3]>means[outlier[1]]:
                        a1="over"
                    outlierPairs.append([outlier[0],outlier[1],nextActivity[1],timeA,timeB,a1,"ok",outlier[2]])
                    outlierId+=1
                except: #there is no next activity
                    outlierId+=1 
        except IndexError:
            outlierId+=1
    return outlierPairs


def main(logFile,threshold):
    print("Loading data..")
    log=xes_factory.apply(logFile)
    print("Preprocessing")
    dataVectors,index=dataPreprocess(log)
    print("Detecting outliers")
    timeStart=time.time()
    outliers,distributions,means=outlierDetectionWithDistribution(log,dataVectors,threshold)
    timeEnd=time.time()
    print("Creating pairs")
    outlierPairs=createPairsFromOutliers(outliers,index,dataVectors,means)
    return outlierPairs,timeEnd-timeStart

