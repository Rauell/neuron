"""
Code for testing how neurons respond in NEURON to synaptic connections of different distances
Max Henderson
Drexel University
Novemeber 15, 2012
"""

"""
Import appropriate packages
"""

from neuron import *
from nrn import *
from itertools import chain
from neuron import h
from numpy import *
from pylab import *
import random
import os

# Construct initial sections of neurons 1-4.
Soma1 = h.Section()
Soma2 = h.Section()
Soma3 = h.Section()
Soma4 = h.Section()
AD1 = h.Section()
AD2 = h.Section()
AD3 = h.Section()
AD4 = h.Section()
BD1 = h.Section()
BD2 = h.Section()
BD3 = h.Section()
BD4 = h.Section()
Axon1 = h.Section()
Axon2 = h.Section()
Axon3 = h.Section()
Axon4 = h.Section()

# Give these sections 

