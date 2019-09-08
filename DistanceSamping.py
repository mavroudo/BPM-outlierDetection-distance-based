#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
def calculateDiffernce(trace1,trace2,cells):
   difActivities=0
   difTime=0
   for i in range(int(len(trace1)/2)): 
       difActivities+=abs(trace1[i]-trace2[i])
   for i in range(int(len(trace1)/2),len(trace1)): #for the time
       cellActivity=cells[i-int(len(trace1)/2)]
       if trace1[i]==0 or trace2[i]==0:
           difTime+=0
       else:
           difTime+=difBasedOnCells(trace1[i],trace2[i],cellActivity)
   return round(difActivities+difTime)

#return what percent of the data are between this 2 data approx
def difBasedOnCells(time1,time2,cellActivity):
    if time1==time2:
        return 0
    index1=0
    for index,cell in enumerate(cellActivity):
        if cell > time1:
            index1=index
            break
    if index1==0:
        index1=len(cellActivity)-1
    index2=0
    for index,cell in enumerate(cellActivity):
        if cell > time2:
            index2=index
            break
    if index2==0:
        index2=len(cellActivity)-1
        
    dif=abs(index2-index1)-1
    try:
        if dif==-1: #they are in the same cell but they are not equal
            return (abs(time1-time2)/(cellActivity[index2]-cellActivity[index2-1]))*(1/len(cellActivity))
        else:
            return (dif+ ((time1-cellActivity[index1-1])/(cellActivity[index1]-cellActivity[index1-1])) + ((time2-cellActivity[index2-1])/(cellActivity[index2]-cellActivity[index2-1])))*(1/len(cellActivity))
    except:
        return 0
    
    
            

def findAllDistancesWithSampling(results,statsTimes,percentOfData=0.1,numberOfCells=10):
    cells=sampleTimes(statsTimes,percentOfData,numberOfCells)
    distances=[[]for i in range(len(results))]
    for i in range(len(results)):
        print(i)
        for j in range(len(results)):
            if j<=i:
                distances[i].append(0)
            else:
                distances[i].append(calculateDiffernce(results[i],results[j],cells))
    return distances

def sampleTimes(statsTimes,percentOfData=0.1,numberOfCells=10):
    sampledTime=[sorted(random.sample(population=statsTimes[i],k=int(len(statsTimes[i])*percentOfData))) for i in range(len(statsTimes))]
    cells=[[] for sampledData in sampledTime]
    for index,sampledData in enumerate(sampledTime):
        for i in range(numberOfCells):
            try:
                cells[index].append(sampledData[int(i/numberOfCells*len(sampledData))])
            except:
                cells[index].append(sampledData[-1])
    return cells
    
