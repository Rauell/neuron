
from NEURON import NEURON
from Stimulus import Stimulus

__all__ = ["NEURON", "Stimulus", "Data"]



def test(run_time, stim_int, quiet=False):
	
	fin = open("networkConstants.txt")
	inhib = float(fin.readlines()[1]) - 1
	fin.close()

	if quiet:
		import sys
		old_stdout = sys.stderr
		log = open("log.txt", 'w')
		sys.stderr = log

	
	sim = NEURON()
	sim.load("D.txt", "C.txt", run_time, inhib)
	sim.construct_chem_conn()
	sim.add_stim(interval=stim_int)
	sim.run()
	sim.write_spike_trains_to_file("test.dat")

	if quiet:
		sys.stderr=old_stdout
		log.close()
		

	return sim.data