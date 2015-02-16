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
Section = h. Section
from numpy import *
from pylab import *

###########################################################################
#Main
###########################################################################

#The first step is to get the data specifying the geometry of the neuron. The resulting data set will be an N by 7 multi-dimensional list.

fh = open( "/home/hendemd/Desktop/MATLAB/bin/Neural research/New neurons/c5 Dated 2011 11 15 18 14 4.160536e+01.swc" );

x = []
for line in fh.readlines():
    y = [value for value in line.split()]
    x.append( y )

fh.close()

soma = h.Section()
h.pt3dadd(0,0,0,3,sec=soma)
h.pt3dadd(0,0,1,3,sec=soma)
dend1 = h.Section()
h.pt3dadd(0,0,5,3,sec=dend1)
h.pt3dadd(5,0,5,2,sec=dend1)
h.pt3dadd(15,15,15,10,sec=dend1)
dend2 = h.Section()
h.pt3dadd(0,0,-5,3,sec=dend2)
h.pt3dadd(-5,0,-5,4,sec=dend2)
h.pt3dadd(-15,-15,-15,50,sec=dend2)
dend1.connect(soma, 0, 0)
dend2.connect(soma, 1, 0)

soma1 = h.Section()
h.pt3dadd(10,10,10,3,sec=soma1)
h.pt3dadd(10,10,11,3,sec=soma1)
dend3 = h.Section()
h.pt3dadd(10,10,15,3,sec=dend3)
h.pt3dadd(15,10,15,2,sec=dend3)
h.pt3dadd(5,5,5,1,sec=dend3)
dend4 = h.Section()
h.pt3dadd(10,10,5,3,sec=dend4)
h.pt3dadd(5,10,5,4,sec=dend4)
h.pt3dadd(0,1,5,5,sec=dend4)
dend3.connect(soma1, 0, 0)
dend4.connect(soma1, 1, 0)

#Display what happens when you drive a current through the neuron..

for sec in soma, dend1, dend2, soma1, dend3, dend4 :
    sec.insert('hh')
# inject current in the pre - synaptic section
stim = h.IClamp(0.25, sec = soma )
stim.amp = 10.0
stim.delay = 5.0
stim.dur = 5.0
stim1 = h.IClamp(0.25, sec = soma1 )
stim1.amp = 10.0
stim1.delay = 8.5
stim1.dur = 5.0

# create a synapse in the pre - synaptic section
syn = h.ExpSyn (0.5, sec = soma)
# connect the pre - synaptic section to the
# synapse object

soma1.push()
nc = h.NetCon( soma1(0.5)._ref_v, syn )
nc.weight[0] = 2.0

vec = {}
for var in 'v_pre ', 'v_post ', 't ':
    vec[var] = h.Vector()

# record the membrane potentials
vec['v_pre '].record(soma(0.5)._ref_v)
vec ['v_post '].record(soma1(0.5)._ref_v)
vec ['t '].record(h._ref_t)

# run the simulation
h.load_file("stdrun.hoc")
h.init()
h.tstop = 20.0
h.run()

# plot the results
figure()
subplot(2,1,1)
plot(vec['t '],vec['v_pre '])
subplot(2,1,2)
plot(vec['t '], vec['v_post '])
show()

###########################################################################
#Definitions
###########################################################################

def constructGeometry( geometry ):
	soma = h.Section()
	apicalDend = h.Section()
	basalDend = h.Section()
	axon = h.Section()
	l = len(geometry)
    	for i in range(0,l+1):
		if (geometry[i][1]==1):
			h.pt3dadd(geometry[i][2],geometry[i][3],geometry[i][4],geometry[i][5],sec=soma)
		elif (geometry[i][1]==2):
			h.pt3dadd(geometry[i][2],geometry[i][3],geometry[i][4],geometry[i][5],sec=axon)
		elif (geometry[i][1]==3):
			h.pt3dadd(geometry[i][2],geometry[i][3],geometry[i][4],geometry[i][5],sec=basalDend)
		else:
			h.pt3dadd(geometry[i][2],geometry[i][3],geometry[i][4],geometry[i][5],sec=axonDend)
	return (soma, apicalDend, basalDend, axon)








