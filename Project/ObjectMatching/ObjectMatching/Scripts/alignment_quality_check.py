# CHECKS IF ALL CAMERAS ARE ALIGNED IF THERE ARE SOME MISALIGNED CAMERAS
# Version 1.0.9.4

# Import packages/modules
import os
import glob
import time
import math
import sys
import traceback
import numpy as np
import PhotoScan

import mpl_toolkits.mplot3d as m3d
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

import scipy.optimize
import functools

import imp

#cloud compare libs
import configparser
import time
from math import cos,sin,log,exp,sqrt
from numpy import loadtxt,arange,array,dot,delete,reshape,kron,eye,ones,zeros,trace,s_,r_,c_,squeeze
from numpy.linalg import svd,qr,norm
from scipy.optimize import fmin_bfgs, fmin_l_bfgs_b

from sys import argv
from scipy import spatial
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch
from sklearn.metrics.pairwise import euclidean_distances
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch
from sklearn.neighbors import BallTree
from math import cos,sin,log,exp,sqrt
from numpy import loadtxt,arange,array,dot,delete,reshape,kron,eye,ones,zeros,trace,s_,r_,c_,squeeze
from numpy.linalg import svd,qr,norm
from scipy.optimize import fmin_bfgs, fmin_l_bfgs_b
from ctypes import *
import csv

import re
import PS124_alignment_quality as cca

def create_camearas_obj_file(chunk):
	obj_file = ""
	if chunk:
		if chunk.cameras:
			radius_distance = calculate_radius(chunk.cameras)
			if not os.path.exists(obj_directory):
				os.makedirs(obj_directory)
			obj_file = open(obj_directory+ chunk.label + ".obj", 'w')
			print(obj_file)
			for cam in chunk.cameras:
				if(cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None):
					#print("v {0} {1} {2} 1".format(cam.center[0],cam.center[1],cam.center[2]))
					obj_file.write("v {0} {1} {2} 1 #{3}\n".format(cam.center[0],cam.center[1],cam.center[2],chunk.label))
			obj_file.close()
	return obj_file, radius_distance


