#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 09:01:48 2020

@author: mavroudo
"""

import random
import matplotlib.pyplot as plt
import numpy as np
x=[]
y=[]
for _ in range(80):
    x.append(random.uniform(0,0.5))
    y.append(random.uniform(0,0.5))
    x.append(random.uniform(-0.5,0))
    y.append(random.uniform(-0.5,0))
for _ in range(15):
    x.append(random.uniform(0.5,2))
    y.append(random.uniform(0.5,2))
    x.append(random.uniform(-2,-0.5))
    y.append(random.uniform(-2,-0.5))
for _ in range(5):
    x.append(random.uniform(2,15))
    y.append(random.uniform(2,15))
    x.append(random.uniform(-15,-2))
    y.append(random.uniform(-15,-2))


random.shuffle(x)
random.shuffle(y)
x.append(-10)
y.append(15)
x.append(10)
y.append(12)
colors=[]
for a,b in zip(x[:-2],y[:-2]):
    if a>=2 or b>=2 or a<=-2 or b<=-2:
        colors.append([0,0,255])
    else:
        colors.append([0,0,0])
colors.append([255,0,0])
colors.append([0,255,0])
C=np.array(colors)
fig = plt.figure()
plt.scatter(x,y,c=C/255.0)
plt.title(label="Data points distribution") 
plt.savefig("datapointsdistr.png")
plt.show()