from lmircam_tools import pi
from lmircam_tools.exposures import get_lmircam_frames
from lmircam_tools.utils import nod, rawbg


#################################################
# USER DEFINED PARAMETERS                       #
#################################################

dit = 0.7 
coadds = 1 # this should probably be 1
nseqs = 50

nod_x = -4.5 #arcseconds in detector coords
nod_y = 0
side = 'both'

N_cycles = 10

#################################################
# /USER DEFINED PARAMETERS                       #
#################################################

for ii in xrange(N_cycles):
    get_lmircam_frames(dit, coadds, nseqs)
    rawbg()
    print 'nodding'
    #nod(nod_x, nod_y, side)
    get_lmircam_frames(dit, coadds, nseqs)
    rawbg()
    print 'nodding'
    #nod(-1*nod_x, -1*nod_y, side)

