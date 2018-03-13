#!/usr/bin/python
#Darks/flats/linearity script
from pyindi import * 
import sys
import os
import fnmatch
import time
import pyfits

print 'Please provide the date YYMMDD'
date=raw_input()
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
        exps.append((hdu[0].header['ITIME'],hdu[0].header['SUBSECNM']))
    except IOError:
        print f

unique_exps=set(exps)
tot_time=[]
for ee in unique_exps:
    tot_time.append(ee[0]*50)
    print ee
print 'This will take %f minutes of darks, not including overheads'%(sum(tot_time)/60.)
print 'Press enter to begin, Ctrl-c to cancel'
raw_input()
pi.setINDI("LMIRCAM.Command.text", "0 contacq", wait=True)
pi.setINDI("LMIRCAM.Command.text", "1 savedata", wait=True)
pi.setINDI("Lmir.lmir_FW4.command", 'Blank', timeout=45, wait=True)
pi.setINDI("LMIRCAM.EditFITS.Keyword=OBJNAME;Value=EndDayDarks;Comment=Object name")
pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=DRK;Comment=SCI/CAL/DRK/FLT")
for ee in unique_exps:
    print ee
    pi.setINDI("LMIRCAM.Command.text", '"%s" subsectmap'%ee[1],timeout=45)
    get_lmircam_frames(ee[0],1,50)
    time.sleep(1)



