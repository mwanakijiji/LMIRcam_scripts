#!/usr/bin/python
import time
import sys
sys.path.append('/home/observer/Scripts/observing_scripts/templates/')
from pyindi import * 
import math
import numpy as np
from lmircam_tools.utils import wait4AORunning, setFLAG
from lmircam_tools.ALESutils import get_ales_frames, nod_sneakSomeDarks

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi = PyINDI(verbose=False)
side=sys.argv[1]

##################################################################
# USER INPUTS:                                                   #
##################################################################
dark_integration_time = 1.4#seconds
dark_coadds = 1
dark_frames = 1

light_integration_time = 1.4#seconds
light_coadds = 1
light_frames = 15 #nseqs for camera

skyXOff=0
skyYOff=-3 #Detxy arcseconds

Nseqs = 2 #number of nod pairs
##################################################################
# /USER INPUTS:                                                   #
##################################################################

darkIntParams = (dark_integration_time*1000, dark_coadds, dark_frames)#seconds to milliseconds
lightIntParams = (light_integration_time*1000, light_coadds, light_frames)

pi.setINDI("LMIRCAM.enable_save.value=On" , wait=True)
priXOff=-1*skyXOff
priYOff=-1*skyYOff
for j in range(Nseqs):
    print j
#PRIMARY
# take frames and save the data
    print 'DO PRIMARY'
    print 
#python star syntax below...
    get_ales_frames(*lightIntParams,side=side, use_bg=True,save_data=True,flag='PRI')

# NOD TO SKY
    print 'Get Sky'
    print
    nod_sneakSomeDarks(skyXOff,skyYOff,darkIntParams,side,coords="DETXY", absrel="REL")
# wait for AO to close loop and stabilize for a second before taking next set
    wait4AORunning(side)
    get_ales_frames(*lightIntParams,side=side, use_bg=True,save_data=True,flag='SKY')
    pi.setINDI("LMIRCAM.use_as_bg.value=On")

# NOD BACK TO PRIMARY
    print 'Go Back to Primary'
    print
    nod_sneakSomeDarks(priXOff,priYOff,darkIntParams,side,coords="DETXY",absrel="REL")
    wait4AORunning(side)
    

# end of script: set up to be compatible with the observer running in continuous mode
# turn off save data
pi.setINDI("LMIRCAM.enable_save.value=On" , wait=True)
