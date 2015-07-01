NEURON {
	POINT_PROCESS gapc
	NONSPECIFIC_CURRENT i
	RANGE g, i
	POINTER vgap
}
PARAMETER {
	v (millivolt)
	vgap (millivolt)
	g = 0 (microsiemens)
}
ASSIGNED {
	i (nanoamp)
}
BREAKPOINT {
	i = (v - vgap)*g
}

