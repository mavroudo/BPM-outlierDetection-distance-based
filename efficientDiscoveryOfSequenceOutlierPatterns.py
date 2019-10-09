#!/usr/bin/env python3
# -*- coding: utf-8 -*-


S=[i for i in "abcdabcacbeac"]
vocab=['a','b','c','d','e']
minSup=2
seqGap=2

#find search space based on frequent events
def getPrefixSet(S,seqGap):
    #keep only frequent events
    frequentEvents,infrequentEvents=[],[]
    for event in set(S):
        if S.count(event)>=minSup:
            frequentEvents.append(event)
        else:
            infrequentEvents.append(event)
    prefixSet=[]
    for index,freqEvent in enumerate(frequentEvents):
        prefixSet.append([freqEvent,[]])
        for startingPoint in [i for i, x in enumerate(S) if x == freqEvent]:
            pattern=[(freqEvent,startingPoint)] 
            for i in range(startingPoint+1,startingPoint+seqGap+2):                    
                if i>=len(S) :
                    break
                if  S[i] not in infrequentEvents:
                    pattern.append((S[i],i))
            prefixSet[index][1].append(pattern)
    return prefixSet
            
        
def Reduce(seqGap,minSup,cntThr,vocab,S):
    prefixSet=getPrefixSet(S,seqGap)
    globalAvail=[1 for i in S]
    gMax=max([max([len(i) for i in j[1]]) for j in prefixSet]) #optimize the way gmax starts
    currentLen=gMax
    freqPatterns,CO=[],[]
    while currentLen > 0 and len(prefixSet) :
        curFreq=[]
        usedPositionsTotal=dict()
        coCandidates=[]
        for prefSet in prefixSet:
            if max([len(i) for i in prefSet[1]]) >= currentLen:
                freqSeqs,usedPositions,coCand=ConstructCF(prefSet[1],currentLen,minSup,globalAvail,cntThr)
                curFreq.extend(freqSeqs)
                usedPositionsTotal.update(usedPositions)
                coCandidates.extend(coCand)        
        for freq in curFreq:
            for index in usedPositionsTotal[freq]:
                globalAvail[index]=0
        for coCandidate in coCandidates:
            for index in usedPositionsTotal[coCandidate]:
                globalAvail[index]=0
        for prefSet in list(prefixSet):     
            updatePrefix(prefSet,globalAvail)
            if prefSet[1]==[]:
                prefixSet.remove(prefSet)
        for pattern in curFreq:
            freqPatterns.append(pattern)
        #Determine who of coCandidates are co
        invertedIndex=conductInvertedIndex(freqPatterns,vocab)
        CO.extend(coCandidateExamination(coCandidates,invertedIndex,freqPatterns))
        
        currentLen-=1
    return freqPatterns,CO
            
        
                
                
def ConstructCF(prefSet,currentLen,minSup,globalAvail,cntThr): 
    subseqs=dict()
    usedPositions=dict()
    freqSeqs,coCandidates=[],[]
    for seq in prefSet:
        subs=findSubSeqs(seq,currentLen,globalAvail)
        for Op in subs:
            P=",".join([i[0] for i in Op])
            if notUsed(Op,usedPositions.get(P)):
                putInSubSequences(P,subseqs)
                setUsed(Op,usedPositions) 
    for k in subseqs.keys():
        if subseqs[k] >= minSup:
            freqSeqs.append(k)
        if subseqs[k] <=cntThr:
            coCandidates.append(k)
    return freqSeqs,usedPositions,coCandidates
    
    
    
def updatePrefix(prefixSet,globalAvail):
    for seq in list(prefixSet[1]):
        if not seqIsAvaliable(seq,globalAvail):
            prefixSet[1].remove(seq)
    

from itertools import combinations
def findSubSeqs(seq,currentLen,globalAvail):
    if len(seq)<currentLen:
        return []
    elif len(seq)==currentLen :
        return [seq]
    else:
        s=[list(i) for i in list(combinations(seq[1:],currentLen-1))]
        for sequence in s:
            sequence.insert(0,seq[0])
        for sequence in s:
            if not seqIsAvaliable(sequence,globalAvail):
                s.remove(sequence)
        return s
        

def conductInvertedIndex(CF,vocab):
    transform=list(map(lambda x : "".join(x.split(",")),CF))
    matrix=[[0 for i in range(len(transform))] for j in range(len(vocab))]
    for index,cf in enumerate(transform):
        for char in set(cf):
            matrix[vocab.index(char)][index]=1
    response=dict()
    for index,bitMap in enumerate(matrix):
        response[vocab[index]]=bitMap
    return response

def coCandidateExamination(coCandidates,invertedIndex,CF):
    co=[]
    transformCF=list(map(lambda x : "".join(x.split(",")),CF))
    transformCOCandidates=list(map(lambda x : "".join(x.split(",")),coCandidates))
    print(coCandidates)
    for coCandidate in transformCOCandidates:
        bitMaps=[]
        for char in set(coCandidate): #bitMaps that will determine what CFs we will use
            bitMaps.append(invertedIndex[char])
        cfsToCheck=[transformCF[i] for i in bitOperation(bitMaps)]
        if examination(cfsToCheck,coCandidate): co.append(coCandidate)
    return co

from itertools import permutations      
def examination(CFS,coCandidate):
    for cf in CFS:
        if coCandidate in cf: return False
        if coCandidate in list(permutations(cf)):return False
    return True
        
def bitOperation(bitmaps):
    positions=[]
    for j in range(len(bitmaps[0])):
        counter=0
        for i in range(len(bitmaps)):
            counter+=bitmaps[i][j]
        if counter==len(bitmaps):
            positions.append(j)
    return positions


def seqIsAvaliable(seq,globalAvail):
    counter=0
    for (char,index) in seq:
        counter+=globalAvail[index]
    if counter==0:
        return False
    return True

def notUsed(occurance,positions):
    if positions==None:
        return True
    for (char,index) in occurance:
        if index in positions:
            return False
    return True
    
def putInSubSequences(P,subseqs):
    if subseqs.get(P)==None:
        subseqs[P]=1
    else:
        subseqs[P]=subseqs[P]+1
        
def setUsed(Op,usedPositions):
    P=",".join([i[0] for i in Op])
    if usedPositions.get(P) == None:
        usedPositions[P]=set()
    for (char,index) in Op:
        usedPositions[P].add(index)
        
