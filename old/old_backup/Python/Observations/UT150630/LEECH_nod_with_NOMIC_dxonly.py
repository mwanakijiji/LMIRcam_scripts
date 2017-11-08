#!/usr/bin/python
#This is a simple script to set camera parameters, take data, and offset the telescope
#PMH June 16, 2013
#DD  June 25, 2013 -- duplicate to use NOMIC at the same time

from pyindi import *

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

def wait4AORunning():
    while True:
        pi.setINDI("LBTO.Dictionary.Name=L_AOStatus;Value=")
        lstatus = pi.getINDI("LBTO.Dictionary.Value")
        pi.setINDI("LBTO.Dictionary.Name=R_AOStatus;Value=")
        rstatus = pi.getINDI("LBTO.Dictionary.Value")
        #print lstatus, rstatus
        #print rstatus
        if rstatus == "AORunning" and lstatus == "AORunning":
        #if lstatus == "AORunning":
            break

pi.setINDI("LMIRCAM.Command.text","0 contacq")
pi.setINDI("NOMIC.Command.text","0 contacq")
pi.setINDI("LMIRCAM.Command.text","1 obssequences",timeout=300,wait=True)
pi.setINDI("NOMIC.Command.text","1 obssequences",timeout=300,wait=True)
for j in range(1):
        print j
        pi.setINDI("LMIRCAM.Command.text","0 savedata")
        pi.setINDI("NOMIC.Command.text","0 savedata")

        pi.setINDI("NOMIC.Command.text","go",timeout=300,wait=False)
        pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
        pi.setINDI("NOMIC.Command.text","rawbg",timeout=300,wait=False)
        pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)

        pi.waitINDI(["NOMIC.Command.text"],timeout=300)
        pi.waitINDI(["LMIRCAM.Command.text"],timeout=300)

        #Note that these are X and Y values of the star on the array where LL is 0,0.
        #There is a rotation and sign flip in Elwood's INDI-IIF interface to make this work.
        pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0.0, "LBTO.OffsetPointing.OffsetY", -4.5, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL",timeout=400)

        wait4AORunning()
        pi.setINDI("LMIRCAM.Command.text","1000 sleep")
        pi.setINDI("NOMIC.Command.text","go",timeout=300,wait=False)
        pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
        pi.setINDI("NOMIC.Command.text","rawbg",timeout=300,wait=False)
        pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)

        pi.waitINDI(["NOMIC.Command.text"],timeout=300,wait=True)
        pi.waitINDI(["LMIRCAM.Command.text"],timeout=300,wait=True)

        #Note that these are X and Y values of the star on the array where LL is 0,0.
        #There is a rotation and sign flip in Elwood's INDI-IIF interface to make this work.
        pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0.0, "LBTO.OffsetPointing.OffsetY", 4.5, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL",timeout=400)

        wait4AORunning()
        pi.setINDI("LMIRCAM.Command.text","1000 sleep")
        
pi.setINDI("LMIRCAM.Command.text","0 savedata",timeout=300,wait=True)
pi.setINDI("NOMIC.Command.text","0 savedata",timeout=300,wait=True)
pi.setINDI("LMIRCAM.Command.text","1 obssequences")
pi.setINDI("NOMIC.Command.text","1 obssequences")

