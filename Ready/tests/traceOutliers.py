#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 10:33:48 2020

@author: mavroudo
"""
# import sys
# sys.path.insert(0,'../algorithms')
import algorithms.traceOutlierDistance as trace
import matplotlib.pyplot as plt
import numpy as np

logFile="../BPI_Challenge_2012.xes"
kOptions=[10,20,50,100,250]

neighbors=trace.main(logFile,max(kOptions),None)
data=[]
for k in kOptions:
    sumOfDistances=[]
    for n in neighbors:
        sumOfDistances.append(sum(n[:k]))
    data.append(sumOfDistances.sort())

try:
    with open("tests/krTests.txt","w") as f:
        for k,d in zip(kOptions,data):
            f.write(str(k))
            for distance in d:
                f.write(","+str(distance))
            f.write(",\n")

    distances=[]
    with open("tests/krTests.txt","r") as f:
        for line in f:
            distances.append(list(map(float,line.split(",")[:-1])))

    for d in distances:
        plt.plot([i for i in range(len(d[1:]))],d[1:],label=str(d[0]))
    plt.legend(loc='best')
    plt.title("K-R test")
    plt.savefig('tests/krTest.png')
except:
    for d in data:
        plt.plot([i for i in range(len(d[1:]))],d[1:],label=str(d[0]))
    plt.legend(loc='best')
    plt.title("K-R test")
    plt.savefig('tests/krTest.png')

