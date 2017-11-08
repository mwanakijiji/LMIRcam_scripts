#!/usr/bin/python
#Script to demonstrate bad response from lmircam electronics

import time
from pyindi import * 
pi=PyINDI(verbose=True)

#turn off save data
pi.setINDI("LMIRCAM.Command.text", "0 savedata 1 autodispwhat 0 loglevel", wait=True)

#take a sequence of 10 frames, 10 times
for i in range (10) :
    pi.setINDI("LMIRCAM.Command.text", "0.1 1 10 lbtintpar", timeout=300, wait=True)
    #time.sleep(0.1)
    pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)
    print 'Successful' ,(i+1) , 'times'
