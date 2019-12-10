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

"""
These 3 functions used for outliers activities 
"""
from heapq import nsmallest
def neighrestNeighbors(activityVector,element,k):
    return nsmallest(k, activityVector, key=lambda x: abs(x[1]-element[1]))

def neighborsScore(activityVector,k):
    score=[]
    for event in activityVector:
        neighbors=neighrestNeighbors(activityVector,event,k)
        score.append([event,sum([abs(neighbor[1]-event[1]) for neighbor in neighbors])])
    return sorted(score,key=lambda x: x[1],reverse=True)

def calculatePairwise(activityVector):
    sum=0
    for event in activityVector:
        for event2 in activityVector:
            sum+=event[1]*event2[1]
    return (sum/2)/len(activityVector)

def outlierActivities(activityVector,k,threshold):
    scores=neighborsScore(activityVector,k)
    expected=calculatePairwise(activityVector)
    outliers=[]
    for score in scores:
        if score[1]>threshold:
            outliers.append(score[0])
        else:
            break
    return outliers