#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pm4py.objects.log.importer.xes import factory as xes_factory
from DataPreprocess import dataPreprocess

log=xes_factory.apply("BPI_Challenge_2012.xes")
results,statsTimes=dataPreprocess(log)
timeToSeconds=[[i.total_seconds() for i in j] for j in statsTimes] #transform to seconds

#try to curve fit in the first dimention
import scipy
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

y=timeToSeconds[0]
x=np.arange(len(y))
size=len(y)
plt.hist(y)
plt.show()