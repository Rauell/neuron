from neuron import *
from nrn import *
from itertools import chain
from neuron import h
import random
import os
import time
import sys
from numpy import *
from pylab import *

numNeurons = 2
numSegs = 3
Neurons = []
for i in range(0, numNeurons):
	Neurons.append(h.Section())

#Set biophysics for the different neural structures. IAF will contain all data pertaining to the refractory period between spikes.
for sec in Neurons:
	sec.insert('hh')
	sec.nseg = numSegs

syn = h.ExpSyn (0.5, sec = Neurons[1])
Neurons[0].push()
nc = h.NetCon( Neurons[0](0.5)._ref_v, syn )

nc.delay = 10
nc.weight[0] = 1
nc.threshold = 10

interval = 1
stimNc = h.NetStim()
stimNc.noise = 0		
stimNc.start = 10		
stimNc.number = 1
stimNc.interval = interval
syn1 = h.ExpSyn (0.5, sec = Neurons[1])		
nc1 = h.NetCon(stimNc, syn1)
nc.weight[0] = 100

# record 
vec = {}
for var in 'v_1 ', 'v_2 ', 't ':
    vec[var] = h.Vector()
vec['v_1 '].record(Neurons[0](0.5)._ref_v)
vec['v_2 '].record(Neurons[1](0.5)._ref_v)
vec ['t '].record(h._ref_t)

# run the simulation
h.load_file("stdrun.hoc")
h.init()
h.tstop = 50
h.run()

# plot the results
figure()
plot(vec['t '],vec['v_1 '], vec['t '], vec['v_2 '])
show()
h.topology()
