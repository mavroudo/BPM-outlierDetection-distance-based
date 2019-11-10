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
K=[i/10 for i in range(2,31)]
R=[i for i in range(20,500,20)]
outlierPerKR,preparedQueries=testKNNparameters(R,K,dataVectorsStandarized,myTree,preparedQueries=preparedQueries)

#plot 
import matplotlib.pyplot as plt
rStatic=[i[2] for i in outlierPerKR if i[1]==1]
kStatic=[i[2] for i in outlierPerKR if i[0]==300]
fig,(ax1,ax2)=plt.subplots(1,2)
plt.title("Number of outliers base on K and R values")
ax1.plot(K,rStatic)
ax1.set_title("R is constant")
ax2.plot(R,kStatic)
ax2.set_title("K is constant")
plt.show()





from distanceEvaluation import readFromFileSampling
distances=readFromFileSampling("distances.txt")
from random import sample
sampled=sample(distances,int((len(log)**2)/100))
del distances
import matplotlib.pyplot as plt
fig1, ax1 = plt.subplots()
ax1.set_title('Basic Plot')
ax1.boxplot(sampled)
plt.show()












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
        


      
