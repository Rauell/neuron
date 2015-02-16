from neuron import *
from nrn import *
from itertools import chain
from neuron import h
from numpy import *
from pylab import *
import random
import os
import time

def recordData( numNeurons, Soma ):
	"""
		This definition will construct a vector to record all the data taken in the simulation.  The potential across each soma will be recorded for each time step.
	"""
	vec = {}
	#Record appropriate number of potentials.
	for var in range(0,numNeurons):
    		vec[str(var + 1)] = h.Vector()
    		vec[str(var + 1)].record(Soma[var](0.5)._ref_v)
	#Record time.
	vec['t '] = h.Vector()
	vec ['t '].record(h._ref_t)
	return vec

# Make integrate and fire cells.
N = 5000
Neurons = []
for i in range(0, N):
	Neurons.append(h.Section())


# Record data.
vec = recordData( N, Neurons )

# Run Simulation.
start_time = time.time()
h.load_file("stdrun.hoc")
h.init()
h.tstop = 100
h.run()
print time.time() - start_time, "seconds"
