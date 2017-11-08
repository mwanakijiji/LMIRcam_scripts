# This script, to be run in LMIRCam, is for keeping the PSF of a star fixed on LMIRCam with
# the FPC and SPC mirrors. The immediate science goal of this is for 'wall-eyed pointing', so two PSFs
# (science and comparison stars), and therefore both the FPC and SPC, will be needed.

# Note: 'testLMIR = True' means that the script is just being tested using previously-saved frames,
# and is not interfacing with LMIRCam itself; 'testLMIR = False' means, 'I'm really using LMIRCam;
# send parameters to it, and look at each frame as it's read out'

# patched together by E. Spalding, June 2015

# basic outline of script (first draft, 9 June):
# 1. Take LMIRCam readouts
# 2. Find PSF centroid (just one, for now, and without nodding)
# 3. Take progressive position changes to move the FPC and SPC mirrors

testLMIR = False     # True or False. If true, do not actually configure LMIRCam or take new images
print 'testLMIR ='
print testLMIR
useFileList = True  # Load LMIRCam images listed in lmFileList instead of reading current LMIRCam buffer?
lmFileList = '/home/observer/data/140214/testdata/filelist2.txt' # One img name per line. Irrelevant if useFileList=False

autoFindStar = True  # auto-detect star in frame?
# if autoFindStar, specify which half of frame to search ('left' or 'right') [CHANGE THIS TO UP-DOWN LATER]
# set to 'both' or '' to search whole frame. Irrelevant if autoFindStar = False
PSFside = 'right'
# if autoFindStar = False, uses star coordinates below
# Overwritten if autoFindStar = True
cx = 612
cy = 700



#######################################################################


import sys, os, string, time, pyfits,  pdb, copy
import numpy
from pyindi import *
#import matplotlib.pyplot as plt
from scipy import ndimage, sqrt, stats

pi=PyINDI()

day = time.strftime('%Y%m%d')

# files will be written to LMIRCam
datadir = '/home/observer/data/'+day+'/'
if not os.path.exists(datadir):
    os.makedirs(datadir)


############################################
########  FUNCTION DEFINITIONS  ############

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
        image[0:20,:] = 0 # avoid edge effects
        image[-20:,:] = 0
        image[:,0:20] = 0
        image[:,-20:] = 0

        # [NEEDS TO BE TOP-BOTTOM]
        #if string.lower(PSFside) == 'left':
        #    image[:,-round(len(image)/2):] = 0
        #elif string.lower(PSFside) == 'right':
        #    image[:,:round(len(image)/2)] = 0

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


# LMIRCam setup param default values (note that the integration time cannot 
# be fixed otherwise)
# note: frames are grabbed as displayed in LMIRCam software; this script works
#   best if frames are background subtracted. So decide on the int params,
#   take a bkgd image, nod, then start script
Lint = 0.029  # integration in [sec]
Lcoadd = 1   # number of coadds
Lseq = 1     # number of sequences (you probably want just 1)
Lsave = 0    # save frames to LMIRCam computer? 0=no, 1=yes

if not testLMIR: # grab integration parameters from GUI
	settingsL  = pi.getINDI('LMIRCAM.CamInfo.*')
	#Lint = settingsL[]  # integration in [sec]
	Lcoadd = settingsL['LMIRCAM.CamInfo.NCoAdds']   # number of coadds
	Lseq = settingsL['LMIRCAM.CamInfo.NSeqs']     # number of sequences (you probably want just 1)
	Lsave = 1    # save frames to LMIRCam computer? 0=no, 1=yes

# set integration parameters
if not testLMIR: #set up integration parameters
    print 'Setting LMIRCam integration parameters'
    pi.setINDI("LMIRCAM.Command.text", str(Lsave)+" savedata", wait=True)
    pi.setINDI("LMIRCAM.Command.text", str(Lint)+" "+str(Lcoadd)+" "+str(Lseq)+" lbtintpar 500 sleep", wait=True)

