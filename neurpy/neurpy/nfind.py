"""
nsim.py

This module implements useful functions to find neuron ID's.
Each function call returns the desired neurons and adds
the new set to a global copy. The global set can be plotted
in 3D and can be reset with the clear command.

This module follows the convention that neuron ID's range
from 1 to N.


Michael Royster
Drexel University
March 3, 2015 
"""
import numpy
import nset


# Module variables
_select = []
_center = []


############################# BEGIN FIND REGION #############################
# FUNCTION: Find neurons in Rectangle
# Returns a list of neuron ID's. Limits are given as percentages, of the
# form [low, high], inclusive.
# These boundaries are not periodic.
# If the length of the box is not specified, 
def Rect( pos, L=None, x=[0.0, 1.0], y=[0.0, 1.0], z=[0.0, 1.0], mark=True ):

	# Useful function variables
	xyz = [x, y, z]
	dim = [0, 1, 2]
	dist = numpy.amax(pos) if L is None else L
	lim = [[xyz[i][0]*dist, xyz[i][1]*dist] for i in dim ]

	# Finding if neurons are within the specified rectangle
	n_ID = []
	for i in range(len(pos)):
		include = True
		for j in dim:
			include = include and (lim[j][0]<=pos[i,j]) and (pos[i,j]<=lim[j][1])
		if include:
			n_ID.append(i+1)


	# Including selection in module list
	if mark:		
		global _select
		_select = nset.unique(_select + n_ID)

	# Returning selected neurons
	return n_ID



# FUNCTION: Find neurons in sphere
# Returns a list of neuron ID's, centered on a specific neuron. 
# The sphere can be converted to a shell by defining the inner_radius
def Sphere( dists, center, radius, inner_radius=0, mark=True):

	# Prepping function varaiables
	c = center-1
	a = inner_radius
	b = radius

	# Creating nueron id list
	n_ID = []
	for i in range(len(dists)):
		r = dists[i,c]
		if a <= r and r < b:
			n_ID.append(i+1)

	# Including selection in module list
	if mark:		
		global _select, _center
		_select = nset.unique(_select + n_ID)
		_center.append(center)

	# Returning selected neurons
	return n_ID



# FUNCTION: Find neurons in columns
# Returns a list of neuron ID's in the specfied columns
def Column( col_list, IDs, mark=True ):

	# Prepping input variables
	if type(IDs) is not list:
		IDs = [IDs]
	cols = numpy.array(col_list)
	n_ID = []

	# Creating nueron id list
	for id in IDs:
		temp = list(numpy.where(cols==id)[0]+1)
		n_ID = n_ID + temp

	# Including selection in module list
	if mark:		
		global _select
		_select = nset.unique(_select + n_ID)

	# Returning selected neurons
	return n_ID



# FUNCTION: Find intersticial neurons
# Returns a list intersticial neuron ID's
def Intersticial(col_list, mark=True ):
	return Column(col_list, -1, mark)

############################# END FIND REGION #############################

def Clear():
	global _select, _center
	_select = []
	_center = []

def Plot(pos, mark_center=True, show=True):
	global _select, _center


	# Loading necessary plotting modules
	try:
		import matplotlib.pyplot
		from mpl_toolkits.mplot3d import Axes3D
	except RuntimeError as e:
		print "RuntimeError importing matplotlib.pyplot: ", e
		print "Leaving nfind.Plot"
		return
	

	# Prepping variables	
	c = list(_center)
	norm = list(_select) 
	unselect = nset.subtract(range(1,len(pos)+1), _select)

	# Prepping figure
	fig = matplotlib.pyplot.figure()
	ax = fig.add_subplot(111, projection='3d')

	# Plotting the center of a shell
	if mark_center and len(c) != 0:
		
		# Finding coordinates
		i = numpy.array(c)-1
		r = pos[i,:]

		# Plotting points
		ax.scatter(r[:,0], r[:,1], r[:,2], color='g', marker='*', s=60)

		# Removing from other lists
		for j in range(len(c)):
			if c[j] in norm:
				norm.remove(c[j])
			elif c[j] in unselect:
				unselect.remove(c[j])

	# Plotting selected neurons
	if len(norm) != 0:

		# Finding coordinates
		i = numpy.array(norm)-1
		r = pos[i,:]

		# Plotting points
		ax.scatter(r[:,0], r[:,1], r[:,2], color='b', s=10)

	# Plotting unselected neurons
	if len(unselect) != 0:
		# Finding coordinates
		i = numpy.array(unselect)-1
		r = pos[i,:]

		# Plotting points
		ax.scatter(r[:,0], r[:,1], r[:,2], color='0.75', s=5)

	# Updating axis labels
	ax.set_xlabel('$x$ $(\mu m)$')
	ax.set_ylabel('$y$ $(\mu m)$')
	ax.set_zlabel('$z$ $(\mu m)$')

	# Showing plot if desired
	if show:
		matplotlib.pyplot.show()

	return ax
