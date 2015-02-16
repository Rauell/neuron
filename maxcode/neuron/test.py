from neuron import *
from nrn import *
from itertools import chain
from neuron import h
Section = h. Section
from numpy import *
from pylab import *

# topology
soma = Section()
apical = Section()
basilar = Section()
axon = Section()
apical.connect(soma , 1, 0)
basilar.connect(soma , 0, 0)
axon.connect(soma , 0, 0)

# geometry
soma.L = 30
soma.nseg = 1
soma.diam = 30
apical.L = 600
apical.nseg = 23
apical.diam = 1
basilar.L = 200
basilar.nseg = 5
basilar.diam = 2
axon.L = 1000
axon.nseg = 37
axon.diam = 1
# biophysics
for sec in h.allsec():
    sec.Ra = 100
    sec.cm = 1

soma.insert('hh')
apical.insert('pas')
basilar.insert('pas')

for seg in chain(apical, basilar):
    seg.pas.g = 0.0002
    seg.pas.e = -65

axon.insert('hh')

#synaptic input

syn = h.AlphaSynapse(0.5, sec=soma)
syn.onset = 0.5
syn.gmax = 0.05
syn.e = 0

g = h.Graph()
g.size(0,5,-80,40)
g.addvar('v(0.5)', sec=soma)

h.dt = 0.025
tstop = 5
v_init = -65

def initialize():
    h.finitialize(v_init)
    h.fcurrent()

def integrate():
    g.begin()
    while h.t < tstop:
        h.fadvance()
        g.plot(h.t)
    g.flush()

def go():
    initialize()
    integrate()

go()
show()
