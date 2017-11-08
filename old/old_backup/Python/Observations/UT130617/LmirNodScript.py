#!/usr/bin/python
#This is a simple script to set camera parameters, take data, and offset the telescope
#PMH June 16, 2013

from pyindi import *

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI()


pi.setINDI("LMIRCAM.Command.text","1 savedata")
#int=0.3s, three coadds, 60 frames.  Total=1 minute
pi.setINDI("LMIRCAM.Command.text","go",timeout=60)

#Note that these are X and Y values of the star on the array where LL is 0,0.
#There is a rotation and sign flip in Elwood's INDI-IIF interface to make this work.
pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0, "LBTO.OffsetPointing.OffsetY", -4.5, "LBTO.OffsetPointing.Side", "left", "LBTO.OffsetPointing.Type", "REL") 


pi.setINDI("LMIRCAM.Command.text","go",timeout=60)
#Note that these are X and Y values of the star on the array where LL is 0,0.
#There is a rotation and sign flip in Elwood's INDI-IIF interface to make this work.
pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0, "LBTO.OffsetPointing.OffsetY", 4.5, "LBTO.OffsetPointing.Side", "left", "LBTO.OffsetPointing.Type", "REL") 

pi.setINDI("LMIRCAM.Command.text","0 savedata")
#int=0.3s, three coadds, 60 frames.  Total=1 minute
#pi.setINDI("LMIRCAM.Command.text","0.3 1 1 lbtintpar")
#pi.setINDI("LMIRCAM.Command.text","1 contacq")


#get all the INDI properties on the server
#allp = pi.getINDI()

#Use pyINDI's pretty-printer method to display results
#pi.ppD(allp)

#get specific properties using wildcards
#pi.ppD(pi.getINDI("Time.Now.*"))
#pi.ppD(pi.getINDI("Lmir.*.*"))

