
"""
vecCurrent = h.Vector()
vecCurrent.record(stim._ref_i)
time = h.Vector()
time.record(h._ref_t)
listOfSines = []
listOfTimes = []

for i in range(0,1000):
	t = i/1000.
	freq = 5
	pie = 2*3.14
	#listOfSines.append(stimStrength*sin(freq*pie*t)+stimStrength)
	listOfSines.append(stimStrength)
	listOfTimes.append(i)
VecT = h.Vector(listOfTimes)
VecStim = h.Vector(listOfSines)
VecStim.play(stim._ref_amp, VecT, 1)
"""
