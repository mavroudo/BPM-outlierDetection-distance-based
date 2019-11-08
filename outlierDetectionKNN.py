#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
import time
def outliersKNN(D,R,k,outliersPerKR,outliersLock):
   print(k,R)
   outliers=[]  
   d=0
   for indexTrace,trace in enumerate(D): #this will return all the traces
       count=-1
       for indexOthers,x in enumerate(trace):
           if indexTrace==indexOthers :
              d=0
           elif indexTrace>indexOthers:
              d=D[indexOthers][indexTrace-indexOthers]
           else:
              d=D[indexTrace][indexOthers-indexTrace]
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
            while True:
                active=0
                for thread in threads:
                    if thread.isAlive() : 
                        active+=1
                if active<8:
                    break
                else:
                    time.sleep(2)
    [thread.join() for thread in threads]
    return outliersPerKR

