#!/usr/bin/python
from pyindi import * 
import sys
sys.path.append('/home/observer/Scripts/observing_scripts/templates/')
import os
import fnmatch
import pyfits
from lmircam_tools.exposures import get_lmircam_frames

#proper wavelength calibration requires the correct stop in
#LMIRCam FW1. Which side was used for ALES? Use that side's
#single-sided pupile stop.
print "This script requires some manual input."
print "You must ensure that LMIRCam MagWheel, AperWheel, FW1,FW3 and FW4 are in the right positions."
print "Your choices should reflect which aperture, prism, and blocking filter where used, respectively."
print "if you are ready press Enter"
print "To cancel press Ctrl-C"
raw_input()


#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

#turn on off continous mode
pi.setINDI("LMIRCAM.stop.value=On", wait=True)
#turn on save data
pi.setINDI("LMIRCAM.enable_save.value=On", wait=True)
#set header fields
pi.setINDI("LMIRCAM.EditFITS.Keyword=OBJNAME;Value=DOME/SKY;Comment=Object name")
pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=CAL;Comment=SCI/CAL/DRK/FLT")

#set integration parameters
intparams = (1.4,1,2)
for filt in ('NB2925-055','NB3375-025','NB3555-041','NB3950-035'):
    print filt
    #set Filter Wheel positions
    pi.setINDI("Lmir.lmir_FW2.command", filt, timeout=45, wait=True)
    get_lmircam_frames(*intparams, use_bg=True, save_data=True)

pi.setINDI("Lmir.lmir_FW4.command", 'Blank', timeout=45, wait=True)
get_lmircam_frames(*intparams,use_bg=False, save_data=True)
