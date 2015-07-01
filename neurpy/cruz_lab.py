import neurpy
import neurpy.nsim as nsim


def easy_parallize(f, sequence, num_proc=8, async=False):
	import multiprocessing as mp
	pool = mp.Pool(processes=num_proc)
	
	# f is given sequence. guaranteed to be in order
	result = []
	if async:
		result = pool.map_async(f, sequence)
		result = result.get()
	else:
		result = pool.map(f, sequence)
	cleaned = [x for x in result if not x is None]
	
	#cleaned = asarray(cleaned)
	# not optimal but safe
	pool.close()
	pool.join()
	return cleaned



def sim_random(top_dir, interval, sim_time=1000, binary_conn=True):
	import numpy as np

	# Reading network constants
	fin = open("%s/networkConstants.txt" % top_dir, 'r')
	lines = fin.readlines()

	# Reading length if available
	if 3 <= len(lines): 
		L = int(lines[2])
	fin.close()
	
	# Finding inhibitory index
	fin = open ("%s/ID.txt" % top_dir, 'r')
	lines = fin.readlines()


	sim = nsim.NEURON()
	sim.load("%s/D.txt", "%s/C.txt", sim_time, inhib)
	sim.construct_chem_conn(binary_conn = binary_conn)
	sim.run()
	sim.write_spike_trains_to_file("%s/spike.%d.dat" % (top_dir, interval)

	return sim



