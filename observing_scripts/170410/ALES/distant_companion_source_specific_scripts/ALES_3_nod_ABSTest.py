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
dint=0.
dark_integration_time = dint#seconds
dark_coadds = 1
dark_frames = 3
darkIntParams = (dark_integration_time, dark_coadds, dark_frames)

plight_integration_time = dint#seconds
slight_integration_time = dint#seconds
light_coadds = 1
plight_frames = 10
slight_frames = 10
##################################################################
# END USER INPUTS                                                #
##################################################################

plightIntParams = (plight_integration_time, light_coadds, plight_frames)
slightIntParams = (slight_integration_time, light_coadds, slight_frames)

primary_RA =  [14,50,15.81]
primary_Dec = [23,54,42.64]
#from Ginski 2013
secondary_sep = 4.560
secondary_PA = 126.6

def ten(coord):
    '''change a sexageismal to a decimal
    INPUTS:
    coord a python list [hh/dd, mm, ss]'''
    coord=np.array(coord)
    num=len(coord)
    fac=np.array([1.,60.0,3600.0])
    if (coord < 0).sum() > 0:
        sign=-1
    else:
        sign=1
    return sign*(np.abs(coord)/fac[:num]).sum()

def wait4AORunning(side):
    pistr={'left':"LBTO.Dictionary.Name=L_AOStatus;Value=",
           'right':"LBTO.Dictionary.Name=R_AOStatus;Value="}[side]
    while True:
        pi.setINDI(pistr)
        status = pi.getINDI("LBTO.Dictionary.Value")
        time.sleep(0.02) 
        if status == "AORunning":
            break

def makeOffsets(RA,Dec,sep,PA):
    '''Take the RA and Dec of the primary, and the 
    separation and PA of the secondary, and return
    the appropriate nod vectors for 3-point dither
    pattern.
    PA East of North. North up East left.
    INPUTS:
    RA = [hh, mm, ss.dd]
    Dec = [dd, mm, ss.dd]
    sep = arcseconds
    PA = degrees'''
    secDecOff = -1*sep*np.cos(PA*np.pi/180.)#arcseconds
    secRAOff = -1*sep*np.sin(PA*np.pi/180.)#arcseconds NO cos(dec)!!!

    skyDecOff = secDecOff+3
    skyRAOff = 0

    priDecOff = 0 #ABS offsets, from pointing center, which is primary after "absorb"
    priRAOff = 0
    return priRAOff, priDecOff, secRAOff, secDecOff, skyRAOff, skyDecOff
    
#ABS nods, must align to ALES sweetspot, then absorb the alignment using the PCSGUI
#launched from an obs machine
def nod_sneakSomeDarks(RAOff,DecOff,side):
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "RADEC",
           "LBTO.OffsetPointing.OffsetX", DecOff, 
           "LBTO.OffsetPointing.OffsetY", RAOff, 
           "LBTO.OffsetPointing.Side", side, 
           "LBTO.OffsetPointing.Type", "ABS", 
           timeout=400,
           wait=False) 
    time.sleep(0.5)
	###where's FW2
    #pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=DRK;Comment=observation type", wait=False)
    #pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % darkIntParams, wait=True)
    #fw2_pos = pi.getINDI("Lmir.lmir_FW2_status.PosNum", wait=True)
    #pi.setINDI("Lmir.lmir_FW2.command", int(fw2_pos)+25000, timeout=20, wait=True)
    #pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
    #pi.setINDI("Lmir.lmir_FW2.command", int(fw2_pos), timeout=20, wait=True)

def do_exposures(intparams,flag,RAOff,DecOff):
    pi.setINDI("LMIRCAM.Command.text", "1 savedata")
    pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % intparams, wait=True)
    pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=%s ;Comment=observation type"%flag, wait=False)
    pi.setINDI("LMIRCAM.EditFITS.Keyword=OFFSTRA;Value=%s ;Comment=RA offset commanded to here"%RAOff, wait=False)
    pi.setINDI("LMIRCAM.EditFITS.Keyword=OFFSTDC;Value=%s ;Comment=Dec offset commanded to here"%DecOff, wait=False)
    time.sleep(1)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
        
priRAOff, priDecOff, secRAOff, secDecOff, skyRAOff, skyDecOff = makeOffsets(primary_RA, primary_Dec, secondary_sep, secondary_PA)

pi.setINDI("LMIRCAM.Command.text", "0 contacq")
pi.setINDI("LMIRCAM.Command.text", "1 savedata", wait=True)
pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % plightIntParams, wait=True)
for j in range(4):
    print j
    print 'DO PRIMARY ', j
    print
    do_exposures(plightIntParams,'PRI',priRAOff,priDecOff)

# NOD TO SECONDARY
    print 'Get Secondary ', j
    print
    nod_sneakSomeDarks(secRAOff,secDecOff,side)
    wait4AORunning(side)
    print 'begin Secondary ', j
    print
    do_exposures(slightIntParams,'SEC',secRAOff,secDecOff)
# NOD TO SKY
    print 'Get Sky ', j
    print
    nod_sneakSomeDarks(skyRAOff,skyDecOff,side)
    wait4AORunning(side)
    print 'begin Sky ', j
    print
    do_exposures(slightIntParams,'SKY', skyRAOff, skyDecOff)
    pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)

# NOD BACK TO PRIMARY
    print 'Go Back to Primary ', j
    print
    nod_sneakSomeDarks(priRAOff,priDecOff,side)
    wait4AORunning(side)

pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % slightIntParams, wait=True)
pi.setINDI("LMIRCAM.Command.text","0 savedata",timeout=300,wait=True)
pi.setINDI("LMIRCAM.Command.text","1 obssequences")
