from Scripts import non_rigid_registration as nrr
import trimesh as tm
import meshpy
#import vtk_visualizer

mesh = tm.load_mesh("D:/bunny.obj");
mesh.apply_transform([[1,0,0,2],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
mesh2 = tm.load_mesh("D:/bunny.obj");



lm.vertices = [1, 1, 1]

#mesh3 = mesh + mesh2;
#mesh3.show();

#mesh.vertices.show()
#print(mesh.vertices)
#nrr.non_rigid_registration(mesh.vertices,mesh2.vertices#

#vtk_visualizer.plot3d.plotxyz(np.array(mesh2.vertices))