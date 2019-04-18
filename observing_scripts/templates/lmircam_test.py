from lmircam_tools import pi
from lmircam_tools.exposures import get_lmircam_frames
from lmircam_tools.utils import nod, setFLAG
from lmircam_tools.print_tools import info, request


#################################################
# USER DEFINED PARAMETERS                       #
#################################################
#camera
dit = 700              #  What integration time (millisec), will be set by server to closest possible integration time of the camera, which depends on setup.
coadds = 1             #  this should probably be 1
nseqs = 1              #  How many frames per nod?
use_bg = 0             #  1 True, 0 False.  Use a previously taken background.
savedata = False       #  Wanna save data?

nod_names = ('NOD_A','NOD_B')    #  How would you like the two nod positions to be flagged in the fits headers?

#################################################
# COMMAND SEQUENCE                              #
#################################################

setFLAG(nod_names[0])                                                          #  Set/update the nod position flag in the fits header.
pi.setINDI("lmircam_display.use_last_as_bg.value=On")
get_lmircam_frames(dit, coadds, nseqs, use_bg=use_bg, save_data=savedata)      #  

setFLAG(nod_names[1])                                                          #  Set/update the nod position flag in the fits header.
pi.setINDI("lmircam_display.use_last_as_bg.value=On")
get_lmircam_frames(dit, coadds, nseqs, use_bg=use_bg, save_data=savedata)      #  

