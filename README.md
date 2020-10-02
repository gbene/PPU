# Python Photogrammetric Utilities

PPU is a collection of python scripts that can help in the photogrammetric process. It contains a series of scripts that can be used directly with **Agisoft Metashape** and a python executable that can help in the process of converting images from raw to other formats, creating csv files that can be used to scale the object based on calculated camera position, masking and exif data copying. The executable is completely standalone and cross-platform. In this way it can be used even if the machine doesn't have Python insalled and works on every platform.

PPU executable is in PPU-main>PPU>PPU_v1 folder

## PPU executable

 The executable helps with easly queue and batch process folders of images that normally are created during the process of constructing a model. It is composed by a main menu in which the user can import the main working directory and select or navigate the folders present inside the former. Once the desired folders are selected, there are several scripts to choose depending on the process that needs to be done.
### False geodata
This script calculates the position in cartesian coordinates of the cameras given the distance from the center of rotation and the camera lens, the pitch the camera and, if present, the added focal distance given from macro rings. The output will be written in a csv file with the right format so that it can be imported in Metashape to scale and orient the reconstructed object.

### Raw conversion
This script converts raw images to the desired image format using the rawpy package. As a result it will create a folder with the output files and the files, if possibile, **will preserve the original exif data**

### Mask
This scripts (still very much a WIP) aims to mask automatically an object from the background. The user needs to write the input images that need to be masked, the output masked image and the threshold value. Then the user can choose to save the mask or apply the mask to the image or both. The output files will be saved in the newly created output folder. 

### Exif copy
This script copies the exif data from a series of source images to a series of target images. It is necessary that source and target images are in the same folder and that the number of source and target images are the same.


## Metashape scripts

These scripts can to be used in the Agisoft Metashape console.

### obj_center.py

This script calculates the center of geometry coordinates of any meshed model present in an active chunk and creates a marker called _center_ positioned at the determined coordinates.

### quality_check.py

This script runs the _quality check_ for the imported photos in the active chunk and disables the ones that have a value below the one defined by the user.


