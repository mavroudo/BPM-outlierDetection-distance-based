#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 20:32:08 2019

@author: mavroudo
"""

from typing import Tuple

class TrieNode(object):
    """
    Our trie node implementation. Very basic. but does the job
    """
    
    def __init__(self, char: str):
        self.char = char
        self.children = []
        self.precentagePerChildren=[]
        self.word_finished = False
        self.counter = 1
        
    def updatePercentages(self):
        for index,child in enumerate(self.children):
            try:
                self.precentagePerChildren[index]=child.counter/self.counter
            except:
                self.precentagePerChildren.append(child.counter/self.counter)
        
def add(root, word: str):
    """
    Adding a word in the trie structure
    """
    node = root
    for char in word:
        found_in_child = False
        for child in node.children:
            if child.char == char:
                child.counter += 1
                node.updatePercentages()
                node = child                
                found_in_child = True
                break
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            node.updatePercentages()
            node = new_node
    node.word_finished = True
    
def find_prefix(root, prefix: str) -> Tuple[bool, int]:
    """
    Check and return 
      1. If the prefix exsists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    node = root
    if not root.children:
        return False, 0
    for char in prefix:
        char_not_found = True
        for child in node.children:
            if child.char == char:
                char_not_found = False
                node = child
                break
        if char_not_found:
            return False, 0
    return True, node.counter

def preOrder(root,path):
    path=path+root.char
    for child in root.children:
        path=preOrder(child,path)
    return path+str(0)

def preOrderRepresentation(root):
    return preOrder(root,"")[:-1]

def findLongestPrefix(W,W1):
    """
        W=prefix representation of TST 
        W1- an activity sequence
    """ 
    untilTheEnd=None
    for i in range(2,len(W1)):
        Wp=W1[len(W1)-i:] #tail of the activity       
        try:
            match=W.index(Wp)
        except:
            match=[]
        if match != []:
            untilTheEnd=[]
            while W[match]!='0':
                untilTheEnd.append(W[match])
                match+=1
        else:
            return W1[len(W1)-i+1:],"".join(untilTheEnd)
        


def removeOutlierEdges(root,threshold):
    head=[i for i in root.children]
    while len(head)>0:
        node=head.pop()
        toRemoved=[]
        for index,child in enumerate(list(node.children)):
            if node.precentagePerChildren[index] <threshold:
                node.children.remove(child)
                node.counter-=child.counter
                toRemoved.append(index)
            else:
                head.append(child)
        for index in toRemoved:
            del node.precentagePerChildren[index]
        node.updatePercentages()



def outliersDiscovery(sequenceList,threshold):
    """
        threshold = float that indicates the lower bound of an edge in the trie
        edges that have lower that that percentage will be removed from trie 
        with the subtree
    """
    root = TrieNode('*')
    for seq in sequenceList:
        add(root,seq)
    removeOutlierEdges(root,threshold)
    outliers=[]
    for index,seq in enumerate(sequenceList):
        if not find_prefix(root,seq)[0]:
            outliers.append([index,seq])
    return outliers
    
seqList=["abcbc","abcbc","adc"]   
outliers=outliersDiscovery(seqList,0.34)
    
root = TrieNode('*')
add(root, "abcbc")
add(root, "adc")

