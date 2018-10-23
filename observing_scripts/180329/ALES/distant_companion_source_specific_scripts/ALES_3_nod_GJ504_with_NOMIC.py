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
dint=2
#LMIRCAM
dark_integration_time = dint#seconds
dark_coadds = 1
dark_frames = 1
darkIntParams = (dark_integration_time, dark_coadds, dark_frames)

plight_integration_time = dint#seconds
slight_integration_time = dint#seconds
light_coadds = 1.
plight_frames = 2.
slight_frames = 30.

#NOMIC
Nplight_integration_time = 2#seconds
Nslight_integration_time = 2#seconds
nomic_coadds=1
Nplight_frames = 1
Nslight_frames = 13

primary_RA =  [13,16,46.52]
primary_Dec = [9,25,26.96]
#from kuzuhara et al for GJ 504b
#In [5]: np.average([2.481,2.448,2.499],weights=[1/0.033,1/0.024,1/0.026])
#Out[5]: 2.4748179419525065
#
#In [6]: np.average([326.84,325.82,326.14],weights=[1/0.94,1/0.66,1/0.61])
#Out[6]: 326.2015960912052
secondary_sep = 2.475
secondary_PA = 326.20


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
    #lmircam can't handle subtracting a dark
    #pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)

# NOD BACK TO PRIMARY
    print 'NOD to Primary position, cycle: ', j
    print
    nod_sneakSomeDarks(priRAOff,priDecOff,darkIntParams,side)
    wait4AORunning(side)

pi.setINDI("LMIRCAM.Command.text","0 savedata",timeout=300,wait=True)
