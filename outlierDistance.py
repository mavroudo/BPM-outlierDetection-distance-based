#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this script we find outlier traces based on  their distance from outhers.
Every trace isbecomivng a vector which contain information both from the
structure and times. Then based on the k and r we found the outlyiers.
"""
import datetime 
from pm4py.algo.filtering.log.attributes import attributes_filter as log_attributes_filter
from sklearn.preprocessing import StandardScaler
import numpy as np
from pm4py.objects.log.importer.xes import factory as xes_factory
from mtree import MTree
import math
import os

def dataPreprocess(log):
    """
        In this function data from log, will be transformed to a vector
    """
    activities_all = log_attributes_filter.get_attribute_values(log, "concept:name")
    activities=list(activities_all.keys())
    dataVectors=[]
    times=[[] for i in range(len(activities))]
    for trace in log:
        activitiesCounter=[0 for i in range(len(activities))]
        timesSpend=[datetime.timedelta(0) for i in range(len(activities))]
        previousTime=trace.attributes["REG_DATE"]
        for index,event in enumerate(trace):
            indexActivity=activities.index(event["concept:name"])
            activitiesCounter[indexActivity]+=1
            timesSpend[indexActivity]+=event["time:timestamp"]-previousTime
            times[indexActivity].append(event["time:timestamp"]-previousTime)
            previousTime=event["time:timestamp"]
        timesSpend=[(timesSpend[i]/activitiesCounter[i]).total_seconds() if activitiesCounter[i]!=0 else 0 for i in range(len(activities))] #contains the mo of all the activities
        dataVectors.append(activitiesCounter+timesSpend) 
    return dataVectors,times


def transform(dataVectors):
    """
        Data will be standarized so every attribute can contribute the same to the distance
    """
    transposeVector=[[data[i] for data in dataVectors] for i in range(len(dataVectors[0]))]
    standarizedData=[]
    for field in transposeVector:
        y=np.array(field).reshape(-1,1)
        sc=StandardScaler()
        sc.fit(y)
        standarizedData.append(sc.transform(y))
    transformedData=[[float(i) for i in k] for k in standarizedData]
    return [[data[i] for data in transformedData] for i in range(len(transformedData[0]))]

def distanceMtree(v1,v2):
    """
        This is the function that calculated the distance between 2 elements
        in the M-Tree
    """
    v1List=[float(i) for i in v1[1:-1].split(",")]
    v2List=[float(i) for i in v2[1:-1].split(",")]
    rmse=0
    for index in range(len(v1List)):
       rmse+=pow(v1List[index]-v2List[index],2)
    return round(math.sqrt(rmse/len(v2List)),4)

def calculateQueries(mtree:MTree, dataVectors:list,K,R):
    """
        If there is no previous data of calculated queries, or the value of 
        k and r are not combatable, this method will create the queries
        in the M-Tree based on the given values
    """
    queries=[]
    for index,dataVector in enumerate(dataVectors): 
        print(index)
        x=list(mtree.get_nearest(str(dataVector),range=R,limit=K))
        m=[i[1] for i in x]
        queries.append(m)
    return queries

def writeTopKNeighborsToFile(preparedQueries,k,r,fileName):
    """
        This method writes the prepared Queries in a file, so next time it will
        not be needed to calculate them again
    """
    newName=fileName+"-"+str(k)+"-"+str(r)+".txt"
    with open(newName,"w") as f:
        f.write(str(k)+","+str(r)+"\n")
        for neighbors in preparedQueries:
            for neighbor in neighbors:
                f.write(str(neighbor)+" ")
            f.write("\n")
        
def readFromFile(fileName):
    """
        read the prepared Queries from the file
    """
    preparedQueries=[]
    with open(fileName,"r") as f:
        k,r=map(int,f[0].spli(",")[:-1])
        for index,line in enumerate(f[1:]):
            print(index)
            preparedQueries.append([float(i) for i in line.split(" ")[:-1]])
    return k,r,preparedQueries

def outliersKNN(queries:list,R,K):
    """
        Calculate the outliers based on the K and R
    """
    outliers=[]
    for index,i in enumerate(queries):
        try:
            if i[K+1]>R:
                outliers.append(index)
        except IndexError:
            outliers.append(index)
    return outliers

def outliers(logName,k,r,mtree,dataVectors):
    nameFile=logName.split(".")[0]
    fileFound=None
    for filename in os.listdir('.'):
        if filename.startswith(nameFile):
            name=filename.split(".")[0]
            K,R=map(int,name.split("-")[1:])
            if k<=K and r<=R:
                fileFound=filename
                break
    preparedQueries=[]
    if fileFound==None:
       preparedQueries=calculateQueries(mtree,dataVectors,k,r)
       writeTopKNeighborsToFile(preparedQueries,k,r,logFile)
    else:
        preparedQueries=readFromFile(fileFound)
    return outliersKNN(preparedQueries,r,k)
    
      
def createMTree(dataVectorsStandarized):
    """
        Add 1 by 1 all the vectors in the M-Tree
    """
    myTree=MTree(distance_function=distanceMtree,min_node_capacity=50)
    for index,vector in enumerate(dataVectorsStandarized):
        print(index)
        try:
            myTree.add(str(vector))
        except:
            pass
    return myTree

logFile="BPI_Challenge_2012.xes"
k=500
r=3

print("Loading data..")
log=xes_factory.apply(logFile)

print("Preprocess Data..")
dataVectors,statsTimes=dataPreprocess(log)
dataVectorsStandarized=transform(dataVectors)

print("Creating Mtree...")
mtree=createMTree(dataVectorsStandarized)
    
print("Find outliers based on given K and R")
outliersFound=outliers(logFile,k,r,mtree,dataVectorsStandarized)