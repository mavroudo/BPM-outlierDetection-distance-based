#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 11:53:51 2020

@author: mavroudo
"""

import os

from algorithms import outlierDistanceActivities, preprocess, outlierPairsDistribution

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
