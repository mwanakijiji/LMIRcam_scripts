#!/usr/bin/python
# This is a simple script to set camera parameters, take data, and offset the telescope
# This is a *dual aperture* script

# Operator must set exposure time and number of coadds first!
# must begin with the stars in the *UP* nod position

import sys, os, string, time, pyfits,  pdb, copy, numpy
from pyindi import * 
from scipy import ndimage, sqrt, stats

# do simple for-loops to move the FPC and HPC

pi = PyINDI()

#pi.setINDI("LMIRCAM.Command.text=1 savedata")

pi.setINDI("LMIRCAM.Command.text=go")

for step in range(0,4):
    pi.setINDI("Acromag.HPC.Tip=0;Tilt=0.5;Piston=0;Mode=1")
    time.sleep(1.0)
    pi.setINDI("LMIRCAM.Command.text=go")
    pi.setINDI("Acromag.HPC.Tip=-0.5;Tilt=0.0;Piston=0;Mode=1")
    time.sleep(1.0)
    pi.setINDI("LMIRCAM.Command.text=go")
    pi.setINDI("Acromag.HPC.Tip=0;Tilt=-0.5;Piston=0;Mode=1")
    time.sleep(1.0)
    pi.setINDI("LMIRCAM.Command.text=go")
    pi.setINDI("Acromag.HPC.Tip=0.5;Tilt=0.0;Piston=0;Mode=1")
    time.sleep(1.0)
    pi.setINDI("LMIRCAM.Command.text=go")
    pi.setINDI("Acromag.FPC.Tip=0.0;Tilt=0.5;Piston=0;Mode=1")
    time.sleep(1.0)
    pi.setINDI("LMIRCAM.Command.text=go")
    pi.setINDI("Acromag.FPC.Tip=-0.5;Tilt=0;Piston=0;Mode=1")
    time.sleep(1.0)
    pi.setINDI("LMIRCAM.Command.text=go")
    pi.setINDI("Acromag.FPC.Tip=0.0;Tilt=-0.5;Piston=0;Mode=1")
    time.sleep(1.0)
    pi.setINDI("LMIRCAM.Command.text=go")
    pi.setINDI("Acromag.FPC.Tip=0.5;Tilt=0;Piston=0;Mode=1")
    time.sleep(1.0)
    pi.setINDI("LMIRCAM.Command.text=go")
