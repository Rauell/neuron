"""
This program will simulate two different brains, one 'young' and one 'old'.  We age the neural networks by assuming that neurons 'age' by moving from some original position.  Depending on how far the neurons move from their original positions, the neurons will either break or weaken the respective chemical and electrical synapses connecting other neurons.  These results are then exported to files in another directory.

Max Henderson
Drexel University
Jan 1, 2014
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
import time
import sys

"""
Definitions
"""

def constructConnections1( connections, numNeurons, Neurons ):
	"""
		This definition will a connectivity matrix and make the appropriate synaptic connections.
	"""
	gaps = []
	for i in range(0, numNeurons):
		count = 0
 		for j in range(0, numNeurons):
			if connections[i][j] == 1:
				gap_junction = h.gapc(1, sec=Neurons[i])
				gap_junction.g = 0.5
				h.setpointer(Neurons[j](1)._ref_v, 'vgap', gap_junction)
				gaps.append(gap_junction)
	return gaps		

def constructConnections2( connections, numNeurons, Neurons ):
	"""
		This definition will a connectivity matrix and make the appropriate synaptic connections.
	"""
	SYN = []
	NC  = []
	for i in range(0, numNeurons):
		count = 0
 		for j in range(0, numNeurons):
			if connections[i][j] == 1:
				syn = h.ExpSyn (0.5, sec = Neurons[j])
				Neurons[i].push()
				nc = h.NetCon( Neurons[i](0.5)._ref_v, syn )
				nc.weight[0] = 1
				SYN.append(syn)
				NC.append(nc)
	return (SYN,NC)		

def recordData( numNeurons, Neurons ):
	"""
		This definition will construct a vector to record all the data taken in the simulation.  The potential across each Neurons will be recorded for each time step.
	"""
	vec = {}
	#Record appropriate number of potentials.
	for var in range(0,numNeurons):
    		vec[str(var + 1)] = h.Vector()
    		vec[str(var + 1)].record(Neurons[var](0.5)._ref_v)
	#Record time.
	vec['t '] = h.Vector()
	vec ['t '].record(h._ref_t)
	return vec

def makeStimulus( Neurons, simTime ):
	interval = 1
	stimNc = h.NetStim()
	stimNc.noise = 1		
	stimNc.start = 0		
	stimNc.number = simTime
	stimNc.interval = interval
	syn = h.ExpSyn (0.5, sec = Neurons)		
	nc = h.NetCon(stimNc, syn)
	nc.weight[0] = 1
	#For recording events...
	tvec = h.Vector() #time
	idvec = h.Vector() #cell number
	nc.record(tvec, idvec)
	return (stimNc, syn, nc, tvec, idvec)

def runSimulation(young_chem1_con1, young_elec1_con1, numNeurons, young, fileIndex):
	"""
		This defintion will run the simulation.
	"""

	print 'Run simulation!!'
	#Create neurons in the networks.
	numSegs = 3
	Neurons = []
	for i in range(0, numNeurons):
		Neurons.append(h.Section())

	#Set biophysics for the different neural structures. IAF will contain all data pertaining to the refractory period between spikes.
	for sec in Neurons:
		sec.insert('hh')
		sec.nseg = numSegs

	#Import connectivity between neurons.
	gapsYoung = constructConnections1( young_elec1_con1, numNeurons, Neurons)
	synYoung,ncYoung = constructConnections2( young_chem1_con1, numNeurons, Neurons )

	#Create vectors for recording potentials, currents, etc in the neural network during the simulation.
	vec = recordData( numNeurons, Neurons )

	#Stimulate system with random noise.
	stims = []
	for i in range(0,numNeurons):
		stims.append(makeStimulus(Neurons[i],simTime))

	#Run the simulation.
	h.load_file("stdrun.hoc")
	h.init()
	h.tstop = simTime
	h.run()

	#Simplify the files and write out the data of neural ID and spike times.
	canFire = []
	for i in range(0, numNeurons):
		canFire.append(1)
	if young == 1:
		file = open(path + 'spikesYoung' + fileIndex + '.txt',"wb")
	else:
		file = open(path + 'spikesOld' + fileIndex + '.txt',"wb")
	print "Writing results..."
	for i in range(0,len(vec ['t '])):
		for j in range(0,numNeurons+1):
			for var in vec:
	    			if (var == str(j+1)):
					if (vec[var][i] > 0) & (canFire[j] == 1):
						file.write(str(j+1)+"\n")
						file.write(str(vec['t '][i])+"\n")
						canFire[j] = 0
					if (vec[var][i] < 0):
						canFire[j] = 1
	file.close()
	
	#Destroy neuron sections.
	Neurons = []

"""
Main method
"""

#Time it and set simulation parameters.
start_time = time.time()
simTime = 1000
path = '/data2/L/Brain/max/testingWritingColumns_v1/'
fileIndex = sys.argv[1]

#Load the various electrical and chemical synaptic connectivities.
data =[]
fh = open(path + 'data' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	data.append( y )
fh.close()
for l in range(0, shape(data)[0]):				
	data[l] = data[l][0].split(",")
#numNeurons = len(data)
numNeurons = 100

young_chem1_con1 =[]
fh = open(path + 'young_chem1_con' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	young_chem1_con1.append( y )
fh.close()
for l in range(0, shape(young_chem1_con1)[0]):				
	young_chem1_con1[l] = young_chem1_con1[l][0].split(",")

young_elec1_con1 =[]
fh = open(path + 'young_elec1_con' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	young_elec1_con1.append( y )
fh.close()
for l in range(0, shape(young_elec1_con1)[0]):				
	young_elec1_con1[l] = young_elec1_con1[l][0].split(",")

old_chem1_con1 =[]
fh = open(path + 'old_chem1_con' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	old_chem1_con1.append( y )
fh.close()
for l in range(0, shape(old_chem1_con1)[0]):				
	old_chem1_con1[l] = old_chem1_con1[l][0].split(",")

old_elec1_con1 =[]
fh = open(path + 'old_elec1_con' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	old_elec1_con1.append( y )
fh.close()
for l in range(0, shape(old_elec1_con1)[0]):				
	old_elec1_con1[l] = old_elec1_con1[l][0].split(",")

#Run simulation and export results.
young = 1
runSimulation(young_chem1_con1, young_elec1_con1, numNeurons, young, fileIndex)
young = 0
runSimulation(old_chem1_con1,   old_elec1_con1,   numNeurons, young, fileIndex)

print time.time() - start_time, "seconds"
