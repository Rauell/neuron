"""
This is an example script to use the nsim.py module.
"""


# Import appropriate packages
import time
import sys
import nsim


	
'''
**********************************************
                  Main Method
**********************************************
'''

#Main program variables
neur_dists = []
neur_conn = []

#Acquiring input file
if len(sys.argv) < 2:
	print "Error! Syntax is SignalProc_v1.py <input file>"
	exit()

#Input File is of the given form:
'''
sim_time	total simulation time
out_file	file to be overwritten with output
dists_file	file containing neuron distances
conn_file	file containing connectivity matrix
net_con_file	file containing network constants
'''

#Initialzation Begin
#######################################################
#Reading inputs
fin = open(sys.argv[1], 'r') 
inputs = fin.readlines()

sim_time = int(inputs[0].split()[1])
out_file = inputs[1].split()[1]
dists_file = inputs[2].split()[1]
conn_file = inputs[3].split()[1]
net_con_file = inputs[4].split()[1]
fin.close()


#Reading in network constants
fin = open(net_con_file, 'r')
inputs = fin.readlines()
num_neurons = int(inputs[0])
index_inhib = int(inputs[1])
fin.close()


#Reading in neuron distances
fin = open(dists_file, 'r')

for line in fin.readlines():
	y = [value for value in line.split()]
	neur_dists.append(y)
for i in range(num_neurons):
	neur_dists[i] = neur_dists[i][0].split(',')
	neur_dists[i] = [float(num_str) for num_str in neur_dists[i]]

fin.close()


#Reading in connectivity matrix
fin = open(conn_file, 'r')

for line in fin.readlines():
	y = [value for value in line.split()]
	neur_conn.append(y)
for i in range(num_neurons):
	neur_conn[i] = neur_conn[i][0].split(',')
	neur_conn[i] = [int(num_str) for num_str in neur_conn[i]]

fin.close()
#######################################################
#Initialzation End


#Runnning Simulation
#######################################################

#Time it and set simulation parameters.
start_time = time.time()

dist = [[0, 100],[100, 0]]
conns = [[0, 1],[1, 0]]

Simulation = nsim.NeuSim(2, dist, conns, 1000, 999)
#Simulation = nsim.NeuSim(num_neurons, neur_dists, neur_conn, sim_time, index_inhib)
#Simulation.Set_Chem_Conn_Weights(0.5, 0.2, -0.05, -0.1, 155.0, 150.0, 300.0)
Simulation.Construct_Chem_Conn()

#Convention is that neuron id's range from 1, 2, 3, ..., N-1, N


start = 593
interval = 25
Simulation.Stim.Add(neuron_id = 1, interval=200, noise=0)
Simulation.Stim.Add(neuron_id = 1, interval=25, noise=0, t_start=225, t_end=350)
Simulation.Stim.Add(neuron_id = 1, interval=25, noise=0, t_start=start, t_end=start+interval)
Simulation.Stim.Add(neuron_id = 2, interval=200, noise=0, t_start=100)
#Simulation.Stim_List(interval=60, noise=0)
#Simulation.Stim_Random(60, t_start = 350, t_end = 700, noise = 0)

#Simulation.Stim_Set(nsim.Stimulus(0, interval=100, t_start=50, t_end = 650, noise=0, weight=3))
#Simulation.Stim_Set(nsim.Stimulus(1, interval=100, t_start=475, t_end = 675, noise=0))
#Simulation.Stim_Random(50, t_start = 10, noise = 0.5)
#Simulation.Run(out_file)
vec = Simulation.Run(raster_file=out_file, raster_format="%d\n%f\n")
print time.time() - start_time, "seconds"


import matplotlib
import matplotlib.pyplot as plt
for i in range(len(vec)-1):
	plt.figure()
	plt.plot(vec['t '], vec[str(i+1)])
	plt.xlim([0, sim_time])
	plt.xlabel('Time (ms)')
	plt.ylabel('Membrane Potential (mV)')
	plt.title('Neuron %d' % (i+1))
plt.show()


#######################################################
#Ending Simulation
