"""
Simple network to test using PyNN.  Creates 2 neurons and tests.

Maxwell Philip Henderson
Drexel University
October 15th, 2014
"""

from pyNN.neuron import *
import numpy

p1 = Population(2, IF_curr_alpha, cellparams={'tau_m': 15.0, 'cm': 0.9}) # Create neural population of 2 neurons

p1.set({'tau_m':20, 'v_rest':-65}) # Set various parameters

view = p1[:1] # Select only first neuron

view.set('tau_m', 11.0) # Change parameter

p1.get('tau_m') # View parameters to validate the changes were correct

p1.initialize('v', -65.0) # Initialize

pulse = DCSource(amplitude=0.5, start=20.0, stop=80.0) # Inject stimulus
pulse.inject_into(p1[:1])
p1.inject(pulse)

p1.record() # Record for entire neural population

#connector = AllToAllConnector(weights=0.7)
#prj1_2e = Projection(p1, p1, connector)
#prj1_1.setDelays(0.6)

p1.printSpikes("spikefile.dat")

run(100)

end()


