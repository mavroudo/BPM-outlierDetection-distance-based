#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#Load for the first time
from pm4py.objects.log.importer.xes import factory as xes_factory
log=xes_factory.apply("BPI_Challenge_2012.xes")
from DataPreprocess import dataPreprocess
results,statsTimes=dataPreprocess(log)
minmaxTimes=[[min(statsTimes[i]),max(statsTimes[i])] for i in range(len(statsTimes))]

#distance naive with uniform distributon of time and not equally value in the final metric
from DistancenNaive import findAllDistances 
distancesNaive=findAllDistances(results,minmaxTimes)
from distanceEvaluation import writeToFile
writeToFile(distancesNaive,"distancesNaive.txt")

from DistanceSamping import findAllDistancesWithSampling
distanceSampling=findAllDistancesWithSampling(results,statsTimes,percentOfData=0.1,numberOfCells=20)
from distanceEvaluation import writeToFile
writeToFile(distanceSampling,"distancesSampling.txt")



#Have already being saved in a file
from distanceEvaluation import readFromFile
from distanceEvaluation import plotDistanceDistribution
distancesNaive=readFromFile("distancesNaive.txt")
plotDistanceDistribution(distancesNaive,"DistributionNaiveDistance")
distanceSampling=readFromFile("distancesSampling.txt")
plotDistanceDistribution(distanceSampling,"DistributionSamplingDistance")



#Testing KNN for different R and K values
from outlierDetectionKNN import testKNNparameters
R=[5,10,20,30,50]
K=[20,50,100,200,500]
print("NaiveDistance")
testKNNparameters(R,K,distancesNaive)
print("SamplingDistance")
testKNNparameters(R,K,distanceSampling)






        