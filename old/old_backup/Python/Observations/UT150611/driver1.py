import sys, os, string, time, pyfits,  pdb, copy
import numpy
from pyindi import *
from scipy import ndimage, sqrt, stats
pi=PyINDI()
settingsFPC  = pi.getINDI("Acromag.FPC_status.*")
tipFPC  = settingsFPC["Acromag.FPC_status.Tip"]
tiltFPC  = settingsFPC["Acromag.FPC_status.Tilt"]
pistonFPC  = settingsFPC["Acromag.FPC_status.Piston"]

print 'OLD:'
print tipFPC
print tiltFPC
print pistonFPC

newtipFPC = -1e-5
newtiltFPC = -1e-5
newpistonFPC = 0
mode = 1

keys=("Acromag.FPC.Tip","Acromag.FPC.Tilt","Acromag.FPC.Piston","Acromag.FPC.Mode")
values=(newtipFPC,newtiltFPC,newpistonFPC,mode)

newsettingsFPC={keys[0]:values[0],keys[1]:values[1],keys[2]:values[2],keys[3]:values[3]}
pi.setINDI(newsettingsFPC)
time.sleep(0.05) 

checkSettingsFPC  = pi.getINDI("Acromag.FPC_status.*")
checkTipFPC  = settingsFPC["Acromag.FPC_status.Tip"]
checkTiltFPC  = settingsFPC["Acromag.FPC_status.Tilt"]
checkPistonFPC  = settingsFPC["Acromag.FPC_status.Piston"]

print 'NEW:'
print checkTipFPC
print checkTiltFPC
print checkPistonFPC

#dict = {}





