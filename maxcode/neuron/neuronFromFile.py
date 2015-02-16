###########################################################################
#Code for generating a neural network from 3D data
#Max Henderson
#Drexel University
#January 17, 2012
###########################################################################

from neuron import *
from nrn import *
from itertools import chain
from neuron import h
from numpy import *
from pylab import *
import os

###########################################################################
#Definitions
###########################################################################

def constructGeometry( geometry,segFraction ):
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
		if connAxon[i][0]>-2:
			Axon[i].connect(Axon[int(connAxon[i][0])], connAxon[i][1], 0)
			Axon[i].push()
			if int(h.n3d()/segFraction) > 1:
				Axon[i].nseg = int(h.n3d()/segFraction)
			else:
				Axon[i].nseg = 1
	for i in range(1,len(connBD)):
		BD[i].connect(BD[int(connBD[i][0])], connBD[i][1], 0)
		BD[i].push()
		if int(h.n3d()/segFraction) > 1:
			BD[i].nseg = int(h.n3d()/segFraction)
		else:
			BD[i].nseg = 1
	for i in range(1,len(connAD)):
		AD[i].connect(AD[int(connAD[i][0])], connAD[i][1], 0)
		AD[i].push()
		if int(h.n3d()/segFraction) > 1:
			AD[i].nseg = int(h.n3d()/segFraction)
		else:
			AD[i].nseg = 1
	
	#Check to see if only one soma point; if so, make another closeby so the system doesn't crash
	Soma.push()
	if h.n3d() < 2:
		h.pt3dadd(float(soma[0][2])+10,float(soma[0][3])+10,float(soma[0][4])+10,float(soma[0][5]),sec=Soma)
	Soma.nseg = 1
	return (Soma, Axon, BD, AD)

###########################################################################
#Main
###########################################################################

#The first step is to get the data specifying the geometry of the neuron. The resulting data set will be an N by 7 multi-dimensional list.

numFiles = 0
path = '/home/hendemd/Desktop/MATLAB/bin/Neural research/NumberNeurons3 Dated 2012 2 6 13 50/'
listing = os.listdir(path)
for infile in listing:
	numFiles = numFiles + 1
Soma = []
Axon = []
BD = []
AD = []
numFiles

#for infile in listing:
    #print "current file is: " + infile
    #fh = open( path + infile )
    #x = []
    #for line in fh.readlines():
    #	y = [value for value in line.split()]
    #	x.append( y )
    #fh.close()
    #soma, axon, basalDend, apicalDend = constructGeometry(x,1)
    #if numFiles == 0:
    #	Soma = soma
    #	Axon = axon
    #	BD = basalDend
    #	AD = apicalDend
    #	numFiles = numFiles + 1
    #else:
	#Soma = [Soma, soma]
    	#Axon = [Axon, axon]
    	#BD = [BD, basalDend]
    	#AD = [AD, apicalDend]
    	#numFiles = numFiles + 1
fh = open('/home/hendemd/Desktop/MATLAB/bin/Neural research/NumberNeurons3 Dated 2012 2 6 15 14/num1.swc')
x = []
for line in fh.readlines():
    y = [value for value in line.split()]
    x.append( y )
fh.close()
soma, axon, basalDend, apicalDend = constructGeometry(x,1)
fh = open('/home/hendemd/Desktop/MATLAB/bin/Neural research/NumberNeurons3 Dated 2012 2 6 15 14/num2.swc')
x = []
for line in fh.readlines():
    y = [value for value in line.split()]
    x.append( y )
fh.close()
soma1, axon1, basalDend1, apicalDend1 = constructGeometry(x,1)
fh = open('/home/hendemd/Desktop/MATLAB/bin/Neural research/NumberNeurons3 Dated 2012 2 6 15 14/num3.swc')
x = []
for line in fh.readlines():
    y = [value for value in line.split()]
    x.append( y )
fh.close()
soma2, axon2, basalDend2, apicalDend2 = constructGeometry(x,1)
#Determine electric stimulation of neural network...

soma.insert('hh')
for i in range(0, size(axon)):
	axon[i].insert('hh')
for i in range(0, size(basalDend)):
	basalDend[i].insert('pas')
for i in range(0, size(apicalDend)):
	apicalDend[i].insert('pas')

#soma1.insert('hh')
#for i in range(0, size(axon1)):
#	axon1[i].insert('hh')
#for i in range(0, size(basalDend1)):
#	basalDend1[i].insert('pas')
#for i in range(0, size(apicalDend1)):
#	apicalDend1[i].insert('pas')

# create a synapse in the pre - synaptic section
syn = h.ExpSyn (0.5, sec = soma)
syn1 = h.ExpSyn (0.5, sec = soma)
# connect the pre - synaptic section to the
# synapse object

soma1.push()
nc = h.NetCon( soma1(0.5)._ref_v, syn )
nc.weight[0] = 10.0
soma2.push()
nc1 = h.NetCon( soma2(0.5)._ref_v, syn1 )
nc1.weight[0] = 10.0

vec = {}
for var in 'v_pre ', 'v_post ', 't ':
    vec[var] = h.Vector()

# inject current in the pre - synaptic section, and to mimic 'real life', make it a fun sinusoidal current
stim = h.IClamp(soma(0.5) )
stim1 = h.IClamp(0.5, sec = soma2)
stim1.amp = 100
stim1.delay = 50
stim1.dur = 100
stim.dur = 500
vecCurrent = h.Vector()
vecCurrent.record(stim._ref_i)
time = h.Vector()
time.record(h._ref_t)
listOfSines = []
listOfTimes = []
for i in range(0,500):
	t = i/1000.
	freq = 10
	pie = 2*3.14
	listOfSines.append(14*sin(freq*pie*t)*cos(freq*2*pie*t)+14)
	#listOfSines.append(50)
	listOfTimes.append(i)
VecT = h.Vector(listOfTimes)
VecStim = h.Vector(listOfSines)
VecStim.play(stim._ref_amp, VecT, 1)

# record the membrane potentials
vec ['v_pre '].record(soma(0.5)._ref_v)
vec ['v_post '].record(basalDend[5](1)._ref_v)
#vec ['v_post '].record(stim._ref_i)
vec ['t '].record(h._ref_t)



# run the simulation
h.load_file("stdrun.hoc")
h.init()
h.tstop = 500.0
h.run()

# plot the results
figure()
subplot(2,1,1)
plot(vec['t '],vec['v_pre '])
subplot(2,1,2)
plot(VecT, VecStim)
show()
print h.topology()










