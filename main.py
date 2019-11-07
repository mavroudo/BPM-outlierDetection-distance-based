#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#import 

from DataPreprocess import dataPreprocess, transform
from outlierDetectionKNN import testKNNparameters
from distanceEvaluation import writeToFile,plotDistanceDistribution
from Distance import calculateDistances

from pm4py.objects.log.importer.xes import factory as xes_factory
log=xes_factory.apply("BPI_Challenge_2012.xes")

dataVectors,statsTimes=dataPreprocess(log)
dataVectorsStandarized=transform(dataVectors)
distances=calculateDistances(dataVectorsStandarized)
writeToFile(distances,"distances.txt")
plotDistanceDistribution(distances,"Distances")
R=[0.5,1,1.5,2,2.5,3]
K=[20,50,100,200,500]
print("Testing distance parameters")
outliersPerParameter=[i for i in testKNNparameters(R,K,distances)]





log2=xes_factory.apply("BPI Challenge 2017.xes")

#outlier detection based on sequences 
from DataPreprocess import dataSequence
from CreatingGraph import condactWeightedEdges
from CreatingGraph import outliers

dataSequence,bag=dataSequence(log)
weightedEdges=condactWeightedEdges(dataSequence,bag[1])
outlierSequences,outlierEdges=outliers(weightedEdges,0.1,dataSequence)

dataSequence2,bag2=dataSequence(log2)
weightedEdges=condactWeightedEdges(dataSequence2,bag2[1])
outlierSequences,outlierEdges=outliers(weightedEdges,0.1,dataSequence)
        

#def transform(dataVector):
from distanceEvaluation import readFromFile
distances=readFromFile("distances.txt")
values=[]
for i in range(len(distances)):
    for j in range(len(distances)):
        if i<j:
            values.append(distances[i][j])
del distances
values=[round(i,5) for i in list(values)]


      
import matplotlib.pyplot as plt
fig1, ax1 = plt.subplots()
ax1.set_title('Basic Plot')
ax1.boxplot(values)