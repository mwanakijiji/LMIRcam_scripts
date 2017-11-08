#!/usr/bin/python
#Darks/flats/linearity script
#AS-131019
#DD-150206-added datatype and wait statements
#AS-15001-corrected data types
#DD-151222-now change object name
#DD-160215-changed timeout time to accomodate for slower filter wheel motion

#prereq: LMIR FW1 is LargeDualAperture
#prereq: 30*0.029 in the flat configuration just barely non-linear

from pyindi import * 
import sys
import os
import fnmatch

import pyfits

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

#turn on save data
pi.setINDI("LMIRCAM.Command.text", "1 savedata 0 loglevel", wait=True)
#set objname
pi.setINDI("LMIRCAM.EditFITS.Keyword=OBJNAME;Value=DOME/SKY;Comment=Object name")
pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=CAL;Comment=SCI/CAL/DRK/FLT")

pi.setINDI("LMIRCAM.Command.text", "10.0137 1 30 lbtintpar" , timeout=300)
for filt in ('NB2925-055','NB3375-025','NB3555-041','NB3950-035'):
    print filt
    pi.setINDI("Lmir.lmir_FW2.command", filt, timeout=45, wait=True)
    pi.setINDI("LMIRCAM.Command.text", "go", timeout=500, wait=True)

pi.setINDI("Lmir.lmir_FW3.command", 'Blank', timeout=45, wait=True)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=500, wait=True)




