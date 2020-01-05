#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 12:25:57 2020

@author: mavroudo
"""
import outlierPairsCurveFitting,outlierPairWise
logFile="../BPI_Challenge_2012.xes"

with open("tests.txt","w") as f:
    f.write("Neighbors Threshold Hits Misses\n")
    for neighbors in [20,50,100,250,100]:
        for threshold in [0.1,0.05,0.01,0.005,0.001]:
            print("Finding outliers with distribution ...")
            #[traceIndex,activity1,activity2,time1,time2,over/under/ok,over/under/ok,eventIndexInTrace1]
            distributionOutlierPairs=outlierPairsCurveFitting.main(logFile,threshold)
            print("Finding outliers using distance ...")
            #[traceIndex,activity1,activity2,scaledTime1,scaledTime2,eventIndexInTrace1,score]
            distanceOutlierPairs=outlierPairWise.main(logFile,neighbors,len(distributionOutlierPairs))
            
            hits=[]
            miss=[]
            for do in distanceOutlierPairs:
                flag=False
                for io in distributionOutlierPairs:
                    if do[0]==io[0] and do[1]==io[1] and do[2]==io[2] and do[5]==io[7]:
                        hits.append(do)
                        flag=True
                        break
                if not flag:
                    miss.append(do)
            f.write(str(neighbors)+" "+str(threshold)+" "+str(len(hits))+" "+str(len(miss))+"\n")
