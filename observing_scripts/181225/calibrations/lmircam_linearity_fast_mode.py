from pyindi import * 
import time
import sys
import os
import fnmatch
import pyfits
from lmircam_tools.exposures import get_lmircam_frames

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)
N_IMS=5

pi.setINDI("PID.SetCurrent.PID", "19")

#set filters 
pi.setINDI("Lmir.lmir_FW2.command", 'Open', timeout=45, wait=True)
pi.setINDI("Lmir.lmir_FW25.command", "Lspec2.8-4.0", timeout=45, wait=True)
pi.setINDI("Lmir.lmir_FW3.command", "Open", timeout=45, wait=True)
pi.setINDI("Lmir.lmir_FW4.command", "Open", timeout=45, wait=True)
#turn on fast mode (also sets full frame)
pi.setINDI("LMIRCAM.enable_fast_mode.value=On", timeout=30)

#set some header key words
pi.setINDI("LMIRCAM.EditFITS.Keyword=OBJNAME;Value=DOME/Linearity;Comment=Object name")
pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")
#save frames
for j in xrange(1, 30):
    dit = j * 27.5 - 10.0     # Request DITs in steps of multiples of minimum DIT, but subtract a little so the camera rounds up to the correct DIT.  
    get_lmircam_frames(dit, 1, N_IMS, use_bg=0, save_data=True)

pi.setINDI("Lmir.lmir_FW4.command", "Blank", timeout=45, wait=True)
pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=DRK;Comment=SCI/CAL/DRK/FLT")
for j in xrange(1, 30):
    dit = j * 27.5 - 10.0     # Request DITs in steps of multiples of minimum DIT, but subtract a little so the camera rounds up to the correct DIT.  
    get_lmircam_frames(dit, 1, N_IMS, use_bg=0, save_data=True)

