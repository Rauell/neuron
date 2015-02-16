import mayavi
v = mayavi.mayavi() # create a MayaVi window.
d = v.open_vtk('/tmp/test.vtk', config=0) # open the data file.
# The config option turns on/off showing a GUI control for the data/filter/module.
# load the filters.
f = v.load_filter('WarpScalar', config=0) 
n = v.load_filter('PolyDataNormals', 0)
n.fil.SetFeatureAngle (45) # configure the normals.
# Load the necessary modules.
m = v.load_module('SurfaceMap', 0)
a = v.load_module('Axes', 0)
a.axes.SetCornerOffset(0.0) # configure the axes module.
o = v.load_module('Outline', 0)
v.Render() # Re-render the scene.
