#!/usr/bin/python
from pyindi import * 
import sys
import os
import fnmatch
import pyfits

#proper wavelength calibration requires the correct stop in
#LMIRCam FW1. Which side was used for ALES? Use that side's
#single-sided pupile stop.
print "This script requires some manual input."
print "You must ensure that LMIRCam FW1,FW3 and FW4 are in the right positions."
print "Your choices should reflect which aperture," 
print "prism, and blocking filter where used, respectively."
print "if you are ready press Enter"
print "To cancel press Ctrl-C"
raw_input()


#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

#turn on off continous mode
pi.setINDI("LMIRCAM.Command.text", "0 contacq", wait=True)
#turn on save data
pi.setINDI("LMIRCAM.Command.text", "1 savedata", wait=True)
#set header fields
pi.setINDI("LMIRCAM.EditFITS.Keyword=OBJNAME;Value=DOME/SKY;Comment=Object name")
pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=CAL;Comment=SCI/CAL/DRK/FLT")

#set integration parameters
pi.setINDI("LMIRCAM.Command.text", "10.0137 1 20 lbtintpar" , timeout=300)
#Make sure the Magnifier and lenslet array are in
pi.setINDI("Lmir.Mag_Wheel.command","Lens2",timeout=45,wait=True)
pi.setINDI("Lmir.lmir_APERWHL.command","SiLensletArray+pinholes",timeout=45,wait=True)
#cycle through the narrow band filters
for filt in ('NB2925-055','NB3375-025','NB3555-041','NB3950-035'):
    print filt
    #set Filter Wheel positions
    pi.setINDI("Lmir.lmir_FW2.command", filt, timeout=45, wait=True)
    pi.setINDI("LMIRCAM.Command.text", "go", timeout=600, wait=True)

#Get Darks
pi.setINDI("Lmir.lmir_FW3.command", 'Blank', timeout=45, wait=True)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=600, wait=True)
