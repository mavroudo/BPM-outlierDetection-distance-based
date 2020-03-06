#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 12:35:37 2020

@author: mavroudo
"""

from pm4py.objects.log.importer.xes import factory as xes_factory
from algorithms.outlierDistanceActivities import findOutlierEvents
import os
from algorithms import outlierDistanceActivities,preprocess,outlierPairsDistribution
import algorithms.outlierPairsCurveFitting
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

def addOutliers(seq:list,dataVectors:list,outliers:list):
    """
        Add the outliers at the end of the sequences and to the dataVectors,
        so we can run the outlierDetection Algorithm on top of that.
    """
    positionOutliers=[]
    for outlier in outliers:
        traceIndex=random.randint(0,len(seq)-1)
        lengthTrace=len(seq[traceIndex])
        seq[traceIndex].append(outlier)
        dataVectors[outlier[0]].append([traceIndex,lengthTrace,outlier[1]])
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

kOptions=[250,500,750,1000,1250,1500,1750,2000]
thresholds=[0.0025,0.005,0.0075,0.01,0.0125,0.0150,0.0175,0.02]
logFiles=["../BPI_Challenge_2012.xes","BPI Challenge 2017.xes"]

for logFile in logFiles:
    print("importing log")
    log = xes_factory.apply(logFile)
    if logFile=="../BPI_Challenge_2012.xes":
        dataVectors, seq = preprocess.dataPreprocess2012(log)
        identifier="2012"
    else:
         dataVectors, seq = preprocess.dataPreprocess2017(log)
         identifier="2017"
    onlyTimes=[[x[2] for x in i] for i in dataVectors]
    info=[]
    for activity in onlyTimes:
        info.append([len(activity),mean(activity),stdev(activity)])    
    for x,y in zip([3,4],[4,5]):
        outliersCreated=createOutliers(info,x,y,100)
        outliersPositioned=addOutliers(seq,dataVectors,outliersCreated)
        results=[]
        for n in kOptions:
            print(x,y,n)
            foundOutliersDistance=findOutlierEvents(dataVectors,n,stdDeviationTImes=3)
            totalFoundDistance=checkIfOutliersFoundDistance(foundOutliersDistance,outliersPositioned)
            results.append([n,totalFoundDistance/100,len(foundOutliersDistance)])    
        with open("tests/resultsDistanceErrors("+str(x)+"-"+str(y)+").txt","w") as f:
            for r in results:
                f.write(str(r[0])+","+str(r[1])+","+str(r[2])+"\n")
    #   using curve fitting to find the outliers       
        results=[]
        for t in thresholds:   
            print(x,y,t)
            foundOutliersCurve=outlierPairsDistribution.outlierDetectionWithDistribution(log,dataVectors,t)
            totalFoundCurve=checkIfOutliersFoundDistance(foundOutliersCurve,outliersPositioned)
            results.append([t,totalFoundCurve/100,len(foundOutliersDistance)]) 
        with open("tests/resultsCurveErrors("+str(x)+"-"+str(y)+").txt","w") as f:
            for r in results:
                f.write(str(r[0])+","+str(r[1])+","+str(r[2])+"\n")
        os.remove("distributions.txt")