# Get initial FPC/SPC settings (FYI)
settingsFPC  = pi.getINDI('Acromag.FPC_status.*')
#settingSPC  = pi.getINDI('Acromag.SPC_status.*')
tipFPC  = settingsFPC['Acromag.FPC_status.Tip']       # up/down, arc seconds
tiltFPC = settingsFPC['Acromag.FPC_status.Tilt']      # left/right, arc seconds
#pistFPC = settingsFPC['Acromag.FPC_status.Piston']    # in/out relative to center, microns; probably not needed here
#tipSPC  = settingsSPC['Acromag.SPC_status.Tip']       # up/down, arc seconds
#tiltSPC = settingsSPC['Acromag.SPC_status.Tilt']      # left/right, arc seconds


prefix = 'lm'
img = []

if testLMIR and useFileList: # parse input file list
    f = open(lmFileList,'rU')
    l = f.read() # concatenate into one line
    f.close()
    l = l.replace("\n"," ")
    fileList = l.split() # split on whitespace
    fileCt = 0
    #print l

# now,
# - save a first, 'original' frame from LMIRCam and retrieve it for analysis
# - clean up bias and bad px
# - find centroid
# - save a second frame
# - make, send SPC/FPC corrections
# - save successive frames, make corrections after each ad infinitum

# SAVE FIRST, ORIGINAL PSF
# [SET LSEQ = 1 FOR THIS ONE?]

if not testLMIR:
    print 'Taking LMIRCam original image...'
    pi.setINDI("LMIRCAM.Command.text","go",wait=True)
    f=pi.getFITS("LMIRCAM.DisplayImage.File", "LMIRCAM.GetDisplayImage.Now", wait=True)
    f.verify('fix')
    head = f[0].header
    imgb4 = f[0].data
    imgb4bk = bkgdsub(imgb4,'median',50)
    imgb4bk -= numpy.median(imgb4bk)
    fN = datadir+'lm_original.fits'
    pyfits.writeto(fN, imgb4bk, header=head, clobber=1)
elif testLMIR and useFileList:
    print 'Reading in file ' + fileList[fileCt]
    f = pyfits.open(fileList[fileCt])
    fileCt += 1
else:
    print 'No new LMIRCam image will be taken. Using whatever is in buffer.'
    #import current frame as PyFITS object...
    f=pi.getFITS("LMIRCAM.DisplayImage.File", "LMIRCAM.GetDisplayImage.Now", wait=True)

# get the image as an array. [0,0]=LL, [1023,0]=UL
if img==[]:
    img = f[0].data
else:
    img = numpy.dstack(( img, f[0].data ))
#print img.shape # a check


#### PROCESS ORIGINAL IMAGE

imgSubBP = processImg(img,'median')


#### FIND THE ORIGINAL PSF LOCATION

[orig_cy,orig_cx] = findStar(imgSubBP, cx, cy)
print [orig_cy,orig_cx]
img = [] # clear

#[USEFUL?]
#write the file to the wfs machine
#fileNames.append( datadir+prefix+'_%dZ%d.fits' % (round(a), mode) )
#print 'Saving LMIRCam frame as %s' % (fileNames[step])
#pyfits.writeto(fileNames[step], imgSubBP, header=head, clobber=1)

#####################################
#### NOW, TAKE SUCCESSIVE FRAMES ####
#####################################

# one frame for now; NEED TO MAKE THIS A FOR LOOP

# take or load LMIRCam img
if not testLMIR:
    print 'Taking new LMIRCam image...'
    pi.setINDI("LMIRCAM.Command.text","go",wait=True)
    #import current frame as PyFITS object...
    f=pi.getFITS("LMIRCAM.DisplayImage.File", "LMIRCAM.GetDisplayImage.Now", wait=True)
    f.verify('fix')
    head = f[0].header
    imgb4 = f[0].data
    imgb4bk = bkgdsub(imgb4,'median',50)
    imgb4bk -= numpy.median(imgb4bk)
    ####[CHANGE BELOW, SO AS TO INCLUDE NUMBERING; MAY NEED TO SEE LEECH SCRIPT]
    fN = datadir+'lm_before.fits'
    pyfits.writeto(fN, imgb4bk, header=head, clobber=1)
