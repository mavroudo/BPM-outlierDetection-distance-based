#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 10:33:48 2020

@author: mavroudo
"""
#import sys 
#sys.path.insert(0,'../algorithms')
import algorithms.traceOutlierDistance as trace
from pm4py.objects.log.importer.xes import factory as xes_factory
import matplotlib.pyplot as plt
import numpy as np
import time


def createFiles(logFile,kOptions):
    neighbors=trace.main(logFile,max(kOptions),None)
    with open("tests/data/trace_neighbors.txt","w") as f:
        for event in neighbors:
            string=""
            for n in event:
                string+=str(n)+","
            f.write(string[:-1]+"\n")
            
    neighbors=[]       
    with open("tests/data/trace_neighbors.txt","r") as f:
       for line in f:
           neighbors.append(list(map(float,line.split(","))))
    data=[]
    for k in kOptions:
        sumOfDistances=[]
        for n in neighbors:
            sumOfDistances.append(sum(n[:k+1]))
        data.append(sorted(sumOfDistances))
        
    with open("tests/data/baxplot.txt","w") as f:
        for k,d in zip(kOptions,data):
            string=str(k)
            for distance in d:
                string+=","+str(distance)
            f.write(string+"\n")  
            
    with open("tests/data/krTests.txt","w") as f:
        for k in kOptions:
            distancefromK=[]
            for n in neighbors:
                distancefromK.append(sum(n[:k-1]))
            distancefromK.sort()
            string=str(k)
            for d in distancefromK:
                string+=","+str(d)
            f.write(string+"\n")
    
def createKR(fileName):
    distances=[]
    with open(fileName,"r") as f:        
        for line in f:
            data=list(map(float,line.split(",")))
            distances.append(data)
            plt.plot([i for i in range(len(data[1:]))],data[1:],label=str(data[0]))
    plt.legend(loc='best')
    plt.title("K-R test")
    plt.savefig('tests/graphs/krTest.png')
    return distances

from statistics import mean
def createBoxPlot(fileName,neighbors):
    data=[]
    with open(fileName,"r") as f: 
        for line in f:
            if int(line.split(",")[0])==neighbors:
               data=(list(map(float,line.split(",")[:-1])))
               print(mean(data[1:]))
               plt.boxplot(data[1:])
               plt.title("Outlying Factor Distribution")
               plt.ylabel("Sum of distances from {}-nn".format(neighbors))
               plt.savefig("tests/graphs/boxplotTrace.png")

def createPlotTimeDimention(fileName):
    x=[]
    y=[]
    with open(fileName,"r") as f:       
        for line in f:
            data=list(map(float,line.split(",")))
            x.append(data[0])
            y.append(data[1])
    plt.plot(x,y)
    plt.title("Compare time with dimentions")
    plt.xlabel("Dimentions")
    plt.ylabel("Time (s)")
    plt.savefig("tests/graphs/dimentionsTime.png")
            
            


def timeBaseOnDimentions(logFile):
    print("Loading data..")
    log=xes_factory.apply(logFile)   
    print("Preprocess Data..")
    dataVectors,statsTimes,activities=trace.dataPreprocess(log)
    dataVectorsStandarized=trace.transform(dataVectors)
    times=[]
    for i in range(4,int(len(dataVectorsStandarized[0]))+1,4):
        startingTime=time.time()
        data=[k[:i] for k in dataVectorsStandarized]
        print("Creating Mtree...")
        mtree=trace.createMTree(data)
        neighbors=trace.getNeirestNeighbors(mtree,data,50)
        print(time.time()-startingTime)
        times.append([i,time.time()-startingTime])
    with open("tests/data/timesDimentions.txt","w") as f:
        for d  in x:
            f.write(str(d[0])+","+str(d[1])+"\n")
    return times
   
    

logFile="../BPI_Challenge_2012.xes"

"""
x=timeBaseOnDimentions(logFile)
with open("tests/timesDimentions.txt","w") as f:
    for d  in x:
        f.write(str(d[0])+","+str(d[1])+"\n")
"""
kOptions=[10,20,50,100,250]
# createFiles(logFile,kOptions)
k=createKR("tests/data/krTests.txt")
     


