#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def edges(listWithSequences, letters):
    '''
    Given a list of sequences and the list of chars used for representation it will create a matrix n*n, where n is
    the number of letters used. matrix[i,j] will represent how many times in the sequences there was an edge from ith
    letter to jth letter
    :param listWithSequences: total sequences we want to analyze
    :param letters: a vocabulary with all the available chars that represent an activity
    :return: a matrix n*n as described above
    '''
    matrix = [[0 for i in range(len(letters))] for j in range(len(letters))]
    for sequence in listWithSequences:
        for index, letter in enumerate(sequence.split(",")[:-1]):
            matrix[letters.index(letter)][letters.index(sequence[index * 2 + 2])] += 1
    return matrix


def condactWeightedEdges(listWihSequences, letters):
    '''
    This function will remove all the edges that are 0 in the matrix and transform the rest in a edges list with format
    (startingActivity,EndingActivity]),numberOfTimesOccurred
    :param listWihSequences: List with sequences
    :param letters: Vocabulary of the avaliable letters
    :return: a list with the edges that appeared at lease 1 time
    '''
    matrix = edges(listWihSequences, letters)
    wedges = []
    for start, line in enumerate(matrix):
        for end, connections in enumerate(line):
            if connections != 0:
                wedges.append([(letters[start], letters[end]), connections])
    return wedges


def outliers(weightedEdges, minPercentOfApperences, listWithSequences):
    '''
    It will return the outliers based on the sequence of activities. Based on a given minimum percentage of appearances
    it will find the edges that are under this threshold and then report all the sequences that contains this edge
    :param weightedEdges: the edges computed from the listSequence 
    :param minPercentOfApperences: percent of total sequence that the edge should be appear in order not to consider as an
    outlier
    :param listWithSequences: list with all the sequences
    :return: The list with outlier sequences + the index that appeared in the log file and the outlier edges
    '''
    minBound = int(len(listWithSequences) * minPercentOfApperences / 100)
    outlierEdges = []
    for edge in weightedEdges:
        if edge[1] < minBound:
            outlierEdges.append(edge)
    outlierSequences = []
    for index, sequence in enumerate(listWithSequences):
        for edge in outlierEdges:
            if ",".join(edge[0]) in sequence:
                outlierSequences.append([index, sequence])
                break
    return outlierSequences, outlierEdges
