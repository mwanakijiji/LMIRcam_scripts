#!/usr/bin/python
from pyindi import * 
import sys
import os
import fnmatch
import pyfits
import time

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI()

NUMBER_OF_NOD_PAIRS = 10
NOD_DISTANCE_ASEC = 5

def wait4AORunning():
    while True:
        pi.setINDI("LBTO.Dictionary.Name=L_AOStatus;Value=")
        lstatus = pi.getINDI("LBTO.Dictionary.Value")
        pi.setINDI("LBTO.Dictionary.Name=R_AOStatus;Value=")
        rstatus = pi.getINDI("LBTO.Dictionary.Value")
        time.sleep(1) 
        if rstatus == "AORunning" and lstatus == "AORunning":
            break

#turn on off continous mode
pi.setINDI("LMIRCAM.Command.text", "0 contacq", wait=True)
#turn on save data
pi.setINDI("LMIRCAM.Command.text", "1 savedata", wait=True)

#set integration parameters
pi.setINDI("LMIRCAM.Command.text", "0 1 300 lbtintpar" , timeout=300)
#fw2s=('Open','Open','ND1.0-T10')
fw2s=('Open','Open','Open')
fw3s=('Kshort','N03946-4','Open')
fw4s=('PK50-Blocker','Open','Std-M')
for j in range(NUMBER_OF_NOD_PAIRS):
    print 'start %i up' % j
    for fw2, fw3, fw4 in zip(fw2s, fw3s, fw4s):
        print fw2, fw3, fw4
        #set Filter Wheel positions
        pi.setINDI("Lmir.lmir_FW2.command", fw2, timeout=45, wait=False)
        pi.setINDI("Lmir.lmir_FW3.command", fw3, timeout=45, wait=False)
        pi.setINDI("Lmir.lmir_FW4.command", fw4, timeout=45, wait=False)
        pi.waitINDI("Lmir.lmir_FW2.command")
        pi.waitINDI("Lmir.lmir_FW3.command")
        pi.waitINDI("Lmir.lmir_FW4.command")
        pi.setINDI("LMIRCAM.Command.text", "go", timeout=600, wait=True)

    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY",
               "LBTO.OffsetPointing.OffsetX", NOD_DISTANCE_ASEC, 
               "LBTO.OffsetPointing.OffsetY", 0, 
               "LBTO.OffsetPointing.Side", "both", 
               "LBTO.OffsetPointing.Type", "REL",
               timeout=30,
               wait=True)

    wait4AORunning()

    print 'start %i down' % j
    for fw2, fw3, fw4 in zip(fw2s[::-1], fw3s[::-1], fw4s[::-1]):
        print fw2, fw3, fw4
        #set Filter Wheel positions
        pi.setINDI("Lmir.lmir_FW2.command", fw2, timeout=45, wait=False)
        pi.setINDI("Lmir.lmir_FW3.command", fw3, timeout=45, wait=False)
        pi.setINDI("Lmir.lmir_FW4.command", fw4, timeout=45, wait=False)
        pi.waitINDI("Lmir.lmir_FW2.command")
        pi.waitINDI("Lmir.lmir_FW3.command")
        pi.waitINDI("Lmir.lmir_FW4.command")
        pi.setINDI("LMIRCAM.Command.text", "go", timeout=600, wait=True)

    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY",
               "LBTO.OffsetPointing.OffsetX", -1*NOD_DISTANCE_ASEC, 
               "LBTO.OffsetPointing.OffsetY", 0, 
               "LBTO.OffsetPointing.Side", "both", 
               "LBTO.OffsetPointing.Type", "REL",
               timeout=30,
               wait=True) 

#Get Darks
