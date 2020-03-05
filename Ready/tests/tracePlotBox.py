#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 11:33:26 2020

@author: mavroudo
"""
import matplotlib.pyplot as plt
neighbors=50
data=[]
with open("tests/krTest.txt","r") as f: 
    for line in f:
        if int(line.split(",")[0])==neighbors:
           data=(list(map(float,line.split(",")[:-1])))

       
#import random
#data=sorted([random.randint(0,100) for i in range(100)])

plt.boxplot(data[1:])
plt.title("Outlying Factor Distribution")
plt.ylabel("Sum of distances from {}-nn".format(neighbors))
plt.show()