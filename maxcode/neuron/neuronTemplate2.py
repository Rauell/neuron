from neuron import *
from nrn import *
from itertools import chain
from neuron import h
Section = h. Section
from numpy import *
from pylab import *

load_file ("netpcell.hoc")

pcx = new PCell()
pcy = new PCell()

pcy.soma stim = new IClamp (0.5)
stim.del = 100
stim.dur = 300
stim.amp = 0.1

tstop = 500
