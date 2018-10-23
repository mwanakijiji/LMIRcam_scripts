import time
from pyindi import * 
import numpy as np

pi = PyINDI(verbose = False)

def ten(coord):
    '''change a sexageismal to a decimal
    INPUTS:
    coord a python list [hh/dd, mm, ss]'''
    coord=np.array(coord)
    num=len(coord)
    fac=np.array([1.,60.0,3600.0])
    if (coord < 0).sum() > 0:
        sign=-1
    else:
        sign=1
    return sign*(np.abs(coord)/fac[:num]).sum()

def wait4AORunning(side):
    pistr={'left':"LBTO.Dictionary.Name=L_AOStatus;Value=",
           'right':"LBTO.Dictionary.Name=R_AOStatus;Value="}[side]
    while True:
        pi.setINDI(pistr)
        status = pi.getINDI("LBTO.Dictionary.Value")
        time.sleep(0.02) 
        if status == "AORunning":
            break

def makeOffsets(RA,Dec,sep,PA):
    '''Take the RA and Dec of the primary, and the 
    separation and PA of the secondary, and return
    the appropriate nod vectors for 3-point dither
    pattern.
    PA East of North. North up East left.
    INPUTS:
    RA = [hh, mm, ss.dd]
    Dec = [dd, mm, ss.dd]
    sep = arcseconds
    PA = degrees'''
    secDecOff = -1*sep*np.cos(PA*np.pi/180.)#arcseconds
    secRAOff = -1*sep*np.sin(PA*np.pi/180.)#arcseconds NO cos(dec)!!!

    skyDecOff = -1*secDecOff
    skyRAOff = -1*secRAOff

    priDecOff = 0
    priRAOff = 0

    return priRAOff, priDecOff, secRAOff, secDecOff, skyRAOff, skyDecOff
    
def nod_sneakSomeDarks(RAOff,DecOff,darkIntParams,side):
    '''send an ABS RADEC nod in the direction RAOff, DecOff. While moving
    spin lmir_fw2 by half a position to act as a blank and grab some
    dark frames. Then move lmir_fw2 back to where it was.'''
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "RADEC",
           "LBTO.OffsetPointing.OffsetX", DecOff, 
           "LBTO.OffsetPointing.OffsetY", RAOff, 
           "LBTO.OffsetPointing.Side", side, 
           "LBTO.OffsetPointing.Type", "ABS", 
           timeout=400,
           wait=False) 
	###where's FW2
    pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=DRK;Comment=observation type", wait=False)
    pi.setINDI("LMIRCAM.Command.text", "0 contacq", wait=True)
    pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % darkIntParams, wait=True)
    fw2_pos = pi.getINDI("Lmir.lmir_FW2_status.PosNum", wait=True)
    pi.setINDI("Lmir.lmir_FW2.command", int(fw2_pos)+25000, timeout=20, wait=True)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
    pi.setINDI("Lmir.lmir_FW2.command", int(fw2_pos), timeout=20, wait=True)

def nod_sneakSomeDarksDETXY(XOff,YOff,darkIntParams,side):
    pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY",
           "LBTO.OffsetPointing.OffsetX", XOff, 
           "LBTO.OffsetPointing.OffsetY", YOff, 
           "LBTO.OffsetPointing.Side", side, 
           "LBTO.OffsetPointing.Type", "REL", 
           timeout=400,
           wait=False) 
	###where's FW2
    pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=DRK;Comment=observation type", wait=False)
    pi.setINDI("LMIRCAM.Command.text", "0 contacq", wait=True)
    pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % darkIntParams, wait=True)
    fw2_pos = pi.getINDI("Lmir.lmir_FW2_status.PosNum", wait=True)
    pi.setINDI("Lmir.lmir_FW2.command", int(fw2_pos)+25000, timeout=20, wait=True)
    pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
    pi.setINDI("Lmir.lmir_FW2.command", int(fw2_pos), timeout=20, wait=True)

