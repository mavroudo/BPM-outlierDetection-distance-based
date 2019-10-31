#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#arxika kanonikopoioume ta dedomena kai kanoume fit thn sunarthsh distribution
#sth sunexeia me to pdf gia ka8ena kanoume remove an anhkei sto ligotero apo 1%
#se ka8e katanomh, sth sunexeia kanoume report ta apotelesmata

#auto tha diagrafei otan dhmiourgh8ei h sunarthsh
from pm4py.objects.log.importer.xes import factory as xes_factory
from DataPreprocess import dataPreprocess

log=xes_factory.apply("BPI_Challenge_2012.xes")
results,statsTimes=dataPreprocess(log)
allTimes=[[i.total_seconds() for i in j] for j in statsTimes] #transform to seconds

timedata=[i[int(len(i)/2):] for i in results]
timeDataToSeconds=[[i.total_seconds() if i !=0 else 0 for i in j] for j in timedata]#make them seconds

#standarize data
from sklearn.preprocessing import StandardScaler
import numpy as np
standarized=[]
standarScalers=[]
for index,i in enumerate(allTimes):
    sc=StandardScaler()
    k=np.array(i)
    k = k.reshape (-1,1)
    sc.fit(k) #fit to the all of the times spend 
    standarScalers.append(sc)
    #resultsTimeData=np.array(timeDataToSeconds[index]).reshape (1,-1)
    standarized.append(sc.transform(k)) #trnasform the values in the result
    
#read distrs from txt
f=open("distributions.txt","r")
dists=[]
for i in f:
    dists.append(i.split(" "))

#get the distributions in a array
import warnings  
import scipy
warnings.filterwarnings("ignore")
distributions=[]
for index,i in enumerate(dists):
    if i[0]!="non":
        dist = getattr(scipy.stats, i[1])
        param = dist.fit(standarized[index])
        distributions.append([dist,param])
    else: 
        distributions.append([])
    
#perform outlier detection trace by trace
outliers=[]
threshold=0.01 #0,1% if it belongs to 1% of the data in a dist is an outlier
trace=results[:2]
for index,i in enumerate(results):
    print(index)
    for innerIndex,event in enumerate(timedata[index]): # looping through the time events
        seconds=None if event == 0 else [event.total_seconds()]
        if seconds != None:
            dist,param=distributions[innerIndex]
            x=standarScalers[innerIndex].transform(np.array(seconds).reshape(1,-1))
            predict=float(dist.pdf(x,*param[:-2], loc=param[-2],scale=param[-1]))
            if predict<threshold:
                outliers.append([index,innerIndex])
                break

#this working except from 0 position
possitions=[i[1] for i in outliers]
from collections import Counter
Counter(possitions).keys()
Counter(possitions).values()
