#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
def outliersKNN(D,R,k,outliersPerKR,outliersLock):
   print(k,R)
   outliers=[]  
   d=0
   for indexTrace,trace in enumerate(D):
       count=-1
       for indexOthers,x in enumerate(trace):
           if indexTrace>indexOthers :
              d=D[indexOthers][indexTrace]
           else:
              d=D[indexTrace][indexOthers]
           if d<=R:
              count+=1
              if count==k:
                  break
       if count<k:
           outliers.append(indexTrace)
   while outliersLock.locked():
       continue
   outliersLock.acquire()
   outliersPerKR.append([k,R,len(outliers)]) 
   outliersLock.release()
   
def testKNNparameters(R,K,D):
    threads=[]
    outliersPerKR=[]
    outliersLock=threading.Lock()
    for r in R:
        for k in K:
            t=threading.Thread(target=outliersKNN,args=(D,r,k,outliersPerKR,outliersLock))
            threads.append(t)
            t.start()
    [thread.join() for thread in threads]
    return outliersPerKR