elif testLMIR and useFileList:
    print 'Reading in file ' + fileList[fileCt]
    f = pyfits.open(fileList[fileCt])
    fileCt += 1
else:
    print 'No new LMIRCam image will be taken. Using whatever is in buffer.'
    #import current frame as PyFITS object...
    f=pi.getFITS("LMIRCAM.DisplayImage.File", "LMIRCAM.GetDisplayImage.Now", wait=True)


#get the image as an array. [0,0]=LL, [1023,0]=UL
if img==[]:
    img = f[0].data
else:
    img = numpy.dstack(( img, f[0].data ))


#### PROCESS NEW IMAGE

imgSubBP = processImg(img,'median')


#### FIND THE NEW PSF LOCATION

[new_cy,new_cx] = findStar(imgSubBP, cx, cy)
img = [] # clear
print [new_cy,new_cx]


#### MEASURE DISTANCE MOVED

plateScale = 0.011 # asec per pixel (LMIRCam)
xDispPix = new_cx - orig_cx
yDispPix = new_cy - orig_cy
xDispAsec = xDispPix*plateScale
yDispAsec = yDispPix*plateScale

newtipFPC = -yDispPix # negative relative movement, to correct
newtiltFPC = -xDispPix

print newtipFPC
print newtiltFPC

# I'll worry about SPC next
#newtipSPC =
#newtiltSPC =


#### SEND CORRECTIONS TO SPC, FPC MIRRORS

# Get initial INDI values (FYI)
settingsFPC  = pi.getINDI('Acromag.FPC_status.*')
#settingsSPC  = pi.getINDI('Acromag.SPC_status.*')


# Get initial FPC/SPC settings (FYI)
tipFPC  = settingsFPC['Acromag.FPC_status.Tip']       # up/down, arc seconds
tiltFPC = settingsFPC['Acromag.FPC_status.Tilt']      # left/right, arc seconds
#pistFPC = settingsFPC['Acromag.FPC_status.Piston']    # in/out relative to center, microns; probably not needed here
#tipSPC  = settingsSPC['Acromag.SPC_status.Tip']       # up/down, arc seconds
#tiltSPC = settingsSPC['Acromag.SPC_status.Tilt']      # left/right, arc seconds

# Make sure we are not saving data, turn off continuous acquisition, and turn coadd mode on (much faster than taking individual images)
pi.setINDI("LMIRCAM.Command.text", "1 contacq 0 savedata 1 autodispwhat", wait=True)

# Print info
# print('Initial setpoint = %f degrees' % setpoint0)

#### set needed relative shifts
mode = 1; # 1 = relative to current; 0 = absolute
newsettingsFPC = settingsFPC
newsettingsFPC['Acromag.FPC_status.Tip'] = newtipFPC;        # up/down, arc seconds
newsettingsFPC['Acromag.FPC_status.Tilt'] = newtiltFPC;      # left/right, arc seconds
#newsettingsFPC['Acromag.FPC_status.Piston'] = newpist;    # in/out, microns
newsettingsFPC['Acromag.FPC_status.Mode'] = mode;         # 0 = absolute, 1 = relative to current
#newsettingsSPC['Acromag.SPC_status.Tip'] = newtipSPC;        # up/down, arc seconds
#newsettingsSPC['Acromag.SPC_status.Tilt'] = newtiltSPC;      # left/right, arc seconds
#newsettingsSPC['Acromag.SPC_status.Mode'] = mode;         # 0 = absolute, 1 = relative to current
#pi.setINDI(newsettingsFPC)
#pi.setINDI(newsettingsSPC)
