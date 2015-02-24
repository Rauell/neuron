"""
template.py

The following is a template script to run the neuron simulation.
The only thing that needs to be modified are the addition of
stimuli to make this fully functional.

Michael Royster
Drexel University
February 24, 2015
"""


'''
# The input file is of the form below

# The order in which the inputs are given
# does not matter.

# COMMENTs ARE INSERTED WITH '#'

# Whitespace is fine, but the variable names
# cannot change (aka, 'sim_time')


## Mandatory input files ##
sim_time		total simulation time
conn_file		file containing connectivity matrix
dist_file		file containing neuron distances
net_con_file	file containing network constants

## Optional input files ##
col_file		file containing column ids
pos_file		file containing neuron positions
col_pos_file	file containing column ids and neuron positions

## Output files ##
raw_file		file to overwrite with raw sim data
raster_file		file to overwrite with raswer sim data
'''


# Import appropriate packages
import time
import sys
import nsim
import nfind
import numpy


# Returns a dictionary in the given format
def ReadInputFile(file):
	# Prepping variables
	fin = open(file, 'r')
	ret = {}

	# Looping over contents in file
	for line in fin.readlines():
		vals = line.split()
		# Checking for correct format
		if len(vals) != 2:
			continue
		# Checking for comments
		if vals[0][0] == '#':
			continue
		# Storing values in dictionary for easy access
		ret[vals[0]] = vals[1]

	# Cleaning up
	fin.close()
	return ret

	
'''
**********************************************
                  Main Method
**********************************************
'''


#Acquiring input file
if len(sys.argv) < 2:
	print "Error! Syntax is [script] <input file>"
	exit()



#Initialzation Begin
#######################################################

#Allocating used variables
neur_L = None
neur_pos = None
neur_col = None
neur_conn = None
neur_dist = None
raw_out_file = None
raster_out_file = None


#Reading inputs
inputs = ReadInputFile(sys.argv[1])

#Reading in simulation time
sim_time = int(inputs['sim_time'])


#Reading in network constants
fin = open(inputs['net_con_file'], 'r')
lines = fin.readlines()
fin.close()

num_neurons = int(lines[0])
index_inhib = int(lines[1])
if 3 <= len(lines): #Accounting for variability in file format
	L = int(lines[2])


#Reading in neuron topology files 
neur_dist = numpy.loadtxt(inputs['dist_file'], delimiter=',')
neur_conn = numpy.loadtxt(inputs['conn_file'], delimiter=',')


#Reading in optional topology files
if 'col_pos_file' in inputs:
	neur_col = numpy.loadtxt(inputs['col_pos_file'], usecols=[0], dtype='int')
	nuer_pos = numpy.loadtxt(inputs['col_pos_file'], usecols=[1,2,3])
else:
	if 'col_file' in inputs:
		neur_col = numpy.loadtxt(inputs['col_pos_file'], usecols=[0], dtype='int')
	if 'pos_file' in inputs:
		nuer_pos = numpy.loadtxt(inputs['pos_file'], usecols=[0,1,2])

#Reading in output files
if 'raw_file' in inputs:
 	raw_out_file = inputs['raw_file']
if 'raster_file' in inputs:
	raster_out_file = inputs['raster_file']
#######################################################
#Initialzation End




#Ending Double-Checking
#######################################################
if raw_out_file is None and raster_out_file is None:
	print "\nWARNING! No ouptut file specfied. No data will be recorded"
	answer = raw_input("Continue anyway? (y/n): ")

	if len(answer) == 0 or answer.lower()[0] != 'y':
		print "Terminating Program"
		exit()
	else:
		print "Continuing with program"

#######################################################
#Ending Double-Checking



#Runnning Simulation
#######################################################

#Time simulation setup and runtime
start_time = time.time()

#Convention is that neuron id's range from 1, 2, 3, ..., N-1, N
Simulation = nsim.NeuSim(num_neurons, neur_dist, neur_conn, sim_time, index_inhib)

''' INSERT NEW CODE HERE '''
#Creating stimulations


''' EXAMPLES '''
#Simulation.AddStim()
#Simulation.AddStim(neuron_id=3, interval=25, t_start=0, t_end=sim_time, noise = 0)

#corner = nfind.Rect(neur_pos, L=L, x=[0,0.25], y=[0,0.25], z=[0,0.25])
#Stimulation.AddStim(corner, interval=100, t_start=200)

# WARNING: Possible changes to sphere in the future
#center_ID = 32
#radius = 40
#sphere = nfind.Sphere(neur_dists, center_ID, radius, inner_radius=5)
#Stimulation.AddStim(sphere, interval=65, noise=0)


#Running simulation
vec = Simulation.Run(raster_out_file, raw_out_file)

# Displaying information
print "Entire simulation took %f seconds" % (time.time() - start_time)

#######################################################
#Ending Simulation
