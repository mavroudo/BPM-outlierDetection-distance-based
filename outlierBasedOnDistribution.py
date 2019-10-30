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
timeToSeconds=[[i.total_seconds() for i in j] for j in statsTimes] #transform to seconds

#standarize data
from sklearn.preprocessing import StandardScaler
import numpy as np
sc=StandardScaler()
standarized=[]
standarScalers=[]
for i in timeToSeconds:
    k=np.array(i)
    k = k.reshape (-1,1)
    sc.fit(k)
    standarScalers.append(sc)
    standarized.append(sc.transform(k))
    
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

#test=standarized[1]
dist,param=distributions[1]

for i in test:
    outliers.append(float(dist.pdf(i,*param[:-2], loc=param[-2],scale=param[-1])))
    
outliers=[]
threshold=0.005 #1% if it belongs to 1% of the data in a dist is an outlier
trace=results[:2]
for index,i in enumerate(trace):
    for innerIndex,event in enumerate(i[int(len(i)/2):]): # looping through the time events
        seconds=0.0 if event == 0 else event.total_seconds()
        dist,param=distributions[innerIndex]
        x=standarScalers[innerIndex].transform(np.array(seconds).reshape(1,-1))
        predict=float(dist.pdf(x,*param[:-2], loc=param[-2],scale=param[-1]))
        if predict<threshold:
            outliers.append([index,innerIndex])
            break

        
            