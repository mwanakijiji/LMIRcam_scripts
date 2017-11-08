#!/usr/bin/python
import time
from pyindi import * 
########
#This script does not change filters or set integration times.
#it just does 10 down up nod sequences. Set the filters, 
#the star positions and the integration parameters manually.
#The nod is 4.5 arcseconds down first and then up
#########
#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)
#############################
# USER INPUTS, SET INTPARAMS IN GUI!!!
#############################
NUMBER_OF_NOD_PAIRS = 10
NOD_DISTANCE_ASEC = 4.5

def wait4AORunning():
    while True:
        pi.setINDI("LBTO.Dictionary.Name=L_AOStatus;Value=")
        lstatus = pi.getINDI("LBTO.Dictionary.Value")
        time.sleep(0.5) 
        if lstatus == "AORunning":
            break

#make sure to set the integration parameters in the gui
#set the number of up-down pairs
pi.setINDI("LMIRCAM.Command.text","1 savedata")
for j in range(NUMBER_OF_NOD_PAIRS):
    print j
    pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
    pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=False)

#set the down nod vector
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY",
               "LBTO.OffsetPointing.OffsetX", 0.0, 
               "LBTO.OffsetPointing.OffsetY", -1*NOD_DISTANCE_ASEC, 
               "LBTO.OffsetPointing.Side", "left", 
               "LBTO.OffsetPointing.Type", "REL",
               timeout=300)

    wait4AORunning()
    #time.sleep(1)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
    pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=False)

#set the up nod vector
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY",
               "LBTO.OffsetPointing.OffsetX", 0.0, 
               "LBTO.OffsetPointing.OffsetY", NOD_DISTANCE_ASEC, 
               "LBTO.OffsetPointing.Side", "left", 
               "LBTO.OffsetPointing.Type", "REL",
               timeout=300) 
    wait4AORunning() 
    #time.sleep(1)
pi.setINDI("LMIRCAM.Command.text","0 savedata",timeout=300,wait=True)


