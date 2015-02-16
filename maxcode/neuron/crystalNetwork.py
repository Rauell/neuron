###########################################################################
#Code for generating a crystal neural network from 3D data
#Max Henderson
#Drexel University
#February 6, 2012
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
	return (Soma, Axon, BD, AD)

###########################################################################
#Main
###########################################################################

#The first step is to get the data specifying the geometry of the network and neurons in the network.

fh = open('/home/hendemd/Desktop/MATLAB/bin/Neural research/Crystal Size 2/num1.swc')
x = []
for line in fh.readlines():
    y = [value for value in line.split()]
    x.append( y )
fh.close()
soma1, axon1, basalDend1, apicalDend1 = constructGeometry(x,1)

fh = open('/home/hendemd/Desktop/MATLAB/bin/Neural research/Crystal Size 2/num2.swc')
x = []
for line in fh.readlines():
    y = [value for value in line.split()]
    x.append( y )
fh.close()
soma2, axon2, basalDend2, apicalDend2 = constructGeometry(x,1)

fh = open('/home/hendemd/Desktop/MATLAB/bin/Neural research/Crystal Size 2/num3.swc')
x = []
for line in fh.readlines():
    y = [value for value in line.split()]
    x.append( y )
fh.close()
soma3, axon3, basalDend3, apicalDend3 = constructGeometry(x,1)

fh = open('/home/hendemd/Desktop/MATLAB/bin/Neural research/Crystal Size 2/num4.swc')
x = []
for line in fh.readlines():
    y = [value for value in line.split()]
    x.append( y )
fh.close()
soma4, axon4, basalDend4, apicalDend4 = constructGeometry(x,1)

fh = open('/home/hendemd/Desktop/MATLAB/bin/Neural research/Crystal Size 2/num5.swc')
x = []
for line in fh.readlines():
    y = [value for value in line.split()]
    x.append( y )
fh.close()
soma5, axon5, basalDend5, apicalDend5 = constructGeometry(x,1)

fh = open('/home/hendemd/Desktop/MATLAB/bin/Neural research/Crystal Size 2/num6.swc')
x = []
for line in fh.readlines():
    y = [value for value in line.split()]
    x.append( y )
fh.close()
soma6, axon6, basalDend6, apicalDend6 = constructGeometry(x,1)

fh = open('/home/hendemd/Desktop/MATLAB/bin/Neural research/Crystal Size 2/num7.swc')
x = []
for line in fh.readlines():
    y = [value for value in line.split()]
    x.append( y )
fh.close()
soma7, axon7, basalDend7, apicalDend7 = constructGeometry(x,1)

fh = open('/home/hendemd/Desktop/MATLAB/bin/Neural research/Crystal Size 2/num8.swc')
x = []
for line in fh.readlines():
    y = [value for value in line.split()]
    x.append( y )
fh.close()
soma8, axon8, basalDend8, apicalDend8 = constructGeometry(x,1)

fh = open('/home/hendemd/Desktop/MATLAB/bin/Neural research/Crystal Size 2/Connections.txt')
connections = []
for line in fh.readlines():
    y = [value for value in line.split()]
    connections.append( y )
fh.close()
l = size(connections)
for i in range(0, l):
	connections[i] = connections[i][0].split(",")

#Determine electric stimulation of neural network...

for sec in soma1,soma2,soma3,soma4,soma5,soma6,soma7,soma8:
	sec.insert('hh')
	sec.nseg = 10

axon1[0].insert('hh')
axon2[0].insert('hh')
axon3[0].insert('hh')
axon4[0].insert('hh')
axon5[0].insert('hh')
axon6[0].insert('hh')
axon7[0].insert('hh')
axon8[0].insert('hh')
axon1[0].nseg = 10
axon2[0].nseg = 10
axon3[0].nseg = 10
axon4[0].nseg = 10
axon5[0].nseg = 10
axon6[0].nseg = 10
axon7[0].nseg = 10
axon8[0].nseg = 10


basalDend1[0].insert('pas')
basalDend2[0].insert('pas')
basalDend3[0].insert('pas')
basalDend4[0].insert('pas')
basalDend5[0].insert('pas')
basalDend6[0].insert('pas')
basalDend7[0].insert('pas')
basalDend8[0].insert('pas')
basalDend1[0].nseg = 10
basalDend2[0].nseg = 10
basalDend3[0].nseg = 10
basalDend4[0].nseg = 10
basalDend5[0].nseg = 10
basalDend6[0].nseg = 10
basalDend7[0].nseg = 10
basalDend8[0].nseg = 10

apicalDend1[0].insert('pas')
apicalDend2[0].insert('pas')
apicalDend3[0].insert('pas')
apicalDend4[0].insert('pas')
apicalDend5[0].insert('pas')
apicalDend6[0].insert('pas')
apicalDend7[0].insert('pas')
apicalDend8[0].insert('pas')
apicalDend1[0].nseg = 10
apicalDend2[0].nseg = 10
apicalDend3[0].nseg = 10
apicalDend4[0].nseg = 10
apicalDend5[0].nseg = 10
apicalDend6[0].nseg = 10
apicalDend7[0].nseg = 10
apicalDend8[0].nseg = 10

