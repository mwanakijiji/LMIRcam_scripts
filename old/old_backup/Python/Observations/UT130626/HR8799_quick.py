#!/usr/bin/python
#HR 8799 multi-filter/both camera script
#AS-130627

from pyindi import * 

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

#turn on save data
pi.setINDI("LMIRCAM.Command.text", "1 savedata")
pi.setINDI("NOMIC.Command.text", "1 savedata")

#LMIRCam filter 1
pi.setINDI("Lmir.LMIR_FW2.command", "H2O-Ice1", timeout=20)

pi.setINDI("LMIRCAM.Command.text", "0.1 10 1 lbtintpar 500 sleep", timeout=15)
pi.setINDI("LMIRCAM.Command.text","go",timeout=100)

pi.setINDI("LMIRCAM.Command.text", "4.0 1 13 lbtintpar 500 sleep", timeout=15)
pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)

pi.setINDI("NOMIC.Command.text", "0.08 10 48 lbtintpar 500 sleep", timeout=15)
pi.setINDI("NOMIC.Command.text","go",timeout=100,wait=False)

pi.waitINDI(["NOMIC.Command.text"],timeout=100)
pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)

#LMIRCam filter 2
pi.setINDI("Lmir.LMIR_FW2.command", "L-cont1", timeout=20)

pi.setINDI("LMIRCAM.Command.text", "0.1 10 1 lbtintpar 500 sleep", timeout=15)
pi.setINDI("LMIRCAM.Command.text","go",timeout=100)

pi.setINDI("LMIRCAM.Command.text", "4.0 1 13 lbtintpar 500 sleep", timeout=15)
pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)

pi.setINDI("NOMIC.Command.text", "0.08 10 48 lbtintpar 500 sleep", timeout=15)
pi.setINDI("NOMIC.Command.text","go",timeout=100,wait=False)

pi.waitINDI(["NOMIC.Command.text"],timeout=100)
pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)

#LMIRCam filter 3
pi.setINDI("Lmir.LMIR_FW2.command", "N03309-8", timeout=20)

pi.setINDI("LMIRCAM.Command.text", "0.1 10 1 lbtintpar 500 sleep", timeout=15)
pi.setINDI("LMIRCAM.Command.text","go",timeout=100)

pi.setINDI("LMIRCAM.Command.text", "2.5 1 20 lbtintpar 500 sleep", timeout=15)
pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)

pi.setINDI("NOMIC.Command.text", "0.08 10 48 lbtintpar 500 sleep", timeout=15)
pi.setINDI("NOMIC.Command.text","go",timeout=100,wait=False)

pi.waitINDI(["NOMIC.Command.text"],timeout=100)
pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)

#LMIRCam filter 4
pi.setINDI("Lmir.LMIR_FW2.command", "L-cont2", timeout=20)

pi.setINDI("LMIRCAM.Command.text", "0.1 10 1 lbtintpar 500 sleep", timeout=15)
pi.setINDI("LMIRCAM.Command.text","go",timeout=100)

pi.setINDI("LMIRCAM.Command.text", "2.0 1 25 lbtintpar 500 sleep", timeout=15)
pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)

pi.setINDI("NOMIC.Command.text", "0.08 10 48 lbtintpar 500 sleep", timeout=15)
pi.setINDI("NOMIC.Command.text","go",timeout=100,wait=False)

pi.waitINDI(["NOMIC.Command.text"],timeout=100)
pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)

#NOD down 4"
#try:
pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0, "LBTO.OffsetPointing.OffsetY", -4.0, "LBTO.OffsetPointing.Side", "left", "LBTO.OffsetPointing.Type", "REL") 
#except:
#    print, "Exception!"
#    raw_input("Press any key to continue")

#LMIRCam filter 1
pi.setINDI("Lmir.LMIR_FW2.command", "H2O-Ice1", timeout=20)

pi.setINDI("LMIRCAM.Command.text", "0.1 10 1 lbtintpar 500 sleep", timeout=15)
pi.setINDI("LMIRCAM.Command.text","go",timeout=100)

pi.setINDI("LMIRCAM.Command.text", "4.0 1 13 lbtintpar 500 sleep", timeout=15)
pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)

pi.setINDI("NOMIC.Command.text", "0.08 10 48 lbtintpar 500 sleep", timeout=15)
pi.setINDI("NOMIC.Command.text","go",timeout=100,wait=False)

pi.waitINDI(["NOMIC.Command.text"],timeout=100)
pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)

#LMIRCam filter 2
pi.setINDI("Lmir.LMIR_FW2.command", "L-cont1", timeout=20)

pi.setINDI("LMIRCAM.Command.text", "0.1 10 1 lbtintpar 500 sleep", timeout=15)
pi.setINDI("LMIRCAM.Command.text","go",timeout=100)

pi.setINDI("LMIRCAM.Command.text", "4.0 1 13 lbtintpar 500 sleep", timeout=15)
pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)

pi.setINDI("NOMIC.Command.text", "0.08 10 48 lbtintpar 500 sleep", timeout=15)
pi.setINDI("NOMIC.Command.text","go",timeout=100,wait=False)

pi.waitINDI(["NOMIC.Command.text"],timeout=100)
pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)

#LMIRCam filter 3
pi.setINDI("Lmir.LMIR_FW2.command", "N03309-8", timeout=20)

pi.setINDI("LMIRCAM.Command.text", "0.1 10 1 lbtintpar 500 sleep", timeout=15)
pi.setINDI("LMIRCAM.Command.text","go",timeout=100)

pi.setINDI("LMIRCAM.Command.text", "2.5 1 20 lbtintpar 500 sleep", timeout=15)
pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)

pi.setINDI("NOMIC.Command.text", "0.08 10 48 lbtintpar 500 sleep", timeout=15)
pi.setINDI("NOMIC.Command.text","go",timeout=100,wait=False)

pi.waitINDI(["NOMIC.Command.text"],timeout=100)
pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)

#LMIRCam filter 4
pi.setINDI("Lmir.LMIR_FW2.command", "L-cont2", timeout=20)

pi.setINDI("LMIRCAM.Command.text", "0.1 10 1 lbtintpar 500 sleep", timeout=15)
pi.setINDI("LMIRCAM.Command.text","go",timeout=100)

pi.setINDI("LMIRCAM.Command.text", "2.0 1 25 lbtintpar 500 sleep", timeout=15)
pi.setINDI("LMIRCAM.Command.text","go",timeout=100,wait=False)

pi.setINDI("NOMIC.Command.text", "0.08 10 48 lbtintpar 500 sleep", timeout=15)
pi.setINDI("NOMIC.Command.text","go",timeout=100,wait=False)

pi.waitINDI(["NOMIC.Command.text"],timeout=100)
pi.waitINDI(["LMIRCAM.Command.text"],timeout=100)

#NOD up 4"
#try:
pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", 0, "LBTO.OffsetPointing.OffsetY", 4.0, "LBTO.OffsetPointing.Side", "left", "LBTO.OffsetPointing.Type", "REL") 
#except:
#    print, "Exception!"
#    raw_input("Press any key to continue")

#turn off save data
pi.setINDI("LMIRCAM.Command.text", "0 savedata")
pi.setINDI("NOMIC.Command.text", "0 savedata")
