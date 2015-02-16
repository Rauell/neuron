from neuron import *
from nrn import *
from itertools import chain
from neuron import h
import random
import os
import time
import sys
import numpy
from pylab import *

# Try to make the excitory cell.
h.load_file ("sPY_template")
exc = h.sPY()

# Try to make the excitory cell.
h.load_file ("sIN_template")
inh = h.sIN()

# Stimulate the exc cell.
stimNc = h.NetStim()	
stimNc.noise = 1		
stimNc.start = 150		
stimNc.number = 1
stimNc.interval = 1
syn = h.ExpSyn (0.5, sec = exc.soma[0])		
nc = h.NetCon(stimNc, syn)
nc.weight[0] = 5
nc.record()

"""
# Stimulate the exc cell.
stimNcI = h.NetStim()	
stimNcI.noise = 1		
stimNcI.start = 50		
stimNcI.number = 1
stimNcI.interval = 1
synI = h.ExpSyn (0.5, sec = inh.soma[0])		
ncI = h.NetCon(stimNcI, synI)
ncI.weight[0] = 1
ncI.record()
"""

"""
# Test NC1
syn1 = h.ExpSyn (0.5, sec = exc.soma[0])
inh.soma[0].push()
nc1 = h.NetCon( inh.soma[0](0.5)._ref_v, syn1 )
nc1.delay = 25
nc1.weight[0] = 0.1
nc1.threshold = 5
"""

# Test NC2 -> EXC TO INH
syn2 = h.ExpSyn (0.5, sec = inh.soma[0]) #Target
exc.soma[0].push()
nc2 = h.NetCon( exc.soma[0](0.5)._ref_v, syn2 ) #Source
nc2.delay = 1
nc2.weight[0] = 1
nc2.threshold = 5


# record 
vec = {}
for var in 'v_1 ', 'v_2 ', 't ':
    vec[var] = h.Vector()
vec['v_1 '].record(exc.soma[0](0.5)._ref_v)
vec['v_2 '].record(inh.soma[0](0.5)._ref_v)
vec ['t '].record(h._ref_t)

# run the simulation
h.load_file("stdrun.hoc")
h.init()
h.tstop = 300.0
h.run()

# plot the results
figure()
plot(vec['t '],vec['v_1 '], vec['t '], vec['v_2 '])
show()
print "It works!"
