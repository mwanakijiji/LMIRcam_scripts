#!/usr/bin/python
#HR 8799 multi-filter/both camera script
#AS-130707

from pyindi import * 

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

def wait4AORunning():
    while True:
        pi.setINDI("LBTO.Dictionary.Name=L_AOStatus;Value=")
        lstatus = pi.getINDI("LBTO.Dictionary.Value")
        pi.setINDI("LBTO.Dictionary.Name=R_AOStatus;Value=")
        rstatus = pi.getINDI("LBTO.Dictionary.Value")
        #print lstatus, rstatus
        #print rstatus
        if lstatus == "AORunning":#: and rstatus == "AORunning":
            break

#turn on save data
pi.setINDI("LMIRCAM.Command.text", "1 savedata")

#Start loop
for j in range(10):

    #LMIRCam H2O Ice
    #pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=30)
    pi.setINDI("Lmir.LMIR_FW2.command", "H2O-Ice1", timeout=30)
    
    pi.setINDI("LMIRCAM.Command.text", "5 3 3 lbtintpar 500 sleep", timeout=300)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=True)
    
    #LMIRCam L-cont1
    pi.setINDI("Lmir.LMIR_FW2.command", "L-cont1", timeout=30)
    
    pi.setINDI("LMIRCAM.Command.text", "5 3 3 lbtintpar 500 sleep", timeout=300)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=True)
    
    #LMIRCam N03309-8
    pi.setINDI("Lmir.LMIR_FW2.command", "N03309-8", timeout=30)
    
    pi.setINDI("LMIRCAM.Command.text", "3.0 3 10 lbtintpar 500 sleep", timeout=300)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=True)

    #LMIRCam L-cont2
    pi.setINDI("Lmir.LMIR_FW2.command", "L-cont2", timeout=30)
    
    pi.setINDI("LMIRCAM.Command.text", "2.0 3 10 lbtintpar 500 sleep", timeout=15)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=True)
 
    #LMIRCam L-cont3
    pi.setINDI("Lmir.LMIR_FW2.command", "L-cont3", timeout=30)
    
    pi.setINDI("LMIRCAM.Command.text", "2 3 10 lbtintpar 500 sleep", timeout=300)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=True)

    #LMIRCamL-cont4
    pi.setINDI("Lmir.LMIR_FW2.command", "L-cont4", timeout=30)
    
    pi.setINDI("LMIRCAM.Command.text", "1.5 3 10 lbtintpar 500 sleep", timeout=15)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=True)
      
    #LMIRCam N03946
    pi.setINDI("Lmir.LMIR_FW2.command", "N03946-4", timeout=30)
    
    pi.setINDI("LMIRCAM.Command.text", "0.5 3 20 lbtintpar 500 sleep", timeout=300)
    pi.setINDI("LMIRCAM.Command.text","go",stimeout=100,wait=True)

    #LMIRCam M
    #pi.setINDI("Lmir.LMIR_FW2.command", "Open", timeout=30)
    #pi.setINDI("Lmir.LMIR_FW3.command", "Std-M", timeout=30)
    
    #pi.setINDI("LMIRCAM.Command.text", "0.1 1 1 lbtintpar 500 sleep", timeout=15)
    #pi.setINDI("LMIRCAM.Command.text","go",timeout=100)
    
    #NOD down 4"
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0, "LBTO.OffsetPointing.OffsetY", 4.5, "LBTO.OffsetPointing.Side", "right", "LBTO.OffsetPointing.Type", "REL") 
    wait4AORunning()

    #LMIRCam H2O Ice
    #pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=30)
    pi.setINDI("Lmir.LMIR_FW2.command", "H2O-Ice1", timeout=30)
    
    pi.setINDI("LMIRCAM.Command.text", "5 3 3 lbtintpar 500 sleep", timeout=300)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=True)
    
    #LMIRCam L-cont1
    pi.setINDI("Lmir.LMIR_FW2.command", "L-cont1", timeout=30)
    
    pi.setINDI("LMIRCAM.Command.text", "5 3 3 lbtintpar 500 sleep", timeout=300)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=True)
    
    #LMIRCam N03309-8
    pi.setINDI("Lmir.LMIR_FW2.command", "N03309-8", timeout=30)
    
    pi.setINDI("LMIRCAM.Command.text", "3.0 3 10 lbtintpar 500 sleep", timeout=300)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=True)

    #LMIRCam L-cont2
    pi.setINDI("Lmir.LMIR_FW2.command", "L-cont2", timeout=30)
    
    pi.setINDI("LMIRCAM.Command.text", "2.0 3 10 lbtintpar 500 sleep", timeout=15)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=True)
 
    #LMIRCam L-cont3
    pi.setINDI("Lmir.LMIR_FW2.command", "L-cont3", timeout=30)
    
    pi.setINDI("LMIRCAM.Command.text", "2 3 10 lbtintpar 500 sleep", timeout=300)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=True)

    #LMIRCamL-cont4
    pi.setINDI("Lmir.LMIR_FW2.command", "L-cont4", timeout=30)
    
    pi.setINDI("LMIRCAM.Command.text", "1.5 3 10 lbtintpar 500 sleep", timeout=15)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=True)
      
    #LMIRCam N03946
    pi.setINDI("Lmir.LMIR_FW2.command", "N03946-4", timeout=30)
    
    pi.setINDI("LMIRCAM.Command.text", "0.5 3 20 lbtintpar 500 sleep", timeout=300)
    pi.setINDI("LMIRCAM.Command.text","go",stimeout=100,wait=True)
    #LMIRCam M
    #pi.setINDI("Lmir.LMIR_FW2.command", "Open", timeout=30)
    #pi.setINDI("Lmir.LMIR_FW3.command", "Std-M", timeout=30)
    
    #pi.setINDI("LMIRCAM.Command.text", "0.1 1 1 lbtintpar 500 sleep", timeout=15)
    #pi.setINDI("LMIRCAM.Command.text","go",timeout=100)
    
    #NOD down 4"
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0, "LBTO.OffsetPointing.OffsetY", 4.5, "LBTO.OffsetPointing.Side", "right", "LBTO.OffsetPointing.Type", "REL") 
    wait4AORunning()
    
    
#turn on save data
pi.setINDI("LMIRCAM.Command.text", "0 savedata")

