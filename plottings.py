#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 10:29:01 2019

@author: mavroudo
"""

#ploting for k        
K=[5,10,50,100,150,200,250]
sums=[]
for k in K:
    print(k)
    sumsForKneighbors=[]
    for q in preparedQueries:
        count=0
        for i in range(1,k+1):
            try:
                count+=q[i]
            except:
                pass
        sumsForKneighbors.append(count)
    sums.append(sumsForKneighbors)
ordered=[sorted(i) for i in sums ]
del sums
import matplotlib.pyplot as plt
import numpy as np
plt.plot(np.arange(1,len(ordered[0])+1),ordered[0],"-",label="k=5")
plt.plot(np.arange(1,len(ordered[0])+1),ordered[1],":",label="k=10")
plt.plot(np.arange(1,len(ordered[0])+1),ordered[2],"-.",label="k=50")
plt.plot(np.arange(1,len(ordered[0])+1),ordered[3],"--",label="k=100")
plt.plot(np.arange(1,len(ordered[0])+1),ordered[4],"-",label="k=150")
plt.plot(np.arange(1,len(ordered[0])+1),ordered[5],":",label="k=200")
plt.plot(np.arange(1,len(ordered[0])+1),ordered[6],"-.",label="k=250")
plt.legend(loc='best')
plt.savefig("Kneigherest-Sum.png")
plt.show()


#Distance plot
from distanceEvaluation import readFromFileSampling
import numpy as np
distances=readFromFileSampling("distances.txt")
from random import sample
sampled=sample(distances,int((len(log)**2)/100))
del distances
import matplotlib.pyplot as plt
sampledNonZero=[i for i in sampled if i !=0.0]
fig1, ax1 = plt.subplots()
ax1.set_title('Basic Plot')
plt.yticks(np.arange(min(sampled), max(sampled), 1))
ax1.boxplot(sampledNonZero)
plt.title("Distance Distribution")
plt.savefig("BoxPlot-Distances.png")
plt.show()