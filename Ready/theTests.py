#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 12:47:26 2020

@author: mavroudo
"""

logFile="../BPI_Challenge_2012.xes"
import outlierDistanceActivities,outlierPairsCurveFitting, outlierPairWise
n=[10,20,50,100,250]
d1=[outlierDistanceActivities.main(logFile,neighbors,stdDeviationTimes=4,threshold=None) for neighbors in n]
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


thresholds = [0.1,0.05,0.02,0.01,0.0075,0.005,0.0025,0.001]
d=[outlierPairsCurveFitting.main(logFile,threshold) for threshold in thresholds]
with open("distributionTimes.txt","w") as f:
    for index,x in enumerate(d):
        f.write(str(thresholds[index])+","+str(x[1])+"\n")
        with open("outliersDistribution.txt","a+") as outFile:
            outFile.write(str(thresholds[index])+"\n")
            for outlier in x[0]:
                outFile.write(str(outlier)+"\n")

#plot the times for outlier r tree and outlier event   
import matplotlib.pyplot as plt
dataTree=[]
with open("rTreeDistance.txt","r") as f:
    for line in f:
        dataTree.append(list(map(float,line.split(","))))
dataDistance=[]
with open("outlierEventTime.txt","r") as f:
    for line in f:
        dataDistance.append(list(map(float,line.split(","))))

plt.plot([i[0] for i in dataTree],[i[2] for i in dataTree])
plt.plot([i[0] for i in dataDistance],[i[1] for i in dataDistance])
plt.legend(["Using R-Tree","Calculating anomalous events first"])
plt.title("Times of methods based on different k")
plt.ylabel("Time (s)")
plt.xlabel("K-neighbors")
plt.savefig("RtreeVSEvents.png")

#plot in one axis
import random
x=[random.randint(0,40) for i in range(30)]
y=[random.randint(80,120) for _ in range(30)]
k=x+[60]+y
plt.scatter(k,[0 for _ in range(len(k))])
plt.savefig("1doutlier.png")

#plot time based on threshold
dataDistance=[]
with open("distributionTimes.txt","r") as f:
    for line in f:
        dataDistance.append(list(map(float,line.split(","))))
        
#png for time based on different values of threshold
plt.plot(thresholds,[i[1] for i in d])
plt.axis([None,None,35,45])
plt.title("Time based on different threshold")
plt.ylabel("Times(s)")
plt.xlabel("Different Thresholds")
plt.savefig("distribuptionTimeThreshold.png")

#read the outliers from distance
dDistanceLen=[len(i[0]) for i in d1]
dDistribLen=[len(i[0]) for i in d]
fig,axis=plt.subplots(2)
fig.suptitle("Number of outliers")
axis[0].plot(n,dDistanceLen)
axis[1].plot(thresholds[2:],dDistribLen[2:])
plt.savefig("outlierNumbers.png")

dataDistance=d1[3][0]
dataDistrib=d[-2][0]
counter=0
for i in dataDistance:
    for j in dataDistrib:
        if i[0]==j[0] and i[1]==j[1] and i[2]==j[2] and i[-1]==j[-1]:
            counter+=1
            break
