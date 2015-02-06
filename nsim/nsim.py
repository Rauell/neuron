"""
nsim.py

Version 0.01
02/04/15

This module implements the basic procedures and operations necessary to run the a 
NEURON firing simulation with a given connectivity scheme. Both chemical connections
and gap junctions are available for connectivity. The defualt values were taken from
Max Henderson's 'microcolumnSim_v5.py' code. 

Order of operations:
 	Instantiate
	Initialize (if necessary)
	Set Conncetions
	Set Stimuli
	Run (Saves results)

Michael Royster
Drexel University
February 5, 2015

Next time, on nsim.py...
Create stimulation functions

"""

# Importing modules
from neuron import *
from neuron import h as _h
from nrn import *

#To delete a list:
#	del list[:]

class NeuSim:

	# neuron_id is a list of nueron ID's. Specifiying this list will make it set only the neurons specified 
	def Stim_Random(self, interval=35, num_neuron=-1, neuron_id=[]):
		if len(neuron_id) == 0:
			pass

	# TEMPORARY FUNCTION!
	def Temp_Stim(self, interval):
		for i in range(self.__num):
			stim_nc = self.__h.NetStim()
			stim_nc.noise = 1
			stim_nc.start = 0
			stim_nc.number = self.__time / interval
			stim_nc.interval = interval
			
			syn = self.__h.ExpSyn(0.5, sec = self.__neurons[i].soma[0])
			nc = self.__h.NetCon(stim_nc, syn)
			nc.weight[0] = 1
	
			t_vec = self.__h.Vector()
			id_vec = self.__h.Vector()
			nc.record(t_vec, id_vec)
			self.__stims.append([stim_nc, syn, nc, t_vec, id_vec])
		return 


######################### BEGIN INITIALIZATION REGION ###########################

# FUNCTION: Constructor
# Constructor that loads hoc files, and calls necessary intializations, sans connections	
	def __init__(self, neur_num, neur_dists, neur_conn, sim_time, index_inhib):
		
		# Instantiating lists
		self.__stims = []
		self.__neurons = []
		self.__SYN = []
		self.__NC = []
		self.__stims = []

		# Creating access to hoc interface
		self.__h = _h
		self.__h.load_file("stdrun.hoc")

		# Load file to make model regular spiking excitory cells.
		self.__h.load_file ("sPY_template")
	
		# Load file to make model fast spiking inhibitory cells.
		self.__h.load_file ("sIN_template")
	
		# Initializing variables		
		
		self.Initialize(neur_num, neur_dists, neur_conn, sim_time, index_inhib)
		# Defualt chemical connection weights taken from M. Henderson's 'microcolumnSim_v5py'
		self.Set_Chem_Conn_Weights(0.05, 0.2, -0.05, -0.1, 155.0, 150.0, 300.0)
		return
	



# FUNCTION: Initialize Simulation Variables
# Initialization function for neuron geometry & inhibition network
	def Initialize(self, neur_num, neur_dists, neur_conn, sim_time, index_inhib):
		self.__num = neur_num
		self.__dists = neur_dists
		self.__conn = neur_conn
		self.__time = sim_time
		self.__inhib = index_inhib
	
		#Create neurons in the networks.
		numSegs = 3
		del self.__neurons[:]
		for i in range(0, self.__num):
			if i < self.__inhib:
				neuron = self.__h.sPY()
				self.__neurons.append(neuron)
			else:
				neuron = self.__h.sIN()
				self.__neurons.append(neuron)
				
		# Deleting current stimulations and connections since the network is different
		del self.__stims[:]
		del self.__SYN[:]
		del self.__NC[:]
		return	




# FUNCTION: Set Chemical Connection Weights
# Mutator function to change the weights used with chemical connections	
	def Set_Chem_Conn_Weights(self, EE, EI, IE, II, long_cutoff, delay_short_range, delay_long_range):
		self.__EE = EE 
		self.__EI = EI 
		self.__IE = IE 
		self.__II = II 
		self.__lc = long_cutoff
		self.__de_s = delay_short_range 
		self.__de_l = delay_long_range
		return 
