"""
Stimulus.py

A container class that represents a set of stimulations
to the neural simulation.

Michael Royster
Drexel University
June 8, 2015
"""

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
		# Assigning Stimulation values
		self.ID = ID
		self.interval = self.INT_DEF if interval is None else interval
		self.t_start = self.T_START_DEF if t_start is None else t_start
		self.t_end = self.T_END_DEF if t_end is None else t_end
		self.noise = self.NOISE_DEF if noise is None else noise
		self.weight = self.WEIGHT_DEF if weight is None else weight

		# Ensuring that noise is within the proper range
		if self.noise < 0:
			self.noise = 0
		elif self.noise > 1:
			self.noise = 1
		return