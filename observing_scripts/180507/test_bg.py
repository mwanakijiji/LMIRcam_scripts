from lmircam_tools import pi
from lmircam_tools.exposures import get_lmircam_frames_1bg
from lmircam_tools.utils import nod, rawbg, setFLAG


#################################################
# USER DEFINED PARAMETERS                       #
#################################################
#camera
dit = 0.7 
coadds = 1 # this should probably be 1
nseqs = 10
inner_loop_max = 10

#telesecope
reverse = False
nod_x = 0 #arcseconds in detector coords
nod_y = 5 
side = 'both'

N_cycles = 10

#################################################
# COMPUTATIONS/DEFINITIONS                      #
#################################################
nod_x = (-1*reverse)*nod_x 
nod_y = (-1*reverse)*nod_y
if reverse:
    nod_names = ('NOD_B','NOD_A')
else:
    nod_names = ('NOD_A','NOD_B')

#################################################
# COMMAND SEQUENCE                              #
#################################################
for ii in xrange(N_cycles):
    setFLAG(nod_names[0])
    get_lmircam_frames_1bg(dit, coadds, nseqs, inner_loop_max=inner_loop_max, save_data=False)
    #rawbg()
    print 'nodding'
    #nod(nod_x, nod_y, side)
    setFLAG(nod_names[1])
    get_lmircam_frames_1bg(dit, coadds, nseqs, inner_loop_max=inner_loop_max, save_data=False)
    #rawbg()
    print 'nodding'
    #nod(-1*nod_x, -1*nod_y, side)
setFLAG('')

