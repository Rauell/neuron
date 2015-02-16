from neuron import *
from neuron import h as nrn
from numpy import *
from pylab import *

soma = h.Section()
soma.L = 25
soma.insert('hh')
soma.nseg = 10

soma1 = h.Section()
soma1.L = 25
soma1.insert('hh')
soma1.nseg = 10

stimNc = h.NetStim()	
stimNc.noise = 1		
stimNc.start = 5		
stimNc.number = 1
stimNc.interval = 20
syn = h.ExpSyn (0.5, sec = soma)		
nc = h.NetCon(stimNc, syn)
nc.weight[0] = 1
nc.record()

# Test NC
syn1 = h.ExpSyn (0.5, sec = soma1)
soma.push()
nc1 = h.NetCon( soma(0.5)._ref_v, syn1 )
nc1.delay = 10
nc1.weight[0] = -0.01
nc1.threshold = 10


# record 
vec = {}
for var in 'v_1 ', 'v_2 ', 't ':
    vec[var] = h.Vector()
vec['v_1 '].record(soma(0.5)._ref_v)
vec['v_2 '].record(soma1(0.5)._ref_v)
vec ['t '].record(h._ref_t)

# run the simulation
h.load_file("stdrun.hoc")
h.init()
h.tstop = 50.0
h.run()

# plot the results
figure()
plot(vec['t '],vec['v_1 '], vec['t '], vec['v_2 '])
show()
h.topology()

a = min(vec['v_2 '])
print a+65
