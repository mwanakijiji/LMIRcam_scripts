#!/usr/bin/python
# This is a simple script to set camera parameters, take data, and offset the telescope
# This is a *dual aperture* script

# Operator must set exposure time and number of coadds first!
# must begin with the stars in the *UP* nod position

import sys, os, string, time, pyfits,  pdb, copy, numpy
from pyindi import * 
from scipy import ndimage, sqrt, stats

orig_UL_x = 291
orig_UL_y = 734
orig_UR_x = 665
orig_UR_y = 754

day = time.strftime('%Y%m%d')
img = []
cx = float()
cy = float()
plateScale=0.011
#new_cx = float()
#new_cy = float()

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)
firstPositions = True # are we in the first nod to determine original PSF positions?

autoFindStar = True  # auto-detect star in frame?
# if autoFindStar, specify which half of frame to search ('left' or 'right') [CHANGE THIS TO UP-DOWN LATER]
# set to 'both' or '' to search whole frame. Irrelevant if autoFindStar = False

# fix desired positions of PSFs in up nod


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
            image[:,512:-1] = 0
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
# take only 1 image at a time (note these will not be saved)
pi.setINDI("LMIRCAM.Command.text","1 obssequences",timeout=300,wait=True)


###############################################
## take up nod only, and don't save the file ##
###############################################
pi.setINDI("LMIRCAM.Command.text","0 savedata") # don't save

# take frames
'''
if firstPositions: # if this is the original nod, this loop will find PSF positions
	# SHOULD ALREADY BE IN UP NOD

	print 'Taking original LMIRCam up nod image...'
	pi.setINDI("LMIRCAM.Command.text","go",wait=True)
	f=pi.getFITS("LMIRCAM.DisplayImage.File", "LMIRCAM.GetDisplayImage.Now", wait=True)
	f.verify('fix')
	head = f[0].header
	imgb4 = f[0].data
	imgb4bk = bkgdsub(imgb4,'median',50)
	imgb4bk -= numpy.median(imgb4bk)
	fN = datadir+'lm_original.fits'
	pyfits.writeto(fN, imgb4bk, header=head, clobber=1)

	pi.setINDI("LMIRCAM.Command.text","1 obssequences",timeout=300,wait=True)
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

# retrieve frames, find PSF positions
'''
# read frames, make corrections 3 times

for k in range(3): # do three iterations to get back to the original position
	f=pi.getFITS("LMIRCAM.DisplayImage.File", "LMIRCAM.GetDisplayImage.Now", wait=True)
	#f.verify('fix')
	head = f[0].header
	imgb4 = f[0].data
	imgb4bk = bkgdsub(imgb4,'median')
	imgb4bk -= numpy.median(imgb4bk)

	# get the image as an array. [0,0]=LL, [1023,0]=UL
	if img==[]:
  		img = f[0].data
	else:
    		img = numpy.dstack(( img, f[0].data ))
	#print img.shape # a check


	#### PROCESS IMAGE
	imgSubBP = processImg(img,'median')
	#print img
	#print imgSubBP

	PSFside = 'left'
	[current_cy_L,current_cx_L] = findStar(imgSubBP, cx, cy)
	print 'LEFT:'
	#print [orig_cy_L,orig_cx_L]

	PSFside = 'right'
	print 'RIGHT:'
	[current_cy_R,current_cx_R] = findStar(imgSubBP, cx, cy)
	#print [orig_cy_R,orig_cx_R]

	## now that we have the positions, let's find the displacements and make corrections


	# CORRECTIONS

	# make correction to FPC (left target)
	settingsFPC  = pi.getINDI("Acromag.FPC_status.*")
	tipFPC  = settingsFPC["Acromag.FPC_status.Tip"]
	tiltFPC  = settingsFPC["Acromag.FPC_status.Tilt"]
	pistonFPC  = settingsFPC["Acromag.FPC_status.Piston"]

	xDispPixL = current_cx_L - orig_UL_x
	yDispPixL = current_cy_L - orig_UL_y
	xDispAsecL = xDispPixL*plateScale
	yDispAsecL = yDispPixL*plateScale


	if (abs(xDispAsecL)<1.5) and (abs(yDispAsecL)<1.5): # to avoid catastrophic movement
		newtipFPC = -yDispAsecL # negative relative movement, to correct
		newtiltFPC = -xDispAsecL
	else:
		newtipFPC = 0
		newtiltFPC = 0


	newpistonFPC = 0 # don't move piston
	mode = 1

	keys=("Acromag.FPC.Tip","Acromag.FPC.Tilt","Acromag.FPC.Piston","Acromag.FPC.Mode")
	values=(newtipFPC,newtiltFPC,newpistonFPC,mode)

	newsettingsFPC={keys[0]:values[0],keys[1]:values[1],keys[2]:values[2],keys[3]:values[3]}
	#print newsettingsFPC
	pi.setINDI(newsettingsFPC)
	time.sleep(0.05) 


	# make correction to SPC (right target)
	settingsSPC  = pi.getINDI("Acromag.SPC_status.*")
	tipSPC  = settingsSPC["Acromag.SPC_status.Tip"]
	tiltSPC  = settingsSPC["Acromag.SPC_status.Tilt"]
	# pistonSPC  = settingsSPC["Acromag.SPC_status.Piston"] # no piston

	xDispPixR = current_cx_R - orig_UR_x
	yDispPixR = current_cy_R - orig_UR_y
	xDispAsecR = xDispPixR*plateScale
	yDispAsecR = yDispPixR*plateScale

	if (abs(xDispAsecR)<1.5) and (abs(yDispAsecR)<1.5): # to avoid catastrophic movement
		newtipSPC = -yDispAsecL # negative relative movement, to correct
		newtiltSPC = -xDispAsecL
	else:
		newtipSPC = 0
		newtiltSPC = 0

	mode = 1

	keys=("Acromag.SPC.Tip","Acromag.SPC.Tilt","Acromag.SPC.Mode")
	values=(newtipSPC,newtiltSPC,mode)

	newsettingsSPC={keys[0]:values[0],keys[1]:values[1],keys[2]:values[2]}
	#print newsettingsSPC
	pi.setINDI(newsettingsSPC)

	time.sleep(1) 

	# take new image, but don't save it
	pi.setINDI("LMIRCAM.Command.text","0 savedata")
	pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)

	img = [] # clear
	

