#!/usr/bin/python
#Darks/flats/linearity script
#AS-131019

#prereq: LMIR FW1 is LargeDualAperture
#prereq: 30*0.029 in the flat configuration just barely non-linear (so set the
#filters correctly)

from pyindi import * 

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

#turn on save data
pi.setINDI("LMIRCAM.Command.text", "1 savedata")
pi.setINDI("LMIRCAM.EditFITS.Keyword=OBJNAME;Value=DOME/Linearity;Comment=Object name")
pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=CAL;Comment=SCI/CAL/DRK/FLT")
#set filters to flat
#(LargeDualAperture,ND1-T10,Lspec,Open)
pi.setINDI("Lmir.lmir_FW2.command", 'ND1.0-T10', timeout=45, wait=True)
pi.setINDI("Lmir.lmir_FW4.command", 'Lspec', timeout=45, wait=True)
#save frames
for j in range(80):
    print float(j+1)*0.029
    pi.setINDI("LMIRCAM.Command.text", "%f 1 10 lbtintpar 500 sleep" % ((j+1)*0.029), timeout=300)
    pi.setINDI("LMIRCAM.Command.text", "go", timeout=300)

# dark
#pi.setINDI("Lmir.LMIR_FW2.command", "ND2.0-T1", timeout=20, wait=True)
pi.setINDI("Lmir.lmir_FW3.command", "Blank", timeout=20, wait=True)
#pi.setINDI("Lmir.LMIR_FW4.command", "Std-L", timeout=20, wait=True)

#save frames
for j in range(80):
    print float(j+1)*0.029
    pi.setINDI("LMIRCAM.Command.text", "%f 1 10 lbtintpar 500 sleep" % ((j+1)*0.029), timeout=300)
    pi.setINDI("LMIRCAM.Command.text", "go", timeout=300)

#turn off save data
pi.setINDI("LMIRCAM.Command.text", "0 savedata")
