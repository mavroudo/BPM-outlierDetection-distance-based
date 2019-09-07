#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def outliersKNN(distances,R,k):
   outliers=[]  
   d=0
   for indexTrace,trace in enumerate(distances):
       count=-1
       for indexOthers,x in enumerate(trace):
           if indexTrace>indexOthers :
              d=distances[indexOthers][indexTrace]
           else:
              d=distances[indexTrace][indexOthers]
           if d<=R:
              count+=1
              if count==k:
                  break
       if count<k:
           outliers.append(trace)
   return outliers
   
def testKNNparameters(R,K,distances):
    for r in R:
        for k in K:
            outliers=outliersKNN(distances,r,k)
            print(str(r)+", "+str(k)+", "+str(len(outliers)))

