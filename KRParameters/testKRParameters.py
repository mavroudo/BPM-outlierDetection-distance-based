#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 11:25:37 2019

@author: mavroudo
"""
from DataPreprocess import dataPreprocess, transform
from Distance import calculateDistances
from pm4py.objects.log.importer.xes import factory as xes_factory
log=xes_factory.apply("BPI_Challenge_2012.xes")

dataVectors,statsTimes=dataPreprocess(log)
dataVectorsStandarized=transform(dataVectors)
print("calculating distances")
distances=calculateDistances(dataVectorsStandarized)
from distanceEvaluation import writeToFile
print("writing to file")
distances=writeToFile(distances,"distances.txt")
from outlierDetectionKNN import testKNNparameters
R=[i/10 for i in range(1,30,1)]
K=[i for i in range(20,500,20)]
print("Testing distance parameters")
outliersPerParameter=[i for i in testKNNparameters(R,K,distances)]
file=open("krParameters.txt","w")
for outlier in outliersPerParameter:
    file.write(str(outlier[0])+", "+str(outlier[1])+", "+str(outlier[2])+"\n")
file.close()