from neuron import *
from nrn import *
from itertools import chain
from neuron import h
Section = h. Section
from numpy import *
from pylab import *

def initial():
    soma = h.Section()
    dend0 = h.Section()
    dend1 = h.Section()

    soma.nseg = 1
    soma.diam = 18.8
    soma.L = 18.8
    soma.Ra = 123.0
    soma.insert('hh')
    soma.gnabar_hh=0.5
    soma.gl_hh = .0001666
    soma.el_hh = -60.0

    dend0.nseg = 10
    dend0.diam = 3.18
    dend0.L = 701.9
    dend0.Ra = 123
    dend0.insert('pas')
    dend0.g_pas = .0001666
    dend0.e_pas = -60.0

    dend1.nseg = 5
    dend1.diam = 2.0
    dend1.L = 549.1
    dend1.Ra = 123
    dend1.insert('pas')
    dend1.g_pas = .0001666
    dend1.e_pas = -60.0

    #Connect things together
    dend0.connect(soma, 0, 0)
    dend1.connect(soma, 1, 0)
    
    data = [soma, dend0, dend1]
    return data

nSthcells = 3
neurons = []

for i in range(0, nSthcells):
    neurons.append(initial())

stim = h.IClamp(0.5, neurons[0][0])
stim.delay = 100
stim.dur = 300
stim.amp = 0.1
tstop = 300

#Create a synapse in the pre-synaptic section
syn = h.ExpSyn(0.5, sec=neurons[1][0])

#Connect the two neurons
nc = h.NetCon(neurons[0][0](0.5)._ref_v, syn)
nc.weight[0] = 2.0

vec = {}
for var in 'v_pre ', 'v_post ', 'i_syn ', 't ':
    vec [ var ] = h. Vector ()

#Record potentials! Remember, each entry in neurons is a 3d-list object, which contains one soma, and 2 dendrites..

# record the membrane potentials and
# synaptic currents
vec [ 'v_pre ']. record (neurons[0][0](0.5). _ref_v )
vec [ 'v_post ']. record ( neurons[1][0](0.5)._ref_v )
vec [ 'i_syn ']. record ( syn ._ref_i )
vec [ 't ']. record (h._ref_t )

# run the simulation
h.load_file("stdrun.hoc")
h.init()
h.tstop = 1000.0
h.run()

#plot!

subplot (2 ,1 ,1)
plot ( vec [ 't '] , vec [ 'v_pre '] ,
vec [ 't '] , vec [ 'v_post '])
subplot (2 ,1 ,2)
plot ( vec [ 't '] , vec [ 'i_syn '])

show()
