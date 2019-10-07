#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 15:49:48 2019

@author: mavroudo
"""
def edges(listWithSequences,listWithLetters):
    matrix=[[0 for i in range(len(listWithLetters))] for j in range(len(listWithLetters))]
    for sequence in listWithSequences:
        for index, letter in enumerate(sequence.split(",")[:-1]):
            matrix[listWithLetters.index(letter)][listWithLetters.index(sequence[index*2+2])]+=1          
    return matrix

def condactWeightedEdges(listWihSequences,letters):
    matrix= edges(listWihSequences,letters)
    print(len(matrix),len(matrix[1]))
    wedges=[]
    for start,line in enumerate(matrix):
        for end,connections in enumerate(line):
           if connections != 0:
               wedges.append([(letters[start],letters[end]),connections])
    return wedges


#letters=[i for i in"abcdefghijklmnopqrstuvwxyz"]
#testSequence=['a,b,c,d,d,d,d,e,g,f,h,i,j,d,j,j,j,f,q,h,i,j,j,j,j,j,k,l,j,l,l,l,l,l,o,n,m,p,l','a,b,c,d,d,d,d,d,d,d,d,e,g,f,h,i,j,d,j,f,q,h,i,j,j,j,j,j,j,j,j,j,f,q,h,i,j,j,j,j,j,j,j,j,j,j,j,j,j,k,l,j,l,o,n,m,p,l,r']
#print(condactWeightedEdges(edges(testSequence,letters),letters))
    