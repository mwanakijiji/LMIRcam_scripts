#!/usr/bin/python
import sys
from pyindi import * 
from ALESutils import do_exposures

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
slight_frames = 30.

#NOMIC
Nslight_integration_time = 2#seconds
nomic_coadds=1
Nslight_frames = 13

#DETXY Nod vector asecs
Nodx = 5
Nody = 0

##################################################################
# END USER INPUTS                                                #
##################################################################
def wait4AORunning(side):
    pistr={'left':"LBTO.Dictionary.Name=L_AOStatus;Value=",
           'right':"LBTO.Dictionary.Name=R_AOStatus;Value="}[side]
    while True:
        pi.setINDI(pistr)
        status = pi.getINDI("LBTO.Dictionary.Value")
        time.sleep(0.02) 
        if status == "AORunning":
            break

def nod_sneakSomeDarks(XOff,YOff,darkIntParams,side):
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
    pi.setINDI("Lmir.lmir_FW2.command", int(fw2_pos), timeout=20, wait=True)
    ###put the integration parameters back

slightIntParams = (slight_integration_time, light_coadds, slight_frames)
NslightIntParams = (Nslight_integration_time, nomic_coadds, Nslight_frames)

#set up cameras
pi.setINDI("LMIRCAM.Command.text", "0 loglevel") 
pi.setINDI("LMIRCAM.Command.text", "0 contacq", wait=True)
pi.setINDI("LMIRCAM.Command.text", "1 savedata", wait=True)

pi.setINDI("NOMIC.Command.text", "0 contacq", wait=True)
pi.setINDI("NOMIC.Command.text", "1 savedata", wait=True)
pi.setINDI("NOMIC.Command.text", "%f %i %i lbtintpar" % Nintparams, wait=True)

for j in range(4):
    print 'COLLECT PRIMARY POSITION FRAMES, cycle: ', j
    print
    do_exposures(slightIntParams, 'PRI', side)

# NOD TO SKY
    print 'NOD to Sky position, cycle', j
    print
    nod_sneakSomeDarks(Nodx,Nody,darkIntParams,side)
    wait4AORunning(side)
    print 'COLLECT SKY POSITION FRAMES, cycle: ', j
    print
    do_exposures(slightIntParams, 'SKY', side)
    #lmircam can't handle subtracting a dark
    #pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)

# NOD BACK TO PRIMARY
    print 'NOD to Primary position, cycle: ', j
    print
    nod_sneakSomeDarks(Nodx,Nody,darkIntParams,side)
    wait4AORunning(side)

pi.setINDI("LMIRCAM.Command.text","0 savedata",timeout=300,wait=True)
