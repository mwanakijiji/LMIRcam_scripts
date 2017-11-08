#!/usr/bin/python
#This is a test script to begin understanding the pyINDI interface to LMIRCam and LBTI
#PMH June 16, 2013

from pyindi import *

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI("lbti-lmircam")

#get all the INDI properties on the server
allp = pi.getINDI()

#Use pyINDI's pretty-printer method to display results
pi.ppD(allp)

#get specific properties using wildcards
#pi.ppD(pi.getINDI("Time.Now.*"))
#pi.ppD(pi.getINDI("Lmir.*.*"))

