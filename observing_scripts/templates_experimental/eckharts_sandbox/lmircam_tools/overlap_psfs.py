import sys, os, string, time, pdb, copy, pyfits
import numpy as np
from pyindi import * 
from scipy import ndimage, sqrt, stats
import matplotlib.pyplot as plt
from lmircam_tools import * #process_readout

autoFindStar = True  # auto-detect star in frame?


### BEGIN FCNS

# find star and return coordinates [y,x]
def findStar(image):
    if autoFindStar:

        #imageThis = numpy.copy(image)

        '''
        if (PSFside == 'left'):
            imageThis[:,1024:-1] = 0
        elif (PSFside == 'right'):
            imageThis[:,0:1024] = 0
        '''

        imageG = ndimage.gaussian_filter(image, 6) # further remove effect of bad pixels (somewhat redundant?)
        loc = numpy.argwhere(imageG==imageG.max())
        cx = loc[0,1]
        cy = loc[0,0]

        #plt.imshow(imageG, origin="lower")
        #pdb.set_trace()
        #plt.scatter([cx,cx],[cy,cy], c='r', s=50)
        #plt.colorbar()
        #plt.show()
        #print [cy, cx] # check

    return [cy, cx]


def dist_pix(current,goal):

    dist = np.sqrt(np.power((current[1]-goal[1]),2) + np.power((current[0]-goal[0]),2) )

    return dist

### END FCNS


def overlap_airy_psfs(psf_loc_setpoint):

    ### move in half-moon to see SX first
    pi.setINDI("Lmir.lmir_FW2.command", 'SX-Half-moon', wait=True)#, timeout=45, wait=True)


    ### iterate to try to get SX PSF on the same pixel
    while True: 

        ### locate SX PSF
        f=pi.getFITS("LMIRCAM.DisplayImage.File", "LMIRCAM.GetDisplayImage.Now", wait=True) # get what LMIR is seeing
        imgb4 = f[0].data
        #imgb4bk = bkgdsub(imgb4,'median') # simple background smoothing
        #imgb4bk -= numpy.median(imgb4bk) # subtract residual background

        imgb4bk = processImg(imgb4, 'median') # return background-subtracted, bad-pix-corrected image
        psf_loc = findStar(imgb4bk) # locate the PSF

        ### move FPC in one step to move PSF to right location
        vector_move_pix = np.subtract(psf_loc_setpoint,psf_loc) # vector of required movement in pixel space
        vector_move_asec = np.multiply(vector_move_pix,0.0107) # convert to asec
        pi.setINDI("Acromag.FPC.Tip="+'{0:.1f}'.format(vector_move_asec[0])+";Tilt="+'{0:.1f}'.format(vector_move_asec[1])+";Piston=0;Mode=1")

        ### re-locate SX PSF; correction needed?
        f=pi.getFITS("LMIRCAM.DisplayImage.File", "LMIRCAM.GetDisplayImage.Now", wait=True) # get what LMIR is seeing
        imgb4 = f[0].data
        imgb4bk = processImg(imgb4, 'median') # return background-subtracted, bad-pix-corrected image
        psf_loc = findStar(imgb4bk) # locate the PSF
 
        print('-------------------')
        print('PSF location setpoint:')
        print(psf_loc_setpoint) 
        print('Current PSF loc:') 
        print(psf_loc)
    
        if (dist_pix(psf_loc,psf_loc_setpoint) < 5.):
            print('-------------------')
            print('Done moving one side. Switching to the other side.')
            break 

        print('Moving PSF again...')
    
    
    ### MOVE IN HALF-MOON TO SEE DX NEXT
    pi.setINDI("Lmir.lmir_FW2.command", 'DX-Half-moon', wait=True)
   
    
    ### NEW FOR-LOOP HERE
    while True: # do three iterations to try to get SX PSF on the same pixel
    
        # locate DX PSF
        f=pi.getFITS("LMIRCAM.DisplayImage.File", "LMIRCAM.GetDisplayImage.Now", wait=True) # get what LMIR is seeing
        imgb4 = f[0].data
                        
        imgb4bk = processImg(imgb4, 'median') # return background-subtracted, bad-pix-corrected image
        psf_loc = findStar(imgb4bk) # locate the PSF
                                
        ### MOVE HPC IN ONE STEP TO MOVE PSF TO RIGHT LOCATION
        vector_move_pix = np.subtract(psf_loc_setpoint,psf_loc) # vector of required movement in pixel space
        vector_move_asec = np.multiply(vector_move_pix,0.0107) # convert to asec
        pi.setINDI("Acromag.HPC.Tip="+'{0:.1f}'.format(vector_move_asec[0])+";Tilt="+'{0:.1f}'.format(vector_move_asec[1])+";Piston=0;Mode=1")
                                                
        ### RE-LOCATE SX PSF; CORRECTION NEEDED?
        f=pi.getFITS("LMIRCAM.DisplayImage.File", "LMIRCAM.GetDisplayImage.Now", wait=True) # get what LMIR is seeing
        imgb4 = f[0].data
        imgb4bk = processImg(imgb4, 'median') # return background-subtracted, bad-pix-corrected image
        psf_loc = findStar(imgb4bk) # locate the PSF
    
        print('-------------------')
        print('PSF location setpoint:')
        print(psf_loc_setpoint) 
        print('Current DX PSF loc:')
        print(psf_loc)
                                                                            
        if (dist_pix(psf_loc,psf_loc_setpoint) < 5.):
            print('-------------------')
            print('Done moving DX. Switching to the other side.')
            break
                                                                                                    
        print('Moving DX again...')    


    print('Done moving PSFs. Reopening LMIR FW2.')
    pi.setINDI("Lmir.lmir_FW2.command", 'Open', wait=True)

    ############## END PSF OVERLAP
