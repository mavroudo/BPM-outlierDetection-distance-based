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
for i in timeToSeconds:
    k=np.array(i)
    k = k.reshape (-1,1)
    sc.fit(k)
    standarized.append(sc.transform(k))
    
#read distrs from txt
f=open("distributions.txt","r")
dists=[]
for i in f:
    dists.append(i.split(" "))

#get the distributions in a array
import scipy
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
test=standarized[1]
dist,param=distributions[1]

for i in test:
    outliers.append(float(dist.pdf(i,*param[:-2], loc=param[-2],scale=param[-1])))