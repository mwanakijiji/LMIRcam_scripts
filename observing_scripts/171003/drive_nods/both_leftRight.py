#!/usr/bin/python
import time
from pyindi import * 
########
#This script does not change filters or set integration times.
#it just does 10 right/left nod sequences. Set the filters, 
#the star positions and the integration parameters manually.
#The nod is 4.5 arcseconds right first then left
#########
#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)
#############################
# USER INPUTS, SET INTPARAMS IN GUI!!!
#############################
NUMBER_OF_NOD_PAIRS = 10
NOD_DISTANCE_ASEC = 7

def wait4AORunning():
    while True:
        pi.setINDI("LBTO.Dictionary.Name=L_AOStatus;Value=")
        lstatus = pi.getINDI("LBTO.Dictionary.Value")
        pi.setINDI("LBTO.Dictionary.Name=R_AOStatus;Value=")
        rstatus = pi.getINDI("LBTO.Dictionary.Value")
        time.sleep(1) 
        if rstatus == "AORunning" and lstatus == "AORunning":
	#if lstatus == "AORunning":
            break

pi.setINDI("LMIRCAM.Command.text","0 contacq",wait=True)
pi.setINDI("LMIRCAM.Command.text","1 savedata")
#set number of up down nod pairs
for j in range(NUMBER_OF_NOD_PAIRS):
    print j
    pi.setINDI("LMIRCAM.Command.text","go",timeout=1000,wait=True)
    pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=1000,wait=False)

    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY",
               "LBTO.OffsetPointing.OffsetX", NOD_DISTANCE_ASEC, 
               "LBTO.OffsetPointing.OffsetY", 0, 
               "LBTO.OffsetPointing.Side", "both", 
               "LBTO.OffsetPointing.Type", "REL",
               timeout=30,
               wait=True)

    wait4AORunning()
    #time.sleep(1)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=1000,wait=True)
    pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=1000,wait=False)

    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY",
               "LBTO.OffsetPointing.OffsetX", -1*NOD_DISTANCE_ASEC, 
               "LBTO.OffsetPointing.OffsetY", 0, 
               "LBTO.OffsetPointing.Side", "both", 
               "LBTO.OffsetPointing.Type", "REL",
               timeout=30,
               wait=True) 

    wait4AORunning() 
    #time.sleep(1)
pi.setINDI("LMIRCAM.Command.text","0 savedata",timeout=300,wait=True)


