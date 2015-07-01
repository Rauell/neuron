import numpy as np
import matplotlib.pyplot as plt
import pyspike as spk

_t = None
_raw_f = None
_raster_f = None


def clear():
	global _t, _raw_f, _raster_f
	_t = None
	_raw_f = None
	_raster_f = None

def load_raw(f):
	global _raw_f, _t 
	_raw_f = f
	_t = np.loadtxt(_raw_f, usecols=[0])
	return _t

def raster_plot(file, show_plot=False):

	spike_trains = spk.load_spike_trains_from_txt(file)
	f = plt.figure()
	for (i, spikes) in enumerate(spike_trains):
		plt.plot(spikes, (i+1)*np.ones_like(spikes), 'b|')
	plt.xlabel("Time (ms)")
	plt.ylabel("Neuron ID")
	
	if show_plot:
		plt.show()

	return f

def load_raster(f, t=None):
	global _raster_f, _t
	_raster_f = f

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
