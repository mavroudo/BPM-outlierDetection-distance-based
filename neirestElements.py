#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 08:42:33 2019

@author: mavroudo
"""

from heapq import nsmallest
s = [1,2,3,4,5,6,6,7]
nsmallest(3, s, key=lambda x: abs(x-6.5))