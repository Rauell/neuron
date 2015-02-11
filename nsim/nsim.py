"""
nsim.py

This module implements the basic procedures and operations necessary to run the a 
NEURON firing simulation with a given connectivity scheme. Both chemical connections
and gap junctions are available for connectivity. The defualt values were taken from
Max Henderson's 'microcolumnSim_v5.py' code. 

Order of operations:
 	Instantiate
	Initialize (if necessary)
	Set Conncetions
	Set Stimuli
	Run
	Save Results

Michael Royster
Drexel University
February 11, 2015
"""

# Importing modules
from neuron import *
from neuron import h as _h
from nrn import *

# Stimulus class
# This class contains a wrapper and defualts for a stimulus in the simulation
class Stimulus:
	# Defualt Values
	INT_DEF = 30
	T_START_DEF = 0
	T_END_DEF = -1
	NOISE_DEF = 1
	WEIGHT_DEF = 1  

	#Intialization function
	def __init__(self,
				ID, 
				interval = None, 
				t_start = None, 
				t_end = None, 
				noise = None, 
				weight = None):
		self.ID = ID
		self.interval = self.INT_DEF if interval is None else interval
		self.t_start = self.T_START_DEF if t_start is None else t_start
		self.t_end = self.T_END_DEF if t_end is None else t_end
		self.noise = self.NOISE_DEF if noise is None else noise
		self.weight = self.WEIGHT_DEF if weight is None else weight

		if self.noise < 0:
			self.noise = 0
		elif self.noise > 1:
			self.noise = 1
		return

# Main simulation class
class NeuSim:
########################## BEGIN CONSTANTS REGION ###############################
	#Default values for chemical connections
	#Taken from M. Henderson's 'microcolumnSim_v5.py'
	CHEM_EE_DEF = 0.05
	CHEM_EI_DEF = 0.2
	CHEM_IE_DEF = -0.05
	CHEM_II_DEF = -0.1
	CHEM_DIST_CUT_DEF = 155.0
	CHEM_DELAY_SHORT_DEF = 150.0
	CHEM_DELAY_LONG_DEF = 300.0
#$$$$$$$$$$$$$$$$$$$$$$$$$$$ END CONSTANTS REGION $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#








######################### BEGIN INITIALIZATION REGION ###########################

# FUNCTION: Constructor
# Constructor that loads hoc files, and calls necessary intializations, sans connections	
	def __init__(self, neur_num, neur_dists, neur_conn, sim_time, index_inhib):
		
		# Instantiating lists
		self.__stims = []
		self.__neurons = []
		self.__SYN = []
		self.__NC = []
		self.__GAP = []
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
		self.Set_Chem_Conn_Weights()
		return
	
# FUNCTION: Initialize Simulation Variables
# Initialization function for neuron geometry & inhibition network
	def Initialize(self, neur_num, neur_dists, neur_conn, sim_time, index_inhib):
		# Setting variables
		self.__num = neur_num
		self.__dists = neur_dists
		self.__conn = neur_conn
		self.__time = sim_time
		self.__inhib = index_inhib
	
		# Creating neurons in the networks.
		numSegs = 3
		del self.__neurons[:]
		for i in range(0, self.__num):
			# Creating standard excitory neurons
			if i < self.__inhib:
				neuron = self.__h.sPY()
				self.__neurons.append(neuron)
			# Creating inhibitory neurons
			else:
				neuron = self.__h.sIN()
				self.__neurons.append(neuron)
				
		# Deleting current stimulations and connections since the network has changed
		del self.__stims[:]
		del self.__SYN[:]
		del self.__NC[:]
		del self.__GAP[:]
		return	

