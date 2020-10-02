# -*- coding: utf-8 -*-
"""
Saturday 19 September 2020 11:11:53

@author: gabri

Use:
The script is used to find and display the geometric center of the model.

Summary:
The geometric center is calculated from an arithmetic mean operation
for the x;y;z coordinates of every vertex of the mesh.
"""

#Imports
from operator import itemgetter
import Metashape as mt
import statistics as st

#Variables
chunk = mt.app.document.chunk #define the active chunk 
mesh = chunk.model #define the mesh of the model
coords = {0: {},1: {},2: {}} #x,y and z are grouped respectevly in 0,1,2
center = [] #define the center as a list

for i in range(len(mesh.vertices)): #for every point
	coords[0][i], coords[1][i],coords[2][i] = mesh.vertices[i].coord #add x,y,z in the dictionary


for index1 in coords.values(): #for every value in the dict
	mean = st.mean(index1.values()) #mean of the values
	center.append(mean) #append the mean to the center

chunk.addMarker(center) #add the marker with the center coordinates
chunk.markers[-1].label = 'center' #rename the marker as 'center'






