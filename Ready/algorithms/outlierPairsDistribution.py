#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is a version of outlierPirsCurveFitting without the threads. It will only
run for the distributions that were given in the paper
"""
import pandas as pd
from pm4py.algo.filtering.log.attributes import attributes_filter as log_attributes_filter
import numpy as np
from algorithms.outlierDistanceActivities import  createPairs
from sklearn.metrics import r2_score
import os,warnings,scipy,math ,time
from statistics import mean

def readFromFile(log,activityNames=None):
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
    if log!=None:
        activities_all = log_attributes_filter.get_attribute_values(log, "concept:name")
        activities=list(activities_all.keys())
        distributionsDF["Activity_Name"]=activities
    else:
        distributionsDF["Activity_Name"]=activityNames
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
    warnings.filterwarnings("ignore")
    #the distributions that used in the paper
    dist_names=['beta','expon','norm','lognorm','gamma','uniform','weibull_max','weibull_min','t']
    r2=[]
    rmse=[]
    for index,distribution in enumerate(list(dist_names)):
        dist = getattr(scipy.stats, distribution)
        param = dist.fit(timeData)
        try:
            valuesFromDistribution=np.array([round(i,7) for i in dist.rvs(*param[:-2],loc=param[-2],scale=param[-1], size=len(timeData))])
            rmseValue=calculateRMSE(timeData,valuesFromDistribution)
            r2value=r2_score(timeData,valuesFromDistribution)
            r2.append(r2value)
            rmse.append(rmseValue)
        except ValueError:
            rmse.append(math.inf)
            r2.append(0)
        
    try:   
        distributionsDF = pd.DataFrame()
        distributionsDF['Distribution'] = dist_names
        distributionsDF['RMSE'] = rmse
        distributionsDF["R2"]=r2
        distributionsDF.sort_values(['R2'], inplace=True,ascending=False)
        return distributionsDF
    except Exception as e:
        print('Failed error with pdDataframe: '+ str(e))

def getDistributionsFitting(timeToSeconds,log,activityNames):
    timeStart=time.time()
    dists=[]
    for index,i in enumerate(timeToSeconds):
        distributionsDF=calculateDistributions(i)
        distributions=[str(distributionsDF.iloc[x]["Distribution"])+"-"+str(distributionsDF.iloc[x]["RMSE"])+"-"+str(distributionsDF.iloc[x]["R2"]) for x in range(len(distributionsDF))]
        try:           
            dists.append([index,distributions])
        except:
            dists.append(distributionsDF)
    print("Distribution fitting took: "+str(time.time()-timeStart))
    f=open("distributions.txt","w")
    for dist in dists:
        f.write(str(dist[0])+", ")
        for distribution in dist[1]:
            f.write(distribution+", ")
        f.write("\n")
    f.close()
    return readFromFile(log,activityNames)


def outlierDetectionWithDistribution(log,dataVectors,threshold,activityNames=None):
    times=[[i[2] for i in x]for x in dataVectors]
    means=[mean(i) for i in times]
    print("Getting distributions")
    if not os.path.isfile("distributions.txt"): #check if the distributions exist
       distributionsDF=getDistributionsFitting(times,log,activityNames) #calculate again
    else:
        distributionsDF=readFromFile(log) #read distrs from txt
    warnings.filterwarnings("ignore")
    distributions=[]
    print("check how good they fit")
    for index in range(len(distributionsDF)):
        if distributionsDF.iloc[index]["R2"]>=0.9:
            dist = getattr(scipy.stats, distributionsDF.iloc[index]["Distribution"])
            param = dist.fit(times[index])
            distribution=dist(*param[:-2], loc=param[-2],scale=param[-1])
            distributions.append([distribution])
        else: 
            size=len(times[index])
            down=int(size*threshold)
            up=int(size-size*threshold)
            distributions.append([float(sorted(times[index])[down]),float(sorted(times[index])[up])])
    print("finding  outliers")
    outliers=[]
    for activity_index,activity_vector in enumerate(dataVectors):
        if len(distributions[activity_index])==2: #histogram method
            minValue,maxValue=distributions[activity_index]
            for event in activity_vector:            
                if event[2]<minValue:
                    outliers.append([event[0],event[1],event[2],"down"])
                elif event[2]>maxValue:
                    outliers.append([event[0],event[1],event[2],"up"])
        else: #found a good distribution to fit the data
            dist=distributions[activity_index][0]
            for event in activity_vector:   
                predict=float(dist.pdf(event[2]))
                if predict<threshold:
                    if event[2]>means[activity_index]:
                        outliers.append([event[0],event[1],event[2],"up"])
                    else:
                        outliers.append([event[0],event[1],event[2],"down"])
    return outliers,distributions,means
            


def main(log,dataVectorsDist,seqDist,threshold):
    print("Detecting outliers")
    timeStart=time.time()
    myoutliers,distributions,means=outlierDetectionWithDistribution(log,dataVectorsDist,threshold)
    timeEnd=time.time()
    print("Creating pairs")
    outlierPairs=createPairs(myoutliers,seqDist,positionOfTime=3)
    return outlierPairs,timeEnd-timeStart





