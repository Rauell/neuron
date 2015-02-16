NEURON {
	POINT_PROCESS gapc1
	NONSPECIFIC_CURRENT i
	RANGE g, i
	POINTER vgap
}
PARAMETER {
	v (millivolt)
	vgap (millivolt)
	g = 0 (millisiemens)
}
ASSIGNED {
	i (nanoamp)
}
BREAKPOINT {
	i = (v - vgap)*g
}

