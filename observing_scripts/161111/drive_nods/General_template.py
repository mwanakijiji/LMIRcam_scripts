#!/usr/bin/python
import time
from pyindi import * 
########
#This script does not change filters or set integration times.
#it just does 10 left right nod sequences. Set the filters, 
#the star positions and the integration parameters manually.
#The nod is 4.5 arcseconds right first and then left
#########
#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

SIDE = 'left' # choose 'left', 'right', or 'both'
XOFF = 0 #xoffset in arcseconds
YOFF = 4.5 #yoffset in arcseconds
TYPE = "REL" #offset type
COORDS = "DETXY" #offset coordinate system
NUMBER_OF_NOD_PAIRS = 10

def wait4AORunning(side):
    pistr={'left':["LBTO.Dictionary.Name=L_AOStatus;Value="],
           'right':["LBTO.Dictionary.Name=R_AOStatus;Value="]
           'both':["LBTO.Dictionary.Name=L_AOStatus;Value=",
                   "LBTO.Dictionary.Name=R_AOStatus;Value="]}[side]
    while True:
        status=[]
        for side_string in pisstr:
            pi.setINDI(side_string)
            state = pi.getINDI("LBTO.Dictionary.Value")
            status.append(state)
        time.sleep(0.02) 
        if all([s == "AORunning" for s in status]):
            break

def nod(XOff,YOff,side,Coords="DETXY",Type="REL"):
    pi.setINDI("LBTO.OffsetPointing.CoordSys", Coords,
           "LBTO.OffsetPointing.OffsetX", XOff, 
           "LBTO.OffsetPointing.OffsetY", YOff, 
           "LBTO.OffsetPointing.Side", side, 
           "LBTO.OffsetPointing.Type", Type, 
           timeout=400,
           wait=False) 

pi.setINDI("LMIRCAM.Command.text","0 contacq",wait=True)
pi.setINDI("LMIRCAM.Command.text","1 savedata")
#set number of up down nod pairs
for j in range(NUMBER_OF_NOD_PAIRS):
    print j
    pi.setINDI("LMIRCAM.Command.text","go",timeout=1000,wait=True)
    pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=1000,wait=False)
    nod(XOFF, YOFF, SIDE, Coords=COORDS, Type=TYPE)
    wait4AORunning(SIDE)
    #time.sleep(1)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=1000,wait=True)
    pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=1000,wait=False)
    nod(-1*XOFF, -1*YOFF, SIDE, Coords=COORDS, Type=TYPE)
    wait4AORunning(SIDE) 
    #time.sleep(1)
pi.setINDI("LMIRCAM.Command.text","0 savedata",timeout=300,wait=True)