names = []
for sec in h.allsec(): 
     	names.append(h.secname())

print names	
# Connect neurons in network... 
"""
syn = []
nc = []
for i in range(0,l):
	tempSectionName = "soma" + connections[i][9]
	print tempSectionName
	print soma8.name
	syn.append(h.ExpSyn(float(connections[i][8]), sec = tempSectionName))
"""

syn1 = h.ExpSyn (0.5, sec = soma1)
syn2 = h.ExpSyn (0.5, sec = soma2)
syn3 = h.ExpSyn (0.5, sec = soma3)
syn4 = h.ExpSyn (0.5, sec = soma4)
syn5 = h.ExpSyn (0.5, sec = soma5)
syn6 = h.ExpSyn (0.5, sec = soma6)
syn7 = h.ExpSyn (0.5, sec = soma7)
syn8 = h.ExpSyn (0.5, sec = soma8)
syn9 = h.ExpSyn (0.5, sec = soma5)
IAF =  h.IntFire1 (0.5, sec = soma1)
IAF.tau = 10
IAF.refrac = 5

# connect the pre - synaptic section to the
# synapse object

soma2.push()
nc1 = h.NetCon( soma2(0.5)._ref_v, syn1 )
nc1.weight[0] = 1.0
soma3.push()
nc2 = h.NetCon( soma3(0.5)._ref_v, syn2 )
nc2.weight[0] = 1.0
soma4.push()
nc3 = h.NetCon( soma4(0.5)._ref_v, syn3 )
nc3.weight[0] = 1.0
soma5.push()
nc4 = h.NetCon( soma5(0.5)._ref_v, syn4 )
nc4.weight[0] = 1.0
soma6.push()
nc5 = h.NetCon( soma6(0.5)._ref_v, syn5 )
nc5.weight[0] = 1.0
soma7.push()
nc6 = h.NetCon( soma7(0.5)._ref_v, syn6 )
nc6.weight[0] = 1.0
soma8.push()
nc7 = h.NetCon( soma8(0.5)._ref_v, syn7 )
nc7.weight[0] = 1.0
soma1.push()
nc8 = h.NetCon( soma1(0.5)._ref_v, syn8 )
nc8.weight[0] = 1.0
nc9 = h.NetCon( soma1(0.5)._ref_v, syn9 )
nc9.weight[0] = 1.0

vec = {}
for var in 'v_1 ', 'v_2 ', 'v_3 ', 'v_4 ','v_5 ', 'v_6 ','v_7 ', 'v_8 ','t ':
    vec[var] = h.Vector()

# inject current in the pre - synaptic section, and to mimic 'real life', make it a fun sinusoidal current

stim = h.IClamp(soma1(0.5) )
stim.delay = 5
stim.dur = 10


stim1 = h.IClamp(soma3(0.5) )
stim1.delay = 10
stim1.amp = 2
stim1.dur = 1

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
	listOfSines.append(sin(freq*pie*t)*cos(freq*2*pie*t)+1)
	#listOfSines.append(1)
	listOfTimes.append(i)
VecT = h.Vector(listOfTimes)
VecStim = h.Vector(listOfSines)
VecStim.play(stim._ref_amp, VecT, 1)

# record the membrane potentials
vec ['v_1 '].record(soma1(0.5)._ref_v)
vec ['v_2 '].record(soma2(0.5)._ref_v)
vec ['v_3 '].record(soma3(0.5)._ref_v)
vec ['v_4 '].record(soma4(0.5)._ref_v)
vec ['v_5 '].record(soma5(0.5)._ref_v)
vec ['v_6 '].record(soma6(0.5)._ref_v)
vec ['v_7 '].record(soma7(0.5)._ref_v)
vec ['v_8 '].record(soma8(0.5)._ref_v)
"""
# record the membrane currents
vec ['v_1 '].record(syn1._ref_i)
vec ['v_2 '].record(syn2._ref_i)
vec ['v_3 '].record(syn3._ref_i)
vec ['v_4 '].record(syn4._ref_i)
vec ['v_5 '].record(syn5._ref_i)
vec ['v_6 '].record(syn6._ref_i)
vec ['v_7 '].record(syn7._ref_i)
vec ['v_8 '].record(syn8._ref_i)
"""
# record time
vec ['t '].record(h._ref_t)

# run the simulation
h.load_file("stdrun.hoc")
h.init()
h.tstop = 75.0
h.run()

# plot the results
figure()
#subplot(2,1,1)
plot(vec['t '],vec['v_1 '],vec['t '], vec['v_2 '],vec['t '],vec['v_3 '],vec['t '], vec['v_4 '],vec['t '],vec['v_5 '],vec['t '], vec['v_6 '],vec['t '],vec['v_7 '],vec['t '], vec['v_8 '])
#subplot(2,1,2)
#plot(vec['t '],vec['i_1 '],vec['t '], vec['i_2 '],vec['t '],vec['i_3 '],vec['t '], vec['i_4 '],vec['t '],vec['i_5 '],vec['t '], vec['i_6 '],vec['t '],vec['i_7 '],vec['t '], vec['i_8 '])
#plot(VecT, VecStim)
hoc.execute('load_file("mview.hoc")')
hoc.execute("mview()")
show()










