"""
Code for testing stimulus and reactions for a single neural network specified in directory.
Max Henderson
Drexel University
Feb 14, 2013
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

"""
Definitions
"""

def constructGeometry( index, dendrites, connections, numNeurons):
	Soma = h.Section()
	Soma.L = 30
	Soma.diam = 30
	Axon = h.Section()
	Axon.L = 1000
	Axon.diam = 1
	Dendrites = []
	count = 0
	#Create appropriate number of sections for the dendrites
	for i in range(0, numNeurons):
		if int(connections[index][i]) == 1:
			Dendrites.append(h.Section())
			Dendrites[count].L = float(dendrites[index][i])
			Dendrites[count].diam = 2
			count = count + 1
	#Connect all dendrites and axon
	Axon.connect(Soma, 0.5, 0)
	for i in range(0, count):
		Dendrites[i].connect(Soma, 0.5, 0)
	return (Soma, Axon, Dendrites)

def constructConnections( connections, dendrites, numNeurons, Soma, Axon, Dendrites, strength ):
	"""
		This definition will a connectivity matrix and make the appropriate synaptic connections.
	"""
	gaps = []
	for i in range(0, numNeurons):
		count = 0
 		for j in range(0, numNeurons):
			if int(connections[i][j]) == 1:
				gap_junction = h.gapc(1, sec=Dendrites[i][count])
				gap_junction.g = strength
				h.setpointer(Axon[j](1)._ref_v, 'vgap', gap_junction)
				gaps.append(gap_junction)
	return gaps		

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

def makeStimulus( soma, simTime ):
	interval = 50
	stimNc = h.NetStim()
	stimNc.noise = 1		
	stimNc.start = 0		
	stimNc.number = simTime
	stimNc.interval = interval
	syn = h.ExpSyn (0.5, sec = soma)		
	nc = h.NetCon(stimNc, syn)
	nc.weight[0] = 100
	#For recording events...
	tvec = h.Vector() #time
	idvec = h.Vector() #cell number
	nc.record(tvec, idvec)
	return (stimNc, syn, nc, tvec, idvec)

def runSimulation(numSegs, tau, refrac, simTime, numNeurons, path, strength, dendrites, connections):
	"""
		This defintion will analyze a specific random network geometry and random connectivity type.
	"""
	print 'Run simulation!!'
	#Create lists for somas, axons, basal dendrites, and apical dendrites for each neuron in the network.
	Soma = []
	Axon = []
	Dend = []

	#Begin creating neurons individually from the various geometrical files.
	for index in range(0,numNeurons):		
		soma, axon, dend = constructGeometry( index, dendrites, connections, numNeurons )
		Soma.append(soma)
	    	Axon.append(axon)
	    	Dend.append(dend)

	#Set biophysics for the different neural structures. IAF will contain all data pertaining to the refractory period between spikes.
	IAF = []
	counter = 0
	for i in range(0,numNeurons):
		for sec in Dend[i]:
			sec.insert('pas')
			sec.nseg = numSegs	
			counter = counter + 1
	for sec in Soma:
		sec.insert('hh')
		sec.nseg = numSegs
		counter = counter + 1
	for sec in Axon:
		sec.insert('hh')
		sec.nseg = numSegs
		counter = counter + 1

	#Import connectivity between neurons.
	gaps = constructConnections( connections, dendrites, numNeurons, Soma, Axon, Dend, strength )

	#Create vectors for recording potentials, currents, etc in the neural network during the simulation.
	vec = recordData( numNeurons, Soma )

	#Stimulate system with random noise.
	stims = []
	for i in range(0,numNeurons):
		stims.append(makeStimulus(Soma[i],simTime))

	# run the simulation
	h.load_file("stdrun.hoc")
	h.init()
	h.tstop = simTime
	h.run()
	
	#Save spiking data for visual representation.	
	file = open(path + 'spikes' + str(1) + 'strength' + str(strength*2000) + '.txt',"wb")
	print path + 'spikes' + str(1) + 'strength' + str(strength) + '.txt'
	for i in range(0,len(vec ['t '])):
		for j in range(0,numNeurons+1):
			for var in vec:
	    			if (var == str(j+1)):
					file.write(str(vec[var][i])+"\n")
				elif (j == numNeurons) & (var == 't '):
					file.write(str(vec['t '][i])+"\n")
	file.close()
	#See what we can see with stimulation data...
	file = open(path + 'stims' + str(1) + 'strength' + str(strength) + '.txt',"wb")
	print path + 'spikes' + str(1) + 'strength' + str(strength) + '.txt'
	for i in range(0,numNeurons):
		for j in range(0,len(stims[i][3])):
			file.write(str(stims[i][4][j])+"\n")
			file.write(str(stims[i][3][j])+"\n")
	file.close()
	
	#Destroy neuron sections.
	Dend = []
	Axon = []
	Soma = []

"""
Main method
"""

#Time it!
start_time = time.time()
#Set constants...	
numSegs = 3
tau = 1
refrac = 0.5
simTime = 500
numNeurons = 125
conductances = linspace(0.005, 0.01, 11)
op = '/home/hendemd/Desktop/MATLAB/bin/Paper 2/125 crys nn/'
start_time = time.time()
dendrites =[]
fh = open(op + '/Dendrites.txt')	
for line in fh.readlines():
	y = [value for value in line.split()]	    
	dendrites.append( y )		
fh.close()	
for l in range(0, shape(dendrites)[0]):		
	dendrites[l] = dendrites[l][0].split(",")	
connections =[]		
fh = open(op + '/Connections.txt')
for line in fh.readlines():		    
	y = [value for value in line.split()]		    
	connections.append( y )		
fh.close()	
for l in range(0, shape(connections)[0]):			
	connections[l] = connections[l][0].split(",")
for strength in conductances:				
	runSimulation(numSegs, tau, refrac, simTime, numNeurons, op, strength, dendrites, connections)
print time.time() - start_time, "seconds"
