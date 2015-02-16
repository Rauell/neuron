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

def constructGeometry( geometry ):
	l = len(geometry)
	indexSoma = 0
	indexAxon = 0
	indexBD = 0
	indexAD = 0
	#Determine the number of points in each component of the neuron
    	for i in range(0,l):
		if (int(geometry[i][1])==1):
			indexSoma = indexSoma + 1
		elif (int(geometry[i][1])==2):
			indexAxon = indexAxon + 1	
		elif (int(geometry[i][1])==3):
			indexBD= indexBD + 1	
		else:
			indexAD = indexAD + 1
	#Create lists to store the data for each component, lists being appropriately
	#sized to the number of points from previous step
	soma = zeros([indexSoma,8])
	axon = zeros([indexAxon,8])
	basalDend = zeros([indexBD,8])
	apicalDend = zeros([indexAD,8])
	#Reset indices, and determine # of unique bifurcations in each component	
	indexSoma = 0
	indexAxon = 0
	indexBD = 0
	indexAD = 0
	bifSoma = 0
	bifAxon = 0
	bifBD = 0
	bifAD = 0
	for i in range(0,l):
		if (int(geometry[i][1])==1):
			soma[indexSoma][0] = float(geometry[i][0])
			soma[indexSoma][1] = float(geometry[i][1])
			soma[indexSoma][2] = float(geometry[i][2])
			soma[indexSoma][3] = float(geometry[i][3])
			soma[indexSoma][4] = float(geometry[i][4])
			soma[indexSoma][5] = float(geometry[i][5])
			soma[indexSoma][6] = float(geometry[i][6])
			indexSoma = indexSoma + 1
		elif (int(geometry[i][1])==2):
			axon[indexAxon][0] = float(geometry[i][0])
			axon[indexAxon][1] = float(geometry[i][1])
			axon[indexAxon][2] = float(geometry[i][2])
			axon[indexAxon][3] = float(geometry[i][3])
			axon[indexAxon][4] = float(geometry[i][4])
			axon[indexAxon][5] = float(geometry[i][5])
			axon[indexAxon][6] = float(geometry[i][6])
			indexAxon = indexAxon + 1	
		elif (int(geometry[i][1])==3):
			basalDend[indexBD][0] = float(geometry[i][0])
			basalDend[indexBD][1] = float(geometry[i][1])
			basalDend[indexBD][2] = float(geometry[i][2])
			basalDend[indexBD][3] = float(geometry[i][3])
			basalDend[indexBD][4] = float(geometry[i][4])
			basalDend[indexBD][5] = float(geometry[i][5])
			basalDend[indexBD][6] = float(geometry[i][6])
			indexBD= indexBD + 1	
		else:
			apicalDend[indexAD][0] = float(geometry[i][0])
			apicalDend[indexAD][1] = float(geometry[i][1])
			apicalDend[indexAD][2] = float(geometry[i][2])
			apicalDend[indexAD][3] = float(geometry[i][3])
			apicalDend[indexAD][4] = float(geometry[i][4])
			apicalDend[indexAD][5] = float(geometry[i][5])
			apicalDend[indexAD][6] = float(geometry[i][6])
			indexAD= indexAD + 1
	for i in range(1,len(axon)):
		if axon[i][6]!=axon[i-1][0]:
			bifAxon = bifAxon + 1
	for i in range(1,len(basalDend)):
		if basalDend[i][6]!=basalDend[i-1][0]:
			bifBD = bifBD + 1
	for i in range(1,len(apicalDend)):
		if apicalDend[i][6]!=apicalDend[i-1][0]:
			bifAD = bifAD + 1
	Soma = h.Section()
	Axon = []
	BD = []
	AD = []
	#Create appropriate number of sections/bifs for each component
	for i in range(0, bifAxon+1):
		Axon.append(h.Section())
	for i in range(0, bifBD+1):
		BD.append(h.Section())
	for i in range(0, bifAD+1):
		AD.append(h.Section())
	#Put all the 3D point data into the appropriate bifs
	bifAxon = 0
	bifBD = 0
	bifAD = 0
	for i in range(0, shape(soma)[0]):
		h.pt3dadd(float(soma[i][2]),float(soma[i][3]),float(soma[i][4]),float(soma[i][5]),sec=Soma)
	for i in range(0, len(axon)):
		if i == 0:
			h.pt3dadd(float(axon[i][2]),float(axon[i][3]),float(axon[i][4]),float(axon[i][5]),sec=Axon[bifAxon])
			axon[i][7] = bifAxon
		elif axon[i][6]!=axon[i-1][0]:
			bifAxon = bifAxon + 1
			h.pt3dadd(float(axon[i][2]),float(axon[i][3]),float(axon[i][4]),float(axon[i][5]),sec=Axon[bifAxon])
			axon[i][7] = bifAxon
		else:
			h.pt3dadd(float(axon[i][2]),float(axon[i][3]),float(axon[i][4]),float(axon[i][5]),sec=Axon[bifAxon])
			axon[i][7] = bifAxon
	for i in range(0, len(basalDend)):
		if i == 0:
			h.pt3dadd(float(basalDend[i][2]),float(basalDend[i][3]),float(basalDend[i][4]),float(basalDend[i][5]),sec=BD[bifBD])
			basalDend[i][7] = bifBD
		elif basalDend[i][6]!=basalDend[i-1][0]:
			bifBD = bifBD + 1
			h.pt3dadd(float(basalDend[i][2]),float(basalDend[i][3]),float(basalDend[i][4]),float(basalDend[i][5]),sec=BD[bifBD])
			basalDend[i][7] = bifBD
		else:
			h.pt3dadd(float(basalDend[i][2]),float(basalDend[i][3]),float(basalDend[i][4]),float(basalDend[i][5]),sec=BD[bifBD])
			basalDend[i][7] = bifBD
	for i in range(0, len(apicalDend)):
		if i == 0:
			h.pt3dadd(float(apicalDend[i][2]),float(apicalDend[i][3]),float(apicalDend[i][4]),float(apicalDend[i][5]),sec=AD[bifAD])
			apicalDend[i][7] = bifAD
		elif apicalDend[i][6]!=apicalDend[i-1][0]:
			bifAD = bifAD + 1
			h.pt3dadd(float(apicalDend[i][2]),float(apicalDend[i][3]),float(apicalDend[i][4]),float(apicalDend[i][5]),sec=AD[bifAD])
			apicalDend[i][7] = bifAD
		else:
			h.pt3dadd(float(apicalDend[i][2]),float(apicalDend[i][3]),float(apicalDend[i][4]),float(apicalDend[i][5]),sec=AD[bifAD])
			apicalDend[i][7] = bifAD
	#At this point, we have all the bifurcations of all the sections of all the neural components with the 3D geometry specified. Now, the last
	#steps will involve connecting all the bifurications to the appropropriate spots on the other parts of the bifurications. This will be an
	#approximate connection method, because the connection points will also depend highly on how many segments are alloted to each section.
	connAxon = zeros([bifAxon+1,2])
	connBD = zeros([bifBD+1,2])
	connAD = zeros([bifAD+1,2])
	current = []
	for i in range(1,len(axon)):
		if axon[i][6]!=axon[i-1][0]:
			for j in range(0,len(axon)):
				if axon[i][6]==axon[j][0]:
					connAxon[axon[i][7]][0] = axon[j][7]
					for k in range(0,len(axon)):
						if axon[k][7] == axon[j][7]:
							current.append(axon[k][0])
					if len(current) > 0:
						connAxon[axon[i][7]][1]= (axon[j][0]-current[0])/len(current)
						current = []	
	for i in range(1,len(basalDend)):
		if basalDend[i][6]!=basalDend[i-1][0]:
			for j in range(0,len(basalDend)):
				if basalDend[i][6]==basalDend[j][0]:
					connBD[basalDend[i][7]][0] = basalDend[j][7]
					for k in range(0,len(basalDend)):
						if basalDend[k][7] == basalDend[j][7]:
							current.append(basalDend[k][0])
					if len(current) > 0:
						connBD[basalDend[i][7]][1]= (basalDend[j][0]-current[0])/len(current)
						current = []
	for i in range(1,len(apicalDend)):
		if apicalDend[i][6]!=apicalDend[i-1][0]:
			for j in range(0,len(apicalDend)):
				if apicalDend[i][6]==apicalDend[j][0]:
					connAD[apicalDend[i][7]][0] = apicalDend[j][7]
					for k in range(0,len(apicalDend)):
						if apicalDend[k][7] == apicalDend[j][7]:
							current.append(apicalDend[k][0])
					if len(current) > 0:
						connAD[apicalDend[i][7]][1]= (apicalDend[j][0]-current[0])/len(current)
						current = []	
	#Finally, now that we have all the connections, we can connect all the bifurcations at their
	#approximate points on the different sections. Also, we can determine the # of segments for 
	#each section by the # of 3D points. child.connect(parent,parentPoint, childPoint).
	
	Axon[0].connect(Soma, 0.5, 0)
	BD[0].connect(Soma, 0.5, 0)
	AD[0].connect(Soma, 0.5, 0)
	for i in range(1,len(connAxon)):
		Axon[i].connect(Axon[int(connAxon[i][0])], connAxon[i][1], 0)
		Axon[i].push()
	for i in range(1,len(connBD)):
		BD[i].connect(BD[int(connBD[i][0])], connBD[i][1], 0)
		BD[i].push()
	for i in range(1,len(connAD)):
		AD[i].connect(AD[int(connAD[i][0])], connAD[i][1], 0)
		AD[i].push()
	return (Soma, Axon, BD, AD)

