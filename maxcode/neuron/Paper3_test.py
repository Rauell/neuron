from neuron import *
from nrn import *
from itertools import chain
from neuron import h
from numpy import *
from pylab import *
import random
import os
import time

# Make integrate and fire cells.
IAF1 = h.IntFire2(0.5)
IAF2 = h.IntFire2(1)

# Record data.
#spikes = []
#vec1 = h.Vector()
#vec1.record(nc1)

# Run Simulation.
h.load_file("stdrun.hoc")
h.init()
h.tstop = 100
h.run()

print IAF1
print IAF1.taum
print IAF1.taus
print IAF1.ib
print IAF1.m
print IAF1.M
print IAF1.i
print IAF1.I

# plot the results
figure()
#plot(time, Vec1, time, Vec2)
