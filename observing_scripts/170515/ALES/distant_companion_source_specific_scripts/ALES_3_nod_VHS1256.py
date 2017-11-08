#!/usr/bin/python
import sys
from pyindi import * 
from ALESutils import wait4AORunning, makeOffsets, nod_sneakSomeDarks, do_exposures

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi = PyINDI(verbose=False)
side=sys.argv[1]

##################################################################
# USER INPUTS:                                                   #
##################################################################
primary_RA =  [12,56,01.92]
primary_Dec = [-12,57,23.990]

secondary_sep = 8.06#Gauza et al. 2015
secondary_PA = 218.1

dint=4
dark_integration_time = dint#seconds
dark_coadds = 1
dark_frames = 1
darkIntParams = (dark_integration_time, dark_coadds, dark_frames)

plight_integration_time = dint#seconds
slight_integration_time = dint#seconds
light_coadds = 5.
plight_frames = 3.
slight_frames = 12.

#NOMIC
Nplight_integration_time = 20#seconds
Nslight_integration_time = 20#seconds
nomic_coadds=1
Nplight_frames = 3
Nslight_frames = 11
##################################################################
# END USER INPUTS                                                #
##################################################################

plightIntParams = (plight_integration_time, light_coadds, plight_frames)
slightIntParams = (slight_integration_time, light_coadds, slight_frames)

NplightIntParams = (Nplight_integration_time, nomic_coadds, Nplight_frames)
NslightIntParams = (Nslight_integration_time, nomic_coadds, Nslight_frames)

priRAOff, priDecOff, secRAOff, secDecOff, skyRAOff, skyDecOff = makeOffsets(primary_RA, primary_Dec, secondary_sep, secondary_PA)

pi.setINDI("LMIRCAM.Command.text", "0 loglevel") 
pi.setINDI("LMIRCAM.Command.text", "0 contacq", wait=True)
pi.setINDI("LMIRCAM.Command.text", "1 savedata", wait=True)
pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % plightIntParams, wait=True)

for j in range(4):
    print 'COLLECT PRIMARY POSITION FRAMES, cycle: ', j
    print
    do_exposures(plightIntParams,NplightIntParams,'PRI', side)

# NOD TO SECONDARY
    print 'NOD to secondary position, cycle', j
    print
    nod_sneakSomeDarks(secRAOff,secDecOff,darkIntParams,side)
    wait4AORunning(side)
    print 'COLLECT SECONDARY POSITION FRAMES, cycle: ', j
    print
    do_exposures(slightIntParams,NslightIntParams,'SEC', side)
# NOD TO SKY
    print 'NOD to Sky position, cycle', j
    print
    nod_sneakSomeDarks(skyRAOff,skyDecOff,darkIntParams,side)
    wait4AORunning(side)
    print 'COLLECT SKY POSITION FRAMES, cycle: ', j
    print
    do_exposures(slightIntParams,NslightIntParams,'SKY', side)
    pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)

# NOD BACK TO PRIMARY
    print 'NOD to Primary position, cycle: ', j
    print
    nod_sneakSomeDarks(priRAOff,priDecOff,darkIntParams,side)
    wait4AORunning(side)

pi.setINDI("LMIRCAM.Command.text","0 savedata",timeout=300,wait=True)