def constructConnections( connection, Soma, Axon, BD, AD ):
	"""
		This definition will take a synaptic in the connections matrix and create a synapse and network connection between the appropriate neurons.
	"""
	syn = 0
	nc  = 0
	if int(connection[1]) == 1:
		if int(connection[5]) == 1:
			"""
			syn = h.ExpSyn (float(connection[3]), sec = Soma[int(connection[0])-1][int(connection[2])-1])
			Soma[int(connection[4])-1][int(connection[6])-1].push()
			nc = h.NetCon( Soma[int(connection[4])-1][int(connection[6])-1](float(connection[7]))._ref_v, syn )
			nc.weight[0] = float(connection[8])
			"""
		elif int(connection[5]) == 2:
			"""
			syn = h.ExpSyn (float(connection[3]), sec = Soma[int(connection[0])-1][int(connection[2])-1])
			Axon[int(connection[4])-1][int(connection[6])-1].push()
			nc = h.NetCon( Axon[int(connection[4])-1][int(connection[6])-1](float(connection[7]))._ref_v, syn )
			nc.weight[0] = float(connection[8])
			"""
		elif int(connection[5]) == 3:
			"""
			syn = h.ExpSyn (float(connection[3]), sec = Soma[int(connection[0])-1][int(connection[2])-1])
			BD[int(connection[4])-1][int(connection[6])-1].push()
			nc = h.NetCon( BD[int(connection[4])-1][int(connection[6])-1](float(connection[7]))._ref_v, syn )
			nc.weight[0] = float(connection[8])
			"""
		else:
			"""
			syn = h.ExpSyn (float(connection[3]), sec = Soma[int(connection[0])-1][int(connection[2])-1])
			AD[int(connection[4])-1][int(connection[6])-1].push()
			nc = h.NetCon( AD[int(connection[4])-1][int(connection[6])-1](float(connection[7]))._ref_v, syn )
			nc.weight[0] = float(connection[8])
			"""
	elif int(connection[1]) == 2:
		if int(connection[5]) == 1:
			"""
			syn = h.ExpSyn (float(connection[3]), sec = Axon[int(connection[0])-1][int(connection[2])-1])
			Soma[int(connection[4])-1][int(connection[6])-1].push()
			nc = h.NetCon( Soma[int(connection[4])-1][int(connection[6])-1](float(connection[7]))._ref_v, syn )
			nc.weight[0] = float(connection[8])
			"""
		elif int(connection[5]) == 2:
			syn = h.ExpSyn (float(connection[3]), sec = Axon[int(connection[0])-1][int(connection[2])-1])
			Axon[int(connection[4])-1][int(connection[6])-1].push()
			nc = h.NetCon( Axon[int(connection[4])-1][int(connection[6])-1](float(connection[7]))._ref_v, syn )
			nc.weight[0] = float(connection[8])
		elif int(connection[5]) == 3:
			syn = h.ExpSyn (float(connection[3]), sec = Axon[int(connection[0])-1][int(connection[2])-1])
			BD[int(connection[4])-1][int(connection[6])-1].push()
			nc = h.NetCon( BD[int(connection[4])-1][int(connection[6])-1](float(connection[7]))._ref_v, syn )
			nc.weight[0] = float(connection[8])
		else:
			syn = h.ExpSyn (float(connection[3]), sec = Axon[int(connection[0])-1][int(connection[2])-1])
			AD[int(connection[4])-1][int(connection[6])-1].push()
			nc = h.NetCon( AD[int(connection[4])-1][int(connection[6])-1](float(connection[7]))._ref_v, syn )
			nc.weight[0] = float(connection[8])
	elif int(connection[1]) == 3:
		if int(connection[5]) == 1:
			"""
			syn = h.ExpSyn (float(connection[3]), sec = BD[int(connection[0])-1][int(connection[2])-1])
			Soma[int(connection[4])-1][int(connection[6])-1].push()
			nc = h.NetCon( Soma[int(connection[4])-1][int(connection[6])-1](float(connection[7]))._ref_v, syn )
			nc.weight[0] = float(connection[8])
			"""
		elif int(connection[5]) == 2:
			syn = h.ExpSyn (float(connection[3]), sec = BD[int(connection[0])-1][int(connection[2])-1])
			Axon[int(connection[4])-1][int(connection[6])-1].push()
			nc = h.NetCon( Axon[int(connection[4])-1][int(connection[6])-1](float(connection[7]))._ref_v, syn )
			nc.weight[0] = float(connection[8])
		elif int(connection[5]) == 3:
			syn = h.ExpSyn (float(connection[3]), sec = BD[int(connection[0])-1][int(connection[2])-1])
			BD[int(connection[4])-1][int(connection[6])-1].push()
			nc = h.NetCon( BD[int(connection[4])-1][int(connection[6])-1](float(connection[7]))._ref_v, syn )
			nc.weight[0] = float(connection[8])
		else:
			syn = h.ExpSyn (float(connection[3]), sec = BD[int(connection[0])-1][int(connection[2])-1])
			AD[int(connection[4])-1][int(connection[6])-1].push()
			nc = h.NetCon( AD[int(connection[4])-1][int(connection[6])-1](float(connection[7]))._ref_v, syn )
			nc.weight[0] = float(connection[8])
	else:
		if int(connection[5]) == 1:
			"""
			syn = h.ExpSyn (float(connection[3]), sec = AD[int(connection[0])-1][int(connection[2])-1])
			Soma[int(connection[4])-1][int(connection[6])-1].push()
			nc = h.NetCon( Soma[int(connection[4])-1][int(connection[6])-1](float(connection[7]))._ref_v, syn )
			nc.weight[0] = float(connection[8])
			"""
		elif int(connection[5]) == 2:
			syn = h.ExpSyn (float(connection[3]), sec = AD[int(connection[0])-1][int(connection[2])-1])
			Axon[int(connection[4])-1][int(connection[6])-1].push()
			nc = h.NetCon( Axon[int(connection[4])-1][int(connection[6])-1](float(connection[7]))._ref_v, syn )
			nc.weight[0] = float(connection[8])
		elif int(connection[5]) == 3:
			syn = h.ExpSyn (float(connection[3]), sec = AD[int(connection[0])-1][int(connection[2])-1])
			BD[int(connection[4])-1][int(connection[6])-1].push()
			nc = h.NetCon( BD[int(connection[4])-1][int(connection[6])-1](float(connection[7]))._ref_v, syn )
			nc.weight[0] = float(connection[8])
		else:
			syn = h.ExpSyn (float(connection[3]), sec = AD[int(connection[0])-1][int(connection[2])-1])
			AD[int(connection[4])-1][int(connection[6])-1].push()
			nc = h.NetCon( AD[int(connection[4])-1][int(connection[6])-1](float(connection[7]))._ref_v, syn )
			nc.weight[0] = float(connection[8])
	return (syn,nc)			

