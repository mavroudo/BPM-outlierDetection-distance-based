#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from sklearn.preprocessing import StandardScaler
import numpy as np
import warnings  
import scipy
from CurveFittingNew import getDistributionsFitting

from pm4py.algo.filtering.log.attributes import attributes_filter as log_attributes_filter
def readFromFile(log):
    import pandas as pd
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
        
    
    if not os.path.isfile("distributions.txt"): #check if the distributions exist
       distributionsDF=getDistributionsFitting(timeToSeconds) #calculate again
    else:
        distributionsDF=readFromFile(log) #read distrs from txt

    #get the distributions in a array
    warnings.filterwarnings("ignore")
    distributions=[]
    for index in range(len(distributionsDF)):
        if i[0]!="non":
            dist = getattr(scipy.stats, distributionsDF.iloc[index]["Distribution"])
            param = dist.fit(standarized[index])
            distributions.append([dist,param])
        else: 
            distributions.append([])
        
    #perform outlier detection trace by trace
    outliers=[]
    for index,dataVector in enumerate(dataVectors):
        #print(index)
        for innerIndex,activity in enumerate(dataVector): # looping through the time events
            dist,param=distributions[innerIndex]
            if len(activity)>0:
                mo=sum(activity)/len(activity)  
            else:
                continue
            x=standarScalers[innerIndex].transform(np.array(mo).reshape(1,-1))            
            predict=float(dist.pdf(x,*param[:-2], loc=param[-2],scale=param[-1]))
            if predict<threshold:
                if innerIndex==13:
                    print(predict,x)
                outliers.append([index,innerIndex])
                break
            #flag=False
            #for event in activity:
            #    x=standarScalers[innerIndex].transform(np.array(event).reshape(1,-1))
            #    predict=float(dist.pdf(x,*param[:-2], loc=param[-2],scale=param[-1]))
            #    if predict<threshold:
            #        outliers.append([index,innerIndex])
            #        flag=True
            #        break
            #if flag:
            #    break           
    return outliers




#auto tha diagrafei otan dhmiourgh8ei h sunarthsh
from pm4py.objects.log.importer.xes import factory as xes_factory
from CurveFittingNew import dataPreprocess
log=xes_factory.apply("BPI_Challenge_2012.xes")
dataVectors=dataPreprocess(log)
outliers=outlierDetectionWithDistribution(log,dataVectors,0.01)

#this working except from 0 position
possitions=[i[1] for i in outliers]
from collections import Counter
Counter(possitions).keys()
Counter(possitions).values()
