"""
Code for testing how neurons respond in NEURON to synaptic connections of different distances
Max Henderson
Drexel University
Novemeber 15, 2012
"""

"""
Import appropriate packages
"""

from neuron import *
from nrn import *
from itertools import chain
from neuron import h
from numpy import *
from pylab import *
import random
import os

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

# Construct initial sections of neurons 1-4.
Soma1 = h.Section()
Soma2 = h.Section()
Soma3 = h.Section()
Soma4 = h.Section()
AD1 = h.Section()
AD2 = h.Section()
AD3 = h.Section()
AD4 = h.Section()
BD1 = h.Section()
BD2 = h.Section()
BD3 = h.Section()
BD4 = h.Section()
Axon1 = h.Section()
Axon2 = h.Section()
Axon3 = h.Section()
Axon4 = h.Section()

# Give these sections 3D point respresentations. The structrures will be identical, except 1-2 are closer than 3-4.
h.pt3dadd(0,0,0,20,sec=Soma1)
h.pt3dadd(0,0,20,20,sec=Soma1)
h.pt3dadd(0,1,0,3,sec=AD1)
h.pt3dadd(0,700,0,3,sec=AD1)
h.pt3dadd(0,-1,0,3,sec=BD1)
h.pt3dadd(0,-700,0,3,sec=BD1)
h.pt3dadd(0,0,1,10,sec=Axon1)
h.pt3dadd(0,0,1000,10,sec=Axon1)

h.pt3dadd(100,0,0,20,sec=Soma2)
h.pt3dadd(100,0,20,20,sec=Soma2)
h.pt3dadd(100,1,0,3,sec=AD2)
h.pt3dadd(100,700,0,3,sec=AD2)
h.pt3dadd(100,-1,0,3,sec=BD2)
h.pt3dadd(100,-700,0,3,sec=BD2)
h.pt3dadd(100,0,1,10,sec=Axon2)
h.pt3dadd(100,0,1000,10,sec=Axon2)

h.pt3dadd(200,0,0,20,sec=Soma3)
h.pt3dadd(200,0,20,20,sec=Soma3)
h.pt3dadd(200,1,0,3,sec=AD3)
h.pt3dadd(200,700,0,3,sec=AD3)
h.pt3dadd(200,-1,0,3,sec=BD3)
h.pt3dadd(200,-700,0,3,sec=BD3)
h.pt3dadd(200,0,1,10,sec=Axon3)
h.pt3dadd(200,0,1000,10,sec=Axon3)

h.pt3dadd(500,0,0,20,sec=Soma4)
h.pt3dadd(500,0,20,20,sec=Soma4)
h.pt3dadd(500,1,0,3,sec=AD4)
h.pt3dadd(500,700,0,3,sec=AD4)
h.pt3dadd(500,-1,0,3,sec=BD4)
h.pt3dadd(500,-700,0,3,sec=BD4)
h.pt3dadd(500,0,1,10,sec=Axon4)
h.pt3dadd(500,0,1000,10,sec=Axon4)

# Connect neurons and create stimulus.
Axon1.connect(Soma1, 0.5, 0)
AD1.connect(Soma1, 0.5, 0)
BD1.connect(Soma1, 0.5, 0)
Axon2.connect(Soma2, 0.5, 0)
AD2.connect(Soma2, 0.5, 0)
BD2.connect(Soma2, 0.5, 0)
Axon3.connect(Soma3, 0.5, 0)
AD3.connect(Soma3, 0.5, 0)
BD3.connect(Soma3, 0.5, 0)
Axon4.connect(Soma4, 0.5, 0)
AD4.connect(Soma4, 0.5, 0)
BD4.connect(Soma4, 0.5, 0)
"""
stim12 = h.IClamp(Soma1(0.5) )
stim12.delay = 5
stim12.dur = 1
stim12.amp = 1
stim34 = h.IClamp(Soma3(0.5) )
stim34.delay = 10
stim34.dur = 1
stim34.amp = 1
"""
stimNc = [] 
Stim = []
stimNc.append(h.NetStim(0.5))
stimNc[0].interval = 1
stimNc[0].noise = 1
stimNc[0].start = 1
stimNc[0].number = 100
Soma1.push()
Stim = h.NetCon(Soma1(0.5)._ref_v, stimNc[0])
vect = {}
vect['stim'] = h.Vector()
vect['stim'] = h.record(Stim._ref_v)
# create a synapse in the pre - synaptic section
syn12 = h.ExpSyn (0.5, sec = Soma2)
# connect the pre - synaptic section to the
# synapse object
Soma1.push()
nc12 = h.NetCon( Soma1(0.5)._ref_v, syn12 )
nc12.weight[0] = 1
syn34 = h.ExpSyn (0.5, sec = Soma4)
# connect the pre - synaptic section to the
# synapse object
Soma3.push()
nc34 = h.NetCon( Soma3(0.5)._ref_v, syn34 )
nc34.weight[0] = -1
nc34.delay = 10

# Test to see if the neurons farther apart spatially react differently to identical inputs and plot.
Soma = []
Soma.append(Soma1)
Soma.append(Soma2)
Soma.append(Soma3)
Soma.append(Soma4)
vec = recordData( 4, Soma )
h.load_file("stdrun.hoc")
h.init()
h.tstop = 25
h.run()
figure()
hold(True)
plot(vec['t '],vec['1'])
plot(vec['t '],vec['2'])
plot(vec['t '],vec['3'])
plot(vec['t '],vec['4'])
hoc.execute('load_file("mview.hoc")')
hoc.execute("mview()")
plt.xlabel('Time (ms)')
plt.ylabel('V (mV)')
show()
h.topology()














