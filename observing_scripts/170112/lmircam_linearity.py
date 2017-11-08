from pyindi import * 
import time
import sys
import os
import fnmatch
import pyfits

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)
N_IMS=1

pi.setINDI("PID.SetCurrent.PID", "19")

#turn on save data
pi.setINDI("LMIRCAM.Command.text", "1 savedata")
pi.setINDI("LMIRCAM.EditFITS.Keyword=OBJNAME;Value=DOME/Linearity;Comment=Object name")
pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")
#set filters 
pi.setINDI("Lmir.lmir_FW2.command", 'ND1.0-T10', timeout=45, wait=True)
pi.setINDI("Lmir.lmir_FW3.command", "N03946-4", timeout=45, wait=True)
pi.setINDI("Lmir.lmir_FW4.command", "Open", timeout=45, wait=True)

#save frames
for j in xrange(30):
    print float(j)*0.5822
    pi.setINDI("LMIRCAM.Command.text", "%f 1 %i lbtintpar" % ((j)*0.5822,N_IMS), timeout=300)
    time.sleep(0.5)
    pi.setINDI("LMIRCAM.Command.text", "go", timeout=300)
pi.setINDI("Lmir.lmir_FW3.command", "Blank", timeout=45, wait=True)
pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=DRK;Comment=SCI/CAL/DRK/FLT")
for j in xrange(30):
    print float(j)*0.5822
    pi.setINDI("LMIRCAM.Command.text", "%f 1 %i lbtintpar" % ((j)*0.5822,N_IMS), timeout=300)
    time.sleep(0.5)
    pi.setINDI("LMIRCAM.Command.text", "go", timeout=300)
