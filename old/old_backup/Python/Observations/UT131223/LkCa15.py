#!/usr/bin/python
#LkCa 15 script both sides
#AS-131226

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

#Start loop
for j in range(10):

    #LMIRCam L'
    pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=20, wait=False)
    pi.setINDI("Lmir.LMIR_FW4.command", "Std-L", timeout=20, wait=False)
    pi.waitINDI(["Lmir.LMIR_FW3.command","Lmir.LMIR_FW4.command"], timeout=100)
    
    pi.setINDI("LMIRCAM.Command.text", "0.291 3 50 lbtintpar 500 sleep", timeout=15)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)

    pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)
    
    #LMIRCam M'
    pi.setINDI("Lmir.LMIR_FW3.command", "Std-M", timeout=20, wait=False)
    pi.setINDI("Lmir.LMIR_FW4.command", "_home_", timeout=20, wait=False)
    pi.waitINDI(["Lmir.LMIR_FW3.command","Lmir.LMIR_FW4.command"], timeout=100)

    pi.setINDI("LMIRCAM.Command.text", "0.087 10 50 lbtintpar 500 sleep", timeout=15)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)

    pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)

    #NOD
    #Note that these are X and Y values of the star on the array where LL is 0,0.
    #There is a rotation and sign flip in Elwood's INDI-IIF interface to make this work.
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0, "LBTO.OffsetPointing.OffsetY", -4.5, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL") 

    wait4AORunning()
    pi.setINDI("LMIRCAM.Command.text", "1000 sleep")

    #LMIRCam L'
    pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=20, wait=False)
    pi.setINDI("Lmir.LMIR_FW4.command", "Std-L", timeout=20, wait=False)
    pi.waitINDI(["Lmir.LMIR_FW3.command","Lmir.LMIR_FW4.command"], timeout=100)
    
    pi.setINDI("LMIRCAM.Command.text", "0.291 3 50 lbtintpar 500 sleep", timeout=15)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)

    pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)
    
    #LMIRCam M'
    pi.setINDI("Lmir.LMIR_FW3.command", "Std-M", timeout=20, wait=False)
    pi.setINDI("Lmir.LMIR_FW4.command", "_home_", timeout=20, wait=False)
    pi.waitINDI(["Lmir.LMIR_FW3.command","Lmir.LMIR_FW4.command"], timeout=100)

    pi.setINDI("LMIRCAM.Command.text", "0.087 10 50 lbtintpar 500 sleep", timeout=15)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)

    pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)


    #NOD
    #Note that these are X and Y values of the star on the array where LL is 0,0.
    #There is a rotation and sign flip in Elwood's INDI-IIF interface to make this work.
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0, "LBTO.OffsetPointing.OffsetY", 4.5, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL") 

    wait4AORunning()
    pi.setINDI("LMIRCAM.Command.text", "1000 sleep")


#turn on save data
pi.setINDI("LMIRCAM.Command.text", "0 savedata")

