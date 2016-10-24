#from Scripts import non_rigid_registration as nrr
import trimesh as tm
#import vtk_visualizer

mesh = tm.load_mesh("D:/Repositories/ObjectMatching/Project/ObjectMatching/ObjectMatching/models/sphere.obj");
#mesh.apply_transform([[1,0,0,2],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
#mesh2 = tm.load_mesh("models/pyramid.obj");

mesh.show()
