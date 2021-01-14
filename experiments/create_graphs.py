#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 17:49:30 2021

@author: mavroudo
"""
import matplotlib.pyplot as plt
#for volumes

def create_plot(filename):
    data=[]
    with open(filename,"r") as f:
        for line in f:
            data.append(line.replace("\n","").split(","))
    methods=list(set([i[0] for i in data]))
    dataPerMethod=dict()
    for method in methods:
        dataPerMethod[method]=[]
        for d in data:
            if d[0]==method:
                dataPerMethod[method].append(float(d[4]))
    k=[1,3,10,20,50,100]
    fig=plt.figure()
    for method in methods:
        plt.plot(k,dataPerMethod[method],label=method)
    plt.legend()
    plt.xlabel("Different k")
    plt.ylabel("Percentage of outliers found")
    plt.savefig("figs/"+filename+".png")


# for different dimensions
def create_plot_dimensions(filename):
    data=[]
    with open(filename,"r") as f:
        for line in f:
            data.append(line.replace("\n","").split(","))
    dims=[3, 5, 10, 15, 20, 24]
    pca=[]
    pure=0
    ballTree=0
    for d in data:
        if d[0]=="PCA":
          pca.append(float(d[3]))
        if d[0] =="Pure":
            pure=float(d[3])
        elif d[0]=="BallTree":
            ballTree=float(d[3])
    fig=plt.figure()
    plt.plot(dims,pca,label="PCA")
    plt.plot(dims,[pure for _ in range(len(dims))],label="Without reduction")
    plt.plot(dims,[ballTree for _ in range(len(dims))],label="With indexing Ball Tree")
    plt.xlabel("Dimensions")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.savefig("figs/"+filename+"_time.png")
    pca=[]
    pure=0
    ballTree=0
    for d in data:
        if d[0]=="PCA":
          pca.append(float(d[4]))
        if d[0] =="Pure":
            pure=float(d[4])
        elif d[0]=="BallTree":
            ballTree=float(d[4])
    fig=plt.figure()
    plt.plot(dims,pca,label="PCA")
    plt.plot(dims,[pure for _ in range(len(dims))],label="Without reduction")
    plt.plot(dims,[ballTree for _ in range(len(dims))],label="With indexing Ball Tree")
    plt.xlabel("Dimensions")
    plt.ylabel("Percentage of outliers found")
    plt.legend()
    plt.savefig("figs/"+filename+"_accuracy.png")
    

filename="30_activities_5k_0.1_precision_recall"
data=[]
with open(filename,"r") as f:
    for line in f:
        data.append(line.replace("\n","").split(","))
rs_k_50=[]
for d in data:
    if d[0]=='50':
        rs_k_50.append([float(d[1]),float(d[2]),float(d[3])])
fig=plt.figure()
plt.plot([i[0] for i in rs_k_50],[i[1] for i in rs_k_50],label="Precision")
plt.plot([i[0] for i in rs_k_50],[i[2] for i in rs_k_50],label="Recall")
plt.title("Precision and recall for k=50 and different values of r")
plt.legend()
plt.xlabel("r")
plt.ylabel("Percentage (%)")
plt.savefig("figs/"+filename+"rs.png")

ks_r_005=[]
for d in data:
    if d[1]=='0.01':
        ks_r_005.append([float(d[0]),float(d[2]),float(d[3])])
del ks_r_005[-1]
del ks_r_005[0]
fig=plt.figure()
plt.plot([i[0] for i in ks_r_005],[i[1] for i in ks_r_005],label="Precision")
plt.plot([i[0] for i in ks_r_005],[i[2] for i in ks_r_005],label="Recall")
plt.title("Precision and recall for r=0.0 and different values of r")
plt.legend()
plt.xlabel("r")
plt.ylabel("Percentage (%)")
plt.savefig("figs/"+filename+"ks.png")


k=[1,3,10,20,50,100,200,500]
r=[0.01,0.05,0.1,0.15,0.2]



