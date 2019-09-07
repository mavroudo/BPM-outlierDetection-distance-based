#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Distance import calculateDiffernce
import matplotlib.pyplot as plt 
import os

def findAllDistances(results,minmaxTimes):  
    #find all the distances in the upper corner
    distances=[[]for i in range(len(results))]
    for i in range(len(results)):
        print(i)
        for j in range(len(results)):
            if j<=i:
                distances[i].append(0)
            else:
                distances[i].append(calculateDiffernce(results[i],results[j],minmaxTimes))
    return distances

def writeToFile(distances, filesName):
    if os.path.exists(filesName):
      os.remove(filesName)
    else:
      pass
    with open(filesName, "a") as myfile:
        for index,line in enumerate(distances):
            print(index)
            for distance in line:
                myfile.write(str(distance)+",")
            myfile.write("\n")

def readFromFile(filesName):
    distances=[]
    with open(filesName, "r") as myfile:
        for index,line in enumerate(myfile):
            distances.append([])
            for distance in line.split(","):
                try:
                    distances[-1].append(int(distance))
                except:
                    pass
    return distances


def plotDistanceDistribution(distances,plotTitle):
    #find max and max of maxs
    maxes=[max(d) for d in distances]
    maxMax=max(maxes) # the biggest distance is 254   
    #plot the distance distribution
    countDistances=[0 for i in range(maxMax+1)]
    for trace in distances:
        for distance in trace:
            countDistances[distance]+=1
    countDistances[0]=0
    #plotting
    x=[i for i in range(1,len(countDistances)+1)]
    plt.plot(x, countDistances) 
    plt.xlabel('distance') 
    plt.ylabel('instances') 
    plt.title('Distance Distribution') 
    plt.savefig(plotTitle+'.png')