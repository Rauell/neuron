# generate the data.
from numpy import *
import scipy
x = (arange(50.0)-25)/2.0
y = (arange(50.0)-25)/2.0
r = sqrt(x**2+y**2)
z = x*5.0*sin(x)  # Bessel function of order 0
# now dump the data to a VTK file.
import pyvtk
# Flatten the 2D array data as per VTK's requirements.
z1 = reshape(transpose(z), (-1,))
point_data = pyvtk.PointData(pyvtk.Scalars(z1))
grid = pyvtk.StructuredPoints((50,50, 1), (-12.5, -12.5, 0), (0.5, 0.5, 1))
data = pyvtk.VtkData(grid, point_data)
data.tofile('/tmp/test.vtk')
