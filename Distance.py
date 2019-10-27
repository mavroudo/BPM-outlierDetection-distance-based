#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
def calculateDiffernce(metric1,metric2):
   rmse=0
   for index in range(len(metric1)):
       rmse+=pow(metric1[index]-metric2[index],2)
   return math.sqrt(rmse/len(metric1))
   

def findAllDistances(sequenceData,timeData):
    results=[sequenceData[i]+timeData[i] for i in range(len(timeData))]
    #find all the distances in the upper corner
    distances=[[]for i in range(len(results))]
    for i in range(len(results)):
        print(i)
        for j in range(len(results)):
            if j<=i:
                distances[i].append(0)
            else:
                distances[i].append(calculateDiffernce(results[i],results[j]))
    return distances