# FUNCTION: Set Chemical Connection Weights
# Mutator function to change the weights used with chemical connections	
	def Set_Chem_Conn_Weights(self, 
							EE=None, 
							EI=None, 
							IE=None, 
							II=None, 
							long_cutoff=None, 
							delay_short_range=None, 
							delay_long_range=None):
		self.__EE = self.CHEM_EE_DEF if EE is None else EE 
		self.__EI = self.CHEM_EI_DEF if EI is None else EI
		self.__IE = self.CHEM_IE_DEF if IE is None else IE 
		self.__II = self.CHEM_II_DEF if II is None else II 
		self.__lc = self.CHEM_DIST_CUT_DEF if long_cutoff is None else long_cutoff
		self.__de_s = self.CHEM_DELAY_SHORT_DEF if delay_short_range is None else delay_short_range 
		self.__de_l = self.CHEM_DELAY_LONG_DEF if delay_long_range is None else delay_long_range

		return 
#$$$$$$$$$$$$$$$$$$$$$$$$$$ END INITIALIZATION REGION $$$$$$$$$$$$$$$$$$$$$$$$$$#










########################### BEGIN CONNECTION REGION ############################# 

# FUNCTION: Construct Chemical Connections
# Chemical connection code modifed from Max Henderson's 'microcolumn_v5.py'
	def Construct_Chem_Conn(self):
		# Cleaning relavent lists		
		del self.__SYN[:]
		del self.__NC[:]

		# Useful variables	
		d_short = 1.0/self.__de_s
		d_long = 1.0/self.__de_l	

		# Main connection loop
		for i in range(0, self.__num):
	 		for j in range(0, self.__num):
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
					if i < self.__inhib: 
						if j < self.__inhib: #E -> E
							nc.weight[0] = self.__EE*s1
						else: #E -> I
							nc.weight[0] = self.__EI*s1
					
					# This means the source is INHIBITORY					
					else:   	
						if j < self.__inhib: #I -> E
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
		# Cleaning relavent list
		del self.__GAP[:]

		for i in range(0, self.__num):
 			for j in range(0, self.__num):
				if self.__conn[i][j] > 0:
					gj = self.__h.gapc(1, sec=self.__neurons[i].soma[0])
					gj.g = (1.0e-9)*self.__conn[i][j]	

					self.__h.setpointer(self.__neurons[j].soma[0](1)._ref_v, 'vgap', gj)
					self.__GAP.append(gj)
		
		return
#$$$$$$$$$$$$$$$$$$$$$$$$$$$ END CONNECTION REGION $$$$$$$$$$$$$$$$$$$$$$$$$$$$$# 










