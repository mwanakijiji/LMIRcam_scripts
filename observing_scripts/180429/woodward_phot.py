import sys
from pyindi import *
from lmircam_tools.utils import setFLAG, wait4AORunning, nod
from lmircam_tools.exposures import 
pi = PyINDI(verbose=False)

#################################################
# USER DEFINED PARAMETERS                       #
#################################################
#camera
#LMIRCAM
L_dit = 2
L_coadds = 1 # this should probably be 1
L_nseqs = 30
inner_loop_max = 10

#NOMIC
N_dit = 2 
N_coadds = 1 
N_nseqs = 13

#telesecope
reverse = False
nod_x = 0 #arcseconds in detector coords
nod_y = 5 
side = 'both'

N_cycles = 10

#################################################
# COMPUTATIONS/DEFINITIONS                      #
#################################################
Lintparams = (L_dit, L_coadds, L_nseqs)
Nintparams = (N_dit, N_coadds, N_nseqs)

nod_x = (-1*reverse)*nod_x 
nod_y = (-1*reverse)*nod_y
if reverse:
    nod_names = ('NOD_B','NOD_A')
else:
    nod_names = ('NOD_A','NOD_B')

def do_exposures(Lintparams,Nintparams,flag, inner_loop_max=10):
    #get NOMIC going
    pi.setINDI("NOMIC.Command.text", "0 contacq", wait=True)
    pi.setINDI("NOMIC.Command.text", "1 savedata", wait=True)
    pi.setINDI("NOMIC.Command.text", "%f %i %i lbtintpar" % Nintparams, wait=True)
    time.sleep(0.3)
    pi.setINDI("NOMIC.Command.text","go",timeout=300,wait=False)

    #Get lmircam going, fuss to avoid bad rows with too many nseqs...
    dit, coadds, nseqs = Lintparams
    coadds = int(coadds)
    nseqs = int(nseqs)
    inner_loop_max = int(inner_loop_max)
    N_outer_loops = nseqs / inner_loop_max
    remainder = nseqs % inner_loop_max
    if N_outer_loops == 0:
        lbtintparams = (dit, coadds, nseqs)
    else:
        lbtintparams = (dit, coadds, inner_loop_max)

    pi.setINDI("LMIRCAM.Command.text", "0 contacq", wait=True)
    pi.setINDI("LMIRCAM.Command.text", "1 savedata", wait=True)
    pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % lbtintparams, wait=True)
    #first loop
    pi.setINDI("LMIRCAM.Command.text","go",timeout=(8*dit*coadds*inner_loop_max),wait=True)
    #other loops
    for ii in xrange(max(0,N_outer_loops-1)):
        pi.setINDI("LMIRCAM.Command.text","go",timeout=(8*dit*coadds*inner_loop_max),wait=True)
    if remainder > 0:
        pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % (dit, coadds, remainder), wait=True)
        pi.setINDI("LMIRCAM.Command.text","go",timeout=(8*dit*coadds*nseqs),wait=True) 

#################################################
# COMMAND SEQUENCE                              #
#################################################
for ii in xrange(N_cycles):
    do_exposures(Lintparams, Nintparams, nod_names[0], inner_loop_max=inner_loop_max)
    #rawbg()
    print 'nodding'
    nod(nod_x, nod_y, side)
    do_exposures(Lintparams, Nintparams, nod_names[1], inner_loop_max=inner_loop_max)
    #rawbg()
    print 'nodding'
    nod(-1*nod_x, -1*nod_y, side)
setFLAG('')


