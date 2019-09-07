#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#Load for the first time
from pm4py.objects.log.importer.xes import factory as xes_factory
log=xes_factory.apply("BPI_Challenge_2012.xes")

from DataPreprocess import dataPreprocess
results,statsTimes=dataPreprocess(log)

minmaxTimes=[[min(statsTimes[i]),max(statsTimes[i])] for i in range(len(statsTimes))]

from distanceEvaluation import findAllDistances
distances=findAllDistances(results,minmaxTimes)
from distanceEvaluation import writeToFile
writeToFile(distances,"distances.txt")


#Have already being saved in a file
from distanceEvaluation import readFromFile
distances=readFromFile("distances.txt")
from distanceEvaluation import plotDistanceDistribution
plotDistanceDistribution(distances,"Distribution1")

#Testing KNN for different R and K values
from outlierDetectionKNN import testKNNparameters
R=[5,10,20,30,50]
K=[20,50,100,200,500]
testKNNparameters(R,K,distances)






        