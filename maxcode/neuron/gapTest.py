from neuron import *
from nrn import *
from itertools import chain
from neuron import h
from numpy import *
from pylab import *
import random
import os
import time

pc = h.ParallelContext()
num_processes = int(pc.nhost())
mpi_rank = 0
#print "On process {} of {}".format(mpi_rank+1, num_processes)

print "Creating test network..."
# The pre-synaptic cell is created on the first node and the post-synaptic cell on the last node
# (NB: which will obviously be the same if there is only one node)
if mpi_rank == 0:
    #print "Creating pre-synaptic cell on process {}".format(mpi_rank)
    # Create the pre-synaptic cell
    pre_cell = h.Section()
    pre_cell.insert('pas')
    # Connect the voltage of the pre-synaptic cell to the gap junction on the post-synaptic cell
    pc.source_var(pre_cell(0.5)._ref_v, 0)   
    # Stimulate the first cell to make it obvious whether gap junction is working
    stim = h.IClamp(pre_cell(0.5))
    stim.delay = 50
    stim.amp = 10
    stim.dur = 100
    # Record Voltage of pre-synaptic cell
    pre_v = h.Vector()
    pre_v.record(pre_cell(0.5)._ref_v)
    print "Done!"

h.load_file("stdrun.hoc")
	
h.init()
	
h.tstop = 100
	
h.run()
