from Scripts import non_rigid_registration as nrr
import trimesh as tm
from sklearn.neighbors import BallTree
import numpy as np

def get_score_for_ideal_points(points, ideal_points, IDEAL_HEIGHT):
	

	model,scene,after_tps = nrr.non_rigid_registration(points, ideal_points)

	print("Model: ", model)
	print("Scene: ", scene)
	print("after_tps: ", after_tps)

	distances_array = []

	ballTree = BallTree(after_tps)
	
	i = 0
	for point in ideal_points:
		ind = ballTree.query_radius(point, IDEAL_HEIGHT)
		if len(ind[0]) == 1:
			distances_array.append(np.linalg.norm(point - after_tps[ind[0][0]]))
		else:
			i += 1
			distances_array.append(1000)


	print("SCORE: ", np.mean(distances_array))

	return np.mean(distances_array)

mesh = tm.load_mesh("models/shape_cube.obj");
#mesh.apply_transform([[1,0,0,10],[0,1,0,10],[0,0,1,10],[0,0,0,1]])
#mesh.vertices = mesh.vertices + 5
mesh2 = tm.load_mesh("models/pyramid.obj");

get_score_for_ideal_points(mesh.vertices, mesh2.vertices , 5)
(mesh+mesh2).show()


