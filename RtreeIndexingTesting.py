#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 10:11:22 2019

@author: mavroudo
"""

from mtree import MTree
from Distance import distanceMtree
from pm4py.objects.log.importer.xes import factory as xes_factory
from DataPreprocess import dataPreprocess
log=xes_factory.apply("BPI_Challenge_2012.xes")
dataVectors,statsTime=dataPreprocess(log)
min_node_capacity=30
myTree=MTree(min_node_capacity=min_node_capacity,distance_function=distanceMtree)
for index,vector in enumerate(dataVectors):
    myTree.add(str(vector))

x=myTree.get_nearest(str(dataVectors[1]),range=5)

    





