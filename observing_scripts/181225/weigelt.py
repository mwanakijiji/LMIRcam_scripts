from lmircam_tools import pi
from lmircam_tools.exposures import get_lmircam_frames
from lmircam_tools.utils import nod, setFLAG
from lmircam_tools.print_tools import info, request


#################################################
# USER DEFINED PARAMETERS                       #
#################################################
#camera
dit = 150              #  What integration time (millisec), will be set by server to closest possible integration time of the camera, which depends on setup.
coadds = 1             #  this should probably be 1
nseqs = 300             #  How many frames per nod?
use_bg = 1             #  1 True, 0 False.  Use a previously taken background.
savedata = True       #  Wanna save data?

get_lmircam_frames(dit, coadds, nseqs, use_bg=use_bg, save_data=savedata)      #  
pi.setINDI("LMIRCAM.use_as_bg.value=On")