def constructStimulations( numNeurons, simTime, Soma, Axon, BD, AD ):
	"""
		This defintion will create a random stimulation in the neural network. It will pick two random numbers, one for picking a random neuron and one for picking either the soma, axon, BD, or AD. It will also pick a random bifurcation, amplitude, delay, and duration.
	"""
	#Pick random neuron.
	neuron = random.randint(1,numNeurons)
	neuronSection = random.randint(1,4)
	if neuronSection == 1:
		stim = h.IClamp(Soma[neuron-1](0.5) )
		stim.delay = random.randint(0,simTime-50)
		stim.dur = random.randint(1,5)
		stim.amp = random.randint(1,20)
	elif neuronSection == 2:
		stim = h.IClamp(Axon[neuron-1][0](0.5) )
		stim.delay = random.randint(0,simTime-50)
		stim.dur = random.randint(1,5)
		stim.amp = random.randint(1,20)
	elif neuronSection == 3:
		stim = h.IClamp(BD[neuron-1][0](0.5) )
		stim.delay = random.randint(0,simTime-50)
		stim.dur = random.randint(1,5)
		stim.amp = random.randint(1,20)
	else:
		stim = h.IClamp(AD[neuron-1][0](0.5) )
		stim.delay = random.randint(0,simTime-50)
		stim.dur = random.randint(1,5)
		stim.amp = random.randint(1,20)
	return stim

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
stimDuration = 3
stimStrength = 10
simTime = 50
numNeurons = 154
path = '/home/hendemd/Desktop/MATLAB/bin/Neural research/NumberNeurons154 Dated 2012 5 22 15 32/'
listing = os.listdir(path)

