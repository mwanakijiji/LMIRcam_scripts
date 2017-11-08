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
N_CYCLES = 2
dint=1.4
dark_integration_time = dint#seconds
dark_coadds = 1
dark_frames = 2
darkIntParams = (dark_integration_time, dark_coadds, dark_frames)

plight_integration_time = dint#seconds
slight_integration_time = dint#seconds
light_coadds = 1
plight_frames = 10.
slight_frames = 60.

#NOMIC
Nplight_integration_time = dint#seconds
Nslight_integration_time = dint#seconds
Nplight_frames = 10.
Nslight_frames = 60.
##################################################################
# END USER INPUTS                                                #
##################################################################

plightIntParams = (plight_integration_time, light_coadds, plight_frames)
slightIntParams = (slight_integration_time, light_coadds, slight_frames)

NplightIntParams = (0.082, 10, 23)
NslightIntParams = (0.082, 10, 150)

primary_RA =  [23,40,24.507]
primary_Dec = [44,20,02.156]

secondary_sep = 1.058
secondary_PA = 56.0

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

    skyDecOff = -2.5
    skyRAOff = 0

    priDecOff = -skyDecOff - secDecOff
    priRAOff = -skyRAOff - secRAOff
    return priRAOff, priDecOff, secRAOff, secDecOff, skyRAOff, skyDecOff
    
def nod_sneakSomeDarks(RAOff,DecOff,side):
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "RADEC",
           "LBTO.OffsetPointing.OffsetX", DecOff, 
           "LBTO.OffsetPointing.OffsetY", RAOff, 
           "LBTO.OffsetPointing.Side", side, 
           "LBTO.OffsetPointing.Type", "REL", 
           timeout=400,
           wait=False) 
	###where's FW2
    pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=DRK;Comment=observation type", wait=False)
    pi.setINDI("LMIRCAM.Command.text", "0 contacq", wait=True)
    pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % darkIntParams, wait=True)
    fw2_pos = pi.getINDI("Lmir.lmir_FW2_status.PosNum", wait=True)
    pi.setINDI("Lmir.lmir_FW2.command", int(fw2_pos)+25000, timeout=20, wait=True)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
    pi.setINDI("Lmir.lmir_FW2.command", int(fw2_pos), timeout=20, wait=True)

def do_exposures(Lintparams,Nintparams,flag):
    pi.setINDI("LMIRCAM.Command.text", "0 contacq", wait=True)
    pi.setINDI("LMIRCAM.Command.text", "1 savedata", wait=True)
    pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % Lintparams, wait=True)
    pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=%s ;Comment=observation type"%flag, wait=False)
    #pi.setINDI("NOMIC.Command.text", "%f %i %i lbtintpar" % Nintparams, wait=True)
    time.sleep(1)
    #pi.setINDI("NOMIC.Command.text","go",timeout=300,wait=False)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
        
priRAOff, priDecOff, secRAOff, secDecOff, skyRAOff, skyDecOff = makeOffsets(primary_RA, primary_Dec, secondary_sep, secondary_PA)

pi.setINDI("LMIRCAM.Command.text", "0 loglevel 0 contacq 1 savedata %f %i %i lbtintpar" % plightIntParams, wait=True)
for j in range(N_CYCLES):
    print j
    print 'DO PRIMARY ', j
    print
    do_exposures(plightIntParams,NplightIntParams,'PRI')

# NOD TO SECONDARY
    print 'Get Secondary ', j
    print
    nod_sneakSomeDarks(secRAOff,secDecOff,side)
    wait4AORunning(side)
    print 'begin Secondary ', j
    print
    do_exposures(slightIntParams,NslightIntParams,'SEC')
# NOD TO SKY
    print 'Get Sky ', j
    print
    nod_sneakSomeDarks(skyRAOff,skyDecOff,side)
    wait4AORunning(side)
    print 'begin Sky ', j
    print
    do_exposures(slightIntParams,NslightIntParams,'SKY')
    pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)

# NOD BACK TO PRIMARY
    print 'Go Back to Primary ', j
    print
    nod_sneakSomeDarks(priRAOff,priDecOff,side)
    wait4AORunning(side)

pi.setINDI("LMIRCAM.Command.text","0 savedata",timeout=300,wait=True)
