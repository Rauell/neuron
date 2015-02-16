"""
Code for generating an arbitrary neural network with basic neuronal features
Max Henderson
Drexel University
Novemeber 2, 2012
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

"""
Definitions
"""

def constructGeometry( index, dendrites, connections, numNeurons):
	Soma = h.Section()
	Soma.L = 25
	Axon = h.Section()
	Axon.L = 1000
	Dendrites = []
	count = 0
	#Create appropriate number of sections for the dendrites
	for i in range(0, numNeurons):
		if int(connections[index][i]) == 1:
			Dendrites.append(h.Section())
			Dendrites[count].L = float(dendrites[index][i])
			count = count + 1
	#Connect all dendrites and axon
	Axon.connect(Soma, 0.5, 0)
	for i in range(0, count):
		Dendrites[i].connect(Soma, 0.5, 0)
	return (Soma, Axon, Dendrites)

def constructConnections( connections, dendrites, numNeurons, Soma, Axon, Dendrites ):
	"""
		This definition will a connectivity matrix and make the appropriate synaptic connections.
	"""
	SYN = []
	NC  = []
	for i in range(0, numNeurons):
		count = 0
 		for j in range(0, numNeurons):
			if int(connections[i][j]) == 1:
				syn = h.ExpSyn (0.5, sec = Axon[j])
				Dendrites[i][count].push()
				nc = h.NetCon( Dendrites[i][count](0.5)._ref_v, syn )
				nc.weight[0] = 5
				SYN.append(syn)
				NC.append(nc)
				count = count + 1
	return (SYN,NC)			

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

"""
Main method
"""

#Set constants...

numSegs = 10
tau = 1
refrac = 0.5
simTime = 500
numNeurons = 144
path = '/home/hendemd/Desktop/MATLAB/bin/Neural research/Probabilistic neighbors/'
listing = os.listdir(path)

#Read in network topology information.
connections =[]
fh = open(path + 'Connections.txt')
for line in fh.readlines():
    y = [value for value in line.split()]
    connections.append( y )
fh.close()
for i in range(0, shape(connections)[0]):
	connections[i] = connections[i][0].split(",")
dendrites =[]
fh = open(path + 'Dendrites.txt')
for line in fh.readlines():
    y = [value for value in line.split()]
    dendrites.append( y )
fh.close()
for i in range(0, shape(dendrites)[0]):
	dendrites[i] = dendrites[i][0].split(",")
pos =[]
fh = open(path + 'Positions.txt')
syn = []
for line in fh.readlines():
    y = [value for value in line.split()]
    pos.append( y )
fh.close()
for i in range(0, shape(pos)[0]):
	pos[i] = pos[i][0].split(",")

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
		IAF.append(h.IntFire1 (0.5))
		IAF[counter].tau = tau
		IAF[counter].refrac = refrac
		counter = counter + 1
		for seg in sec:
			seg.pas.g = 0.0002             
     			seg.pas.e = -65
for sec in Soma:
	sec.insert('hh')
	sec.nseg = numSegs
	IAF.append(h.IntFire1 (0.5))
	IAF[counter].tau = tau
	IAF[counter].refrac = refrac
  	for seg in sec:
		seg.hh.gnabar = 0.25
		seg.hh.gl = .0001666
  		seg.hh.el = -60.0
	counter = counter + 1
for sec in Axon:
	sec.insert('hh')
	sec.nseg = numSegs
	IAF.append(h.IntFire1 (0.5))
	IAF[counter].tau = tau
	IAF[counter].refrac = refrac
	for seg in sec:
		seg.hh.gnabar = 0.25
		seg.hh.gl = .0001666
  		seg.hh.el = -60.0
	counter = counter + 1

#Import connectivity between neurons.
synapses, networkConnections = constructConnections( connections, dendrites, numNeurons, Soma, Axon, Dend )

#Create vectors for recording potentials, currents, etc in the neural network during the simulation.
vec = recordData( numNeurons, Soma )

#Stimulate system
stim = []
for i in range(0,numNeurons):
	stim.append(h.IClamp(Soma[i](0.5) ))	
	stim[i].delay = 5	
	stim[i].dur = 100		
	stim[i].amp = 10

# run the simulation
h.load_file("stdrun.hoc")
h.init()
h.tstop = simTime
h.run()

#Save spiking data for visual representation.	
file = open(path + 'spikes.txt',"wb")
for i in range(0,len(vec ['t '])):
	for j in range(0,numNeurons+1):
		for var in vec:
    			if (var == str(j+1)):
				file.write(str(vec[var][i])+"\n")
			elif (j == numNeurons) & (var == 't '):
				file.write(str(vec['t '][i])+"\n")
file.close()

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






