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

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

#turn on save data
pi.setINDI("LMIRCAM.Command.text", "1 savedata 0 autodispwhat 0 loglevel", wait=True)

#set objname
pi.setINDI("LMIRCAM.EditFITS.Keyword=OBJNAME;Value=Test;Comment=Object name")

#set and obstype filters to dark
#pi.setINDI("Lmir.LMIR_FW2.command", "ND2.0-T1", timeout=20, wait=True)
pi.setINDI("Lmir.lmir_FW3.command", "Blank", timeout=300, wait=True)
#pi.setINDI("Lmir.LMIR_FW4.command", "Std-L", timeout=20, wait=True)
pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=DRK;Comment=SCI/CAL/DRK/FLT")

#save frames
for j in range(80):
    print float(j+1)*0.029
    pi.setINDI("LMIRCAM.Command.text", "%f 1 10 lbtintpar 500 sleep" % ((j+1)*0.029), timeout=300)
    pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)
    
#set filters and datatype to flat
#pi.setINDI("Lmir.LMIR_FW2.command", "L-cont4", timeout=20, wait=True)
pi.setINDI("Lmir.lmir_FW3.command", "_home_", timeout=300, wait=True)
#pi.setINDI("Lmir.LMIR_FW4.command", "Std-L", timeout=20, wait=True)
pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

#save frames
for j in range(80):
    print float(j+1)*0.029
    pi.setINDI("LMIRCAM.Command.text", "%f 1 10 lbtintpar 500 sleep" % ((j+1)*0.029), timeout=300)
    pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)

#turn off save data
pi.setINDI("LMIRCAM.Command.text", "0 savedata 1 autodispwhat 1 loglevel", wait=True)
