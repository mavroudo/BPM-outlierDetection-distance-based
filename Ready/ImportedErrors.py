#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 09:15:28 2020

@author: mavroudo
"""
from pm4py.objects.log.importer.xes import factory as xes_factory
from outlierDistanceActivities import findOutlierEvents
import outlierDistanceActivities
import outlierPairsCurveFitting
from statistics import stdev,mean
import random 
#create outliers
def createOutliers(info,timesDeviationMin,timesDeviationMax,howMany):
    """
        Create outliers based on the mean value and the deviation from the activity
    """
    outliers=[]
    for _ in range(howMany):
        index=random.randint(0,len(onlyTimes)-1)
        upOrDown=random.randint(0,1)
        timesDeviation=random.random()*(timesDeviationMax-timesDeviationMin)+timesDeviationMin
        if upOrDown==1:# up
            time=info[index][1]+timesDeviation*info[index][2]
        else:
            time=info[index][1]-timesDeviation*info[index][2]
            if time<0:
                time=info[index][1]+timesDeviation*info[index][2]
        outliers.append([index,time])
    return outliers            

def addOutliersInDataDistance(seq:list,index:list,dataVectorsDistance:list,dataVectorsCurve,outliers:list):
    """
        Add the outliers at the end of the sequences and to the dataVectors,
        so we can run the outlierDetection Algorithm on top of that.
    """
    positionOutliers=[]
    for outlier in outliers:
        traceIndex=random.randint(0,len(seq)-1)
        lengthTrace=len(seq[traceIndex])
        seq[traceIndex].append(outlier)
        counter=0
        for event in index[traceIndex]:
            if event[1]==outlier[0]:
                counter+=1
        index[traceIndex].append([lengthTrace,outlier[0],counter])
        dataVectorsDistance[outlier[0]].append([traceIndex,lengthTrace,outlier[1]])
        dataVectorsCurve[traceIndex][outlier[0]].append(outlier[1])
        positionOutliers.append([traceIndex,lengthTrace])
    return positionOutliers
    
def checkIfOutliersFoundDistance(foundOutliers,outliersPositioned):
    counter=0
    for outlier in foundOutliers:
        for importedOutlier in outliersPositioned:
            if outlier[0]==importedOutlier[0] and outlier[1]==importedOutlier[1]:
                counter+=1
                break
    return counter

def checkIfOutliersFoundCurve(foundOutliers,outliersPositioned,index):
    counter=0
    for outlier in foundOutliers:
        position=0
        for event in index[outlier[0]]:
            if outlier[1]==event[1] and outlier[2]==event[2]:
                position=event[0]
        for importedOutlier in outliersPositioned:
            if outlier[0]==importedOutlier[0] and position==importedOutlier[1]:
                counter+=1
                break
    return counter            
            
def readFile(name):
    results=[]
    with open(name,"r") as f:
        for line in f:
            results.append(list(map(float,line.split(","))))
    return results

logFile="../BPI_Challenge_2012.xes"
log=xes_factory.apply(logFile)
#dataVectors=[traceIndex,position,time]
#seq=[indexInTrace,time]
dataVectorsDistance, seq = outlierDistanceActivities.dataPreprocess(log)
onlyTimes=[[x[2] for x in i] for i in dataVectorsDistance]
dataVectorsCurve,index=outlierPairsCurveFitting.dataPreprocess(log)

info=[]
for activity in onlyTimes:
    info.append([len(activity),mean(activity),stdev(activity)])    
for x,y in zip([2],[3]):
    outliersCreated=createOutliers(info,x,y,100)
    outliersPositioned=addOutliersInDataDistance(seq,index,dataVectorsDistance,dataVectorsCurve,outliersCreated)   
    #using Distance technique to find outlier
    neighbors=[250,500,750,1000,1250,1500,1750,2000]
    results=[]
    for n in neighbors:
        print(x,y,n)
        foundOutliersDistance=findOutlierEvents(dataVectorsDistance,n,stdDeviationTImes=3)
        totalFoundDistance=checkIfOutliersFoundDistance(foundOutliersDistance,outliersPositioned)
        results.append([n,totalFoundDistance/100,len(foundOutliersDistance)])    
    with open("resultsDistanceErrors"+str(x)+"-"+str(y)+".txt","w") as f:
        for r in results:
            f.write(str(r[0])+","+str(r[1])+","+str(r[2])+"\n")
    #using curve fitting to find the outliers       
    thresholds=[0.0025,0.005,0.0075,0.01,0.0125,0.0150,0.0175,0.02]
    results=[]
    for t in thresholds:   
        print(x,y,t)
        foundOutliersCurve=outlierPairsCurveFitting.outlierDetectionWithDistribution(log,dataVectorsCurve,t)
        totalFoundCurve=checkIfOutliersFoundCurve(foundOutliersCurve[0],outliersPositioned,index)
        results.append([t,totalFoundCurve/100,len(foundOutliersCurve[0])])
    with open("resultsCurveErrors"+str(x)+"-"+str(y)+".txt","w") as f:
        for r in results:
            f.write(str(r[0])+","+str(r[1])+","+str(r[2])+"\n")

results=[]       
for x,y in zip([2,3,4],[3,4,5]):
    results.append(readFile("resultsDistanceErrors"+str(x)+"-"+str(y)+".txt"))
    results.append(readFile("resultsCurveErrors"+str(x)+"-"+str(y)+".txt"))
    
    

import matplotlib.pyplot as plt
fig=plt.figure()
plt.subplots_adjust(wspace=0.2,hspace=0.5)
counter=0
for index,x in enumerate(zip([2,3,4],[3,4,5])):
    position="13"+str(index+1)
    ax=fig.add_subplot(int(position), label="distance")
    ax2=fig.add_subplot(int(position), label="distribution", frame_on=False)
    ax.plot(neighbors, [x[1]*100 for x in results[counter]], color="C0")
    if index==0:
        ax.set_ylabel("Percent of outleirs found (%)", color="C0")
    ax.set_ylim([0,100])
    ax.set_xlabel("Number of Neighbors", color="C0")
    ax.tick_params(axis='x', colors="C0")
    ax2.plot(thresholds, [x[1]*100 for x in results[counter+1]], color="C1")
    ax2.xaxis.tick_top()
    ax2.set_xlabel('Threshold', color="C1")      
    ax2.xaxis.set_label_position('top') 
    ax2.tick_params(axis='x', colors="C1")
    ax2.set_ylim([0,100])    
    plt.grid(True)
    counter+=2
counter=0
#for index,x in enumerate(zip([3,4],[4,5])):
#    position="111"
#    ax=fig.add_subplot(int(position), label="distance")
#    ax2=fig.add_subplot(int(position), label="distribution", frame_on=False)
#    data1=[x[2] for x in results[counter]]
#    data2=[x[2] for x in results[counter+1]]
#    minimum=min(min(data1),min(data2))
#    maximum=max(max(data1),max(data2))
#    ax.plot(neighbors, data1, color="C0")
#    ax.set_xlabel("Number of Neighbors", color="C0")
#    if index==0:
#        ax.set_ylabel("Percent of outleirs found (%)", color="C0")
#    ax.set_ylim([minimum,maximum])
#    ax.tick_params(axis='x', colors="C0")
#    ax2.plot(thresholds,data2 , color="C1")
#    ax2.xaxis.tick_top()
#    ax2.tick_params(axis='x', colors="C1")
#    ax2.set_ylim([minimum,maximum])  
#    plt.grid(True)
#    counter+=2
plt.savefig("errorsFound.png")