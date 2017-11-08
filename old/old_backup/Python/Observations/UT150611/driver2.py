import sys, os, string, time, pyfits,  pdb, copy
import numpy
from pyindi import *
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

print 'Taking original LMIRCam up nod image...'
pi.setINDI("LMIRCAM.Command.text","go",wait=True)
f=pi.getFITS("LMIRCAM.DisplayImage.File", "LMIRCAM.GetDisplayImage.Now", wait=True)
f.verify('fix')
head = f[0].header
imgb4 = f[0].data
imgb4bk = bkgdsub(imgb4,'median')
imgb4bk -= numpy.median(imgb4bk)
fN = datadir+'lm_original.fits'
pyfits.writeto(fN, imgb4bk, header=head, clobber=1)

print 'done'
