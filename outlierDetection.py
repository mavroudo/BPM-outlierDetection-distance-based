#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 19:32:03 2019

@author: mavroudo
"""

from pm4py.objects.log.importer.xes import factory as xes_factory
log=xes_factory.apply("BPI_Challenge_2012.xes")

from DataPreprocess import dataPreprocess
results,statsTimes=dataPreprocess(log)



import datetime

activity5=statsTimes[4] #can use min max average mean 


x=sum(statsTimes[0],datetime.timedelta())/len(statsTimes[0])
minimum=min(statsTimes[0])



        