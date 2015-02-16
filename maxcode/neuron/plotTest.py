from neuron import *
from nrn import *
from itertools import chain
from neuron import h
Section = h. Section
from numpy import *
from pylab import *

# create pre - and post - synaptic sections
pre = h.Section()
h.pt3dadd(3,3,3,3,sec=pre)
h.pt3dadd(3,40,4,3,sec=pre)
post = h.Section()
h.pt3dadd(0,0,5,3,sec=post)
h.pt3dadd(5,0,5,3,sec=post)
h.pt3dadd(5,50,5,3,sec=post)
for sec in pre, post :
    sec.insert('hh')
# inject current in the pre - synaptic section
stim = h.IClamp(0.5, sec = pre )
stim.amp = 10.0
stim.delay = 5.0
stim.dur = 5.0
# create a synapse in the pre - synaptic section
syn = h.ExpSyn (0.5, sec = post )
# connect the pre - synaptic section to the
# synapse object
nc = h.NetCon (pre(0.5)._ref_v, syn )
nc.weight[0] = 2.0

vec = {}
for var in 'v_pre ', 'v_post ', 't ':
    vec[var] = h.Vector()

# record the membrane potentials and
# synaptic currents
vec['v_pre '].record(pre(0.5)._ref_v)
vec ['v_post '].record(post(0.5)._ref_v)
vec ['i_syn '].record(syn._ref_i)
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
