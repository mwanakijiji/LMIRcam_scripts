#!/usr/bin/python
from pyindi import * 
import sys
import os
import fnmatch
import pyfits

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

##turn on off continous mode
#pi.setINDI("LMIRCAM.Command.text", "0 contacq", wait=True)
##turn on save data
#pi.setINDI("LMIRCAM.Command.text", "1 savedata", wait=True)
##cycle through the narrow band filters

Lp=      {'fw3':'Open'  ,'fw4':'Std-L'       ,'NSeq':100.,'Expt':1}
Lshort = {'fw3':'Open'  ,'fw4':'Lshort'      ,'NSeq':50. ,'Expt':2}   
Ice=     {'fw3':'Open'  ,'fw4':'H20-Ice2'    ,'NSeq':25. ,'Expt':4}      
Ks=      {'fw3':'Kshort','fw4':'PK50-Blocker','NSeq':25. ,'Expt':4}               

pi.setINDI("NOMIC.Command.text", "go", timeout=3000, wait=False)
#Lp
pi.setINDI("LMIRCAM.Command.text", "%f 1 %i lbtintpar" % (0, 100), timeout=1000)
pi.setINDI("Lmir.lmir_FW3.command", 'Open', timeout=45, wait=True)
pi.setINDI("Lmir.lmir_FW4.command", 'Std-L', timeout=45, wait=True)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=600, wait=True)
#Lshort
pi.setINDI("LMIRCAM.Command.text", "%f 1 %i lbtintpar" % (1, 50), timeout=1000)
pi.setINDI("Lmir.lmir_FW3.command", 'Open', timeout=45, wait=True)
pi.setINDI("Lmir.lmir_FW4.command", 'Lshort', timeout=45, wait=True)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=600, wait=True)
#Ice
pi.setINDI("LMIRCAM.Command.text", "%f 1 %i lbtintpar" % (2, 25), timeout=1000)
pi.setINDI("Lmir.lmir_FW3.command", 'Open', timeout=45, wait=True)
pi.setINDI("Lmir.lmir_FW4.command", 'H2O-Ice2', timeout=45, wait=True)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=600, wait=True)
#Ks
pi.setINDI("LMIRCAM.Command.text", "%f 1 %i lbtintpar" % (0, 100), timeout=1000)
pi.setINDI("Lmir.lmir_FW3.command", 'Kshort', timeout=45, wait=True)
pi.setINDI("Lmir.lmir_FW4.command", 'PK50-Blocker', timeout=45, wait=True)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=600, wait=True)

