#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 15:15:32 2020

@author: mavroudo
"""

from pm4py.objects.log.importer.xes import factory as xes_factory
from algorithms import outlierDistanceActivities, preprocess,outlierPairWise
import time
import matplotlib.pyplot as plt
kOptions=[250,500,750,1000,1250,1500,1750,2000]
logFile="../BPI_Challenge_2012.xes"

def createFiles(logFile,kOptions):
    log = xes_factory.apply(logFile)
    dataVectors, seq = preprocess.dataPreprocess2012(log)
    pairWiseData=outlierPairWise.preprocess(log)
    #if needed to calculate time to create tree
    timeTreeStart=time.time()
    tree=outlierPairWise.createRtree(pairWiseData) #returns values orderd 
    timeTreeEnd=time.time()
    
    with open("tests/data/timeDistancesEvent.txt","w") as f:
       for k in kOptions:
           pairs,executionTime=outlierDistanceActivities.main(dataVectors,seq,k)
           f.write(str(k)+","+str(executionTime)+"\n")
    
    with open('tests/data/timeDistancesRtree.txt','w') as f:
        for k in kOptions:
            startPairWist=time.time()
            scores=outlierPairWise.outlierScore(k,tree,pairWiseData)
            scoreTimeEnd=time.time()
            outliers=[]
            for s in scores:
                pairData=pairWiseData[s[0]]
                outliers.append(pairData+[s[1]])
            f.write(str(k)+","+str(scoreTimeEnd-startPairWist)+"\n")


def createTimeGraph(fileName1,fileName2):
    timeEvent,timeRtree,koptions=[],[],[]
    with open(fileName1,"r") as fEvent:
        with open(fileName2,'r') as fRtree:
            for lineEvent,lineTree in zip(fEvent,fRtree):
                evData=list(map(float,lineEvent.split(",")))
                rData=list(map(float,lineTree.split(",")))
                timeEvent.append(evData[1])
                timeRtree.append(rData[1])
                koptions.append(rData[0])
    plt.plot(koptions,timeRtree,label="R-Tree")
    plt.plot(koptions,timeEvent,label="Events")
    plt.title("Compare 2 distance methods for outlying pairs")
    plt.legend(loc='best')
    plt.savefig("tests/graphs/compareDistancePairs.png")
        




