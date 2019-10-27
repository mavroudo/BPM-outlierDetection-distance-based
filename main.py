#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#import 
from pm4py.objects.log.importer.xes import factory as xes_factory
from DataPreprocess import dataPreprocess, transform
from outlierDetectionKNN import testKNNparameters
from distanceEvaluation import writeToFile,plotDistanceDistribution
from Distance import findAllDistances


log=xes_factory.apply("BPI_Challenge_2012.xes")
results,statsTimes=dataPreprocess(log)
sequenceStandarized,timeStandarized=transform(results,statsTimes)
distances=findAllDistances(sequenceStandarized,timeStandarized)
writeToFile(distances,"distances.txt")
plotDistanceDistribution(distances,"Distances")
R=[0.5,1,1.5,2,2.5,3]
K=[20,50,100,200,500]
print("Testing distance parameters")
outliersPerParameter=[i for i in testKNNparameters(R,K,distances,log)]





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
        