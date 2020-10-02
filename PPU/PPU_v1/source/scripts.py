# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 22:30:58 2020

@author: gabri

Use:
This py file groups all the scripts that are used in the main PPU.py. 

Summary:

run_geo: calculates and writes csv file used for scaling the object with the georeferencing method.
run_conv: converts raw images (eg .nef) in other formats (.jpg,.tiff....) mantaining exif data.
run_mask: automatically masks a photo or applies the mask to the photo.
run_exif: copies exif data from source photos to target photos.
"""

#Imports
import glob
import numpy as np
import os
from pyexiv2 import Image
from fractions import Fraction
import rawpy
import cv2 as cv



#-------------- Functions used in the scripts ------------------------

def pol2cart3(pol_points): #converts polar coords to cartesian
    cart_points3 = []
    for r,theta,phi in pol_points: #for every point in the list
        x = r*np.cos(theta)*np.cos(phi)
        y = r*np.sin(theta)*np.cos(phi)
        z = r*np.sin(phi)
        cart_points3.append([x,y,z])
    return cart_points3

#finds the lens focal length (if present) and approximates 
#mag.ratio with m = d/f with d = distance+focal length
def mag_calc(image,distance,rings): 
    
    with Image(r'{}'.format(image)) as img:
        exif_data = img.read_exif() #take exif data

    try:
        print(float(Fraction(exif_data['Exif.Photo.FocalLength']))/1000)
        focal_length = float(Fraction(exif_data['Exif.Photo.FocalLength']))/1000 #if present converts focal length to m
        
    except KeyError:
        print(f'Error, focal length not found for {image} setting it to 55mm.') #if not sets a standard value
        focal_length = 0.055

    og_mag = 1/((distance+rings+focal_length)/(focal_length)) #calculate the starting mag.ratio
    new_mag = og_mag+(rings/focal_length) #calculate mag.ratio with macro rings
	
    return focal_length,og_mag, new_mag

def rawconv(image,form,directory): #converts raw images to other image formats
    IN = rawpy.imread(image) #read the image
    rgb = IN.postprocess(use_camera_wb=True)
    rgb = cv.cvtColor(rgb,cv.COLOR_BGR2RGB) #write it as a cv obj 
    new_name = f'{os.path.splitext(image)[0]}{form}' #new name of the image (with format) 
    cv.imwrite(f'{directory}\\convertita_{new_name}',rgb) #save 
    
    

def exif_copy (src, target): #transfers exif data from a source image to a target image
    
    with Image(r'{}'.format(src)) as img_src, Image(r'{}'.format(target)) as img_targ:
        
        exif_data = img_src.read_exif() #exif data (if present)
        img_targ.modify_exif(exif_data)
        
        iptc_data = img_src.read_iptc() #iptc data (if present)
        img_targ.modify_iptc(iptc_data)
        
        xmp_data = img_src.read_xmp() #xmp data (if present)
        img_targ.modify_xmp(xmp_data)

#function used to find objects in the image.  
#Every pixelthat has a value below to the thresh 
#is set to 0 the others to 255
def ogg(target,strength):
    minimo,thr= cv.threshold(target, strength, 255, 0) 
    return thr



#--------------------- Scripts ---------------------------

# Script used to calculate and write the csv file used 
#for the georeferencing method
def run_geo(path,par_dict):
    
    os.chdir(path)
    ext = par_dict['in_ext']
    files = glob.glob('*') #list of every file in dir
    img = glob.glob(f'*{ext}') #list of every image with {ext} in file

    lat = par_dict['lat'] #latitude value set from the user
    distance = par_dict['dist']/100 #distance value set from the user
    rings = par_dict['rings']/1000 #rings used set from the user
    
    focal_len,_,mag = mag_calc(img[0],distance,rings) #find focal distance and mag.ratio
	

    tot_distance = distance+rings
	#total distance is distance+rings because metashape automatically does the correction 
	#for the lens taken from exif data but the rings are not registered.
    
    
    n_file = len(img) #number of images present in dir
    rad_lat = np.deg2rad(lat) #conversion of lat in radians
    rad_long = np.linspace(0,2*np.pi,n_file) #approximate dtheta as linear

    #new [n_filex3] empty array where every entry corresponds to a point
    pol_points = np.zeros([n_file,3]) 
    pol_points[:,0] = tot_distance #distance R
    pol_points[:,1] = rad_long #angle theta
    pol_points[:,2] = rad_lat #angle phi
    
    
    cart = pol2cart3(pol_points) # converts from polar to cartesian
    
    if 'list_coord.txt' in files: #delete old csv files 
        os.remove('list_coord.txt')

    
    
    with open('list_coord.txt','w') as OUT: #write file 
        OUT.writelines('#name_img;x;y;z\n')
        for c,i in zip(img,cart): #for every image and point
            x,y,z = i
            if par_dict['corr']: #if correction is set to true
                OUT.writelines(f'{c};{x}*mag;{y}*mag;{z}*mag\n') #apply correction
            else:
                OUT.writelines(f'{c};{x};{y};{z}\n') #don't apply correction
                

#script used to convert raw images to other formats 
#and if possible transfer exif data
def run_conv(path,par_dict): #this needs multiprocessing, too slow

    conv_files = []
    os.chdir(path)
    directory = os.path.join(f'{path}\\','conversion_output')
    os.mkdir(directory) #create a new dir where the output images are saved
	
    ext = par_dict['in_ext']
    img_raw =  glob.glob(f'*{ext}') #list raw images
    form = par_dict['out_ext'] #image format
	
    for img in img_raw: #for every raw image
        print(f'processing {img}', end = "\r")
        rawconv(img,form,directory) #convert the raw image
    conv_files = glob.glob(f'{directory}\\*')#list of converted images
	
    for src,targ in zip(img_raw,conv_files): #for every raw and new image
        exif_copy(img,targ) #copy the exif data from raw to new

#script used to mask an object (not very good, needs reworking)
#needs multiprocessing (not as much as conv)
def run_mask(path,par_dict): 

    os.chdir(path)
    directory = os.path.join(f'{path}\\','masks')
    os.mkdir(directory)#create a new dir where the output images are saved

    input_ext = par_dict['in_ext']
    
    output_ext = par_dict['out_ext']

	#list of files with {ext} present in dir
    files = glob.glob(f'*{input_ext}') 

    for file in files: #for every file
        immagine = cv.imread(file,1) #read image
		#convert to rgb (because open cv is stupid)
        immagine_rgb = cv.cvtColor(immagine,cv.COLOR_BGR2RGB)
		#convert to grayscale
        immagine_gray = cv.cvtColor(immagine,cv.COLOR_BGR2GRAY) 
    
       
        obj_dec = ogg(immagine_gray,par_dict['stren']) #find obj boundaries
        print(f'processing {file}', end = "\r")
        
        name,_ = os.path.splitext(file) #take only the name of the file
        if par_dict['save']: #if "save mask" is true
            
            cv.imwrite(f'masks\\mask_{name}{output_ext}',obj_dec) #save the mask
        if par_dict['apply']: #if "apply mask" is true
            immagine_maschera=cv.bitwise_and(immagine_rgb, immagine_rgb,mask=obj_dec) #apply the mask
            immagine_maschera = cv.cvtColor(immagine_maschera,cv.COLOR_BGR2RGB) #convert from gray to rgb
            cv.imwrite(f'masks\\applicata_{name}{output_ext}',immagine_maschera) #save rgb image

#script used to transfer exif data form source images to target images 
#(for now they need to be in the same folder)
def run_exif(path,par_dict):
    
    os.chdir(path)
    input_ext = par_dict['in_ext']
    input_files = glob.glob(f'*{input_ext}') #list of exif source images
    output_ext = par_dict['out_ext']    
    output_files = glob.glob(f'*{output_ext}') #list of target images
    
    for src,targ in zip(input_files,output_files): #for every source and target image
        exif_copy(src, targ) #copy exif