########################### BEGIN STIMULATION REGION ############################
	# FUNCTION: Create a list of Stimuli
	# Creates a set of stimuli that fire together with the given parameters
	def Stim_List(self, 
				interval = Stimulus.INT_DEF, 
				neuron_id = None,
				noise = Stimulus.NOISE_DEF, 
				t_start = Stimulus.T_START_DEF, 
				t_end = Stimulus.T_END_DEF, 
				weight = Stimulus.WEIGHT_DEF):
		
		# Checking to see if all neurons are to be used					
		if neuron_id is None:
			neuron_id = range(self.__num)
		
		# Checking to see that the input is a list
		elif type(nueron_id) is not list:
			neuron_id = [neuron_id]

		# Creating stimuli list
		stims = [Stimulus(ID, interval, t_start, t_end, noise, weight) for ID in neuron_id]
		self.Stim_Set(stims)
	'''
	From the website: http://www.neuron.yale.edu/neuron/static/docs/help/neuron/neuron/mech.html#NetStim
	NETSTIM

	SYNTAX
	s = new NetStim(x)
	s.interval ms (mean) time between spikes
	s.number (average) number of spikes
	s.start ms (most likely) start time of first spike
	s.noise ---- range 0 to 1. Fractional randomness.
	0 deterministic, 1 intervals have negexp distribution.
	DESCRIPTION
	Generates a train of presynaptic stimuli. Can serve as the source for a NetCon. This NetStim can also be be triggered by an input event. i.e serve as the target of a NetCon. If the stimulator is in the on=0 state and receives a positive weight event, then the stimulator changes to the on=1 state and goes through its burst sequence before changing to the on=0 state. During that time it ignores any positive weight events. If, in the on=1 state, the stimulator receives a negative weight event, the stimulator will change to the off state. In the off state, it will ignore negative weight events. A change to the on state immediately causes the first spike.

	Fractional noise, 0 <= noise <= 1, means that an interval between spikes consists of a fixed interval of duration (1 - noise)*interval plus a negexp interval of mean duration noise*interval. Note that the most likely negexp interval has duration 0.

	Since NetStim sends events, the proper idiom for specifying it as a source for a NetCon is

	    objref ns, nc
	    nc = new NetStim(.5)
	    ns = new NetCon(nc, target...)

	That is, do not use &nc.y as the source for the netcon.

	See $NEURONHOME/src/nrnoc/netstim.mod
	BUGS
	Prior to version 5.2.1 an attempt was made to make the mean start time (noise > 0) correspond to the value of start. However since it is not possible to simulate events occurring at t < 0, these spikes were generated at t=0. Thus the mean start time was not start and the spikes at t=0 did not obey negexp statistics. For this reason, beginning with version 5.2.1 the semantics of start are the time of the most likely first spike and the mean start time is start + noise*interval. 

	'''
	# FUNCTION: Set Stimuli
	# This function adds a set of stimuli to the simulation
	def Stim_Set(self, stimuli):
		
		# Error Handeling
		if type(stimuli) is not list:
			stimuli = [stimuli]
		
		for s in stimuli:
			#Configuring defualt options:
			if Stimulus.T_END_DEF == s.t_end:
				s.t_end = self.__time

			# Create network stimulation
			stim_nc = self.__h.NetStim()
			stim_nc.noise = s.noise
			stim_nc.start = s.t_start
			stim_nc.number = (s.t_end - s.t_start) / s.interval
			stim_nc.interval = s.interval

			# Creating synapse
			syn = self.__h.ExpSyn(0.5, sec=self.__neurons[s.ID].soma[0])
			nc = self.__h.NetCon(stim_nc, syn)
			nc.weight[0] = s.weight

			# Adding the stimulus to the simulation
			t_vec = self.__h.Vector()
			id_vec = self.__h.Vector()
			nc.record(t_vec, id_vec)
			self.__stims.append([stim_nc, syn, nc, t_vec, id_vec])
#$$$$$$$$$$$$$$$$$$$$$$$$$$$ END STIMULATION REGION $$$$$$$$$$$$$$$$$$$$$$$$$$$$#










################################# BEGIN DATA REGION #############################
	


	def Run(self, raster_file=None, raw_data_file=None, raster_format="%d\n%f\n", raster_delim = 0):
		
		#Creating result vector
		rslt_vec = {}

		# Creating a potential vector for each neuron
		for i in range(0, self.__num):
			rslt_vec[str(i+1)] = self.__h.Vector()
			rslt_vec[str(i+1)].record(self.__neurons[i].soma[0](0.5)._ref_v)
		
		# Creating a time vector
		rslt_vec['t '] = self.__h.Vector()
		rslt_vec['t '].record(self.__h._ref_t)

		# Running simulation
		self.__h.init()
		self.__h.tstop = self.__time
		self.__h.run()

		# Writing data to raster plot if desired
		if raster_file is not None:
			self.WriteRasterPlot(raster_file, rslt_vec, raster_delim, raster_format)

		return rslt_vec

	def WriteRasterPlot(self, raster_file, data, fire_delim = 0, format="%d\n%f\n"):
		# Adjusting format to always end with one line
		if format[-1] != '\n':
			format = format + '\n'

		# Opening output file		
		f = open(raster_file, 'wb')

		# Looping over all neurons
		for j in range(0, self.__num):
			
			# Setup for jth neuron
			canFire = True
			jstr = str(j+1)

			# Looping over every time
			for i in range(0,len(data['t '])):
				# If the potneital is above the delimiter and first fire
				if (data[jstr][i] > fire_delim) & (canFire):
					# Writing data
					f.write(format % (j+1, data['t '][i]))
					
					# Signifying the spike has been found
					canFire = False
				elif (data[jstr][i] < fire_delim):
					# The signal can spike again
					canFire = True
		
		# Closing file
		f.close()
		return
		
		
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ END DATA REGION $$$$$$$$$$$$$$$$$$$$$$$$$$$$$#		
		


		
		
