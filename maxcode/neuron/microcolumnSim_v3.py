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
import random
import os
import time
import sys
import numpy

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
				gap_junction.g = float(connections[i][j])/100
				h.setpointer(Neurons[j].soma[0](1)._ref_v, 'vgap', gap_junction)
				gaps.append(gap_junction)
	return gaps		

def constructConnections2( connections, numNeurons, Neurons, inhibInd, delay ):
	"""
		This definition will a connectivity matrix and make the appropriate CHEMICAL JUNCTIONS.
	"""
	SYN = []
	NC  = []
	for i in range(0, numNeurons):
		count = 0
 		for j in range(0, numNeurons):
			if abs(float(connections[i][j])) > 0:
				syn = h.ExpSyn (0.5, sec = Neurons[j].soma[0])
				Neurons[i].soma[0].push()
				nc = h.NetCon( Neurons[i].soma[0](0.5)._ref_v, syn )
				w = float(connections[i][j])
				mu, sigma = 1, 0.1 # mean and standard deviation
				s = numpy.random.normal(mu, sigma, 1)
				#Determine weight from particular type of connection
				if i < inhibInd:
					if j < inhibInd:
						#E -> E
						nc.weight[0] = s*w*0.005
					else:
						#I -> E
						nc.weight[0] = -s*w*0.005
				else:
					if j < inhibInd:
						#E -> I
						nc.weight[0] = s*w*0.02
					else:
						#I -> I
						nc.weight[0] = -s*w*0.01
				#Determine delay from intersomatic distance
				if float(delay[i][j]) > 155:
					nc.delay  = float(delay[i][j])/300
				else:
					nc.delay  = float(delay[i][j])/150
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
    		vec[str(var + 1)].record(Neurons[var].soma[0](0.5)._ref_v)
	#Record time.
	vec['t '] = h.Vector()
	vec ['t '].record(h._ref_t)
	return vec

def makeStimulus( Neurons, simTime ):
	interval = 1
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

def runSimulation_v1(young_chem1_con1, young_elec1_con1, numNeurons, fileIndex, simTime, inhibInd, age, delay):
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
	synYoung,ncYoung = constructConnections2( young_chem1_con1, numNeurons, Neurons, inhibInd, delay )

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

	#Write results.
	if age == 1:
		file = open(path + 'spikesYoung_1_' + fileIndex + '.txt',"wb")
	elif age == 2:
		file = open(path + 'spikesOld1_1_' + fileIndex + '.txt',"wb")
	else:
		file = open(path + 'spikesOld2_1_' + fileIndex + '.txt',"wb")

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
	
	#Plot the results	
	#figure()
		
	#hold(True)	
		
	#plot(vec['t '],vec['1'])
	#show()

def runSimulation_v2(young_chem1_con1, young_elec1_con1, numNeurons, fileIndex, simTime, inhibInd, age, delay):
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
	gapsYoung = constructConnections1( young_elec1_con1, numNeurons, Neurons)
	synYoung,ncYoung = constructConnections2( young_chem1_con1, numNeurons, Neurons, inhibInd, delay )

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

	#Write results.
	if age == 1:
		file = open(path + 'spikesYoung_2_' + fileIndex + '.txt',"wb")
	elif age == 2:
		file = open(path + 'spikesOld1_2_' + fileIndex + '.txt',"wb")
	else:
		file = open(path + 'spikesOld2_2_' + fileIndex + '.txt',"wb")

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
	
	#Plot the results	
	#figure()
		
	#hold(True)	
		
	#plot(vec['t '],vec['1'])
	#show()

"""
Main method
"""

#Time it and set simulation parameters.
start_time = time.time()
simTime = 1000
path = '/data2/L/Brain/max/testingWritingColumns_v1/K0.02/trial10/'
fileIndex = sys.argv[1]

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

#Load YOUNG brain data....
youngDist = []
fh = open(path + 'youngDist_' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	youngDist.append( y )
fh.close()
for l in range(0, numNeurons):				
	youngDist[l] = youngDist[l][0].split(",")
young_chem_con1 =[]
fh = open(path + 'young_chem_con1_' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	young_chem_con1.append( y )
fh.close()
for l in range(0, numNeurons):				
	young_chem_con1[l] = young_chem_con1[l][0].split(",")
young_elec_con1 =[]
fh = open(path + 'young_elec_con1_' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	young_elec_con1.append( y )
fh.close()
for l in range(0, numNeurons):				
	young_elec_con1[l] = young_elec_con1[l][0].split(",")


#Load OLD brain data with CONTINUOUS connections....
oldDist = []
fh = open(path + 'oldDist_' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	oldDist.append( y )
fh.close()
for l in range(0, numNeurons):				
	oldDist[l] = oldDist[l][0].split(",")
old_chem1_age1 =[]
fh = open(path + 'old_chem1_age1_' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	old_chem1_age1.append( y )
fh.close()
for l in range(0, numNeurons):				
	old_chem1_age1[l] = old_chem1_age1[l][0].split(",")

old_elec1_age1 =[]
fh = open(path + 'old_elec1_age1_' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	old_elec1_age1.append( y )
fh.close()
for l in range(0, numNeurons):				
	old_elec1_age1[l] = old_elec1_age1[l][0].split(",")



#Load OLD brain data with DISCRETE connections....
old_chem1_age2 =[]
fh = open(path + 'old_chem1_age2_' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	old_chem1_age2.append( y )
fh.close()
for l in range(0, numNeurons):				
	old_chem1_age2[l] = old_chem1_age2[l][0].split(",")

old_elec1_age2 =[]
fh = open(path + 'old_elec1_age2_' + fileIndex + '.txt')
print fh
for line in fh.readlines():
	y = [value for value in line.split()]
	old_elec1_age2.append( y )
fh.close()
for l in range(0, numNeurons):				
	old_elec1_age2[l] = old_elec1_age2[l][0].split(",")

#Run simulations without gap junctions.
runSimulation_v1(young_chem_con1, young_elec_con1, numNeurons, fileIndex, simTime, inhibInd, 1, youngDist)
runSimulation_v1(old_chem1_age1,   old_elec1_age1, numNeurons, fileIndex, simTime, inhibInd, 2, oldDist)
runSimulation_v1(old_chem1_age2,   old_elec1_age2, numNeurons, fileIndex, simTime, inhibInd, 3, oldDist)

#Run simulations with gap junctions.
runSimulation_v2(young_chem_con1, young_elec_con1, numNeurons, fileIndex, simTime, inhibInd, 1, youngDist)
runSimulation_v2(old_chem1_age1,   old_elec1_age1, numNeurons, fileIndex, simTime, inhibInd, 2, oldDist)
runSimulation_v2(old_chem1_age2,   old_elec1_age2, numNeurons, fileIndex, simTime, inhibInd, 3, oldDist)

print time.time() - start_time, "seconds"
