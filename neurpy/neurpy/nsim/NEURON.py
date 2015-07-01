"""
NEURON.py

This module implements the basic procedures and operations necessary to run the a 
NEURON firing simulation with a given connectivity scheme. Both chemical connections
and gap junctions are available for connectivity. The default values were taken from
Max Henderson's 'microcolumnSim_v5.py' code. 

Order of operations:
 	Instantiate
	Load Topology 
	Connect Neurons
	Add Artificial Stimulations
	Simulate

Michael Royster and Maxwell Henderson
Drexel University
June 24, 2015
"""

# Importing modules
import numpy
import time
import os
import error
from Stimulus import *
from Data import *


"""
Ideas:

Reload function:
	Only needs to put in part of the info, and the class restructures
Save or store:
	Stores the instance of the object to a file (pickle)
	Possible do this at nsim level?
"""





# Implements the interface to NEURON
class NEURON:
	#Default values for chemical connections
	#Taken from M. Henderson's 'microcolumnSim_v5.py'
	CHEM_EE_DEF = 0.05
	CHEM_EI_DEF = 0.2
	CHEM_IE_DEF = -0.05
	CHEM_II_DEF = -0.1
	CHEM_DIST_CUT_DEF = 155.0
	CHEM_DELAY_SHORT_DEF = 150.0
	CHEM_DELAY_LONG_DEF = 300.0

	# Placeholder for invalid SPIKY number
	SPIKE_TRAIN_BLANK = 0.0






	def __init__(self, stim_seed=None):
		"""
		Constuctor for the class

		Parameters
		----------
		stim_seed : int, optional, default: None
			The seed to be used in NEURON's random number generator.
			If unspecified, a combination of the current time and the
			process ID will be used to account for parallel simulations.
		"""
		
		# Instantiating lists
		self.__NC = []
		self.__GAP = []
		self.__SYN = []
		self.__stims = []
		self.__neurons = []

		# Instantiating all other variables
		self.__num = None
		self.__conn = None
		self.__time = None
		self.__dist = None
		self.__inhib = None
		self.__data = None


		
		# Changing directories to appease the Gods of Hoc
		cwd = os.getcwd()
		os.chdir(os.path.dirname(os.path.realpath(__file__))+"/bin")
		from neuron import h as _h

		# Creating access to hoc interface
		self.__h = _h
		self.__h.load_file("stdrun.hoc")

		# Load file to make model regular spiking excitory cells.
		self.__h.load_file("sPY_template")
	
		# Load file to make model fast spiking inhibitory cells.
		self.__h.load_file ("sIN_template")

		# Resetting working directory
		os.chdir(cwd)


		# Initializing random seed
		self.__stim_seed = int(time.time()*10 + 4000*os.getpid()) if stim_seed is None else stim_seed		
		self.__h.NetStim().seed(self.__stim_seed)

		# Initializing safety variables
		self.__has_been_loaded = False
		self.__has_been_conencted = False
		self.__has_artifical_stim = False

		return
	
	"""
	def load_from_txt(self, 
		dist_file, 
		conn_file, 
		num, 
		run_time, 
		index_inhib=None, 
		delimiter=","):

		
		Loads simulation data. Distances and connections are read from text files.

		Parameters
		----------
			
			dist_file 	(str):	File containing 3D distances between neurons.
			conn_file 	(str):	File containing connectivity matrix holding weights of connections. 
			num 		(int):	Number of nuerons for the simulation
			run_time 	(int):	Total time simulation is to run for
			index_inhib	(Optional[int]):	Index of the first inhibitory neuron (Clarification to follow)
			delimiter 	(Optional[str]):	Delimiter for parsing input files.

		Notes:
			The weights given by the connectivity matrix are only used if \"use_defaults=False\" is used
			when constructing chemical connections. Otherwise, they indicate the presence
			or lack of a connection.

			If index_inhib is left blank, then all neurons are considered excitatory.
		

		dist = numpy.loadtxt(dist_file, delimiter=delimiter)
		conn = numpy.loadtxt(conn_file, delimiter=delimiter)

		return self.load(dist, conn, num, run_time, index_inhib)
	"""

	def load(self, dist, conn, run_time, 
		index_inhib=None, delimiter=','):
		"""
		Loads simulation data.

		Parameters
		----------
		dist : array-like or string
			2D matrix (or file) containing neural distances.

		conn : array-like or string
			2D matrix (or file) containing neural connection weights. 

		run_time : integer
			Total time of simulation running time in milliseconds
		
		index_inhib : integer, optional, default: None
			Index of the first inhibitory neuron. 
			If None, then all neurons are excitatory
		
		Delimiter : string, optional, default: ','
			Delimiter for parsing input files.

		Notes
		-----
		The weights given by neur_conn are only used if \"use_defaults=False\" is used
		when constructing chemical connections. Otherwise, they indicate the presence
		or lack of a connection.

		Be careful if using MATLAB to provide index values. MATLAB counts from 1,2,...N 
		while Python counts from 0,1,...,N-1.
		"""

		# Reading topology
		if type(dist) is str:
			self.__dist = numpy.loadtxt(dist, delimiter=delimiter)
		else:
			self.__dist = numpy.array(dist)

		if type(conn) is str:
			self.__conn = numpy.loadtxt(conn, delimiter=delimiter)	
		else:
			self.__conn = numpy.array(conn)	


		# Creating neurons in the networks.
		del self.__neurons[:]
		self.__num = len(self.__dist)
		self.__neurons = [(self.__h.sPY() if i < self.__inhib else self.__h.sIN()) for i in range(self.__num)]


		# Setting variables
		self.__time = run_time
		self.__inhib = self.__num+1 if ((index_inhib is None) or (index_inhib < 0)) else index_inhib


		# Creating data containers
		self.__data = Data(0)
		self.__data.t = self.__h.Vector()
		self.__data.V = [self.__h.Vector() for i in range(self.__num)]

		# Setting data containers to record
		self.__data.t.record(self.__h._ref_t)
		for i in range(self.__num):
			self.__data.V[i].record(self.__neurons[i].soma[0](0.5)._ref_v)

		# Deleting current stimulations and connections since the network has changed
		del self.__stims[:]
		del self.__SYN[:]
		del self.__NC[:]
		del self.__GAP[:]

		# Modifying saftey flags
		self.__has_been_loaded = True	
		self.__has_been_conencted = False
		self.__has_artifical_stim =False

		return	


	def construct_chem_conn(self, **kwargs):
		"""
	    Creates chemical connections.


	    Example Function Calls
	    ----------------------
	    construct_chem_conn()
	    construct_chem_conn(dist="Dxy.txt", conn="C.txt", delimiter="\\t")
	    construct_chem_conn(binary_conn=True, EE=2.5, EI=1.5, IE=-0.15, II=-0.1)
	    construct_chem_conn(dshort=200, dlong=400, lcutoff=550)


	    Keyword Parameters
	    ------------------		    
	    dist : array-like or string, optional, default: None
	        2D matrix (or file) containing neural distances.
	        If specified, overrides the dist matrix from the load command.
	        
	    conn : array-like or string, optional, default: None 
	        2D matrix (or file) containing neural connections.
	        If specified, overrides the conn matrix from the load command.
	        
	    delimiter :	string, optional, default: \',\'
	    	Delimiter for parsing input files.

	    binary_conn : boolean, optional, default: False
	    	If true, the connectivity matrix indicates the presence of a connection
	    	(non-zero weight value) or the lack of a connection (zero weight value).
	    	The conenction weights are set by default or user specified weights
	    	(EE, EI, IE, II).	    	
	    
	    EE : float, optional, default: 0.05
	    	Excitatory-excitatory connection strength

	    EI : float, optional, default: 0.2
	    	Excitatory-inhibitory connection strength

	    IE : float, optional, default: -0.05
	    	Inhibitory-excitatory connection strength

	   	II : float, optional, default: -0.1
	    	Inhibitory-inhibitory connection strength

	    TO BE CHANGED
	    dshort: float, optional, default: 150
	    	Short-range delay speed for a signal (microns / ms ?)

	    dlong: float, optional, default: 300
	    	Long-range delay speed for a signal (microns / ms ?)

	    lcutoff: float, optional, default: 155
	    	Cutoff distance between short and long range (microns ?)
		"""
		# Cleaning relavent lists		
		del self.__SYN[:]
		del self.__NC[:]

		# Setting default values for function parameters
		dist = self.__dist;  conn = self.__conn; 
		delimiter = ','
		delay_short = self.CHEM_DELAY_SHORT_DEF 
		delay_long = self.CHEM_DELAY_LONG_DEF
		long_cutoff = self.CHEM_DIST_CUT_DEF
		EE = self.CHEM_EE_DEF
		EI = self.CHEM_EI_DEF
		IE = self.CHEM_IE_DEF
		II = self.CHEM_II_DEF
		use_binary_conn = False

		# Adjusting for keyword arguments
		for key, value in kwargs.items():
			k = key.lower()
			
			if k in ["dist", "distance", "distance_matrix"]:
				dist = value
			elif k in ["conn", "connection", "connection_matrix"]:
				conn = value
			elif k in ["delim", "delimter"]:
				delimiter = value
			elif k in ["binary", "binary_conn", "use_binary","use_binary_conn", "use_binary_matrix"]:
				use_binary_conn = value
			elif k in ["ee"]:
				EE = value
			elif k in ["ei"]:
				EI = value
			elif k in ["ie"]:
				IE = value
			elif k in ["ii"]:
				II = value
			elif k in ["ds", "dshort", "delay_s", "delay_short"]:
				delay_short = value
			elif k in ["dl", "dlong", "delay_l", "delay_long"]:
				delay_long = value
			elif k in ["lc", "long_c", "lcutoff", "long_cutoff"]:
				long_cutoff = value
			else:
				print "Error. Option \'%s\' not found" % key
				return



		d_short = 1.0/delay_short
		d_long = 1.0/delay_long	

		# Prepping topology
		if type(dist) is str:
			dist = numpy.loadtxt(dist, delimiter=delimiter)

		if type(conn) is str:
			conn = numpy.loadtxt(conn, delimiter=delimiter)

		#counter=0

		# Main connection loop
		for i in range(0, self.__num):
	 		for j in range(0, self.__num):

				# If there is a connection i -> j
				if numpy.abs(conn[i][j]) > 1.0e-8: 					
					#counter = counter+1
					# Creating & storing a synapse targeting the center of j
					syn = self.__h.ExpSyn (0.5, sec = self.__neurons[j].soma[0])
					self.__neurons[i].soma[0].push()
					
					# Creating a connection from the source, i
					nc = self.__h.NetCon( self.__neurons[i].soma[0](0.5)._ref_v, syn ) 
	
					
					#Determine weight from particular type of connection
					#######################################################				
					# Weight determined from file
					if not use_binary_conn:
						nc.weight[0] = conn[i][j]

					# This means the source is EXCITATORY					
					elif i < self.__inhib: 
						if j < self.__inhib: #E -> E
							nc.weight[0] = EE
						else: #E -> I
							nc.weight[0] = EI
					
					# This means the source is INHIBITORY					
					else:   	
						if j < self.__inhib: #I -> E
							nc.weight[0] = IE
						else: #I -> I
							nc.weight[0] = II
					#######################################################

					# Determine delay from intersomatic distance
					# For long range speed
					if dist[i][j] > long_cutoff:	
						nc.delay  = dist[i][j]*d_long
			
					# For short range speed
					else:				
						nc.delay  = dist[i][j]*d_short
					self.__NC.append(nc)
					self.__SYN.append(syn)

		# Preparing accurate safety flags
		self.__has_been_conencted = True

		#print "Number of connections: %d" % counter
		return


	def construct_elec_conn(self):
		"""
		Creates electrical connections through gap junctions.

		Under development. Calling this will raise NotImplementedError.
		"""
		raise NotImplementedError("This function is not yet implemented")

		"""
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
		"""

	def add_stim(self, 
			neuron_id = None,
			interval = Stimulus.INT_DEF, 
			t_start = Stimulus.T_START_DEF, 
			t_end = Stimulus.T_END_DEF,
			noise = Stimulus.NOISE_DEF, 
			weight = Stimulus.WEIGHT_DEF):
		"""
		Adds artificual stimulation with the given properties to the specified
		neuron(s).

		The firing time between each stimulation uses intervals defined by
		(1-noise)*interval + negexp of mean duration noise*interval.
		http://www.neuron.yale.edu/neuron/static/docs/help/neuron/mech.html#NetStim

		Parameters
		----------
		neuron_id : int or list, optional, default: None
			The specified neuron(s) to receive the artificial stimulation.
			If None, all neurons are selected.

		interval : scalar, optional, default: 30
			The average firing rate of the aritifical stimulation in
			milliseconds. The exact firing time depends on the noise
			parameter. Negative values are ignored.

		t_start : scalar, optional, default: 0
			The mean starting time for the aritifical stimulation
			in milliseconds.

		t_end : scalar, optional, default: -1
			The mean ending time for the aritifical stimulation.
			If left at the default value, the stimulations will last for 
			the duration of the simulation.

		noise : float, optional, default: 1
			The fractional amount of randomness in the firing times.
			Bounded from 0 (no randomness) to 1 (pure Poisson distribution).

		weight : scalar, optional, default: 1
			The weight of the artificial stimulation. Positive values are
			excitatory while negative are inhibitory.
		""" 
		
		# Checking to see if all neurons are to be used					
		if neuron_id is None:
			neuron_id = range(self.__num)
		
		# Checking to see that the input is an int
		elif type(neuron_id) is int:
			neuron_id = [neuron_id]

		# Checking to see that the input is a list
		elif type(neuron_id) is not list:
			neuron_id = list(neuron_id)


		# Creating stimuli list
		stims = [Stimulus(ID, interval, t_start, t_end, noise, weight) for ID in neuron_id]
		self.add_stim_list(stims)
		return


	def add_stim_list(self, stimuli):
		"""
		Adds artificial stimulations to the simulation

		Parameters
		----------
		stimuli : Stimulus or list of Stimulus
			Each set of artificial stimulations is added into the simulation.
			No parameters have to be the same between these.
		"""

		# Error Handling
		if type(stimuli) is not list:
			stimuli = [stimuli]

		# Main loop
		for s in stimuli:
			#Configuring default options:
			if Stimulus.T_END_DEF == s.t_end:
				s.t_end = self.__time

			# Create network stimulation
			stim_nc = self.__h.NetStim()
			stim_nc.noise = s.noise
			stim_nc.start = s.t_start
			stim_nc.number = float((s.t_end - s.t_start)) / s.interval
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

		# Preparing accurate safety flags
		self.__has_artifical_stim = True

		return
	
	def run(self, **kwargs):
		"""
		Runs the simulation.

		If the simulation has not been properly configured (ie, loading
		topology files, connecting neurons, and adding aritifical
		stimulation), then IncompleteSimulationSetupError is raised.
		These checks can be ignored with the force_run parameter.

		Keyword Parameters
		------------------

		force_run : boolean, optional, default: False
			Causes the simulation to ignore all warnings generated from 
			safety checks.

		"""

		# Prepping default function arguments
		force_run = False
		loaded = self.__has_been_loaded
		connected = self.__has_been_conencted
		stimulated = self.__has_artifical_stim


		# Looping through keyword arguments
		for key, value in kwargs.items():
			k = key.lower()

			if k in ['force', 'force_run']:
				force_run = key[value]
			else:
				print "Error. Option \'%s\' not found" % key
				return



		# Checking safety flags
		if force_run or (stimulated and connected and loaded):

			# Running simulation
			self.__h.init()
			self.__h.tstop = self.__time
			self.__h.run()

			self.__data.train = self.calc_spike_train()
		else:

			msg = "Ignoring simulation run.\n"
			if not self.__has_been_loaded:
				msg = msg + "Topology information has not been loaded.\n"
			if not self.__has_been_conencted:
				msg = msg + "Connections have not been created.\n"
			if not self.__has_artifical_stim:
				msg = msg + "No artificial stimulation used.\n"


			raise error.IncompleteSimulationSetupError(msg)


		# Writing data to raster plot if desired
		#self.WriteRasterPlot(raster_file, rslt_vec, raster_delim, raster_use_tab)

		# Writing raw data file if desired
		#self.WriteRawData(raw_data_file, rslt_vec)

		# Writing spiky data file if desired
		#self.WriteSpikeData(spike_file, rslt_vec, raster_delim)



		return


	def calc_spike_train(self, threshold=10.0):
		"""
		Calculates the spike trains from the given data.

		If a neuron never fires, then its spike train will contain
		a single spike at t=0.

		Parameters
		----------
		threshold : scalar, optional, default: 10
			The threshold voltage a membrane potential must reach to signify
			the generation of an action potential.
			Defualt value taken from defualt for the NetCon class
			http://www.neuron.yale.edu/neuron/static/docs/help/neuron/neuron/classes/netcon.html

		Returns
		-------
		List containing the spike train for each neuron. Each spike train is
		a list of times.
		"""
		# Prep work
		train = [[] for i in range(self.__num)] 
		step_count = range(len(self.__data.t))

		# Looping over all neurons
		for j in range(len(self.__data.V)):
			
			# Setup for jth neuron
			canFire = True

			# Looping over every time
			for i in step_count:

				# If the potential is above the delimiter and first fire
				if (self.__data.V[j][i] > threshold) and (canFire):
					train[j].append(self.__data.t[i])					

					# Signifying the spike has been found
					canFire = False

				# The signal can spike again
				elif (self.__data.V[j][i] < threshold):
					canFire = True

			# Putting in dummy value if the neuron never fired
			if len(train[j]) == 0:
				train[j].append(NEURON.SPIKE_TRAIN_BLANK)
		return train
  
  
	def write_potentials_to_file(self, fname, **kwargs):
		"""
		Writes the potential for each neuron during each time step.
		
		The first column is the time steps. Each subsequent column is the 
		potential for the nth neuron at that time step.
		
		Parameters
		----------
		fname: string
		  The file to be generated with membrane potential data
		"""
		
		block = [self.__data.t] + self.__data.V
		trans = list(zip(*block))
		numpy.savetxt(fname, trans, fmt="%.4f")
		
		"""
		fout = open(fname, 'w')
		format = "%f\t"
		
		for i, t in enumerate(self.__data.t):
		  fout.write(format % t)
		  for j, V in eumerate(self.__data.V):
		    fout.write(format % 
		fout.close()
		return
		"""
		
	def write_spike_trains_to_file(self, fname, **kwargs):
	  """
	  Writes the current spike trains to file. 
	  
	  The spike train for the nth neuron is stored on the nth line.
	  The length of each line varies per neuron.
	  
	  Parameters
	  ----------
	  fname: string
	    The file to be generated with the spike train data
	  """
	  
	  fout = open(fname, 'w')
	  
	  for train in self.__data.train:
	    for t in train:
	      fout.write('%f\t' % t)
	    fout.write('\n')
	    
	  fout.close()
	  return 
	
	"""
	# FUNCTION: Write Raster Plot Data
	# Writes neuron id's and spike times to output file. 1 id is paried to one 
	# firing time. Spikes are recorded based on the threshold value
	def WriteRasterPlot(self, raster_file, data, threshold = 0, use_tab = False):
		# Checking all inputs
		if raster_file is None or data is None:
			return

		# Using format specified by user
		format = None
		if use_tab:
			format = "%d\t%f\n"
		else:
			format = "%d\n%f\n"


		# Opening output file		
		f = open(raster_file, 'w')

		# Looping over all neurons
		for j in range(0, self.__num):
			
			# Setup for jth neuron
			canFire = True
			jstr = str(j+1)

			# Looping over every time
			for i in range(0,len(data['t'])):
				# If the potneital is above the delimiter and first fire
				if (data[jstr][i] > threshold) & (canFire):
					# Writing data
					f.write(format % (j+1, data['t'][i]))
					
					# Signifying the spike has been found
					canFire = False
				elif (data[jstr][i] < threshold):
					# The signal can spike again
					canFire = True
		
		# Closing file
		f.close()
		return

	def WriteSpikeData(self, spike_file, data, threshold = 0):	
		# Checking all inputs
		if spike_file is None or data is None:
			return

		# Opening output file		
		f = open(spike_file, 'w')

		# Looping over all neurons
		for j in range(0, self.__num):
			# Checking if neuron ever fires
			ever_fire = False

			# Setup for jth neuron
			canFire = True
			jstr = str(j+1)

			# Looping over every time
			for i in range(0,len(data['t'])):
				# If the potneital is above the delimiter and first fire
				if (data[jstr][i] > threshold) & (canFire):
					# Writing data
					f.write("%f " % data['t'][i])
					
					# Signifying the spike has been found
					canFire = False

					# Maraking neuron as having fired
					ever_fire = True

				elif (data[jstr][i] < threshold):
					# The signal can spike again
					canFire = True

			# Ensuring that there is information on the line in case there was no firing
			if not ever_fire:
				f.write("%f " % self.SPIKY_BLANK_TRAIN)

			# Ending line
			f.write("\n")

		# Closing file
		f.close()
		return

	# FUNCTION: Write Raw Data
	# Writes a file with the first column listing the times and each other column
	# representing the neuron potential. Columns are ordered by neuron id. 
	def WriteRawData(self, data_file, data):
		# Checking all inputs
		if data_file is None or data is None:
			return

		# Opening output file
		f = open(data_file, 'w')

		# Looping over time
		for i in range(len(data['t'])):
			# Writing time
			f.write('%f' % data['t'][i])
			
			# Looping over neurons
			for j in range(0, self.__num):
				f.write('\t%f' % data[str(j+1)][i])
			f.write('\n')

		# Closing file
		f.close()
		return
	"""		
		
	@property
	def N(self):
		"""Gets the number of neurons"""
		return self.__num

	@property
	def sim_time(self):
		"""Gets the run time of the simulation"""
		return self.__time

	@property
	def conn(self):
		"""Gets the default connection matrix"""
		return self.__conn

	@property
	def dist(self):
		"""Gets the default distance matrix"""
		return self.__dist

	@property
	def inhib_index(self):
		"""Gets the inhibitory index"""
		return self.__inhib

	@property
	def rand_seed(self):
		"""Gets the seed used for the RNG"""
		return self.__stim_seed

	@property
	def data(self):
		"""
		Gets the data from the simulation

		Containers:
			data.t:		List of each time step in simulation
			data.V:		List of potentials for each neuron at each time step
			data.train 	List of spike trains for each neuron
		"""
		return self.__data

	@property
	def stims(self):
		"""
		Gets the stimulations used in the simulation
		
		Each entry is a tuple of the form:
		[stim_nc, syn, nc, t_vec, id_vec]
		More info on these to come.
		"""
		return self.__stims
