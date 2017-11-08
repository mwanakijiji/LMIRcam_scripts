#!/usr/bin/python
# This is a simple script to set camera parameters, take data, and offset the telescope
# This is a *dual aperture* script

# Operator must set exposure time and number of coadds first!
# must begin with the stars in the *UP* nod position

import time
from pyindi import * 

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)
firstPositions = True # are we in the first nod to determine original PSF positions?

############################################
########  FUNCTION DEFINITIONS  ############

# give AO a time
def wait4AORunning():
    while True:
        pi.setINDI("LBTO.Dictionary.Name=L_AOStatus;Value=")
        lstatus = pi.getINDI("LBTO.Dictionary.Value")
        pi.setINDI("LBTO.Dictionary.Name=R_AOStatus;Value=")
        rstatus = pi.getINDI("LBTO.Dictionary.Value")
        #print lstatus, rstatus
        #print rstatus
	time.sleep(0.05) 
        if rstatus == "AORunning" and lstatus == "AORunning":
            break

# subtract mean or median (method) of the image
# w = edge px on either side
def bkgdsub(image, method):

    image[image==0] = numpy.nan

    ctr = int( numpy.floor( image.shape[0] / 2. ) )
    #w2 = ctr - w

    tmpimg = copy.copy(image)

    #if image.shape[1] == 1024: #leftmost column is flaky
    #    tmpimg[ctr-w2:ctr+w2, ctr-w2+64:ctr+w2] = numpy.nan
    #    tmpimg[ctr-w2:ctr+w2, :64] = numpy.nan
    #else:
    #    tmpimg[ctr-w2:ctr+w2, ctr-w2:ctr+w2] = numpy.nan

    if method == 'mean':
        rowbkgd = stats.nanmean(tmpimg,1)
    elif method == 'median':
        rowbkgd = stats.nanmedian(tmpimg,1)
    rowbkgd2d = numpy.tile(numpy.reshape(rowbkgd,[len(rowbkgd),1]),[1,image.shape[0]])
    tmpimg = tmpimg - rowbkgd2d

    if method == 'mean':
        colbkgd = stats.nanmean(tmpimg,0)
    elif method == 'median':
        colbkgd = stats.nanmedian(tmpimg,0)
    colbkgd2d = numpy.tile(numpy.reshape(colbkgd,[1,len(colbkgd)]),[image.shape[1],1])
    image = image - rowbkgd2d - colbkgd2d

    image[numpy.isnan(image)] = 0

    return image


############################################

# calculate image centroid [y,x]
# returns: centroid [row, col]
def centroid(image):
    image = numpy.array(image)
    yy = range(image.shape[0])
    xx = range(image.shape[1])
    [X, Y] = numpy.meshgrid(xx,yy)
    Xi = X*image
    Yi = Y*image
    centr = [ numpy.sum(Yi)/numpy.sum(image),numpy.sum(Xi)/numpy.sum(image) ]
    return centr


############################################

# find star and return coordinates [y,x]
def findStar(image, cx, cy):
    if autoFindStar:
        #image[0:20,:] = 0 # avoid edge effects
        #image[-20:,:] = 0
        #image[:,0:20] = 0
        #image[:,-20:] = 0

        if string.lower(PSFside) == 'left':
            image[:,512:0] = 0
        elif string.lower(PSFside) == 'right':
            image[:,0:512] = 0

	'''
        if string.lower(PSFside) == 'left_up':
            image[:612,612:] = 0
        elif string.lower(PSFside) == 'right_up':
            image[:612,:612] = 0
        elif string.lower(PSFside) == 'left_down':
            image[612:,612:] = 0
        elif string.lower(PSFside) == 'right_down':
            image[612:,:612] = 0
	'''

        imageG = ndimage.gaussian_filter(image, 6) # remove effect of bad pixels (?)
        loc = numpy.argwhere(imageG==imageG.max())
        cx = loc[0,1]
        cy = loc[0,0]
        #print [cy, cx] # check

    return [cy, cx]


############################################

# process the image
def processImg(imgDummy, methodDummy):
    # bias level correction
    imgSub = bkgdsub(imgDummy,methodDummy)
    imgSub -= numpy.median(imgSub)
    imgSubM = ndimage.median_filter(imgSub,3)

    # define BP mask
    imgDiff = numpy.abs(imgSub - imgSubM)
    stddev = numpy.std(imgDiff)
    mask = ( imgDiff > 4*stddev ) & ( imgDiff > 0.15 * numpy.abs(imgSub) )

    imgSubBP = copy.copy(imgSub)
    imgSubBP[mask] = imgSubM[mask]

    #print numpy.amax(imgSub) # checks
    #print numpy.amin(imgSub)
    #print numpy.median(imgSub)

    return imgSubBP

#######  end function definitions  ############
###############################################

#turn off continuous acquisition
pi.setINDI("LMIRCAM.Command.text","0 contacq")
# take 50 images per nod position
pi.setINDI("LMIRCAM.Command.text","50 obssequences",timeout=300,wait=True)


###################################################################################
## take up-down pairs, correcting position of each PSF to make the original ones ##
###################################################################################

pi.setINDI("LMIRCAM.Command.text","50 obssequences",timeout=300,wait=True)
# take 10 up/down nod pairs
for j in range(10):
	print j
        # take frames and save the data
	pi.setINDI("LMIRCAM.Command.text","1 savedata")
	pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
        # use the last frame taken as the background for the next set
	pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=False)

        # NOD DOWN
	#Note that these are X and Y values of the star on the array where LL is 0,0.
	#There is a rotation and sign flip in Elwood's INDI-IIF interface to make this work.
	pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0.0, "LBTO.OffsetPointing.OffsetY", -4.5, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 

        # wait for AO to close loop and stabilize for a second before taking next set
        wait4AORunning()
	pi.setINDI("LMIRCAM.Command.text","1000 sleep")
	pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
	pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=False)

        # NOD UP in prep for next set
	#Note that these are X and Y values of the star on the array where LL is 0,0.
	#There is a rotation and sign flip in Elwood's INDI-IIF interface to make this work.
	pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0.0, "LBTO.OffsetPointing.OffsetY", 4.5, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 
        wait4AORunning() 
	pi.setINDI("LMIRCAM.Command.text","1000 sleep")




# end of script: set up to be compatible with the observer running in continuous mode
# turn off save data
pi.setINDI("LMIRCAM.Command.text","0 savedata",timeout=300,wait=True)
# set number of images to take to 1
pi.setINDI("LMIRCAM.Command.text","1 obssequences")
