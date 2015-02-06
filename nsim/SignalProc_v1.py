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

#Load the various network information, electrical, and chemical synaptic connectivities.
print num_neurons
print index_inhib
print sim_time

Simulation = nsim.NeuSim(num_neurons, neur_dists, neur_conn, sim_time, index_inhib)
#Simulation.TEST_RUN(num_neurons, neur_dists, neur_conn, sim_time, index_inhib, out_file)
Simulation.Construct_Chem_Conn()
Simulation.Temp_Stim(30)
Simulation.Run(out_file)
#Simulation.Write_To_File(out_file)

print time.time() - start_time, "seconds"
#######################################################
#Ending Simulation
