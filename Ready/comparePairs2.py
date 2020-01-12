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
import outlierDistanceActivities,outlierPairsCurveFitting, outlierPairWise
n=[10,20,50,100,250]
d=[outlierDistanceActivities.main(logFile,neighbors,stdDeviationTimes=4,threshold=None) for neighbors in n]
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
import random
x=[random.randint(0,40) for i in range(30)]
y=[random.randint(80,120) for _ in range(30)]
k=x+[60]+y

thresholds = [0.1,0.05,0.02,0.01,0.0075,0.005,0.0025,0.001]
d=[outlierPairsCurveFitting.main(logFile,threshold) for threshold in thresholds]
with open("distributionTimes.txt","w") as f:
    for index,x in enumerate(d):
        f.write(str(thresholds[index])+","+str(x[1])+"\n")
        with open("outliersDistribution.txt","a+") as outFile:
            outFile.write(str(threshold[index])+"\n")
            for outlier in x[0]:
                outFile.write(str(outlier)+"\n")