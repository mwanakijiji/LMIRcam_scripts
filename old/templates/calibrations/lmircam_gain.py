#!/usr/bin/python
#Darks/flats/linearity script

import time
from pyindi import * 
pi=PyINDI(verbose=True)

#turn on save data
pi.setINDI("LMIRCAM.Command.text", "1 savedata 0 autodispwhat 0 loglevel", wait=True)
#set objname
pi.setINDI("LMIRCAM.EditFITS.Keyword=OBJNAME;Value=GainTest;Comment=Object name")

pi.setINDI("Lmir.lmir_FW3.command", "Blank", timeout=300, wait=True)
pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=DRK;Comment=SCI/CAL/DRK/FLT")
for j in range(80):
    print float(j+1)*0.029
    pi.setINDI("LMIRCAM.Command.text", "%f 1 10 lbtintpar" % ((j+1)*0.029), timeout=300, wait=True)
    pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)
    
set filters and datatype to flat
pi.setINDI("Lmir.lmir_FW3.command", "Open", timeout=300, wait=True)
pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

#save frames
for j in range(80):
    print float(j+1)*0.029
    pi.setINDI("LMIRCAM.Command.text", "%f 1 10 lbtintpar" % ((j+1)*0.029), timeout=300, wait=True)
    time.sleep(0.1)
    pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)

#turn off save data
pi.setINDI("LMIRCAM.Command.text", "0 savedata 1 autodispwhat 1 loglevel", wait=True)