def calculate_radius(cameras):
	calc_distances = []
	if len(cameras) >= 49 and len(cameras) <= 54: #Dooblicator 1.0 54
		for cam_num in range(1,7):

			cam_3 = None
			cam_8 = None
			cam_4 = None
			cam_9 = None
			cam_7 = None
			cam_2 = None
			cam_6 = None
			cam_1 = None
			
			for cam in cameras:
				if re.search("^Pod\s*3\s*Camera\s*[1]?[0-9].*",cam.label, flags = re.IGNORECASE):#"Pod3Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_3 = cam
				elif re.search("^Pod\s*8\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod8Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_8 = cam
				elif re.search("^Pod\s*4\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod4Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_4 = cam
				elif re.search("^Pod\s*9\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod9Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_9 = cam
				elif re.search("^Pod\s*7\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod7Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_7 = cam
				elif re.search("^Pod\s*2\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod2Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_2 = cam
				elif re.search("^Pod\s*6\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod6Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_6 = cam
				elif re.search("^Pod\s*1\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod1Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_1 = cam

				if cam_3 != None and cam_8 != None:
					distance1 = math.sqrt((cam_3.center[0] - cam_8.center[0])**2 + (cam_3.center[1] - cam_8.center[1])**2 + (cam_3.center[2] - cam_8.center[2])**2)
					calc_distances.append(distance1)
				if cam_4 != None and cam_9 != None:
					distance2 = math.sqrt((cam_4.center[0] - cam_9.center[0])**2 + (cam_4.center[1] - cam_9.center[1])**2 + (cam_4.center[2] - cam_9.center[2])**2)
					calc_distances.append(distance2)
				if cam_7 != None and cam_2 != None:
					distance3 = math.sqrt((cam_7.center[0] - cam_2.center[0])**2 + (cam_7.center[1] - cam_2.center[1])**2 + (cam_7.center[2] - cam_2.center[2])**2)
					calc_distances.append(distance3)
				if cam_6 != None and cam_1 != None:
					distance4 = math.sqrt((cam_6.center[0] - cam_1.center[0])**2 + (cam_6.center[1] - cam_1.center[1])**2 + (cam_6.center[2] - cam_1.center[2])**2)
					calc_distances.append(distance4)
	elif len(cameras) >= 61 and len(cameras) <= 66: #Dooblicator 2.0 66 cameras
		for cam_num in range(1,7):
			cam_5 = None
			cam_11 = None

			cam_1 = None
			cam_7 = None

			cam_10 = None
			cam_4 = None

			cam_9 = None
			cam_3 = None

			cam_2 = None
			cam_8 = None
			for cam in cameras:
				if re.search("^Pod\s*5\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod5Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_5 = cam
				elif re.search("^Pod\s*11\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Po11Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_11 = cam
				elif re.search("^Pod\s*1\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod1Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_1 = cam
				elif re.search("^Pod\s*7\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod7Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_7 = cam
				elif re.search("^Pod\s*10\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod10Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_10 = cam
				elif re.search("^Pod\s*4\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#:"Pod4Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_4 = cam
				elif re.search("^Pod\s*9\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod9Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_9 = cam
				elif re.search("^Pod\s*3\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod3Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_3 = cam
				elif re.search("^Pod\s*2\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod2Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_2 = cam
				elif re.search("^Pod\s*8\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod8Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_8 = cam

				if cam_5 != None and cam_11 != None:
					distance1 = math.sqrt((cam_5.center[0] - cam_11.center[0])**2 + (cam_5.center[1] - cam_11.center[1])**2 + (cam_5.center[2] - cam_11.center[2])**2)
					calc_distances.append(distance1)
				if cam_1 != None and cam_7 != None:
					distance2 = math.sqrt((cam_1.center[0] - cam_7.center[0])**2 + (cam_1.center[1] - cam_7.center[1])**2 + (cam_1.center[2] - cam_7.center[2])**2)
					calc_distances.append(distance2)
				if cam_10 != None and cam_4 != None:
					distance3 = math.sqrt((cam_10.center[0] - cam_4.center[0])**2 + (cam_10.center[1] - cam_4.center[1])**2 + (cam_10.center[2] - cam_4.center[2])**2)
					calc_distances.append(distance3)
				if cam_9 != None and cam_3 != None:
					distance4 = math.sqrt((cam_9.center[0] - cam_3.center[0])**2 + (cam_9.center[1] - cam_3.center[1])**2 + (cam_9.center[2] - cam_3.center[2])**2)
					calc_distances.append(distance4)
				if cam_2 != None and cam_8 != None:
					distance5 = math.sqrt((cam_2.center[0] - cam_8.center[0])**2 + (cam_2.center[1] - cam_8.center[1])**2 + (cam_2.center[2] - cam_8.center[2])**2)
					calc_distances.append(distance5)
	else:#Dusseldorf 46 cameras or 40 camearas
		for cam_num in range(1,6):
			cam_3 = None
			cam_7 = None

			cam_4 = None
			cam_8 = None

			cam_6 = None
			cam_2 = None

			cam_5 = None
			cam_1 = None

			for cam in cameras:
				if re.search("^Pod\s*3\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod3Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_3 = cam
				elif re.search("^Pod\s*8\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod8Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_8 = cam
				elif re.search("^Pod\s*4\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod4Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_4 = cam
				elif re.search("^Pod\s*5\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod5Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_5 = cam
				elif re.search("^Pod\s*7\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod7Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_7 = cam
				elif re.search("^Pod\s*2\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):# "Pod2Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_2 = cam
				elif re.search("^Pod\s*6\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod6Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_6 = cam
				elif re.search("^Pod\s*1\s*Camera\s*[1]?[0-9].*",cam.label, flags=re.IGNORECASE):#"Pod1Camera{0}".format(cam_num) in cam.label:
					if cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None:
						cam_1 = cam

				if cam_3 != None and cam_7 != None:
					distance1 = math.sqrt((cam_3.center[0] - cam_7.center[0])**2 + (cam_3.center[1] - cam_7.center[1])**2 + (cam_3.center[2] - cam_7.center[2])**2)
					calc_distances.append(distance1)
				if cam_4 != None and cam_8 != None:
					distance2 = math.sqrt((cam_4.center[0] - cam_8.center[0])**2 + (cam_4.center[1] - cam_8.center[1])**2 + (cam_4.center[2] - cam_8.center[2])**2)
					calc_distances.append(distance2)
				if cam_6 != None and cam_2 != None:
					distance3 = math.sqrt((cam_6.center[0] - cam_2.center[0])**2 + (cam_6.center[1] - cam_2.center[1])**2 + (cam_6.center[2] - cam_2.center[2])**2)
					calc_distances.append(distance3)
				if cam_5 != None and cam_1 != None:
					distance4 = math.sqrt((cam_5.center[0] - cam_1.center[0])**2 + (cam_5.center[1] - cam_1.center[1])**2 + (cam_5.center[2] - cam_1.center[2])**2)
					calc_distances.append(distance4)
					
	return max(calc_distances)

#returns number of pods and array which has count of cameras on each pod
def get_dooblicator_configuration(cameras):
	if len(cameras) >= 49 and len(cameras) <= 54:
		return 9, np.ones((9))*6
	elif len(cameras) >= 61 and len(cameras) <= 66:
		return 11, np.ones((11))*6
	elif len(cameras) >=41 and len(cameras) <= 46:
		pom = np.ones((8))*5
		pom[2] = 11 #pod 3 has 11 cameras (additional 6 for face)
		return 8, pom
	else:
		return 8, np.ones((8))*5

def rename_cameras(chunk):
	pods, cameras_on_pod = get_dooblicator_configuration(chunk.cameras)
	cameras_on_pod = cameras_on_pod.astype(int)
	pom_for_cams = []
	#for every pod number
	for pod_num in range(pods):
		# for every cam on that pod
		for cam_num in range(cameras_on_pod[pod_num]):
			#go through all cameras and check if it matches name
			for cam in chunk.cameras:
				#check if it matches by first digit and afterwards if it is two digit on camera
				if re.search("^[_]?Pod\s*{0}\s*Camera\s*{1}.*".format(pod_num+1, cam_num+1),cam.label, flags=re.IGNORECASE):
					if not re.search("^[_]?Pod\s*2\s*Camera\s*1[1]?[0-9].*".format(pod_num+1, cam_num+1),cam.label, flags=re.IGNORECASE):
						cam.label = "Pod{0}Camera{1}".format(pod_num+1, cam_num+1)
						break;
					else:
						pom_for_cams.append(cam)
	for pod_num in range(pods):
		# for every cam on that pod now check for cameras above ten
		for cam_num in range(cameras_on_pod[pod_num]):
			#go through all cameras and check if it matches name now check for cameras above ten
			for cam in chunk.cameras:
				#check if it matches by first digit and afterwards if it is two digit on camera
				if re.search("^[_]?Pod\s*2\s*Camera\s*1[1]?[0-9].*".format(pod_num+1, cam_num+1),cam.label, flags=re.IGNORECASE):
					cam.label = "Pod{0}Camera{1}".format(pod_num+1, cam_num+1)
					break;
					

def get_model_data():
	model = []
	scene = []
	if chunks:
		for i in range(0,2):
			file = ""
			if(i == 0):
				file = open("model.txt",'w')
				print("Model: ", chunks[i].label)
			else:
				file = open("scene.txt",'w')
				print("Scene: ", chunks[i].label)
			if chunks[i].cameras:
				for cam in chunks[i].cameras:
					if(cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None):
						row_data = [cam.center[0],cam.center[1], cam.center[2]]
						file.write("{0} {1} {2}\n".format(cam.center[0], cam.center[1], cam.center[2]))
						if i == 0:
							model.append(row_data)
						else:
							scene.append(row_data)
	return np.array(model),np.array(scene)

def calculate_ideal_points_cabin_Dooblicator_v1_54(axis):
	radius = 1.343
	height = 0.33
	final_points_3d = np.zeros((6,9,3))
	final_points_2d = []
	point = np.zeros(3)
	ANGLE_DEGRES = 360/8
	ANGLE_RADIANS = ANGLE_DEGRES * math.pi / 180
	for j in range(6):
		for i in range(8):
			angle_rad = i * ANGLE_RADIANS
			x=radius*cos(angle_rad)
			y=j*height
			z=radius*sin(angle_rad)

			point = np.array([y,x,z])#because of the PhotoScan the order is y,x,z
			if axis == 1:
				point = np.array([x,y,z])
			elif axis == 2:
				point = np.array([x,z,y])
			point.round(5,point)
			final_points_3d[j][i] = point
			final_points_2d.append(np.asarray(point))
	for k in range(6):
		radius_for_fifth = radius * cos(ANGLE_RADIANS/2)
		angle_rad_for_fifth = ANGLE_RADIANS*3 + ANGLE_RADIANS / 2
		x=radius_for_fifth*cos(angle_rad_for_fifth)
		y=k*height
		z=radius_for_fifth*sin(angle_rad_for_fifth)
		point = np.array([y,x,z])#because of the PhotoScan the order is y,x,z
		if axis == 1:
			point = np.array([x,y,z])
		elif axis == 2:
			point = np.array([x,z,y])
		point.round(5,point)
		final_points_3d[k][8] = point
		final_points_2d.append(np.asarray(point))

	print("Calculated ideal points for Dooblicator v1 54")

	return np.array(final_points_2d), radius, height



def calculate_ideal_points_cabin_Dooblicator_v1_40(axis):
	radius = 1.963
	height = 0.4
	final_points_3d = np.zeros((5,8,3))
	final_points_2d = []
	point = np.zeros(3)
	ANGLE_DEGRES = 360/8
	ANGLE_RADIANS = ANGLE_DEGRES * math.pi / 180

	for j in range(5):
		for i in range(8):
			angle_rad = i * ANGLE_RADIANS
			x=radius*cos(angle_rad)
			y=j*height

			z=radius*sin(angle_rad)
			point = np.array([y,x,z])#because of the PhotoScan the order is y,x,z
			if axis == 1:
				point = np.array([x,y,z])
			elif axis == 2:
				point = np.array([x,z,y])
			point.round(5,point)
			final_points_3d[j][i] = point
			final_points_2d.append(np.asarray(point))
	print("Calculated ideal points for Dooblicator v1 40")


	return np.array(final_points_2d), radius, height

def calculate_ideal_points_cabin_Dooblicator_v1_46(axis, rotate = False):
	radius = 1.963
	height = 0.4
	final_points_2d = []
	point = np.zeros(3)
	ANGLE_DEGRES = 360/8
	ANGLE_RADIANS = ANGLE_DEGRES * math.pi / 180
	for j in range(5):
		for i in range(8):
			if rotate:
				angle_rad = i * ANGLE_RADIANS + math.pi;
			else:
				angle_rad = i * ANGLE_RADIANS;
			x=radius*cos(angle_rad)
			y=j*height
			z=radius*sin(angle_rad)
			point = np.array([x,y,z])#because of the PhotoScan the order is y,x,z
			if axis == 1:
				point = np.array([y,x,z])
			elif axis == 2:
				point = np.array([x,z,y])
			point.round(5,point)
			#final_points_3d[j][i] = point
			final_points_2d.append(np.asarray(point))
			if i==2 and j == 1:
				if axis == 0:
					final_points_2d.append([x+0.3797104473,y,z+0.1575469724])
					final_points_2d.append([x-0.3797104473,y,z+0.1575469724])
					final_points_2d.append([x+0.6295674132 ,y+0.2,z+0.2612159885])
					final_points_2d.append([x-0.6295674132 ,y+0.2,z+0.2612159885])
					final_points_2d.append([x+0.8795631114, y,z+0.3649425666])
					final_points_2d.append([x-0.8795631114,y, z+0.3649425666])
				elif axis == 1:
					final_points_2d.append([y,x+0.3797104473,z+0.1575469724])
					final_points_2d.append([y,x-0.3797104473,z+0.1575469724])
					final_points_2d.append([ y+0.2,x+0.6295674132,z+0.2612159885])
					final_points_2d.append([ y+0.2,x-0.6295674132,z+0.2612159885])
					final_points_2d.append([y, x+0.8795631114,z+0.3649425666])
					final_points_2d.append([y,x-0.8795631114, z+0.3649425666])
				elif axis == 2:
					final_points_2d.append([x+0.3797104473,z+0.1575469724,y])
					final_points_2d.append([x-0.3797104473,z+0.1575469724,y])
					final_points_2d.append([x+0.6295674132 ,z+0.2612159885,y+0.2])
					final_points_2d.append([x-0.6295674132 ,z+0.2612159885,y+0.2])
					final_points_2d.append([x+0.8795631114,z+0.3649425666, y])
					final_points_2d.append([x-0.8795631114, z+0.3649425666,y])

	print("Calculated ideal points for Dooblicator v1 46")
	return np.array(final_points_2d), radius, height

def calculate_ideal_points_cabin_Dooblicator_v2_66(axis):
	radius = 1.5
	height = 0.37
	final_points_3d = np.zeros((6,11,3))
	final_points_2d = []
	point = np.zeros(3)
	ANGLE_DEGRES = 360/10
	ANGLE_RADIANS = ANGLE_DEGRES * math.pi / 180
	for j in range(6):
		for i in range(10):
			angle_rad = i * ANGLE_RADIANS
			x=radius*cos(angle_rad)
			y = j*height
			z=radius*sin(angle_rad)
			point = np.array([y,x,z])#because of the PhotoScan the order is y,x,z
			if axis == 1:
				point = np.array([x,y,z])
			elif axis == 2:
				point = np.array([x,z,y])
			point.round(5,point)
			final_points_3d[j][i] = point
			final_points_2d.append(np.asarray(point))

	for k in range(6):
		radius_for_fifth = radius * cos(ANGLE_RADIANS/2)
		angle_rad_for_fifth = ANGLE_RADIANS*3 + ANGLE_RADIANS / 2
		x=radius_for_fifth*cos(angle_rad_for_fifth)
		y=k*height
		z=radius_for_fifth*sin(angle_rad_for_fifth)
		point = np.array([y,x,z])#because of the PhotoScan the order is y,x,z
		if axis == 1:
			point = np.array([x,y,z])
		elif axis == 2:
			point = np.array([x,z,y])
		point.round(5,point)
		final_points_3d[k][8] = point
		final_points_2d.append(np.asarray(point))
	print("Calculated ideal points for Dooblicator v2 66")
	return np.array(final_points_2d), radius, height



def save_points_like_obj(points, file_destination):
	obj_file = open(file_destination, 'w')
	for point in points:
		obj_file.write("v {0} {1} {2} 1\n".format(point[0],point[1],point[2]))
	obj_file.close()

def save_points_rotated_like_obj(points, file_destination):
	obj_file = open(file_destination, 'w')
	for point in points:
		obj_file.write("v {0} {1} {2} 1\n".format(point[0,0],point[0,1],point[0,2]))
	obj_file.close()

def get_points_from_point_cloud(file_destination, radius_ideal_points, distance):
	normalized_points = []
	with open(file_destination, 'r') as obj_file:
		for line in obj_file.readlines():
			points = np.asarray(line.split()[1:len(line.split())-1])
			points = np.array([float(points[0]), float(points[1]), float(points[2])])
			scaled_points = points/(distance/radius_ideal_points/2)
			normalized_points.append(np.asarray(scaled_points))
	return np.array(normalized_points)

def get_normalized_points(chunk, ideal_radius):
	normalized_points = []
	if chunk:
		if chunk.cameras:
			radius_distance = calculate_radius(chunk.cameras)
			for cam in chunk.cameras:
				if(cam.center != None and cam.center[0] != None and cam.center[1] != None and cam.center[2] != None):
					points = np.asarray([cam.center[0],cam.center[1],cam.center[2]])
					points = np.array([float(points[0]), float(points[1]), float(points[2])])
					scaled_points = points/(radius_distance/ideal_radius/2)
					normalized_points.append(np.asarray(scaled_points))

	return np.array(normalized_points)

def calculate_ideal_points(cameras, axis = 0):
	if len(cameras) >= 49 and len(cameras) <= 54:
		return calculate_ideal_points_cabin_Dooblicator_v1_54(axis)
	elif len(cameras) >= 61 and len(cameras) <= 66:
		return calculate_ideal_points_cabin_Dooblicator_v2_66(axis)
	elif len(cameras) >=41 and len(cameras) <= 46:
		return calculate_ideal_points_cabin_Dooblicator_v1_46(axis,rotate = True)
	else:
		return calculate_ideal_points_cabin_Dooblicator_v1_40(axis)

def rigid_transform_3D(A, B):
	#assert len(A) == len(B)

	N = A.shape[0]

	centroid_A = np.mean(A, axis=0)
	centroid_B = np.mean(B, axis=0)

	# centre the points
	AA = A - np.tile(centroid_A, (N, 1))
	BB = B - np.tile(centroid_B, (N, 1))

	print("AA:", AA)
	print("BB:", BB)

	# dot is matrix multiplication for array
	H = np.transpose(AA) * BB

	U, S, Vt = np.linalg.svd(H)

	R = Vt.T * U.T

	# special reflection case
	if np.linalg.det(R) < 0:
	   Vt[2,:] *= -1
	   R = Vt.T * U.T

	t = -R*centroid_A.T + centroid_B.T

	return R, t


def get_score_for_ideal_points(c, ideal_points, IDEAL_RADIUS, IDEAL_HEIGHT):
	#rename cameras
	rename_cameras(c)
	
	#get normalized points of cameras currently aligned
	points = get_normalized_points(c,IDEAL_RADIUS)

	

	#get translation and rotation vector

	#get model, scene and after non rigid points
	model,scene,after_tps = cca.non_rigid_registration(points, ideal_points)

	#save_points_like_obj(model, "D:/model{}.obj".format(counter))
	#save_points_like_obj(scene, "D:/scene{}.obj".format(counter))
	#save_points_like_obj(after_tps, "D:/after_tps{}.obj".format(counter))

	distances_array = []

	ballTree = BallTree(after_tps)
	#for dooblicator v1 46 min distance between cameras is height/2
	if len(c.cameras) >= 41 and len(c.cameras) <=51:
		radius = 2*(IDEAL_HEIGHT/2)/3
	else:
		radius = 2*IDEAL_HEIGHT/3
	not_functional = []
	i = 0
	for point in ideal_points:
		ind = ballTree.query_radius(point, radius)
		if len(ind[0]) == 1:
			distances_array.append(np.linalg.norm(point - after_tps[ind[0][0]]))
		else:
			i += 1
			distances_array.append(1000)


	print("SCORE: ", np.mean(distances_array))

	return np.mean(distances_array)


def get_alignment_score(chunk):

	#setting final result for every rotation 1000
	mean_result_X = 1000
	mean_result_Y =1000
	mean_result_Z = 1000

	#get ideal_points, ideal radius and ideal height of current scanner on X orientatio
	print("-------Check cameras alignment on X axis")
	ideal_points, IDEAL_RADIUS, IDEAL_HEIGHT = calculate_ideal_points(chunk.cameras)
	mean_result_X = get_score_for_ideal_points(chunk, ideal_points, IDEAL_RADIUS, IDEAL_HEIGHT)

	if mean_result_X < 1:
		return mean_result_X

	print("-------Check cameras alignment on Y axis")
	#get ideal_points, ideal radius and ideal height of current scanner on Y orientatio
	ideal_points, IDEAL_RADIUS, IDEAL_HEIGHT = calculate_ideal_points(chunk.cameras, axis=1)
	mean_result_Y = get_score_for_ideal_points(chunk, ideal_points, IDEAL_RADIUS, IDEAL_HEIGHT)
	if mean_result_Y < 1:
		return mean_result_Y

	print("-------Check cameras alignment on Z axis")
	#get ideal_points, ideal radius and ideal height of current scanner on Z orientatio
	ideal_points, IDEAL_RADIUS, IDEAL_HEIGHT = calculate_ideal_points(chunk.cameras, axis=2)
	mean_result_Z = get_score_for_ideal_points(chunk, ideal_points, IDEAL_RADIUS, IDEAL_HEIGHT)
	if mean_result_Z < 1:
		return mean_result_Z

	return min(mean_result_Y, mean_result_X, mean_result_Z)


#doc = PhotoScan.app.document
#get_alignment_score(doc.chunk)

#points, _, _ = calculate_ideal_points_cabin_Dooblicator_v1_46(0, rotate = True)
#save_points_like_obj(points, "D:/x_rot.obj");

#points, _, _ = calculate_ideal_points_cabin_Dooblicator_v1_46(1, rotate = True)
#save_points_like_obj(points, "D:/y_rot.obj");

#points, _, _ = calculate_ideal_points_cabin_Dooblicator_v1_46(2, rotate = True)
#save_points_like_obj(points, "D:/z_rot.obj");

#chunks = doc.chunks
#for c in chunks:
#	print("FOR ", c.label, ":")
#	print("RESULT: ", get_alignment_score(c))
#print(get_alignment_score(doc.chunk))
#ideal_xmls_path = "D:\ideal_camera_alignment_xml"
#for chunk in doc.chunks:
	#rename_cameras(chunk)
#	chunk.exportCameras(os.path.join(ideal_xmls_path,chunk.label + ".xml"))