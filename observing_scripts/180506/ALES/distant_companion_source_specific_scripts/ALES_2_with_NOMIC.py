#!/usr/bin/python
import sys
from pyindi import * 
from ALESutils import wait4AORunning, makeOffsets, nod_sneakSomeDarksDETXY, do_exposures

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi = PyINDI(verbose=False)
side=sys.argv[1]

##################################################################
# USER INPUTS:                                                   #
##################################################################
dint=2
#LMIRCAM
dark_integration_time = dint#seconds
dark_coadds = 1
dark_frames = 1
darkIntParams = (dark_integration_time, dark_coadds, dark_frames)

slight_integration_time = dint#seconds
light_coadds = 1.
plight_frames = 2.
slight_frames = 30.

#NOMIC
Nslight_integration_time = 0#seconds
nomic_coadds=1
Nplight_frames = 1
Nslight_frames = 1

Xoff = 5
Yoff = 5
##################################################################
# END USER INPUTS                                                #
##################################################################

slightIntParams = (slight_integration_time, light_coadds, slight_frames)

NslightIntParams = (Nslight_integration_time, nomic_coadds, Nslight_frames)

pi.setINDI("LMIRCAM.Command.text", "0 loglevel") 
pi.setINDI("LMIRCAM.Command.text", "0 contacq", wait=True)
pi.setINDI("LMIRCAM.Command.text", "1 savedata", wait=True)

for j in range(2):
    print 'COLLECT PRIMARY POSITION FRAMES, cycle: ', j
    print
    do_exposures(slightIntParams,NslightIntParams,'SCI', side)

# NOD TO SKY
    print 'NOD to Sky position, cycle', j
    print
    nod_sneakSomeDarksDETXY(Xoff,Yoff,darkIntParams,side)
    wait4AORunning(side)
    print 'COLLECT SKY POSITION FRAMES, cycle: ', j
    print
    do_exposures(slightIntParams,NslightIntParams,'SKY', side)
    #lmircam can't handle subtracting a dark
    #pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)

# NOD BACK TO PRIMARY
    print 'NOD to Primary position, cycle: ', j
    print
    nod_sneakSomeDarksDETXY(-1*Xoff,-1*Yoff,darkIntParams,side)
    wait4AORunning(side)

pi.setINDI("LMIRCAM.Command.text","0 savedata",timeout=300,wait=True)
