import numpy as np
import matplotlib.pyplot as plt

_t = None
_raw_f = None
_raster_f = None


def clear():
	global _t, _raw_f, _raster_f
	_t = None
	_raw_f = None
	_raster_f = None

def load_raw(file):
	global _raw_f, _t 
	_raw_f = file
	_t = np.loadtxt(_raw_f, usecols=[0])
	return _t

def load_raster(file, t=None):
	global _raster_f, _t
	_raster_f = file

def plot_pot(ID, auto_configure=True):
	
	x = np.loadtxt(_raw_f, usecols=[ID])
	ret = plt.plot(_t, x)
	if auto_configure:
		plt.xlabel('Time (ms)')
		plt.ylabel('Potential (mV)')
		plt.title('Neuron %d' % ID)
	return ret



class NeuShow:
	def __init__(self, raw_file):
		self.__f_raw = raw_file
		self.__t = np.loadtxt(raw_file, usecols=[0])

	def Show(self, ID):
		x = np.loadtxt(self.__f_raw, usecols=[ID])
		plt.plot(self.__t, x)
		plt.xlabel('Time (ms)')
		plt.ylabel('Potential (mV)')
		plt.title('Neuron %d' % ID)
