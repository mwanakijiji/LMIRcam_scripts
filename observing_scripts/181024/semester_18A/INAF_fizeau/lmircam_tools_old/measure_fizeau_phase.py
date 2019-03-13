import pyfits
import numpy as np
from lmircam_tools import pi
from lmircam_tools.exposures import get_lmircam_frames
from datetime import datetime
from time import sleep
import glob

def get_amps_and_phases(fringe_im):
    #shift before fft to make sure no checkerboard. this shift actually
    #undoes the shift done by make_fizeau_fringe. shift after fft also
    #to put things where you expect
    fft_sh_im = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(fringe_im)))
    return np.absolute(fft_sh_im), (2*np.pi+np.angle(fft_sh_im))%(2*np.pi)

def measure_fizeau_phase(bgfn,x,y):
    '''Measure the phase of a Fizeau fringe in the last saved image
    bgfn: (int) the filenumber corresponding to the background frame
    x:    (int) the x position of the fringe on the detector
    y:    (int) the y positoin of the fringe on the detector
    CAUTION: x, y correspond to the position in the SAVED frame
    These may be different from the position on the screen if you are
    using a subframe or if you are in slow mode...
    Could fix this by being smarter....'''

    bg = pyfits.open('/mnt/iscsi/lmircam/L0/' + 
                     date + '/lm_' + date + '_' +
                      str(bgfn).zfill(6) + 
                      '.fits')['Primary'].data.astype(np.float)

    filelist = glob.glob('/mnt/iscsi/lmircam/L0/'+date+'/lm_*.fits')
    if len(filelist) == 0: file_number = 0
    else: file_number = int(np.sort(filelist)[-1][-11:-5])

    frame = pyfits.open('/mnt/iscsi/lmircam/L0/' + 
                        date + '/lm_' + date + '_' + 
                        str(file_number).zfill(6) + 
                        '.fits')['Primary'].data.astype(np.float)

    stamp = (frame-bg)[y-100:y+100,x-100:x+100]

    amps, angles = get_amps_and_phases(stamp)
#do something...
