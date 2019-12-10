#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this file we will add a bpi, transform it to contain pairwise + standarized data
every pair will be the 2 sequential points. Then we will add them to the R-Tree
and at the end we will perform queries in the r tree to compute the outling score
"""
from pm4py.algo.filtering.log.attributes import attributes_filter as log_attributes_filter
from sklearn.preprocessing import StandardScaler
import numpy as np
from rtree.index import Rtree
import math
from pm4py.objects.log.importer.xes import factory as xes_factory
def preprocess(log):
    activities_all = log_attributes_filter.get_attribute_values(log, "concept:name")
    activities=list(activities_all.keys())
    dataVectors=[]
    sequentialData=[[] for i in range(len(log))]
    for outerIndex,trace in enumerate(log):
        times=[[] for i in range(len(activities))]
        previousTime=trace.attributes["REG_DATE"]
        for index,event in enumerate(trace):
            indexActivity=activities.index(event["concept:name"])
            time=event["time:timestamp"]-previousTime
            times[indexActivity].append(time)
            previousTime=event["time:timestamp"]
            timesSeconds=[[i.total_seconds() for i in x] for x in times]
            sequentialData[outerIndex].append([indexActivity,time.total_seconds()])
        dataVectors.append(timesSeconds)
    
    #transofrm datavectors to contain times per activity
    timesPerActivity=[[k  for i in [x[index] for x in dataVectors] for k in i] for index in range(len(dataVectors[0]))]
    #standard scalers
    standarScalers=[] #contains all the scalers that have been fitting to the allTimesSeconds
    for index,i in enumerate(timesPerActivity):
        sc=StandardScaler()
        numpyArray=np.array(i)
        numpyArray = numpyArray.reshape (-1,1)
        sc.fit(numpyArray) #fit to the all of the times spend 
        standarScalers.append(sc)

    #create pairwise data [traceIndex,activityA,activityB,standarizedTimeA,standarizedTimeB]
    data=[]
    for traceIndex,trace in enumerate(sequentialData):
        for eventIndex,event in enumerate(trace[:-1]):
            eventNext=sequentialData[traceIndex][eventIndex+1]
            timeA=standarScalers[event[0]].transform(np.array(event[1]).reshape(1,-1))
            timeB=standarScalers[eventNext[0]].transform(np.array(eventNext[1]).reshape(1,-1))
            data.append([traceIndex,event[0],eventNext[0],round(float(timeA),5),round(float(timeB),5)])
    return data


def createRtree(data):
    tree=Rtree()
    for index,pair in enumerate(data): 
        tree.insert(index,(pair[3],pair[4]),obj=pair)
    return tree


def distance2Pairs(pair1,pair2):
    return math.sqrt((pair1[3]-pair2[3])**2+(pair1[4]-pair2[4])**2)

  
def outlierScore(k,tree,data):
    scores=[]
    for index,pair in enumerate(data):
        print(index)
        neirestNeighbors=tree.nearest((pair[3],pair[4]),num_results=k+1)
        #tree returns indexes +1, + the value of the element itself
        distances=[distance2Pairs(pair,data[x-1]) for x in neirestNeighbors]
        scores.append([index,sum(sorted(distances[:k+1]))])
    return sorted(scores,key=lambda x:x[1],reverse=True)

def writeTOPKNeighborsToFile(tree,data,k):
   with open("pairsNeighbors.txt","w") as f:
    for index,pair in enumerate(data):
        print(index)
        neirestNeighbors=tree.nearest((pair[3],pair[4]),num_results=k)
        f.write(str(index)+":")
        for neighbor in neirestNeighbors:
            f.write(str(neighbor)+",")
        f.write("\n") 
    
def readFromFile():
    with open("pairsNeighbors.txt","r") as f:
        data=[]
        for index,line in enumerate(f):
            line=line.split(":")
            data.append([])
            for neighbor in line[1].split(",")[:-1]:
                data[index].append(int(neighbor))
            yield data[index] 

print("Loading data..")
log=xes_factory.apply("BPI_Challenge_2012.xes")
print("Preprocess")
#[traceIndex,activityA,activityB,standarizedTimeA,standarizedTimeB]
pairWiseData=preprocess(log)
print("Create R tree")
tree=createRtree(pairWiseData) #returns values orderd

#This code will take the first 10.000 neighbors of each and print them to a file
print("Writing to file")
writeTOPKNeighborsToFile(tree,pairWiseData,10000)

#print("Calculate the outlierScore")
#scores=outlierScore(50,tree,pairWiseData)


