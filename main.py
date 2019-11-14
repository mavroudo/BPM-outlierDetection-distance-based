#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#import 

from DataPreprocess import dataPreprocess, transform
from distanceEvaluation import writeToFile,plotDistanceDistribution
from Distance import distanceMtree
from mtree import MTree


from pm4py.objects.log.importer.xes import factory as xes_factory
print("Loading data..")
log=xes_factory.apply("BPI_Challenge_2012.xes")
print("Preprocess Data..")
dataVectors,statsTimes=dataPreprocess(log)
dataVectorsStandarized=transform(dataVectors)
print("Creating Mtree...")

myTree=MTree(distance_function=distanceMtree,min_node_capacity=50)
for index,vector in enumerate(dataVectorsStandarized):
    print(index)
    try:
        myTree.add(str(vector))
    except:
        pass


print("Testing distance parameters")
from outlierKNN import testKNNparameters,calculateQueries
preparedQueries=calculateQueries(myTree,dataVectorsStandarized,500,3)
#write distance from neighrest neighbors so we will not need to calculate them again
with open("neirestNeighbors.txt","w") as f:
    for neighbors in preparedQueries:
        for neighbor in neighbors:
            f.write(str(neighbor)+" ")
        f.write("\n")
        
        
#run with the RK after the calculation 
preparedQueries=[]
with open("neirestNeighbors.txt","r") as f:
    for index,line in enumerate(f):
        print(index)
        preparedQueries.append([float(i) for i in line.split(" ")[:-1]])
        
from outlierKNN import outliersKNN2
outliers=outliersKNN2(preparedQueries,50,50)





distances=calculateDistances(dataVectorsStandarized)
writeToFile(distances,"distances.txt")
plotDistanceDistribution(distances,"Distances")
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
        


      
