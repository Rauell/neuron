from neuron import *
from nrn import *
from itertools import chain
from neuron import h
from numpy import *
from pylab import *
import random
import os

def addVectorVariable( recordVec ):
	return 1

##############################################################################################

"""
Main
"""

Soma = []
Soma.append(h.Section())
Soma.append(h.Section())
numNeurons = 2

#Call method and make vec

vec = {}
for var in range(0,numNeurons):
    print str(var)
    vec[str(var)] = h.Vector()
    vec[str(var)].record(Soma[var](0.5)._ref_v)

print vec

