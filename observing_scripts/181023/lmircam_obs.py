from lmircam_tools import pi
from lmircam_tools.exposures import get_lmircam_frames, get_lmircam_bg
from lmircam_tools.utils import nod, setFLAG
from lmircam_tools.print_tools import info, request


#################################################
# USER DEFINED PARAMETERS                       #
#################################################
#camera
dit = 60000              #  What integration time (millisec), will be set by server to closest possible integration time of the camera, which depends on setup.
coadds = 1             #  this should probably be 1
nseqs = 10             #  How many frames per nod?  Make it at least 2!
use_bg = 1             #  1 True, 0 False.  Use a previously taken background.
savedata = True       #  Wanna save data?

#telesecope
reverse = False        #  If True, this inverts the nodding cycle (e.g., it will start on the right instead of the left).
nod_x = 0              #  Nod throw in arcseconds in detector coords. If positive and inverse = False, the first nod will go to the right.
nod_y = 5              #  Nod throw in arcseconds in detector coords. If positive and inverse = False, the first nod will go up.
side = 'both'          #  Which side to nod.  Can be 'left', 'right', or 'both'.

N_cycles = 4          #  How many nodding cycles should be executed by this script with a single execution?

nod_names = ('NOD_A','NOD_B')    #  How would you like the two nod positions to be flagged in the fits headers?

#################################################
# COMPUTATIONS/DEFINITIONS                      #
#################################################
if reverse:                             #  This inverts the nodding direction if reverse = True
    nod_x = -1.0*nod_x                  #  Change sign of the x nod throw.
    nod_y = -1.0*nod_y                  #  Change sign of the y nod throw.
    nod_names = nod_names[::-1]         #  Also flip order of nod position flags.

#################################################
# COMMAND SEQUENCE                              #
#################################################
for ii in xrange(N_cycles):                                                        #  Execute all nodding cycles.
    setFLAG(nod_names[0])                                                          #  Set/update the nod position flag in the fits header.
    get_lmircam_frames(dit, coadds, nseqs-1, use_bg=use_bg, save_data=savedata)    #  Take nseqs-1 frames (because one more will be taken in the next line for a total of nseqs).
    get_lmircam_bg(dit, coadds, save_data=savedata)                                #  Take another frame to be used as background in the next nod position if use_bg = 1.

    info('nodding')
#    nod(nod_x, nod_y, side)                                                        #  Nodding to other position.
    setFLAG(nod_names[1])                                                          #  Set/update the nod position flag in the fits header.
    get_lmircam_frames(dit, coadds, nseqs-1, use_bg=use_bg, save_data=savedata)    #  Take nseqs-1 frames (because one more will be taken in the next line for a total of nseqs).
    get_lmircam_bg(dit, coadds, save_data=savedata)                                #  Take another frame to be used as background in the next nod position if use_bg = 1.

    info('nodding')
#    nod(-1*nod_x, -1*nod_y, side)                                                  #  Nodding back to first position.
setFLAG('')                                                                        #  Resetting flag in order not to confuse any data taken later.
