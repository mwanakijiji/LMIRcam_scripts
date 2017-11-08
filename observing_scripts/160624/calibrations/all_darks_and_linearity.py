#!/usr/bin/python
#Darks/flats/linearity script
from pyindi import * 
import sys
import os
import fnmatch
import time
import pyfits

date=sys.argv[1]

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

all_fns=os.listdir(os.path.join('/home/observer/data/',date))
fns=fnmatch.filter(all_fns,'lm_'+date+'*.fits')
exps=[]
print "WAIT! I'll need you to press enter soon...Thanks"
print "WAIT! I'll need you to press enter soon...Thanks"
for f in fns:
    try:
        hdu=pyfits.open(os.path.join('/home/observer/data/',date,f))
        exps.append((hdu[0].header['ITIME'],hdu[0].header['NCOADDS']))
    except IOError:
        print f

unique_exps=set(exps)
tot_time=[]
for ee in unique_exps:
    tot_time.append(ee[0]*ee[1]*50)
    print ee
print 'This will take %f minutes of darks, not including overheads'%(sum(tot_time)/60.)
print 'Press enter to begin, ctrl-C to cancel'
raw_input()
pi.setINDI("LMIRCAM.Command.text", "0 contacq 1 savedata 0 autodispwhat 0 loglevel", wait=True)
pi.setINDI("Lmir.lmir_FW3.command", 'Blank', timeout=45, wait=True)
pi.setINDI("LMIRCAM.EditFITS.Keyword=OBJNAME;Value=EndDayDarks;Comment=Object name")
pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=DRK;Comment=SCI/CAL/DRK/FLT")
for ee in unique_exps:
    print ee
    pi.setINDI("LMIRCAM.Command.text", "%f %i 50 lbtintpar"%ee , timeout=300)
    time.sleep(1)
    pi.setINDI("LMIRCAM.Command.text", "go", timeout=max(300,int(5*ee[0]*ee[1]*50)), wait=True)

pi.setINDI("LMIRCAM.Command.text", "1 savedata")
pi.setINDI("LMIRCAM.EditFITS.Keyword=OBJNAME;Value=DOME/Linearity;Comment=Object name")
pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=CAL;Comment=SCI/CAL/DRK/FLT")
#set filters to flat
#(LargeDualAperture,ND1-T10,Lspec,Open)
pi.setINDI("Lmir.lmir_FW2.command", 'ND1.0-T10', timeout=45, wait=True)
pi.setINDI("Lmir.lmir_FW3.command", 'Open', timeout=45, wait=True)
pi.setINDI("Lmir.lmir_FW4.command", 'Lspec', timeout=45, wait=True)
#save frames
for j in range(80):
    print float(j+1)*0.029
    pi.setINDI("LMIRCAM.Command.text", "%f 1 10 lbtintpar" % ((j+1)*0.029), timeout=300)
    time.sleep(1)
    pi.setINDI("LMIRCAM.Command.text", "go", timeout=300)

pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=DRK;Comment=SCI/CAL/DRK/FLT")
for j in range(80):
    print float(j+1)*0.029
    pi.setINDI("LMIRCAM.Command.text", "%f 1 10 lbtintpar" % ((j+1)*0.029), timeout=300)
    time.sleep(1)
    pi.setINDI("LMIRCAM.Command.text", "go", timeout=300)

#turn off save data
pi.setINDI("LMIRCAM.Command.text", "0 savedata")


