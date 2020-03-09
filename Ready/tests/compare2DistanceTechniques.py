#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 15:15:32 2020

@author: mavroudo
"""

from pm4py.objects.log.importer.xes import factory as xes_factory
from algorithms import outlierDistanceActivities, preprocess,outlierPairWise
import time

kOptions=[250,500,750,1000,1250,1500,1750,2000]
logFile="../BPI_Challenge_2012.xes"
log = xes_factory.apply(logFile)

dataVectors, seq = preprocess.dataPreprocess2012(log)
pairWiseData=outlierPairWise.preprocess(log)


timeTreeStart=time.time()
tree=outlierPairWise.createRtree(pairWiseData) #returns values orderd 
timeTreeEnd=time.time()

with open("tests/timeDistancesEvent.txt","w") as f:
   for k in kOptions:
       pairs,executionTime=outlierDistanceActivities.main(dataVectors,seq,k)
       f.write(str(k)+","+str(executionTime)+"\n")

with open('tests/timeDistancesRtree.txt','w') as f:
    for k in kOptions:
        startPairWist=time.time()
        scores=outlierPairWise.outlierScore(k,tree,pairWiseData)
        scoreTimeEnd=time.time()
        outliers=[]
        for s in scores:
            pairData=pairWiseData[s[0]]
            outliers.append(pairData+[s[1]])
        f.write(str(k)+","+str(scoreTimeEnd-startPairWist)+"\n")
        print(scoreTimeEnd-timeTreeEnd, len(outliers))

#try for small number

