import copy

class Data:
	def __init__(self, num):
		self.init(num)

	def init(self, num):
		self.N = num
		self.t = None 
		self.V = [None]*num
		self.train = [None]*num
	
	def copy(self):
		return copy.deepcopy(self)

	def __str__(self):
		temp = "N:\t%d" % self.N
		temp = temp + "Times:\n" + str(self.t)
		temp = temp + "Membrane Potentials:\n" + str(self.V)
		return temp + "Spike Trains:\n" + str(self.trains)
