"""
This program will simulate 3 different geometric networks, 'young', 'old', and random.  These networks will be connected using a distant dependent relationship
and also using a common neighbor law.

Max Henderson
Drexel University
May 30, 2014
"""

"""
Import appropriate packages
"""

from neuron import *
from nrn import *
from itertools import chain
from neuron import h
import random
import os
import time
import sys
#import numpy

"""
Definitions
"""

def constructConnections1( connections, numNeurons, Neurons ):
	"""
		This definition will a connectivity matrix and make the appropriate GAP JUNCTIONS.
	"""
	gaps = []
	for i in range(0, numNeurons):
		count = 0
 		for j in range(0, numNeurons):
			if abs(float(connections[i][j])) > 0:
				gap_junction = h.gapc(1, sec=Neurons[i].soma[0])
				gap_junction.g = 0.000000001*float(connections[i][j])
				h.setpointer(Neurons[j].soma[0](1)._ref_v, 'vgap', gap_junction)
				gaps.append(gap_junction)
	return gaps		

def constructConnections2( connections, numNeurons, Neurons, inhibInd, delay, strength ):
	"""
		This definition will a connectivity matrix and make the appropriate CHEMICAL JUNCTIONS.
	"""
	SYN = []
	NC  = []
	for i in range(0, numNeurons):
		count = 0
 		for j in range(0, numNeurons):
			if abs(float(connections[i][j])) > 0:
				syn = h.ExpSyn (0.5, sec = Neurons[j].soma[0]) #Target
				Neurons[i].soma[0].push()
				nc = h.NetCon( Neurons[i].soma[0](0.5)._ref_v, syn ) #Source
				w = float(connections[i][j])
				mu, sigma = 1, 0.1 # mean and standard deviation
				#s = numpy.random.normal(mu, sigma, 1)
				#s = strength
				s1 = 20
				s2 = 1
				#Determine weight from particular type of connection
				if i < inhibInd: #This means the source is EXCITATORY
					if j < inhibInd:
						#E -> E
						#nc.weight[0] = s*w*0.5
						nc.weight[0] = 0.05*s1
					else:
						#E -> I
						#nc.weight[0] = s*w*0.1
						nc.weight[0] = 0.2*s1
				else:   	 #This means the source is INHIBITORY
					if j < inhibInd:
						#I -> E
						#nc.weight[0] = -s*w*0.1
						nc.weight[0] = -0.05*s2
					else:
						#I -> I
						#nc.weight[0] = -s*w*0.5
						nc.weight[0] = -0.1*s2
				#nc.threshold = 1
				#Determine delay from intersomatic distance
				if float(delay[i][j]) > 155:	# Long range speed
					nc.delay  = float(delay[i][j])/300
				else:				# Short range speed
					nc.delay  = float(delay[i][j])/150
				NC.append(nc)
				SYN.append(syn)
	return (SYN,NC)		

def recordData( numNeurons, Neurons ):
	"""
		This definition will construct a vector to record all the data taken in the simulation.  The potential across each Neurons will be recorded for each time step.
	"""
	vec = {}
	#Record appropriate number of potentials.
	for var in range(0,numNeurons):
    		vec[str(var + 1)] = h.Vector()
    		vec[str(var + 1)].record(Neurons[var].soma[0](0.5)._ref_v)
	#Record time.
	vec['t '] = h.Vector()
	vec ['t '].record(h._ref_t)
	return vec

def makeStimulus( Neurons, simTime, stimInterval ):
	interval = stimInterval
	stimNc = h.NetStim()
	stimNc.noise = 1		
	stimNc.start = 0		
	stimNc.number = simTime/interval
	stimNc.interval = interval
	syn = h.ExpSyn (0.5, sec = Neurons.soma[0])		
	nc = h.NetCon(stimNc, syn)
	nc.weight[0] = 1
	#For recording events...
	tvec = h.Vector() #time
	idvec = h.Vector() #cell number
	nc.record(tvec, idvec)
	return (stimNc, syn, nc, tvec, idvec)

