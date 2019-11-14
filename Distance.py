#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
def calculateDiffernce(vector1,vector2):
   rmse=0
   for index in range(len(vector1)):
       rmse+=pow(vector1[index]-vector2[index],2)
   return round(math.sqrt(rmse/len(vector1)),4)


def calculateDistances(dataVectors):
    #find all the distances in the upper corner
    distances=[[]for i in range(len(dataVectors))]
    for i in range(len(dataVectors)):
        for j in range(len(dataVectors)):
            if j>i:
                distances[i].append(calculateDiffernce(dataVectors[i],dataVectors[j]))                
    return distances

def distanceMtree(v1,v2):
    v1List=[float(i) for i in v1[1:-1].split(",")]
    v2List=[float(i) for i in v2[1:-1].split(",")]
    rmse=0
    for index in range(len(v1List)):
       rmse+=pow(v1List[index]-v2List[index],2)
    return round(math.sqrt(rmse/len(v2List)),4)