#Modify the below to work with sketchy lmircam readouts...
#def do_exposures(Lintparams,Nintparams,flag, side):
#    pi.setINDI("NOMIC.Command.text", "0 contacq", wait=True)
#    pi.setINDI("NOMIC.Command.text", "1 savedata", wait=True)
#    pi.setINDI("NOMIC.Command.text", "%f %i %i lbtintpar" % Nintparams, wait=True)
#
#    pi.setINDI("LMIRCAM.Command.text", "0 contacq", wait=True)
#    pi.setINDI("LMIRCAM.Command.text", "1 savedata", wait=True)
#    pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % Lintparams, wait=True)
#
#    bxcur, bycur, bxreq, byreq = get_baysidestage_positions(side)
#    print 'bayside stage positions, xcur, ycur, xreq, yreq:'
#    print bxcur, bycur, bxreq, byreq
#    pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=%s ;Comment=ALES observation type"%flag, wait=False)
#    pi.setINDI("LMIRCAM.EditFITS.Keyword=BAYXCUR;Value=%f ;Comment=ALES current baysidex position"%bxcur,wait=True)
#    pi.setINDI("LMIRCAM.EditFITS.Keyword=BAYXREQ;Value=%f ;Comment=ALES requested baysidex position"%bxreq,wait=True)
#    pi.setINDI("LMIRCAM.EditFITS.Keyword=BAYYCUR;Value=%f ;Comment=ALES current baysidex position"%bycur,wait=True)
#    pi.setINDI("LMIRCAM.EditFITS.Keyword=BAYYREQ;Value=%f ;Comment=ALES requested baysidex position"%byreq,wait=True)
#    pi.setINDI("NOMIC.EditFITS.Keyword=FLAG;Value=%s ;Comment=ALES observation type"%flag, wait=True)
#    pi.setINDI("NOMIC.EditFITS.Keyword=BAYXCUR;Value=%f ;Comment=ALES current baysidex position"%bxcur,wait=True)
#    pi.setINDI("NOMIC.EditFITS.Keyword=BAYXREQ;Value=%f ;Comment=ALES requested baysidex position"%bxreq,wait=True)
#    pi.setINDI("NOMIC.EditFITS.Keyword=BAYYCUR;Value=%f ;Comment=ALES current baysidex position"%bycur,wait=True)
#    pi.setINDI("NOMIC.EditFITS.Keyword=BAYYREQ;Value=%f ;Comment=ALES requested baysidex position"%byreq,wait=True)
#
#    pi.setINDI("NOMIC.Command.text","go",timeout=300,wait=False)
#    pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)

def go_exposures(Lintparams,flag, side, inner_loop_max=10):
    #set keywords for ALES pipeline
    bxcur, bycur, bxreq, byreq = get_baysidestage_positions(side)
    print 'bayside stage positions, xcur, ycur, xreq, yreq:'
    print bxcur, bycur, bxreq, byreq
    pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=%s ;Comment=ALES observation type"%flag, wait=False)
    pi.setINDI("LMIRCAM.EditFITS.Keyword=BAYXCUR;Value=%f ;Comment=ALES current baysidex position"%bxcur,wait=True)
    pi.setINDI("LMIRCAM.EditFITS.Keyword=BAYXREQ;Value=%f ;Comment=ALES requested baysidex position"%bxreq,wait=True)
    pi.setINDI("LMIRCAM.EditFITS.Keyword=BAYYCUR;Value=%f ;Comment=ALES current baysidex position"%bycur,wait=True)
    pi.setINDI("LMIRCAM.EditFITS.Keyword=BAYYREQ;Value=%f ;Comment=ALES requested baysidex position"%byreq,wait=True)
    pi.setINDI("NOMIC.EditFITS.Keyword=FLAG;Value=%s ;Comment=ALES observation type"%flag, wait=True)
    pi.setINDI("NOMIC.EditFITS.Keyword=BAYXCUR;Value=%f ;Comment=ALES current baysidex position"%bxcur,wait=True)
    pi.setINDI("NOMIC.EditFITS.Keyword=BAYXREQ;Value=%f ;Comment=ALES requested baysidex position"%bxreq,wait=True)
    pi.setINDI("NOMIC.EditFITS.Keyword=BAYYCUR;Value=%f ;Comment=ALES current baysidex position"%bycur,wait=True)
    pi.setINDI("NOMIC.EditFITS.Keyword=BAYYREQ;Value=%f ;Comment=ALES requested baysidex position"%byreq,wait=True)

    #get NOMIC going
    #pi.setINDI("NOMIC.Command.text", "0 contacq", wait=True)
    #pi.setINDI("NOMIC.Command.text", "1 savedata", wait=True)
    #pi.setINDI("NOMIC.Command.text", "%f %i %i lbtintpar" % Nintparams, wait=True)
    time.sleep(0.01)
    pi.setINDI("NOMIC.Command.text","go",timeout=300,wait=False)

    #Get lmircam going, fuss to avoid bad rows with too many nseqs...
    dit, coadds, nseqs = Lintparams
    coadds = int(coadds)
    nseqs = int(nseqs)
    inner_loop_max = int(inner_loop_max)
    N_outer_loops = nseqs / inner_loop_max
    remainder = nseqs % inner_loop_max
    if N_outer_loops == 0:
        lbtintparams = (dit, coadds, nseqs)
    else:
        lbtintparams = (dit, coadds, inner_loop_max)

    pi.setINDI("LMIRCAM.Command.text", "0 contacq", wait=True)
    pi.setINDI("LMIRCAM.Command.text", "1 savedata", wait=True)
    #pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % lbtintparams, wait=True)
    #first loop
    pi.setINDI("LMIRCAM.Command.text","go",timeout=(8*dit*coadds*inner_loop_max),wait=True)
    #other loops
    for ii in xrange(max(0,N_outer_loops-1)):
        pi.setINDI("LMIRCAM.Command.text","go",timeout=(8*dit*coadds*inner_loop_max),wait=True)
    if remainder > 0:
        pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % (dit, coadds, remainder), wait=True)
        pi.setINDI("LMIRCAM.Command.text","go",timeout=(8*dit*coadds*nseqs),wait=True) 

