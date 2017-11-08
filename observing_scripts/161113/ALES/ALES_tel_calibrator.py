#!/usr/bin/python
import time
import sys
from pyindi import * 
import math
import numpy as np

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi = PyINDI(verbose=True)
side=sys.argv[1]

##################################################################
# USER INPUTS:                                                   #
##################################################################
dint=0.0# Don't saturate me.
nframes=30

dark_integration_time = dint#seconds
dark_coadds = 1
dark_frames = 2
darkIntParams = (dark_integration_time, dark_coadds, dark_frames)

light_integration_time = dint#seconds
light_coadds = 1
light_frames = nframes
lightIntParams = (light_integration_time, light_coadds, light_frames)

def wait4AORunning(side):
    pistr={'left':"LBTO.Dictionary.Name=L_AOStatus;Value=",
           'right':"LBTO.Dictionary.Name=R_AOStatus;Value="}[side]
    while True:
        pi.setINDI(pistr)
        status = pi.getINDI("LBTO.Dictionary.Value")
        time.sleep(0.02) 
        if status == "AORunning":
            break

def nod_sneakSomeDarks(XOff,YOff,side):
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY",
           "LBTO.OffsetPointing.OffsetX", XOff, 
           "LBTO.OffsetPointing.OffsetY", YOff, 
           "LBTO.OffsetPointing.Side", side, 
           "LBTO.OffsetPointing.Type", "REL", 
           timeout=400,
           wait=False) 
###where's FW2
    pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=DRK;Comment=observation type", wait=False)
    pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % darkIntParams, wait=True)
    fw2_pos = pi.getINDI("Lmir.lmir_FW2_status.PosNum", wait=True)
###offset FW2 to approximate a Blank
    pi.setINDI("Lmir.lmir_FW2.command", int(fw2_pos)+25000, timeout=20, wait=True)
###set integration parameters for darks
###take data
    pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
###put FW2 back
    pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % lightIntParams, wait=True)
    pi.setINDI("Lmir.lmir_FW2.command", int(fw2_pos), timeout=20, wait=True)
###put the integration parameters back
    
pi.setINDI("LMIRCAM.Command.text", "1 savedata", wait=True)
pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % lightIntParams, wait=True)
# take 10 up/down nod pairs
skyXOff=0
skyYOff=-2
priXOff=-1*skyXOff
priYOff=-1*skyYOff
for j in range(2):
    print j
#PRIMARY
# take frames and save the data
    print 'DO PRIMARY'
    print
    pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=SCI;Comment=observation type", wait=False)
    time.sleep(1)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
# use the last frame taken as the background for the next set
    pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)

# NOD TO SKY
    print 'Get Sky'
    print
    nod_sneakSomeDarks(skyXOff,skyYOff,side)
# wait for AO to close loop and stabilize for a second before taking next set
    wait4AORunning(side)
    pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=SKY;Comment=observation type", wait=False)
    time.sleep(1)
# take frames and save the data
    pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
# use the last frame taken as the background for the next set
    pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)

# NOD BACK TO PRIMARY
    print 'Go Back to Primary'
    print
    nod_sneakSomeDarks(priXOff,priYOff,side)
# wait for AO to close loop and stabilize for a second before taking next set
    wait4AORunning(side)

# end of script: set up to be compatible with the observer running in continuous mode
# turn off save data
pi.setINDI("LMIRCAM.Command.text","0 savedata",timeout=300,wait=True)
# set number of images to take to 1
