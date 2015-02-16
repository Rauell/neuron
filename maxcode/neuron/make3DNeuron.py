from neuron import *
from nrn import *
from itertools import chain
from neuron import h
Section = h. Section
from numpy import *
from pylab import *

#This program will test out the definition constructGeometry, which SHOULD take in the 3D points for the different sections of a neuron, create them, and connect the pieces

def constructGeometry( somaPos):
	soma = h.Section()
    	for i in range(0,2):
		h.pt3dadd(somaPos[i][0],somaPos[i][1],somaPos[i][2],somaPos[i][3],sec=soma)
	return soma

soma1 = [0,0,0,3]
soma2 = [0,2,0,3]
soma = [soma1,soma2]
Soma = constructGeometry(soma)




