#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 11:31:21 2021

@author: mavroudo
"""
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
import random
from statistics import mean
from datetime import timedelta

def add_reg_date(log):
    for trace in log:
        trace.attributes["REG_DATE"]=trace[0]["time:timestamp"]
    return log


def mean_value_per_Activity(log):
    data=dict()
    for trace in log:
        previous_time=0
        for index,event in enumerate(trace):
            if index==0:
                previous_time=trace.attributes["REG_DATE"]
            event_name=event["concept:name"]
            if event_name not in data:
                data[event_name]=[[],0]
            time=event["time:timestamp"]
            duration=time-previous_time
            data[event_name][0].append(duration.total_seconds())
            data[event_name][1]+=1
            previous_time=time
    return data
            

def delay_an_activity(log,trace_id,activity_stats):
    activity_id=random.randint(0,len(log[trace_id])-1)
    activity_name=log[trace_id][activity_id]["concept:name"]
    mean_value=mean(activity_stats[activity_name][0])
    diff=timedelta(seconds=3*mean_value) #increase the time by 3 times the standard deviation
    for event in log[trace_id][activity_id:]:
        event["time:timestamp"]+=diff
    return activity_id

def create_measurement_error(log,trace_id,activity_stats):
    activity_id=random.randint(0,len(log[trace_id])-2)
    activity_name=log[trace_id][activity_id]["concept:name"]
    mean_value=mean(activity_stats[activity_name][0])
    diff=timedelta(seconds=3*mean_value)
    log[trace_id][activity_id]["time:timestamp"]+=diff
    log[trace_id][activity_id+1]["time:timestamp"]-=diff
    return activity_id
    
def end_faster_activity(log,trace_id,activity_stats):
    activity_id=random.randint(0,len(log[trace_id])-1)
    activity_name=log[trace_id][activity_id]["concept:name"]
    mean_value=mean(activity_stats[activity_name][0])
    diff=timedelta(seconds=mean_value*0.7)
    for event in log[trace_id][activity_id:]:
        event["time:timestamp"]-=diff
    return activity_id


logfile="30_activities_5k.xes"
log=xes_import_factory.apply(logfile)
log_reg=add_reg_date(log)
activities_stats=mean_value_per_Activity(log_reg)
percentage=0.1
file="results_"+logfile.split(".")[0]+"_"+str(percentage)+"_description"
with open(file,"w") as f:
    for i in range(int(percentage*len(log))):
        trace_id=random.randint(0,len(log)-1)
        mode=random.random()
        outlier=""
        if mode<0.45:
            act_id=delay_an_activity(log_reg,trace_id,activities_stats)
            outlier="delay"
        elif mode<0.9:
            act_id=end_faster_activity(log_reg,trace_id,activities_stats)
            outlier="faster"
        else:
            act_id=create_measurement_error(log_reg,trace_id,activities_stats)
            outlier="measurement"
        f.write(",".join([outlier,str(trace_id),str(act_id)])+"\n")
filename="outliers_"+logfile.split(".")[0]+"_"+str(percentage)
xes_exporter.export_log(log_reg,filename+".xes")
