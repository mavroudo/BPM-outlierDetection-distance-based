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
import utils
import time
import pandas as pd
import matplotlib.pyplot as plt

def preprocess(log):
    """
        Transform every trace in the log file, which is represented as a json,
        in a array that we will have easy access to times for every event in a trace
        and the sequence of these events. Also uses standarization to transofrm
        the time values per activity.
    """
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
            data.append([traceIndex,event[0],eventNext[0],round(float(timeA),5),round(float(timeB),5),eventIndex])
    return data


def createRtree(data):
    """
        Creates an R-Tree from the given data
    """
    tree=Rtree()
    for index,pair in enumerate(data): 
        tree.insert(index,(pair[3],pair[4]),obj=pair)
    return tree


def distance2Pairs(pair1,pair2):
    return math.sqrt((pair1[3]-pair2[3])**2+(pair1[4]-pair2[4])**2)

  
def outlierScore(k,tree,data):
    """
        Calculates the outlierScore for every data, by calculating the sum of 
        distances between this point and the k-neighrest points to it.
    """
    scores=[]
    for index,pair in enumerate(data):
        utils.progress(index,len(data),status="Calculate the outlierScore")
        neirestNeighbors=tree.nearest((pair[3],pair[4]),num_results=k+1)
        #tree returns indexes +1, + the value sof the element itself
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
        for index,line in enumerate(f):
            line=line.split(":")
            data=[]
            for neighbor in line[1].split(",")[:-1]:
                data.append(int(neighbor))
            yield data
            
def testRTree(pairWiseData):
    """
        Is used in order to test the time that takes to create the r-tree, based on 
        the number of values that we have
    """
    data=[20000,50000,100000,150000,200000,249113]
    times=[0,0,0,0,0,0]
    for index,n in enumerate(data):
        print(index)
        for _ in range(5):
            timeTreeStart=time.time()
            createRtree(pairWiseData[:n]) #returns values orderd 
            timeTreeEnd=time.time()
            times[index]+=timeTreeEnd-timeTreeStart
        times[index]=times[index]/5
    rtreeTimes=pd.DataFrame([[data[i],times[i]] for i in range(len(data))],columns=["data inserted","time"] )
    rtreeTimes.plot(kind="scatter",x="data inserted",y="time",title="Time to create R-Tree based on inserted data")
    plt.savefig("rtreeTimes.png")

import random    
def testQueriesInTree(pairWiseData,tree):
    """
        In this method we test how the time of a query increases as the number of
        k in increasing
    """
    neighbors=[100,500,1000,3000,5000,10000,30000,50000]
    times=[0 for _ in range(len(neighbors))]
    queries=1000
    for index,k in enumerate(neighbors):
        print(k)
        for _ in range(queries):           
            data=random.choice(pairWiseData)
            timeQStart=time.time()
            tree.nearest((data[3],data[4]),num_results=k+1)
            timeQEnd=time.time()
            times[index]+=timeQEnd-timeQStart
        times[index]/=queries
    df=pd.DataFrame([[neighbors[i],times[i]]for i in range(len(times))],columns=["Neighbors","Time"])
    df.plot(kind="scatter",x="Neighbors",y="Time",title="Query time in R-Tree based on K")
    plt.savefig("queriesTime.png")
                       

def main(logFile,neighbors,number):
    logFile="../BPI_Challenge_2012.xes"
    print("Loading data..")
    log=xes_factory.apply(logFile)
    print("Preprocessing")
    pairWiseData=preprocess(log)
    print("Create R tree")
    timeTreeStart=time.time()
    tree=createRtree(pairWiseData) #returns values orderd 
    timeTreeEnd=time.time()
    scores=outlierScore(neighbors,tree,pairWiseData)
    scoreTimeEnd=time.time()
    print("Creating pairs")
    outliers=[]
    for s in scores:
        pairData=pairWiseData[s[0]]
        outliers.append(pairData+[s[1]])
    return outliers[:number],timeTreeEnd-timeTreeStart,scoreTimeEnd-timeTreeEnd





#import pandas as pd
#df=pd.DataFrame(pairWiseData,columns=["trace","activityA","ActivityB","x","y","eventId"])
#dfSampled=df.sample(100)
#import matplotlib.pyplot as plt
#dfSampled.plot(x="x",y="y",kind="scatter")
#plt.savefig("sampled100.png")
