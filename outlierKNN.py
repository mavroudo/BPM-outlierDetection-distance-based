#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 11:45:17 2019

@author: mavroudo
"""
import threading
from mtree import MTree
import time
def outliersKNN2(queries:list,R,K):
    outliers=[]
    for index,i in enumerate(queries):
        try:
            if i[K+1]>R:
                outliers.append(index)
        except IndexError:
            outliers.append(index)
    return outliers
    
    #while outliersLock.locked():
    #    continue
    #outliersLock.acquire()
    #outliersPerKR.append([K,R,len(outliers)]) 
    #outliersLock.release()
    
    
def outliersKNN(queries:list,K):
    outliers=[]
    for index,i in enumerate(queries):
        if len(i)<K+1:
            outliers.append(index)
    return outliers
    
def testKNNparameters(R,K,dataVectors,mtree:MTree,preparedQueries=None):
    threads=[]
    outliersPerKR=[]
    outliersLock=threading.Lock()
    print("Prepare Queried Data...")
    if preparedQueries==None:
        preparedQueries=calculateQueries(mtree,dataVectors,max(K),max(R))    
    print("Start multyThreading approach")
    for r in R:
        for k in K:
            t=threading.Thread(target=outliersKNN,args=(preparedQueries,mtree,r,k,outliersPerKR,outliersLock))
            threads.append(t)
            t.start()
            while True:
                active=0
                for thread in threads:
                    if thread.isAlive() : 
                        active+=1
                if active<4:
                    break
                else:
                    time.sleep(2)
    [thread.join() for thread in threads]
    return outliersPerKR,preparedQueries

def calculateQueries(mtree:MTree, dataVectors:list,K,R):
    queries=[]
    for index,dataVector in enumerate(dataVectors): 
        print(index)
        x=list(mtree.get_nearest(str(dataVector),range=R,limit=K))
        m=[i[1] for i in x]
        queries.append(m)
    return queries

    