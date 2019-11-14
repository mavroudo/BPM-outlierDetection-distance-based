#!/usr/bin/env python3

import datetime 
from pm4py.algo.filtering.log.attributes import attributes_filter as log_attributes_filter

def dataPreprocess(log):
    activities_all = log_attributes_filter.get_attribute_values(log, "concept:name")
    activities=list(activities_all.keys())
    dataVectors=[]
    times=[[] for i in range(len(activities))]
    for trace in log:
        activitiesCounter=[0 for i in range(len(activities))]
        timesSpend=[datetime.timedelta(0) for i in range(len(activities))]
        previousTime=trace.attributes["REG_DATE"]
        for index,event in enumerate(trace):
            indexActivity=activities.index(event["concept:name"])
            activitiesCounter[indexActivity]+=1
            timesSpend[indexActivity]+=event["time:timestamp"]-previousTime
            times[indexActivity].append(event["time:timestamp"]-previousTime)
            previousTime=event["time:timestamp"]
        timesSpend=[(timesSpend[i]/activitiesCounter[i]).total_seconds() if activitiesCounter[i]!=0 else 0 for i in range(len(activities))] #contains the mo of all the activities
        dataVectors.append(activitiesCounter+timesSpend) 
    return dataVectors,times

from sklearn.preprocessing import StandardScaler
import numpy as np
def transform(dataVectors):
    transposeVector=[[data[i] for data in dataVectors] for i in range(len(dataVectors[0]))]
    standarizedData=[]
    for field in transposeVector:
        y=np.array(field).reshape(-1,1)
        sc=StandardScaler()
        sc.fit(y)
        standarizedData.append(sc.transform(y))
    transformedData=[[float(i) for i in k] for k in standarizedData]
    return [[data[i] for data in transformedData] for i in range(len(transformedData[0]))]
    
#This is for the data sequence
def getActivityLetter(index,letters):
    result=str(letters[index%26])
    if int(index/26) !=0:
        result+=str(int(index/26))
    return result

def transformAtrace(trace,bag):
    traceSeq=""
    for activity in trace:
        for index,bagAct in enumerate(bag[0]):
            if bagAct==activity["concept:name"]:
                traceSeq+=bag[1][index]+","
    return traceSeq[:-1]

def dataSequence(log):   
    activities = log_attributes_filter.get_attribute_values(log, "concept:name")
    letters=[i for i in "abcdefghijklmnopqrstuvwxyz"]
    bag=[[]for i in range(2)]
    for i in activities:
        bag[0].append(i)
    for index,activity in enumerate(activities):
        bag[1].append(getActivityLetter(index,letters))
    response=[]
    for trace in log:
        response.append(transformAtrace(trace,bag))
    return response,bag
    
    
    