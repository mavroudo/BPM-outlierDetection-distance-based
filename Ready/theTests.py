#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 12:47:26 2020

@author: mavroudo
"""

logFile="../BPI_Challenge_2012.xes"
import outlierDistanceActivities,outlierPairsCurveFitting, outlierPairWise
n=[10,20,50,100,250]
d=[outlierDistanceActivities.main(logFile,neighbors,stdDeviationTimes=4,threshold=None) for neighbors in n]
with open("outlierEventTime.txt","w") as f:
    for index,x in enumerate(d):
        f.write(str(n[index])+","+str(x[1])+"\n")
        with open("outliersDistanceEvents.txt","a+") as outFile:
            outFile.write(str(n[index])+"\n")
            for outlier in x[0]:
                outFile.write(str(outlier)+"\n")
                
d=[outlierPairWise.main(logFile,neighbors,2524) for neighbors in n]
with open("rTreeDistance.txt","w") as f:
    for index,x in enumerate(d):
        f.write(str(n[index])+","+str(x[1])+","+str(x[2])+"\n")
        
#fig which is in the center of the distribution
import random
x=[random.randint(0,40) for i in range(30)]
y=[random.randint(80,120) for _ in range(30)]
k=x+[60]+y

thresholds = [0.1,0.05,0.02,0.01,0.0075,0.005,0.0025,0.001]
d=[outlierPairsCurveFitting.main(logFile,threshold) for threshold in thresholds]
with open("distributionTimes.txt","w") as f:
    for index,x in enumerate(d):
        f.write(str(thresholds[index])+","+str(x[1])+"\n")
        with open("outliersDistribution.txt","a+") as outFile:
            outFile.write(str(threshold[index])+"\n")
            for outlier in x[0]:
                outFile.write(str(outlier)+"\n")