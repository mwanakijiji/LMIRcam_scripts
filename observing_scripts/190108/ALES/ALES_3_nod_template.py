#!/usr/bin/python
import time
import sys
sys.path.append('/home/observer/Scripts/observing_scripts/templates/')
from pyindi import * 
import math
import numpy as np
from lmircam_tools.utils import wait4AORunning, setFLAG
from lmircam_tools.ALESutils import get_ales_frames, nod_sneakSomeDarks, ten, makeOffsets

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi = PyINDI(verbose=True)
side=sys.argv[1]

##################################################################
# USER INPUTS:                                                   #
##################################################################
dint=1.4
dark_integration_time = dint#seconds
dark_coadds = 1
dark_frames = 1

plight_integration_time = dint#seconds
slight_integration_time = dint#seconds
light_coadds = 1
plight_frames = 2
slight_frames = 5

Nseqs = 4

primary_RA =  #[23,7,28.715] HH, MM, SS.ff
primary_Dec = #[21,8,3.3053] DD, MM, SS.ff
secondary_sep = #1.7176 arcseconds
secondary_PA = #65.46 degrees E of N
##################################################################
# END USER INPUTS                                                #
##################################################################

darkIntParams = (dark_integration_time*1000, dark_coadds, dark_frames)
plightIntParams = (plight_integration_time*1000, light_coadds, plight_frames)
slightIntParams = (slight_integration_time*1000, light_coadds, slight_frames)

priRAOff, priDecOff, secRAOff, secDecOff, skyRAOff, skyDecOff = makeOffsets(primary_RA, primary_Dec, secondary_sep, secondary_PA)

pi.setINDI("LMIRCAM.enable_save.value=On" , wait=True)
for j in range(Nseqs):
    print j
    print 'DO PRIMARY ', j
    print
    get_ales_frames(*plightIntParams,side=side, use_bg=True,save_data=True,flag='PRI')

# NOD TO SECONDARY
    print 'Get Secondary ', j
    print
    nod_sneakSomeDarks(secRAOff,secDecOff,darkIntParams,side,coords="RADEC",absrel="ABS")
    wait4AORunning(side)
    print 'begin Secondary ', j
    print
    get_ales_frames(*slightIntParams,side=side, use_bg=True,save_data=True,flag='SEC')
# NOD TO SKY
    print 'Get Sky ', j
    print
    nod_sneakSomeDarks(skyRAOff,skyDecOff,darkIntParams,side,coords="RADEC",absrel="ABS")
    wait4AORunning(side)
    print 'begin Sky ', j
    print
    get_ales_frames(*slightIntParams,side=side, use_bg=True,save_data=True,flag='SKY')
    pi.setINDI("LMIRCAM.use_as_bg.value=On")

# NOD BACK TO PRIMARY
    print 'Go Back to Primary ', j
    print
    nod_sneakSomeDarks(priRAOff,priDecOff,darkIntParams,side,coords="RADEC",absrel="ABS")
    wait4AORunning(side)

pi.setINDI("LMIRCAM.enable_save.value=On" , wait=True)
