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
        print lstatus, rstatus
        #print rstatus
        if lstatus == "AORunning" and rstatus == "AORunning":
        #if rstatus == "AORunning":
            break


for j in range(4):
	print j
	pi.setINDI("LMIRCAM.Command.text","1 savedata")
        pi.setINDI("NOMIC.Command.text","1 savedata")

	pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)
	pi.setINDI("NOMIC.Command.text","go",timeout=100,wait=False)

        pi.waitINDI(["NOMIC.Command.text"],timeout=100)
        pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)

	#Note that these are X and Y values of the star on the array where LL is 0,0.
	#There is a rotation and sign flip in Elwood's INDI-IIF interface to make this work.
	pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0, "LBTO.OffsetPointing.OffsetY", -4.5, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL") 

        wait4AORunning()
	pi.setINDI("LMIRCAM.Command.text", "1000 sleep")

	pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)
	pi.setINDI("NOMIC.Command.text","go",timeout=100,wait=False)

        pi.waitINDI(["NOMIC.Command.text"],timeout=100)
        pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)

	#Note that these are X and Y values of the star on the array where LL is 0,0.
	#There is a rotation and sign flip in Elwood's INDI-IIF interface to make this work.
	pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0, "LBTO.OffsetPointing.OffsetY", 4.5, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL") 
	#pi.setINDI("LMIRCAM.Command.text", "10000 sleep")
        wait4AORunning()
	pi.setINDI("LMIRCAM.Command.text", "1000 sleep")

	pi.setINDI("LMIRCAM.Command.text","0 savedata")
        pi.setINDI("NOMIC.Command.text","0 savedata")




