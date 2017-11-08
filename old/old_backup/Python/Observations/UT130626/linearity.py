#!/usr/bin/python
#Darks/flats/linearity script
#AS-130617

from pyindi import * 

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

#turn on save data
pi.setINDI("LMIRCAM.Command.text", "1 savedata")

#set filters to dark
pi.setINDI("Lmir.LMIR_FW1.command", "SXAperture", timeout=20)
pi.setINDI("Lmir.LMIR_FW2.command", "L-cont4", timeout=20)
pi.setINDI("Lmir.LMIR_FW3.command", "Blank", timeout=20)
pi.setINDI("Lmir.LMIR_FW4.command", "Open", timeout=20)

#save frames
for j in range(100):
	print float(j+1)*0.027
	pi.setINDI("LMIRCAM.Command.text", "%f 1 3 lbtintpar 500 sleep" % ((j+1)*0.027), timeout=15)
	pi.setINDI("LMIRCAM.Command.text", "go", timeout=15)
	
#set filters to flat
pi.setINDI("Lmir.LMIR_FW1.command", "SXAperture", timeout=20)
pi.setINDI("Lmir.LMIR_FW2.command", "L-cont4", timeout=20)
pi.setINDI("Lmir.LMIR_FW3.command", "Open", timeout=20)
pi.setINDI("Lmir.LMIR_FW4.command", "Open", timeout=20)

#save frames
for j in range(100):
	j=j+1 #lbtintpar doesn't work with 0 seconds
	print float(j+1)*0.027
	pi.setINDI("LMIRCAM.Command.text", "%f 1 3 lbtintpar 500 sleep" % ((j+1)*0.027), timeout=15)
	pi.setINDI("LMIRCAM.Command.text", "go", timeout=15)

#turn off save data
pi.setINDI("LMIRCAM.Command.text", "0 savedata")
