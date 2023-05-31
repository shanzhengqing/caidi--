# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 22:48:48 2023

@author: shanz
"""

a = {1,2,3,4,5}
a.add(1)

import numpy as np

a = np.array([1,2,3,4])
print(a[[False,True,False, False]])

a = {x : x*x for x in range(1,100)}

table = np.array([
    [1,3],
    [2,4]])

print(table.max(axis=1))