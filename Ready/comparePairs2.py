#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 19:22:53 2020

@author: mavroudo
"""
import outlierDistanceActivities,outlierPairsCurveFitting, outlierPairWise
logFile="../BPI_Challenge_2012.xes"
with open("tests.txt","w") as f:
    f.write("Neighbors Threshold Hits Misses\n")
    #for neighbors in [20,50,100,250,1000]:
    with open("timeDistanceTest.txt","w") as timeTest:
        for neighbors in [10,25,50,75,100,150,200]:
            distanceOutlierPairsPre,t1=outlierDistanceActivities.main(logFile,neighbors,stdDeviationTimes=4,threshold=None)
            with open("timeDistributionTest.txt","w") as dtimeTest:            
                for threshold in [0.1,0.075,0.05,0.025,0.01,0.0075,0.005,0.0025,0.001]:                    
                    timeTest.write(str(neighbors)+","+str(t1)+"\n")
                    print(neighbors,threshold)
                    #[traceIndex,activity1,activity2,time1,time2,over/under/ok,over/under/ok,eventIndexInTrace1]
                    distributionOutlierPairs,time=outlierPairsCurveFitting.main(logFile,threshold)
                    dtimeTest.write(str(threshold)+","+str(time)+"\n")
                    #[traceIndex,activity1,activity2,scaledTime1,scaledTime2,eventIndexInTrace1,score]
                    distanceOutlierPairs=distanceOutlierPairsPre[:len(distributionOutlierPairs)]
                    
                    hits=[]
                    miss=[]
                    for do in distanceOutlierPairs:
                        flag=False
                        for io in distributionOutlierPairs:
                            if do[0]==io[0] and do[1]==io[1] and do[2]==io[2] and do[7]==io[7]:
                                hits.append(do)
                                flag=True
                                break
                        if not flag:
                            miss.append(do)
                    f.write(str(neighbors)+" "+str(threshold)+" "+str(len(hits))+" "+str(len(miss))+"\n")



neighbors=10
distanceOutlierPairsPre,t1=outlierDistanceActivities.main(logFile,neighbors,stdDeviationTimes=4,threshold=None)
neighbors=50
distanceOutlierPairsPre50,t50=outlierDistanceActivities.main(logFile,neighbors,stdDeviationTimes=4,threshold=None)
neighbors=10

logFile="../BPI_Challenge_2012.xes"
import outlierDistanceActivities,outlierPairsCurveFitting
n=[20,50,100,250,500,750,1000]
d1=[outlierDistanceActivities.main(logFile,neighbors,stdDeviationTimes=4,threshold=None) for neighbors in n]
with open("outlierEventTime.txt","w") as f:
    for index,x in enumerate(d1):
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
import random
x=[random.randint(0,40) for i in range(30)]
y=[random.randint(80,120) for _ in range(30)]
k=x+[60]+y

#thresholds = [0.1,0.05,0.02,0.01,0.0075,0.005,0.0025,0.001]
thresholds=[0.0025,0.005,0.0075,0.01,0.0125,0.0150,0.0175,0.02]
d=[outlierPairsCurveFitting.main(logFile,threshold) for threshold in thresholds]
with open("distributionTimes.txt","w") as f:
    for index,x in enumerate(d):
        f.write(str(thresholds[index])+","+str(x[1])+"\n")
        with open("outliersDistribution.txt","a+") as outFile:
            outFile.write(str(threshold[index])+"\n")
            for outlier in x[0]:
                outFile.write(str(outlier)+"\n")
                

#compare the number of outliers in d (distributions) and d1 (distance)
n=[100,250,500,750,1000,1500,2000]
d1=[outlierDistanceActivities.main(logFile,neighbors,stdDeviationTimes=4,threshold=None) for neighbors in n]
import matplotlib.pyplot as plt
import numpy as np
thresholds=[0.001,0.0025,0.005,0.0075,0.01,0.0125,0.0150,0.0175,0.02]
d=[outlierPairsCurveFitting.main(logFile,threshold) for threshold in thresholds]
d_length=[len(x[0]) for x in d]
d1_length=[len(x[0]) for x in d1]
yaxis=np.arange(min(min(d_length),min(d1_length)),max(max(d1_length),max(d_length))+200,200)
minimum=min(min(d_length),min(d1_length))
maximum=max(max(d1_length),max(d_length))
fig=plt.figure()
ax=fig.add_subplot(111, label="distance")
ax2=fig.add_subplot(111, label="distribution", frame_on=False)
ax.plot(n, d1_length, color="C0")
ax.set_xlabel("Number of Neighbors", color="C0")
ax.set_ylabel("Number of outliers", color="C0")
ax.set_ylim([minimum,maximum])
ax.tick_params(axis='x', colors="C0")
#ax.tick_params(axis='y', colors="C0")
ax2.plot(thresholds, d_length, color="C1")
ax2.xaxis.tick_top()
ax2.set_xlabel('Threshold', color="C1")      
ax2.xaxis.set_label_position('top') 
ax2.tick_params(axis='x', colors="C1")
ax2.set_ylim([minimum,maximum])
plt.grid(True)
plt.savefig("numberofoutliers.png")
plt.show()

k=outlierPairsCurveFitting.main(logFile,0.003)
k1=outlierDistanceActivities.main(logFile,300,stdDeviationTimes=4,threshold=None)
hits=[]
miss=[]
for distrO in k[0]:
    flag=False
    for distanceO in k1[0]:
        if distrO[0]==distanceO[0] and distrO[1]==distanceO[1] and distrO[2]==distanceO[2] and distrO[7]==distanceO[7]:
            hits.append(distrO)
            flag=True
            break
    if not flag:
        miss.append(distrO)
