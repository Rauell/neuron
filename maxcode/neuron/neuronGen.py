from neuron import *
from neuron import h
from numpy import *

#My attempt here is to make a generic neuron class - one that initializes a soma with N dendrites

class neuronGen:

    def _init_(self, soma = object, dend1 = object, dend2 = object, axon = object, syn1 = object, syn2 = object, syn3 = object, syn4 = object):
        self.soma = soma
        self.dend1 = dend1
        self.dend2 = dend2
        self.axon = axon
        self.syn1 = syn1
        self.syn2 = syn2
        self.syn3 = syn3
        self.syn4 = syn4

    def construct(self):
        #Create soma and two dendrites
        self.soma = h.Section()
        #Set soma parameters
        self.soma.nseg = 1
        self.soma.diam = 18.8
        self.soma.L = 18.8
        self.soma.Ra = 123.0
        self.soma.insert('hh')
        self.soma.gnabar_hh=0.25
        self.soma.gl_hh = .0001666
        self.soma.el_hh = -60.0
        #Create dendrite model
        self.dend1 = h.Section()
        self.dend1.nseg = 5
        self.dend1.diam = 3.18
        self.dend1.L = 701.9
        self.dend1.Ra = 123
        self.dend1.insert('pas')
        self.dend1.g_pas = .0001666
        self.dend1.e_pas = -60.0
        #Create dendrite model
        self.dend2 = h.Section()
        self.dend2.nseg = 5
        self.dend2.diam = 2.0
        self.dend2.L = 549.1
        self.dend2.Ra = 123
        self.dend2.insert('pas')
        self.dend2.g_pas = .0001666
        self.dend2.e_pas = -60.0
        #Create axon model
        self.axon = h.Section()
        self.axon.nseg = 10
        self.axon.diam = 2
        self.axon.L = 5000
        self.axon.Ra = 10000
        self.axon.insert('pas')
        self.axon.g_pas = .0001666
        self.axon.e_pas = -60.0
        #Connect two dendrites to soma, as well as axon
        self.dend1.connect(self.soma,0,1)
        self.dend2.connect(self.soma,1,0)
        self.axon.connect(self.soma, 0.5, 0)
        #Add on our synapses! Two on each dendrite, and one on the axon, and one on the soma.
        self.syn1 = h.ExpSyn(0.5, sec=self.soma)
        self.syn2 = h.ExpSyn(0, sec=self.dend1)        
        self.syn3 = h.ExpSyn(1, sec=self.dend2)        
        self.syn4 = h.ExpSyn(1, sec=self.axon)
