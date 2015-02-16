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

for seg in soma:	
	seg.hh.gnabar = 0.25
	seg.hh.gl = .0001666		
	seg.hh.el = -60.0

stimNc = h.NetStim()	
stimNc.noise = 1		
stimNc.start = 5		
stimNc.number = 50
stimNc.interval = 20
syn = h.ExpSyn (0.5, sec = soma)		
nc = h.NetCon(stimNc, syn)
nc.weight[0] = 0.5
nc.record()
#stimNc1 = h.NetStim()	
#stimNc1.noise = 1		
#stimNc1.start = 10		
#stimNc1.number = 5
#stimNc1.interval = 20
#syn1 = h.ExpSyn (0.5, sec = soma1)		
#nc1 = h.NetCon(stimNc1, syn1)
#nc1.weight[0] = 0.5
#nc1.record()
vec = {}
for var in 'v_1 ', 'v_2 ', 't ':
    vec[var] = h.Vector()

# record 
vec['v_1 '].record(soma(0.5)._ref_v)
vec['v_2 '].record(soma1(0.5)._ref_v)
vec ['t '].record(h._ref_t)

# run the simulation
h.load_file("stdrun.hoc")
h.init()
h.tstop = 200.0
h.run()

# plot the results
figure()
plot(vec['t '],vec['v_1 '], vec['t '], vec['v_2 '])
show()
h.topology()