#Create lists for somas, axons, basal dendrites, and apical dendrites for each neuron in the network.

Soma = []
Axon = []
BD = []
AD = []

#Begin creating neurons individually from the various geometrical files.

for i in range(0,numNeurons):
	for infile in listing:
    		if (infile == "num" + str(i+1) + ".swc"):
			print infile
    			fh = open( path + infile )
    			x = []
    			for line in fh.readlines():
    				y = [value for value in line.split()]
    				x.append( y )
    			fh.close()
    			#Store temporary data in 
    			soma, axon, bd, ad = constructGeometry(x)
    			Soma.append(soma)
    			Axon.append(axon)
    			BD.append(bd)
    			AD.append(ad)

#Set biophysics for the different neural structures. IAF will contain all data pertaining to the refractory period between spikes.

IAF = []
counter = 0
for i in range(0,numNeurons):
	for sec in Axon[i]:
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
	for sec in BD[i]:
		sec.insert('pas')
		sec.nseg = numSegs
		IAF.append(h.IntFire1 (0.5))
		IAF[counter].tau = tau
		IAF[counter].refrac = refrac
		counter = counter + 1
		for seg in sec:
			seg.pas.g = 0.0002             
     			seg.pas.e = -65
	for sec in AD[i]:
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

#Import connectivity between neurons.

connections =[]
fh = open(path + 'Connections.txt')
syn = []
for line in fh.readlines():
    y = [value for value in line.split()]
    connections.append( y )
fh.close()
print connections
for i in range(0, shape(connections)[0]):
	connections[i] = connections[i][0].split(",")
#for i in range(0,8900):
for i in range(0, shape(connections)[0]):
	print i
	syn.append(constructConnections( connections[i], Soma, Axon, BD, AD ))
print syn

#Create vectors for recording potentials, currents, etc in the neural network during the simulation.

vec = recordData( numNeurons, Soma )

#Create random, unique simulation for the network.
"""
numberStimulations = random.randint(1,numNeurons-1)
stim = []
for i in range(0,numberStimulations):
	stim.append(constructStimulations( numNeurons-1, simTime, Soma, Axon, BD, AD ))
print stim
"""


stim = h.IClamp(Soma[0](0.5) )		
stim.delay = 5	
stim.dur = 1		
stim.amp = 1
"""
stim1 = h.IClamp(Soma[7](0.5) )		
stim1.delay = 5	
stim1.dur = 1		
stim1.amp = 10
"""

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






