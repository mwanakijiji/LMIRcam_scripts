from lmircam_tools import pi
from lmircam_tools.exposures import get_lmircam_frames
from lmircam_tools.utils import nod, rawbg
#################################################
# USER DEFINED PARAMETERS                       #
#################################################
dit = 0
coadds = 1 # this should probably be 1
nseqs = 10

nod_x = 7 #arcseconds in detector coords
nod_y = 0
side = 'left'

N_cycles = 2

#################################################
# /USER DEFINED PARAMETERS                       #
#################################################

for ii in xrange(N_cycles):
    print ''
    print 'Starting nodding cycle #' + str(ii+1) + ' of ' + str(N_cycles)

    get_lmircam_frames(dit, coadds, nseqs, inner_loop_max=10)
    rawbg()
    nod(nod_x, nod_y, side)

    get_lmircam_frames(dit, coadds, nseqs, inner_loop_max=10)
    rawbg()
    nod(-1*nod_x, -1*nod_y, side)

