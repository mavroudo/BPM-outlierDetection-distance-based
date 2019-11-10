#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
def calculateDiffernce(vector1,vector2):
   rmse=0
   for index in range(len(vector1)):
       rmse+=pow(vector1[index]-vector2[index],2)
   return round(math.sqrt(rmse/len(vector1)),4)


   

def calculateDistances(dataVector):
    #find all the distances in the upper corner
    distances=[[]for i in range(len(dataVector))]
    for i in range(len(dataVector)):
        print(i)
        for j in range(len(dataVector)):
            if j>i:
                distances[i].append(calculateDiffernce(dataVector[i],dataVector[j]))                
    return distances

def distanceMtree(v1,v2):
    v1List=[float(i) for i in v1[1:-1].split(",")]
    v2List=[float(i) for i in v2[1:-1].split(",")]
    return calculateDiffernce(v1List,v2List)