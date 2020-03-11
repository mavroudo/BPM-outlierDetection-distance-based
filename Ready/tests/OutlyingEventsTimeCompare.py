#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 11:53:51 2020

@author: mavroudo
"""

import os,time

from algorithms import outlierDistanceActivities, preprocess, outlierPairsDistribution
import algorithms.outlierDistanceActivities as activities
import algorithms.outlierPairsDistribution as distribution
kOptions=[250,500,750,1000,1250,1500,1750,2000]
thresholds=[0.0025,0.005,0.0075,0.01,0.0125,0.0150,0.0175,0.02]

logFiles=["../BPI_Challenge_2012.xes","BPI Challenge 2017.xes"]
from pm4py.objects.log.importer.xes import factory as xes_factory
for logFile in logFiles:
    print("importing log")
    log = xes_factory.apply(logFile)
    # [trace,activity index,time]
    print("preprocess ...")
    if logFile=="../BPI_Challenge_2012.xes":
        dataVectors, seq = preprocess.dataPreprocess2012(log)
        identifier="2012"
    else:
         dataVectors, seq = preprocess.dataPreprocess2017(log)
         identifier="2017"
    with open("tests/data/events-{}-distance.txt".format(identifier),"w") as f:
        for k in kOptions:
            pairs,time=outlierDistanceActivities.main(dataVectors,seq,k)
            f.write(str(k)+","+str(time)+"\n")
    with open("tests/data/events-{}-distribution.txt".format(identifier),"w") as f:
        for threshold in thresholds:
            pairs,time=outlierPairsDistribution.main(log,dataVectors,seq,threshold)
            f.write(str(threshold)+","+str(time)+"\n")
            os.remove("distributions.txt")

#plot the times
timeDataEvent=[]
timeDataDistribution=[]
for identifier in ["2012","2017"]:
    with open("tests/data/events-{}-distance.txt".format(identifier),"r") as f:
        data=[]
        for line in f:
            data.append(list(map(float,line.split(","))))
        timeDataEvent.append(data[:8])
    with open("tests/data/events-{}-distribution.txt".format(identifier),"r") as f:
        data=[]
        for line in f:
            data.append(list(map(float,line.split(","))))
        timeDataDistribution.append(data)
#load the synthetic data first      
kOptions=[5,10,20,50,75,100,250,500]
data=[]
for k in kOptions:
    print(k)
    timeStart=time.time()
    myOutliers = activities.findOutlierEvents(dataVectors, k, stdDeviationTImes=3,threshold=None)
    data.append([k,time.time()-timeStart])
timeDataEvent.append(data)

thresholds=[0.0025,0.005,0.0075,0.01,0.0125,0.0150,0.0175,0.02]
data=[]
for t in thresholds:
    timeStart=time.time()
    myOutliers2,distributions,means= distribution.outlierDetectionWithDistribution(None,dataVectors,t,activityNames=["a1","a2","a3","a4"])
    data.append([t,time.time()-timeStart])
    os.remove("distributions.txt")
timeDataDistribution.append(data)

import matplotlib.pyplot as plt
fig=plt.figure()
ax=fig.add_subplot(131, label="distance")
ax2=fig.add_subplot(131, label="distribution", frame_on=False)

minimum=min(min([i[1] for i in timeDataEvent[0]]),min([i[1] for i in timeDataDistribution[0]]))
maximum=max(max([i[1] for i in timeDataEvent[0]]),max([i[1] for i in timeDataDistribution[0]]))
ax.plot([i[0] for i in timeDataEvent[0]], [i[1] for i in timeDataEvent[0]], color="C0")
ax.set_xlabel("Number of Neighbors", color="C0")
ax.set_ylabel("Execution time (s)", color="C0")
ax.tick_params(axis='x', colors="C0")
ax.set_ylim([minimum,maximum])
ax2.plot(thresholds,[i[1] for i in timeDataDistribution[0]], color="C1")
ax2.xaxis.tick_top()
ax2.set_xlabel('Threshold', color="C1")      
ax2.xaxis.set_label_position('top') 
ax2.tick_params(axis='x', colors="C1")
ax2.set_ylim([minimum,maximum])
plt.grid(True)

ax=fig.add_subplot(132, label="distance")
ax2=fig.add_subplot(132, label="distribution", frame_on=False)

minimum=min(min([i[1] for i in timeDataEvent[1]]),min([i[1] for i in timeDataDistribution[1]]))
maximum=max(max([i[1] for i in timeDataEvent[1]]),max([i[1] for i in timeDataDistribution[1]]))
ax.plot([i[0] for i in timeDataEvent[1]], [i[1] for i in timeDataEvent[1]], color="C0")
ax.set_xlabel("Number of Neighbors", color="C0")
ax.tick_params(axis='x', colors="C0")
ax.set_ylim([minimum,maximum])
ax2.plot(thresholds,[i[1] for i in timeDataDistribution[1]], color="C1")
ax2.xaxis.tick_top()
ax2.set_xlabel('Threshold', color="C1")      
ax2.xaxis.set_label_position('top') 
ax2.tick_params(axis='x', colors="C1")
ax2.set_ylim([minimum,maximum])
plt.grid(True)

ax=fig.add_subplot(133, label="distance")
ax2=fig.add_subplot(133, label="distribution", frame_on=False)

minimum=min(min([i[1] for i in timeDataEvent[2]]),min([i[1] for i in timeDataDistribution[2]]))
maximum=max(max([i[1] for i in timeDataEvent[2]]),max([i[1] for i in timeDataDistribution[2]]))
ax.plot([i[0] for i in timeDataEvent[2]], [i[1] for i in timeDataEvent[2]], color="C0")
ax.set_xlabel("Number of Neighbors", color="C0")
ax.tick_params(axis='x', colors="C0")
ax.set_ylim([minimum,maximum])
ax2.plot(thresholds,[i[1] for i in timeDataDistribution[2]], color="C1")
ax2.xaxis.tick_top()
ax2.set_xlabel('Threshold', color="C1")      
ax2.xaxis.set_label_position('top') 
ax2.tick_params(axis='x', colors="C1")
ax2.set_ylim([minimum,maximum])
plt.grid(True)
plt.savefig("tests/graphs/executionTimes.png")






