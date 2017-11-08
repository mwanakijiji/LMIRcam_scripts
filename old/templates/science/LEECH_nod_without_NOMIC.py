#!/usr/bin/python
#This is a simple script to set camera parameters, take data, and offset the telescope
#PMH June 16, 2013
#DD  June 25, 2013 -- duplicate to use NOMIC at the same time
#DD  Oct 04,  2014 -- add short time delay in wait4AORunning function 

import time
from pyindi import * 

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

def wait4AORunning():
    '''wait until both AO loops close before proceeding'''
    while True:
        pi.setINDI("LBTO.Dictionary.Name=L_AOStatus;Value=")
        lstatus = pi.getINDI("LBTO.Dictionary.Value")
        pi.setINDI("LBTO.Dictionary.Name=R_AOStatus;Value=")
        rstatus = pi.getINDI("LBTO.Dictionary.Value")
        time.sleep(1) 
        if rstatus == "AORunning" and lstatus == "AORunning":
            break

#Make sure to turn off continuous mode.
pi.setINDI("LMIRCAM.Command.text","0 contacq",wait=True)

#Make sure to set filter wheels and integration
#parameters parameters manually with the GUI
#before running this script

#set number of up down nod pairs
for j in range(10):
    print j
    #start saving data
    pi.setINDI("LMIRCAM.Command.text","1 savedata")

    #start exposing
    pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)

    #use the last image as the background to subtract from the gui display
    pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=False)

    #Nod down 4.5''
    #Note that these are X and Y values of the star on the array 
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY",
               "LBTO.OffsetPointing.OffsetX", 0.0, 
               "LBTO.OffsetPointing.OffsetY", -4.5, 
               "LBTO.OffsetPointing.Side", "both", 
               "LBTO.OffsetPointing.Type", "REL",
               timeout=30)

    #wait until AO loops close...
    wait4AORunning()
    time.sleep(1)

    #begin exposing
    pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)

    #use the last image as the background to subtract from the gui display
    pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=False)

    #Nod up 4.5''
    #Note that these are X and Y values of the star on the array 
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY",
               "LBTO.OffsetPointing.OffsetX", 0.0, 
               "LBTO.OffsetPointing.OffsetY", 4.5, 
               "LBTO.OffsetPointing.Side", "both", 
               "LBTO.OffsetPointing.Type", "REL",
               timeout=30) 

    #wait until AO loops close...
    wait4AORunning() 
    time.sleep(1)

pi.setINDI("LMIRCAM.Command.text","0 savedata",timeout=300,wait=True)


