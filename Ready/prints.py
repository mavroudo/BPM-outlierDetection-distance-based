#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:48:36 2020

@author: mavroudo
"""

import pandas as pd
import matplotlib.pyplot as plt
data=[]
with open("timeDistanceTest.txt","r") as timeTest:
    for line in timeTest:
       data.append(list(map(float,line.split(","))))       
distanceDF=pd.DataFrame(data,columns=["neighbors","create R-tree","calculate score"])

distanceDF.plot(kind="scatter",x="neighbors",y="create R-tree",ylim=[0,50],title="Time to create the R - tree")
plt.savefig("rTree.png")

distanceDF.plot(kind="scatter",x="neighbors",y="calculate score",title="Time to caclulate the outlier score")
plt.savefig("score.png")

data=[]
with open("timeDistributionTest.txt","r") as timeTest:
    for line in timeTest:
       data.append(list(map(float,line.split(","))))
distributionDF=pd.DataFrame(data,columns=["threshold","time to find the outlying pairs"])
distributionDF.plot(kind="scatter",x="threshold",y="time to find the outlying pairs",ylim=[0,50],title="Time to calculate the noutlying pairs")
plt.savefig("distributionOutliers.png")

data=[]
with open("tests.txt","r") as file:
    for index,line in enumerate(file):
        if index!=0:
            data.append(list(map(float,line.split(" "))))
newData20=[]           
for d in data:
    if d[0]==100:
        newData20.append([d[1],d[2]/(d[2]+d[3])])
testDF=pd.DataFrame(data,columns='Neighbors Threshold Hits Misses'.split(" "))

for d in data:
    print(d[2]/(d[2]+d[3]))