#$$$$$$$$$$$$$$$$$$$$$$$$$$ END INITIALIZATION REGION $$$$$$$$$$$$$$$$$$$$$$$$$$#










########################### BEGIN CONNECTION REGION ############################# 

# FUNCTION: Construct Chemical Connections
# Chemical connection code modifed from Max Henderson's 'microcolumn_v5.py'
	def Construct_Chem_Conn(self):
		# Function variables		
		del self.__SYN[:]
		del self.__NC[:]

		inhib = self.__inhib	
		num = self.__num
		d_short = 1.0/self.__de_s
		d_long = 1.0/self.__de_l	

		# Main connection loop
		for i in range(0, num):
	 		for j in range(0, num):
				# If there is a connection i -> j
				if self.__conn[i][j] > 0: 					

					# Creating & storing a synapse targeting the center of j
					syn = self.__h.ExpSyn (0.5, sec = self.__neurons[j].soma[0])
					self.__neurons[i].soma[0].push()
					
					# Creating a connection from the source, i
					nc = self.__h.NetCon( self.__neurons[i].soma[0](0.5)._ref_v, syn ) 
	
					
					#Determine weight from particular type of connection
					#######################################################
					s1 = 20
					s2 = 1					

					# This means the source is EXCITATORY					
					if i < inhib: 
						if j < inhib: #E -> E
							nc.weight[0] = self.__EE*s1
						else: #E -> I
							nc.weight[0] = self.__EI*s1
					
					# This means the source is INHIBITORY					
					else:   	
						if j < inhib: #I -> E
							nc.weight[0] = self.__IE*s2
						else: #I -> I
							nc.weight[0] = self.__II*s2
					#######################################################

					# Determine delay from intersomatic distance
					# For long range speed
					if float(self.__dists[i][j]) > self.__lc:	
						nc.delay  = self.__dists[i][j]*d_long
			
					# For short range speed
					else:				
						nc.delay  = self.__dists[i][j]*d_short
					self.__NC.append(nc)
					self.__SYN.append(syn)

		return





# FUNCTION: Construct Gap Junctions
# Gap junction code modifed from Max Henderson's 'microcolumn_v5.py'
	def Construct_Gap_Conn(self):
		gaps = []
		for i in range(0, numNeurons):
 			for j in range(0, numNeurons):
				if abs(float(connections[i][j])) > 0:
					gap_junction = h.gapc(1, sec=Neurons[i].soma[0])
					gap_junction.g = (1.0e-9)*float(connections[i][j])	
					h.setpointer(Neurons[j].soma[0](1)._ref_v, 'vgap', gap_junction)
					gaps.append(gap_junction)
		
		# Storing to avoid garbage collection
		self.__GAP = gaps
		return
#$$$$$$$$$$$$$$$$$$$$$$$$$$$ END CONNECTION REGION $$$$$$$$$$$$$$$$$$$$$$$$$$$$$# 






########################### BEGIN STIMULATION REGION ############################
	'''
	Code to Come
	'''
#$$$$$$$$$$$$$$$$$$$$$$$$$$$ END STIMULATION REGION $$$$$$$$$$$$$$$$$$$$$$$$$$$$#










################################# BEGIN RUN #####################################
	
# FUNCTION: Run
# The main method to run a simulation
	def Run(self, output_file):
		
		#Record appropriate number of potentials.
		vec = {}
		for var in range(0,self.__num):
				vec[str(var + 1)] = self.__h.Vector()
				vec[str(var + 1)].record(self.__neurons[var].soma[0](0.5)._ref_v)
		#Record time.
		vec['t '] = self.__h.Vector()
		vec['t '].record(self.__h._ref_t)
		

		# Running 
		self.__h.init()
		self.__h.tstop = self.__time
		self.__h.run()

		# Writing to file		
		f = open(output_file, 'wb')

		for j in range(0, self.__num):
			canFire = True
			var = str(j+1)
			for i in range(0,len(vec ['t '])):
				if (vec[var][i] > 0) & (canFire):
					f.write(var + "\n")
					f.write(str(vec['t '][i]) + "\n")
					canFire = False
				elif (vec[var][i] < 0):
					canFire = True
		f.close()
		return
		
		
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ END RUN $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#		
		


		
		
