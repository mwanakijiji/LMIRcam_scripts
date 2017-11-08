#!/usr/bin/python
#HR 8799 multi-filter/both camera script
#AS-130707

from pyindi import * 

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

#turn on save data
pi.setINDI("LMIRCAM.Command.text", "1 savedata")

def wait4AORunning():
    while True:
        pi.setINDI("LBTO.Dictionary.Name=L_AOStatus;Value=")
        lstatus = pi.getINDI("LBTO.Dictionary.Value")
        pi.setINDI("LBTO.Dictionary.Name=R_AOStatus;Value=")
        rstatus = pi.getINDI("LBTO.Dictionary.Value")
        print lstatus, rstatus
        if lstatus == "AORunning" and rstatus == "AORunning":
            break

#set K-filter
pi.setINDI("Lmir.LMIR_FW3.command", "Ks", timeout=20, wait=False)
pi.setINDI("Lmir.LMIR_FW4.command", "PK50-Blocker", timeout=20, wait=False)
pi.waitINDI(["Lmir.LMIR_FW3.command","Lmir.LMIR_FW4.command"], timeout=100)


#Start loop
for j in range(10):

    #LMIRCam Ks
    pi.setINDI("LMIRCAM.Command.text", "4.0 1 7 lbtintpar 500 sleep", timeout=15)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)
#    pi.setINDI("NOMIC.Command.text","go",timeout=100,wait=False)
    
    pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)
#    pi.waitINDI(["NOMIC.Command.text"],timeout=100)

    #LMIRCam L'
    pi.setINDI("Lmir.LMIR_FW3.command", "home", timeout=20, wait=False)
    pi.setINDI("Lmir.LMIR_FW4.command", "Std-L", timeout=20, wait=False)
    pi.waitINDI(["Lmir.LMIR_FW3.command","Lmir.LMIR_FW4.command"], timeout=100)
    
    pi.setINDI("LMIRCAM.Command.text", "0.1 10 1 lbtintpar 500 sleep", timeout=15)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100)
    
    pi.setINDI("LMIRCAM.Command.text", "0.291 3 30 lbtintpar 500 sleep", timeout=15)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)
#    pi.setINDI("NOMIC.Command.text","go",timeout=100,wait=False)

    pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)
#    pi.waitINDI(["NOMIC.Command.text"],timeout=100)
    
    #NOD down 4"
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0, "LBTO.OffsetPointing.OffsetY", -4.0, "LBTO.OffsetPointing.Side", "right", "LBTO.OffsetPointing.Type", "REL") 
   # wait4AORunning()
    pi.setINDI("LMIRCAM.Command.text", "8000 sleep")

    #LMIRCam L'
    pi.setINDI("LMIRCAM.Command.text", "0.1 10 1 lbtintpar 500 sleep", timeout=15)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100)
    
    pi.setINDI("LMIRCAM.Command.text", "0.291 3 30 lbtintpar 500 sleep", timeout=15)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)
#    pi.setINDI("NOMIC.Command.text","go",timeout=100,wait=False)

    pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)
#    pi.waitINDI(["NOMIC.Command.text"],timeout=100)

    #LMIRCam Ks
    pi.setINDI("Lmir.LMIR_FW3.command", "Ks", timeout=20, wait=False)
    pi.setINDI("Lmir.LMIR_FW4.command", "PK50-Blocker", timeout=20, wait=False)
    pi.waitINDI(["Lmir.LMIR_FW3.command","Lmir.LMIR_FW4.command"], timeout=100)
    
    pi.setINDI("LMIRCAM.Command.text", "4.0 1 7 lbtintpar 500 sleep", timeout=15)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)
#    pi.setINDI("NOMIC.Command.text","go",timeout=100,wait=False)

    pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)
#    pi.waitINDI(["NOMIC.Command.text"],timeout=100)
    
    #NOD up 4"
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0, "LBTO.OffsetPointing.OffsetY", 4.0, "LBTO.OffsetPointing.Side", "right", "LBTO.OffsetPointing.Type", "REL") 
#    wait4AORunning()   
    pi.setINDI("LMIRCAM.Command.text", "8000 sleep") 

#turn on save data
pi.setINDI("LMIRCAM.Command.text", "0 savedata")

