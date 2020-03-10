#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 10:22:47 2020

@author: mavroudo
"""
from pm4py.objects.log.importer.xes import factory as xes_factory
from bisect import bisect
from heapq import nsmallest
import time
from statistics import stdev
from statistics import mean

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


def scoreKR(dataList,k,r):
    outliers=[]
    sortedTimes = sorted([i[2] for i in dataList])
    for index,event in enumerate(dataList):
        neighbors=k_nearest(k+1,event[2],sortedTimes)
        if neighbors[k]>r:
            outliers.append(event)
    return outliers

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

def findOutlierEventsWithKR(dataVectors,k,r):
    pass

def createPairs(outliers, sequenceOfIndexes,positionOfTime):
    """
        After finding the outliers, we will use the original sequence of events in 
        every trace in order to create the pairs. The pairs will be also 
        take the value of over if the are outliers at the top edge of the distribution,
        under if they are at the down edge and ok if they are somewhere in the middle.
    """
    outliersSortedByTrace = sorted(outliers, key=lambda x: (x[0], x[1]))
    indexInOutliers = 0
    outlyingPairs = []
    while indexInOutliers < len(outliersSortedByTrace):
        outlier = outliersSortedByTrace[indexInOutliers]
        inSeq = sequenceOfIndexes[outlier[0]][outlier[1]]
        # checking for previous
        previous=outliersSortedByTrace[indexInOutliers-1]
        if indexInOutliers == 0 or (outlier[1] == 0 or (previous[0] == outlier[0] and previous[1] == outlier[1] + 1)):
            pass
        else:  # check to create the previous only in sequence
            previous = sequenceOfIndexes[outlier[0]][outlier[1] - 1]
            outlyingPairs.append(
                [outlier[0], previous[0], inSeq[0], previous[1], outlier[2], "ok", outlier[positionOfTime], outlier[1] - 1])

        if indexInOutliers != len(outliers) - 1 and outliersSortedByTrace[indexInOutliers + 1][0] == outlier[0] and \
                outliersSortedByTrace[indexInOutliers + 1][1] == outlier[1] - 1:  # check if the next outlier is the
            # next event in the seq
            nextEvent = outliersSortedByTrace[indexInOutliers + 1]
            inSeq2 = sequenceOfIndexes[nextEvent[0]][nextEvent[1]]  # that means it is the next
            outlyingPairs.append(
                [outlier[0], inSeq[0], inSeq2[0], outlier[2], nextEvent[2], outlier[positionOfTime], nextEvent[positionOfTime], outlier[1]])
        else:  # the next activity is not an outlier
            try:
                nextEvent = sequenceOfIndexes[outlier[0]][outlier[1] + 1]  # this may throw exception
                outlyingPairs.append(
                    [outlier[0], inSeq[0], nextEvent[0], outlier[2], nextEvent[1], outlier[positionOfTime], "ok", outlier[1]])
            except:
                pass  # there is no next event in this trace to check
        indexInOutliers += 1
    return outlyingPairs


def main(dataVectors,seq, k, stdDeviationTimes=4, threshold=None):
    print("Finding outliers")
    start = time.time()
    myOutliers = findOutlierEvents(dataVectors, k, stdDeviationTImes=stdDeviationTimes, threshold=threshold)
    executionTime=time.time() - start
    print("calculate pairs")
    pairs = createPairs(myOutliers, seq,positionOfTime=4)
    return pairs, executionTime

def usingKR(dataVectors,seq,k,r):
    pass

