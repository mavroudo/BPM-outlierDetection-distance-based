#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from sklearn.preprocessing import StandardScaler
import numpy as np
import warnings  
import scipy
from CurveFitting import getDistributionsFitting
def outlierDetectionWithDistribution(traces,allTimes,threshold):
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

    allTimesSeconds=[[i.total_seconds() for i in j] for j in allTimes] #transform to seconds
    timedata=[i[int(len(i)/2):] for i in traces] #time data is the second half of the trace

    #standarize data
    standarized=[] #contains all the times standarized
    standarScalers=[] #contains all the scalers that have been fitting to the allTimesSeconds
    for index,i in enumerate(allTimesSeconds):
        sc=StandardScaler()
        numpyArray=np.array(i)
        numpyArray = numpyArray.reshape (-1,1)
        sc.fit(numpyArray) #fit to the all of the times spend 
        standarScalers.append(sc)
        standarized.append(sc.transform(numpyArray)) #trnasform the values in the result
        
    #read distrs from txt
    if not os.path.isfile("distributions.txt"): #check if the distributions exist
       getDistributionsFitting(allTimes) 
    f=open("distributions.txt","r") 
    dists=[]
    for i in f:
        dists.append(i.split(" "))

    #get the distributions in a array
    warnings.filterwarnings("ignore")
    distributions=[]
    for index,i in enumerate(dists):
        if i[0]!="non":
            dist = getattr(scipy.stats, i[1])
            param = dist.fit(standarized[index])
            distributions.append([dist,param])
        else: 
            distributions.append([])
        
    #perform outlier detection trace by trace
    outliers=[]
    for index,i in enumerate(traces):
        print(index)
        for innerIndex,event in enumerate(timedata[index]): # looping through the time events
            seconds=None if event == 0 else [event.total_seconds()]
            if seconds != None:
                dist,param=distributions[innerIndex]
                x=standarScalers[innerIndex].transform(np.array(seconds).reshape(1,-1))
                predict=float(dist.pdf(x,*param[:-2], loc=param[-2],scale=param[-1]))
                if predict<threshold:
                    outliers.append([index,innerIndex])
                    break
    return outliers


#auto tha diagrafei otan dhmiourgh8ei h sunarthsh
from pm4py.objects.log.importer.xes import factory as xes_factory
from DataPreprocess import dataPreprocess
log=xes_factory.apply("BPI_Challenge_2012.xes")
results,statsTimes=dataPreprocess(log)
outliers=outlierDetectionWithDistribution(results,statsTimes,0.01)

#this working except from 0 position
possitions=[i[1] for i in outliers]
from collections import Counter
Counter(possitions).keys()
Counter(possitions).values()