def do_exposures(Lintparams,Nintparams,flag, side, inner_loop_max=10):
    #set keywords for ALES pipeline
    bxcur, bycur, bxreq, byreq = get_baysidestage_positions(side)
    print 'bayside stage positions, xcur, ycur, xreq, yreq:'
    print bxcur, bycur, bxreq, byreq
    pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=%s ;Comment=ALES observation type"%flag, wait=False)
    pi.setINDI("LMIRCAM.EditFITS.Keyword=BAYXCUR;Value=%f ;Comment=ALES current baysidex position"%bxcur,wait=True)
    pi.setINDI("LMIRCAM.EditFITS.Keyword=BAYXREQ;Value=%f ;Comment=ALES requested baysidex position"%bxreq,wait=True)
    pi.setINDI("LMIRCAM.EditFITS.Keyword=BAYYCUR;Value=%f ;Comment=ALES current baysidex position"%bycur,wait=True)
    pi.setINDI("LMIRCAM.EditFITS.Keyword=BAYYREQ;Value=%f ;Comment=ALES requested baysidex position"%byreq,wait=True)
    pi.setINDI("NOMIC.EditFITS.Keyword=FLAG;Value=%s ;Comment=ALES observation type"%flag, wait=True)
    pi.setINDI("NOMIC.EditFITS.Keyword=BAYXCUR;Value=%f ;Comment=ALES current baysidex position"%bxcur,wait=True)
    pi.setINDI("NOMIC.EditFITS.Keyword=BAYXREQ;Value=%f ;Comment=ALES requested baysidex position"%bxreq,wait=True)
    pi.setINDI("NOMIC.EditFITS.Keyword=BAYYCUR;Value=%f ;Comment=ALES current baysidex position"%bycur,wait=True)
    pi.setINDI("NOMIC.EditFITS.Keyword=BAYYREQ;Value=%f ;Comment=ALES requested baysidex position"%byreq,wait=True)

    #get NOMIC going
    pi.setINDI("NOMIC.Command.text", "0 contacq", wait=True)
    pi.setINDI("NOMIC.Command.text", "1 savedata", wait=True)
    pi.setINDI("NOMIC.Command.text", "%f %i %i lbtintpar" % Nintparams, wait=True)
    time.sleep(0.3)
    pi.setINDI("NOMIC.Command.text","go",timeout=300,wait=False)

    #Get lmircam going, fuss to avoid bad rows with too many nseqs...
    dit, coadds, nseqs = Lintparams
    coadds = int(coadds)
    nseqs = int(nseqs)
    inner_loop_max = int(inner_loop_max)
    N_outer_loops = nseqs / inner_loop_max
    remainder = nseqs % inner_loop_max
    if N_outer_loops == 0:
        lbtintparams = (dit, coadds, nseqs)
    else:
        lbtintparams = (dit, coadds, inner_loop_max)

    pi.setINDI("LMIRCAM.Command.text", "0 contacq", wait=True)
    pi.setINDI("LMIRCAM.Command.text", "1 savedata", wait=True)
    pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % lbtintparams, wait=True)
    #first loop
    pi.setINDI("LMIRCAM.Command.text","go",timeout=(8*dit*coadds*inner_loop_max),wait=True)
    #other loops
    for ii in xrange(max(0,N_outer_loops-1)):
        pi.setINDI("LMIRCAM.Command.text","go",timeout=(8*dit*coadds*inner_loop_max),wait=True)
    if remainder > 0:
        pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % (dit, coadds, remainder), wait=True)
        pi.setINDI("LMIRCAM.Command.text","go",timeout=(8*dit*coadds*nseqs),wait=True) 

def get_baysidestage_positions(side):
    sidestrs = {'left':('sx','L'),'right':('dx','R')}[side]
    bayxcur = pi.getINDI("indi_"+sidestrs[0]+"_wfs_msgd.baysidex___"+sidestrs[1]+"___POS___CUR.value")
    bayxreq = pi.getINDI("indi_"+sidestrs[0]+"_wfs_msgd.baysidex___"+sidestrs[1]+"___POS___REQ.value")
    bayycur = pi.getINDI("indi_"+sidestrs[0]+"_wfs_msgd.baysidey___"+sidestrs[1]+"___POS___CUR.value")
    bayyreq = pi.getINDI("indi_"+sidestrs[0]+"_wfs_msgd.baysidey___"+sidestrs[1]+"___POS___REQ.value")
    return bayxcur, bayycur, bayxreq, bayyreq