def runSimulation(young_chem1_con1, young_elec1_con1, numNeurons, fileIndex, simTime, inhibInd, age, delay, stimInterval, con, strength):
	"""
		This defintion will run the simulation.
	"""

	print 'Run simulation!!'
	
	# Load file to make model regular spiking excitory cells.
	h.load_file ("sPY_template")
	
	# Load file to make model fast spiking inhibitory cells.
	h.load_file ("sIN_template")

	#Create neurons in the networks.
	numSegs = 3
	Neurons = []
	for i in range(0, numNeurons):
		if i < inhibInd:
			neuron = h.sPY()
			Neurons.append(neuron)
		else:
			neuron = h.sIN()
			Neurons.append(neuron)

	#Import connectivity between neurons.
	#gapsYoung = constructConnections1( young_elec1_con1, numNeurons, Neurons)
	synYoung,ncYoung = constructConnections2( young_chem1_con1, numNeurons, Neurons, inhibInd, delay, strength )

	#Create vectors for recording potentials, currents, etc in the neural network during the simulation.
	vec = recordData( numNeurons, Neurons )

	#Stimulate system with random noise.
	stims = []
	for i in range(0,numNeurons):
		stims.append(makeStimulus(Neurons[i],simTime,int(stimInterval)))

	#Run the simulation.
	h.load_file("stdrun.hoc")
	h.init()
	h.tstop = simTime
	h.run()

	#Write results.
	file = open(path + 'spikes' + str(con) + '_' + str(age) + '_' + str(fileIndex) + '_' + str(stimInterval) + '.txt',"wb")

	print "Writing results to..."
	print file
	for j in range(0,numNeurons):
		canFire = 1
		var = str(j+1)
		for i in range(0,len(vec ['t '])):
			if (vec[var][i] > 0) & (canFire == 1):
				file.write(str(j+1)+"\n")
				file.write(str(vec['t '][i])+"\n")
				canFire = 0
			if (vec[var][i] < 0):
				canFire = 1
	file.close()
	
"""
Main method
"""

#Time it and set simulation parameters.
start_time = time.time()
simTime = 1000
path = '/data2/L/Brain/mroyster/thinning/sims/dry_run_0/aut/'

fileIndex = '10'#sys.argv[2]

stimInterval = '30'#sys.argv[4]

strength = 1;
#strength = sys.argv[6]
#strength = float(strength)

#Load the various network information, electrical, and chemical synaptic connectivities.
data =[]
fh = open(path + 'networkConstants' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	data.append( y )
fh.close()
for l in range(0, 2):				
	data[l] = data[l][0].split(",")
numNeurons = int(data[0][0])
inhibInd = int(data[1][0])
print numNeurons
print inhibInd

#Load young data....
Dyoung = []
fh = open(path + 'youngDist_' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	Dyoung.append( y )
fh.close()
for l in range(0, numNeurons):				
	Dyoung[l] = Dyoung[l][0].split(",")

C1_1 = []
fh = open(path + 'young_chem_con1_' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	C1_1.append( y )
fh.close()
for l in range(0, numNeurons):				
	C1_1[l] = C1_1[l][0].split(",")
'''
C2_1 = []
fh = open(path + 'C2_1_' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	C2_1.append( y )
fh.close()
for l in range(0, numNeurons):				
	C2_1[l] = C2_1[l][0].split(",")

E_1 = []
fh = open(path + 'E_1_' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	E_1.append( y )
fh.close()
for l in range(0, numNeurons):				
	E_1[l] = E_1[l][0].split(",")
'''
E_1 = []
#Load random data....
'''
Drand = []
fh = open(path + 'Drand' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	Drand.append( y )
fh.close()
for l in range(0, numNeurons):				
	Drand[l] = Drand[l][0].split(",")

C1_3 = []
fh = open(path + 'C1_3_' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	C1_3.append( y )
fh.close()
for l in range(0, numNeurons):				
	C1_3[l] = C1_3[l][0].split(",")

C2_3 = []
fh = open(path + 'C2_3_' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	C2_3.append( y )
fh.close()
for l in range(0, numNeurons):				
	C2_3[l] = C2_3[l][0].split(",")

E_3 = []
fh = open(path + 'E_3_' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	E_3.append( y )
fh.close()
for l in range(0, numNeurons):				
	E_3[l] = E_3[l][0].split(",")
'''
#Run young simulations.
runSimulation(C1_1, E_1, numNeurons, fileIndex, simTime, inhibInd, 1, Dyoung, stimInterval, 1, strength)
#runSimulation(C2_1, E_1, numNeurons, fileIndex, simTime, inhibInd, 1, Dyoung, stimInterval, 2, strength)

#Run random simulations.
#runSimulation(C1_3, E_3, numNeurons, fileIndex, simTime, inhibInd, 3, Drand,  stimInterval, 1, strength)
#runSimulation(C2_3, E_3, numNeurons, fileIndex, simTime, inhibInd, 3, Drand,  stimInterval, 2, strength)

print time.time() - start_time, "seconds"
