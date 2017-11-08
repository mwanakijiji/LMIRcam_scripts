#!/usr/bin/python
#HR 8799 multi-filter/both camera script
#AS-130707

from pyindi import * 

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

#turn on save data
pi.setINDI("LMIRCAM.Command.text", "0 savedata")

#Start loop
for j in range(500):

    #LMIRCam Ks
    pi.setINDI("Lmir.LMIR_FW3.command", "Ks", timeout=20, wait=True)
    #pi.waitINDI("Lmir.LMIR_FW3.command", timeout=100)
    pi.setINDI("LMIRCAM.Command.text", "3000 sleep", timeout=15)

    pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=20, wait=True)
    #pi.waitINDI("Lmir.LMIR_FW3.command", timeout=100)
    pi.setINDI("LMIRCAM.Command.text", "3000 sleep", timeout=15)
        
#turn on save data
pi.setINDI("LMIRCAM.Command.text", "0 savedata")

