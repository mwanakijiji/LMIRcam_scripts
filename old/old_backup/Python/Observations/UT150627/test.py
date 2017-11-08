#!/usr/bin/python
# This is a simple script to set camera parameters, take data, and offset the telescope
# This is a *dual aperture* script

# Operator must set exposure time and number of coadds first!
# must begin with the stars in the *UP* nod position

import time
from pyindi import * 

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)
'''
def wait4AORunning():
    while True:
        pi.setINDI("LBTO.Dictionary.Name=L_AOStatus;Value=")
        lstatus = pi.getINDI("LBTO.Dictionary.Value")
        pi.setINDI("LBTO.Dictionary.Name=R_AOStatus;Value=")
        rstatus = pi.getINDI("LBTO.Dictionary.Value")
        #print lstatus, rstatus
        #print rstatus
	time.sleep(0.05) 
        if rstatus == "AORunning" and lstatus == "AORunning":
            break
'''
#turn off continuous acquisition
pi.setINDI("LMIRCAM.Command.text","0 contacq")
# take 50 images per nod position
pi.setINDI("LMIRCAM.Command.text","10 obssequences",timeout=300,wait=True)


# take 10 up/down nod pairs
for j in range(2):
	print j
        # take frames and save the data
	pi.setINDI("LMIRCAM.Command.text","1 savedata")
	pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
        # use the last frame taken as the background for the next set
	pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=False)

        # NOD DOWN
	#Note that these are X and Y values of the star on the array where LL is 0,0.
	#There is a rotation and sign flip in Elwood's INDI-IIF interface to make this work.
#	pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0.0, "LBTO.OffsetPointing.OffsetY", -4.5, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 

        # wait for AO to close loop and stabilize for a second before taking next set
 #       wait4AORunning()
	pi.setINDI("LMIRCAM.Command.text","1000 sleep")
	pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
	pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=False)

        # NOD UP in prep for next set
	#Note that these are X and Y values of the star on the array where LL is 0,0.
	#There is a rotation and sign flip in Elwood's INDI-IIF interface to make this work.
#	pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0.0, "LBTO.OffsetPointing.OffsetY", 4.5, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 
#        wait4AORunning() 
	pi.setINDI("LMIRCAM.Command.text","1000 sleep")




# end of script: set up to be compatible with the observer running in continuous mode
# turn off save data
pi.setINDI("LMIRCAM.Command.text","0 savedata",timeout=300,wait=True)
# set number of images to take to 1
pi.setINDI("LMIRCAM.Command.text","1 obssequences")
