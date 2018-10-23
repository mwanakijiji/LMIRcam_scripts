from lmircam_tools import pi
from lmircam_tools.exposures import get_lmircam_frames
from lmircam_tools.utils import nod, rawbg, setFLAG


#################################################
# USER DEFINED PARAMETERS                       #
#################################################
#camera
dit = 0.0 
coadds = 1 # this should probably be 1
nseqs = 1000
inner_loop_max = 10
go_nomic = True

#telesecope
reverse = False
nod_x = 1.5 #arcseconds in detector coords
nod_y = 0 
side = 'both'

N_cycles = 1

#################################################
# COMPUTATIONS/DEFINITIONS                      #
#################################################
if reverse:
    nod_x = -1.0*nod_x 
    nod_y = -1.0*nod_y
if reverse:
    nod_names = ('NOD_B','NOD_A')
else:
    nod_names = ('NOD_A','NOD_B')

#################################################
# COMMAND SEQUENCE                              #
#################################################
for ii in xrange(N_cycles):
    setFLAG(nod_names[0])
    if go_nomic:
      pi.setINDI('NOMIC.Command.text', 'go', wait=False)
    get_lmircam_frames(dit, coadds, nseqs, inner_loop_max=inner_loop_max)
    #rawbg()
    print 'nodding'
    nod(nod_x, nod_y, side)
    setFLAG(nod_names[1])
    if go_nomic:
      pi.setINDI('NOMIC.Command.text', 'go', wait=False)
    get_lmircam_frames(dit, coadds, nseqs, inner_loop_max=inner_loop_max)
    #rawbg()
    print 'nodding'
    nod(-1*nod_x, -1*nod_y, side)
setFLAG('')

