#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 11:53:51 2020

@author: mavroudo
"""

from algorithms import outlierDistanceActivities,preprocess,outlierPairsCurveFitting
kOptions=[100,250,500,750,1000,1500,2000]
thresholds=[0.0025,0.005,0.0075,0.01,0.0125,0.0150,0.0175,0.02]

logFiles=["../BPI_Challenge_2012.xes","BPI Challenge 2017.xes"]
from pm4py.objects.log.importer.xes import factory as xes_factory
for logFile in logFiles:
    print("importing log")
    log = xes_factory.apply(logFile)
    # [trace,activity index,time]
    print("preprocess ...")
    dataVectors, seq = preprocess.dataPreprocess2012(log)
    pairs,time=outlierPairsCurveFitting.main(logFile,dataVectors,seq,0.0025)
    with open("tests/events-{}-distance.txt".format(logFile),"w") as f:
        for k in kOptions:
            pairs,time=outlierDistanceActivities.main(dataVectors,seq,50)
            f.write(str(k)+","+str(time)+"\n)
    with open("tests/events-{}-distribution.txt".format(logFile),"w") as f:
        for threshold in thresholds:
            
    