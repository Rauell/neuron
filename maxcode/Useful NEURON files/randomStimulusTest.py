from neuron import *
from nrn import *
from itertools import chain
from neuron import h
from numpy import *
from pylab import *
import os

axon = Section()
axon.L = 3
axon.nseg = 3
axon.insert('hh')

VecAxon = h.Vector()
VecAxon.record(axon(0.5)._ref_v)
stim = h.IClamp(axon(0))
stim.dur = 20
vecCurrent = h.Vector()
vecCurrent.record(stim._ref_i)

time = h.Vector()
time.record(h._ref_t)
listOfSines = []
listOfTimes = []
for i in range(0,100):
	if random() > 0.95:
		listOfSines.append(1)
	else:
		listOfSines.append(0)
	listOfTimes.append(i)
VecT = h.Vector(listOfTimes)
VecStim = h.Vector(listOfSines)


#stim.amp = 1e9

VecStim.play(stim._ref_amp, VecT, 1)
#h.VecStim.play(stim.amp, h.VecT, 1)
#h.VecStim.play(stim, VecT, 1)

h.finitialize(-68)
run(10)


# plot the results
figure()
subplot(2,1,1)
plot(VecT,VecStim)
#print vecCurrent
subplot(2,1,2)
plot(time, VecAxon)
show()
