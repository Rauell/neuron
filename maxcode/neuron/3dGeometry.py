from neuron import *
from nrn import *
from itertools import chain
from neuron import h
Section = h. Section
from numpy import *
from pylab import *

NDEND = 10
totalPoints = 0 

soma = h.Section()
h.pt3dadd(3,3,3,3,sec=soma)
h.pt3dadd(3,4,4,3,sec=soma)
dend1 = h.Section()
h.pt3dadd(0,2,5,3,sec=dend1)
h.pt3dadd(5,4,5,3,sec=dend1)
h.pt3dadd(5,5,5,3,sec=dend1)
totalPoints = totalPoints + h.n3d()
h.pop_section()
totalPoints = totalPoints + h.n3d()
dend1.connect(soma, 1, 0)
for sec in soma, dend1 :
    sec.insert('hh')
# inject current
stim = h.IClamp(0.5, sec = dend1 )
stim.amp = 5.0
stim.delay = 5.0
stim.dur = 5.0

vec = {}
for var in 'v_pre ', 'v_post ', 't ':
    vec[var] = h.Vector()

# record the membrane potentials and
# synaptic currents
vec['v_pre '].record(soma(0)._ref_v)
vec ['v_post '].record(dend1(1)._ref_v)
#vec ['i_syn '].record(syn._ref_i)
vec ['t '].record(h._ref_t)

# run the simulation
h.load_file("stdrun.hoc")
h.init()
h.tstop = 20.0
h.run()

# plot the results
figure()
subplot(2,1,1)
plot(vec['t '],vec['v_pre '],
vec['t '],vec['v_post '])
show()
