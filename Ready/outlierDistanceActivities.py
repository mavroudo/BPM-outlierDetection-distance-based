#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 10:22:47 2020

@author: mavroudo
"""
from pm4py.objects.log.importer.xes import factory as xes_factory
from pm4py.algo.filtering.log.attributes import attributes_filter as log_attributes_filter
from bisect import bisect
from heapq import nsmallest
import time
from statistics import stdev
from statistics import mean


def dataPreprocess(log):
    activities_all = log_attributes_filter.get_attribute_values(log, "concept:name")
    activities = list(activities_all.keys())
    times = [[] for i in range(len(activities))]
    sequence = []
    for indexTrace, trace in enumerate(log):
        previousTime = trace.attributes["REG_DATE"]
        sequence.append([])
        for index, event in enumerate(trace):
            indexActivity = activities.index(event["concept:name"])
            time = event["time:timestamp"] - previousTime
            times[indexActivity].append([indexTrace, index, time.total_seconds()])
            previousTime = event["time:timestamp"]
            sequence[-1].append([indexActivity, time.total_seconds()])
    return times, sequence


def k_nearest(k, center, sorted_data):
    'Return *k* members of *sorted_data* nearest to *center*'
    i = bisect(sorted_data, center)
    segment = sorted_data[max(i - k, 0): i + k]
    return nsmallest(k, segment, key=lambda x: abs(x - center))


def score(dataList, k):
    """
        Calculate the outlying score based on the k neighrest neighbors for every event
        of this activity. Distance is calculating by the the absolute value between
        2 elements and the all the distances are summed up. It returns the scores
        sorted reverse, the mean value of the times and the standard deviation.
    """
    scores = []
    distances = []
    sortedTimes = sorted([i[2] for i in dataList])
    for index, event in enumerate(dataList):
        neighbors = k_nearest(k + 1, event[2], sortedTimes)
        distance = sum([abs(event[2] - n) for n in neighbors])
        scores.append(event + [distance])
        distances.append(distance)
    return sorted(scores, key=lambda x: x[3], reverse=True), mean(distances), stdev(distances)


def findOutlierEvents(dataVectors, k, stdDeviationTImes=4, threshold=None):
    """
        This function will return all the outlier events of their activity based
        on one of the 2 things. Either find the events that deviates more than 
        stdDeviationTImes from the mean value, or if a value for threshold is given,
        it will report the top "threshold" events based on their outlying score.
        The outlying score is calculated by the distance from each event from the
        k neighrest neighbors.
    """
    outliers = []
    for activity in dataVectors:
        scores, mean, std = score(activity, k)
        if threshold != None:
            topOutliers = int(threshold * len(activity))
            for i in range(1, topOutliers + 1):
                outliers.append(scores[-1 * i])
        else:
            outlyingUP = mean + stdDeviationTImes * std  # need over and under here
            outlyingDown = mean - stdDeviationTImes * std
            for s in scores:
                if s[3] > outlyingUP:
                    outliers.append(s + ["up"])
                else:
                    break
            for s in reversed(scores):
                if s[3] < outlyingDown:
                    outliers.append(s + ["down"])
                else:
                    break
    return outliers


def createPairs(outliers, sequenceOfIndexes):
    outliersSortedByTrace = sorted(outliers, key=lambda x: (x[0], x[1]))
    indexInOutliers = 0
    outlyingPairs = []
    while indexInOutliers < len(outliersSortedByTrace):
        outlier = outliersSortedByTrace[indexInOutliers]
        inSeq = sequenceOfIndexes[outlier[0]][outlier[1]]
        try:  # this try is for the outliers
            previous = outliersSortedByTrace[indexInOutliers - 1]  # search in the outliers
            if outlier[1] == 0 or (previous[0] == outlier[0] and previous[1] == outlier[1] + 1):
                pass
            else:  # check to create the previous only in sequence
                previous = sequenceOfIndexes[outlier[0]][outlier[1] - 1]
                outlyingPairs.append(
                    [outlier[0], previous[0], inSeq[0], previous[1], outlier[2], "ok", outlier[4], outlier[1] - 1])
        except:
            pass  # there was no previous at some point

        if indexInOutliers != len(outliers) - 1 and outliersSortedByTrace[indexInOutliers + 1][0] == outlier[0] and \
                outliersSortedByTrace[indexInOutliers + 1][1] == outlier[1] - 1:  # check if the next outlier is the
            # next event in the seq
            nextEvent = outliersSortedByTrace[indexInOutliers + 1]
            inSeq2 = sequenceOfIndexes[nextEvent[0]][nextEvent[1]]  # that means it is the next
            outlyingPairs.append(
                [outlier[0], inSeq[0], inSeq2[0], outlier[2], nextEvent[2], outlier[4], nextEvent[4], outlier[1]])
        else:  # the next activity is not an outlier
            try:
                nextEvent = sequenceOfIndexes[outlier[0]][outlier[1] + 1]  # this may throw exception
                outlyingPairs.append(
                    [outlier[0], inSeq[0], nextEvent[0], outlier[2], nextEvent[1], outlier[4], "ok", outlier[1]])
            except:
                pass  # there is no next event in this trace to check
        indexInOutliers += 1
    return outlyingPairs



def main(logFile,k,stdDeviationTimes=4,threshold=None):
    print("importing log")
    log = xes_factory.apply(logFile)
    # [trace,activity index,time]
    print("preprocess ...")
    dataVectors, seq = dataPreprocess(log)
    print("calculate pairs")
    start = time.time()
    myOutliers = findOutlierEvents(dataVectors, k, stdDeviationTImes=stdDeviationTimes,threshold=threshold)
    pairs = createPairs(myOutliers, seq)
    return pairs,time.time() - start

#print 1d
#import matplotlib.pyplot as plt
#import random
#data=random.choices(dataVectors[8],100)
#data=random.choices(dataVectors[8],k=100)
#df=pd.DataFrame([[i[2],0] for i in data],columns=["times","nulls"])
#df.plot(kind="scatter",x="times",y="nulls")
#plt.savefig("1d.png")
