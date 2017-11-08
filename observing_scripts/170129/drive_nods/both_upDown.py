#!/usr/bin/python
import time
from pyindi import * 
########
#This script does not change filters or set integration times.
#it just does 10 up/down nod sequences. Set the filters, 
#the star positions and the integration parameters manually.
#The nod is 4.5 arcseconds down first then up
#########
#pi is an instance of PyINDI. Here we connect to the lmircam server
#############################
# USER INPUTS, SET INTPARAMS IN GUI!!!
#############################
pi=PyINDI(verbose=True)
NUMBER_OF_NOD_PAIRS = 10
NOD_DISTANCE_ASEC = 4.5

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
#set number of up down nod pairs
pi.setINDI("LMIRCAM.Command.text","1 savedata")
for j in range(NUMBER_OF_NOD_PAIRS):
    print j
    pi.setINDI("LMIRCAM.Command.text","go",timeout=1000,wait=True)
    pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=1000,wait=False)

#Note that these are X and Y values of the star on the array where LL is 0,0.
#There is a rotation and sign flip in Elwood's INDI-IIF interface to make this work.
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY",
               "LBTO.OffsetPointing.OffsetX", 0.0, 
               "LBTO.OffsetPointing.OffsetY", -1*NOD_DISTANCE_ASEC, 
               "LBTO.OffsetPointing.Side", "both", 
               "LBTO.OffsetPointing.Type", "REL",
               timeout=30)

    wait4AORunning()
    #time.sleep(1)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=1000,wait=True)
    pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=1000,wait=False)

#Note that these are X and Y values of the star on the array where LL is 0,0.
#There is a rotation and sign flip in Elwood's INDI-IIF interface to make this work.
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY",
               "LBTO.OffsetPointing.OffsetX", 0.0, 
               "LBTO.OffsetPointing.OffsetY", NOD_DISTANCE_ASEC, 
               "LBTO.OffsetPointing.Side", "both", 
               "LBTO.OffsetPointing.Type", "REL",
               timeout=30) 

    wait4AORunning() 
    #time.sleep(1)
pi.setINDI("LMIRCAM.Command.text","0 savedata",timeout=300,wait=True)


