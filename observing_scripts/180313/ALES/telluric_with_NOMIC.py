#!/usr/bin/python
import sys
from pyindi import * 
from ALESutils import wait4AORunning, do_exposures

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

plight_integration_time = dint#seconds
light_coadds = 1.
plight_frames = 5.

#NOMIC
Nplight_integration_time = 3#seconds
nomic_coadds=1
Nplight_frames = 3

##################################################################
# END USER INPUTS                                                #
##################################################################
lightIntParams = (plight_integration_time, light_coadds, plight_frames)
NlightIntParams = (Nplight_integration_time, nomic_coadds, Nplight_frames)

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


pi.setINDI("LMIRCAM.Command.text", "0 loglevel") 
pi.setINDI("LMIRCAM.Command.text", "0 contacq", wait=True)
pi.setINDI("LMIRCAM.Command.text", "1 savedata", wait=True)

for j in range(4):
    print 'COLLECT PRIMARY POSITION FRAMES, cycle: ', j
    print
    do_exposures(lightIntParams,NlightIntParams,'PRI', side)

# NOD to sky
    print 'NOD to sky position, cycle', j
    print
    nod_sneakSomeDarks(4,4,side)
    wait4AORunning(side)
    print 'COLLECT sky, cycle: ', j
    print
    do_exposures(lightIntParams,NlightIntParams,'SKY', side)
# NOD BACK TO PRIMARY
    print 'NOD to Primary position, cycle: ', j
    print
    nod_sneakSomeDarks(-4,-4,side)
    wait4AORunning(side)

pi.setINDI("LMIRCAM.Command.text","0 savedata",timeout=300,wait=True)
