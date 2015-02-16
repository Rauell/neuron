from neuron import *
from nrn import *
from itertools import chain
from neuron import h
from numpy import *
from pylab import *
import os

def makeStimulus( neuron ):
	print neuron
	VecAxon = h.Vector()
	VecAxon.record(neuron(0.5)._ref_v)
	stim = h.IClamp(neuron(0))
	stim.dur = 50
	vecCurrent = h.Vector()
	vecCurrent.record(stim._ref_i)
	time = h.Vector()
	time.record(h._ref_t)
	listOfSines = []
	listOfTimes = []
	for i in range(0,stim.dur):
		if random() > 0.75:
			listOfSines.append(10)
		else:
			listOfSines.append(0)
		listOfTimes.append(i)
	VecT = h.Vector(listOfTimes)
	VecStim = h.Vector(listOfSines)
	VecStim.play(stim._ref_amp, VecT, 1)
	return (VecStim, VecT, stim)

def recordData( numNeurons, neurons ):
	"""
		This definition will construct a vector to record all the data taken in the simulation.  The potential across each soma will be recorded for each time step.
	"""
	vec = {}
	#Record appropriate number of potentials.
	for var in range(0,numNeurons):
    		vec[str(var + 1)] = h.Vector()
    		vec[str(var + 1)].record(neurons[var](0.5)._ref_v)
	#Record time.
	vec['t '] = h.Vector()
	vec ['t '].record(h._ref_t)
	return vec

neurons = [] #This will contain my generate neurons
stims = [] #This will contain the connections between neurons
numNeurons = 4
for i in range(0, numNeurons):
    	neurons.append(Section())
	stims.append(makeStimulus(neurons[i]))

print stims
vec = recordData( numNeurons, neurons )
h.finitialize(-68)
run(50)

#Plot the results
figure()
hold(True)
for i in range(0,numNeurons):
	plot(vec['t '],vec[str(i+1)])
hoc.execute('load_file("mview.hoc")')
hoc.execute("mview()")
plt.xlabel('Time (ms)')
plt.ylabel('V (mV)')
show()
h.topology()
