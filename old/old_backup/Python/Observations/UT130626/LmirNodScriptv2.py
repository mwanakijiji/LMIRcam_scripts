#!/usr/bin/python
#This is a simple script to set camera parameters, take data, and offset the telescope
#PMH June 16, 2013

from pyindi import *

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI()

for j in range(10):
	print j
	pi.setINDI("LMIRCAM.Command.text","1 savedata")
	#int=0.3s, three coadds, 50 frames.  Total=50 s
	pi.setINDI("LMIRCAM.Command.text","go",timeout=60)

	#Note that these are X and Y values of the star on the array where LL is 0,0.
	#There is a rotation and sign flip in Elwood's INDI-IIF interface to make this work.
	pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 4.5, "LBTO.OffsetPointing.OffsetY", 0, "LBTO.OffsetPointing.Side", "left", "LBTO.OffsetPointing.Type", "REL") 
	pi.setINDI("LMIRCAM.Command.text","go",timeout=60)
	#Note that these are X and Y values of the star on the array where LL is 0,0.
	#There is a rotation and sign flip in Elwood's INDI-IIF interface to make this work.
	pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", -4.5, "LBTO.OffsetPointing.OffsetY", 0, "LBTO.OffsetPointing.Side", "left", "LBTO.OffsetPointing.Type", "REL") 

	pi.setINDI("LMIRCAM.Command.text","0 savedata")
	#int=0.3s, three coadds, 60 frames.  Total=1 minute
	#pi.setINDI("LMIRCAM.Command.text","0.3 1 1 lbtintpar")
	#pi.setINDI("LMIRCAM.Command.text","1 contacq")



