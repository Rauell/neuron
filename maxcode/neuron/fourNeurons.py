from neuron import *
from neuron import h as nrn
from numpy import *
from neuronGen import *
from pylab import *

#The goal here is to build a 4 neuron system that have several dendritic attachments and connections with axons. The, I shall put a current clamp on one of the neurons. Finally, I will try and graph the results of the neuron clamp and 4 interconnected neurons.

neurons = [] #This will contain my generate neurons
nc = [] #This will contain the connections between neurons
numNeurons = 4
for i in range(0, numNeurons):
    neurons.append(neuronGen())
    neurons[i].construct()

stim = h.IClamp(0.5, sec = neurons[0].soma)
stim.amp = 205.0
stim.delay = 5.0
stim.dur = 5.0
stim1 = h.IClamp(0.5, sec = neurons[2].soma)
stim1.amp = 205.0
stim1.delay = 7.0
stim1.dur = 5.0

#Now, I will connect the neurons...

#nc.append(h.NetCon(neurons[0].dend1(0.75)._ref_v,neurons[1].syn2, sec=neurons[0].dend1))
#nc[0].weight[0] = 2
#nc.append(h.NetCon(neurons[2].soma(0.55)._ref_v,neurons[1].syn4, sec=neurons[2].soma))
#nc.append(h.NetCon(neurons[3].dend2(0.75)._ref_v,neurons[2].syn3, sec=neurons[3].dend2))
#nc.append(h.NetCon(neurons[3].soma(0.65)._ref_v,neurons[0].syn2, sec=neurons[3].soma))

vec = {}
for var in 'v_1 ', 'v_2 ','v_3 ', 'v_4 ', 't ':
    vec[var] = h.Vector()

# record the membrane potentials and
# synaptic currents
vec['v_1 '].record(neurons[0].soma(0.5)._ref_v)
vec['v_2 '].record(neurons[1].soma(0.5)._ref_v)
vec['v_3 '].record(neurons[2].soma(0.5)._ref_v)
vec['v_4 '].record(neurons[3].soma(0.5)._ref_v)
vec ['t '].record(h._ref_t)

# run the simulation
h.load_file("stdrun.hoc")
h.init()
h.tstop = 20.0
h.run()

# plot the results
figure()
plot(vec['t '],vec['v_1 '],vec['t '],vec['v_2 '],vec['t '],vec['v_3 '],vec['t '],vec['v_4 '])
h.topology()
print h.n3d()

show()
