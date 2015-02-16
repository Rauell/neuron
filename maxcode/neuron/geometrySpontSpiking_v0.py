from neuron import *
from neuron import h as nrn
from numpy import *
from pylab import *

"""
This program will be trying to replicate exactly the results from the paper, "The Geometry of Spontaneous Spiking in Neuronal Networks".

Max Henderson
2/23/13
"""

#Definition for constructing neural geometry with parameters specified in the paper.
def makeNeuron():
	neuron = h.Section()
	neuron.cm = 20
	neuron.insert('hh')
	neuron.nseg = 10
	neuron.L = 30
	neuron.diam = 30
	for seg in neuron:
		seg.hh.gl = 0.002
		seg.hh.el = -60
		seg.hh.gk = 0.008
		seg.hh.gna = 0.044
	return neuron

#Definition for making stimulus.
def makeStimulus( neuron, simTime ):
	interval = 50
	stimNc = h.NetStim()
	stimNc.noise = 1		
	stimNc.start = 0		
	stimNc.number = simTime
	stimNc.interval = interval
	syn = h.ExpSyn (0.5, sec = neuron)		
	nc = h.NetCon(stimNc, syn)
	nc.weight[0] = 5
	return (stimNc, syn, nc)

#Definition for recording neural data during the simulation.
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

"""
Main method.
"""
#Set constants.
simTime = 100
numNeurons = 10
#Make neurons and stimulations.
stims = []
neurons = []
for i in range(0,numNeurons):
	neurons.append(makeNeuron())
	stims.append(makeStimulus(neurons[i], simTime))
#Record data.
vec = recordData( numNeurons, neurons )
#Run the simulation.
h.load_file("stdrun.hoc")
h.init()
h.tstop = simTime
h.run()
#Plot results.
"""
figure()
hold(True)
for i in range(0,numNeurons):	
	plot(vec['t '],vec[str(i+1)])	
	plt.xlabel('Time (ms)')	
	plt.ylabel('V (mV)')
show()
"""
#Save data.
path = '/home/hendemd/Desktop/MATLAB/bin/Neural research/testing gaps/'		
file = open(path + 'spikes.txt',"wb")
print len(vec ['t '])
print len(vec ['1'])
print len(vec ['1'][10])
for i in range(0,len(vec ['t '])):		
	for j in range(0,numNeurons+1):			
		for var in vec:	    			
			if (var == str(j+1)):
				file.write(str(vec[var][i])+"\n")
			elif (j == numNeurons) & (var == 't '):
				file.write(str(vec['t '][i])+"\n")
file.close()
