# -*- coding: utf-8 -*-
"""
Tuesday 1 September, 2020, 16:49:19
@author: gabri

Use:
This script can be used to analize the metashape "quality" parameter
and disable the images that are below a certain quality
limit set by the user.

Summary:
This script runs the metashape funciton analyzePhotos to estimate the quality and
then disables the cameras that have the quality below the threshold.
"""

#Imports
import Metashape as mt

#Variables
chunk = mt.app.document.chunk #define the active chunk
cameras = chunk.cameras #define the cameras in the chunk
quality_thr = mt.app.getFloat(label= 'Choose the quality value threshold',value=0.4) #define the threshold value

chunk.analyzePhotos(cameras) #run the analyzePhotos function


for camera in cameras: #for every camera in the chunk
	quality = float(camera.meta['Image/Quality']) #read the the quality of the photo
	if quality < float(quality_thr): #disable the photo if the quality value is below the threshold
		camera.enabled = False
