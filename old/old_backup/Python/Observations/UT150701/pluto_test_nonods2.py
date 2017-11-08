#!/usr/bin/python
#Darks/flats/linearity script
#AS-131019
#DD-150206-added datatype and wait statements
#AS-15001-corrected data types
#ES-150628-modified for more filters, specific to Pluto observation

# for now, this script includes a different section for each filter
# (later we can compactify each section into a function)

################################
################################
# PARAMETERS TO BE SET BY USER 

# notes
# 1. prereq: LMIR FW1 is LargeDualAperture
# 2. prereq: start in up nod
# 3. prereq: as usual, make sure NIL BEAMDIV, DICHROIC are +,- (trichroic, imaging)

# detector integration times (if not multiples of 0.029 sec, camera will round to nearest one)
dit_h2oice2 = 0.2
dit_lcont1 = 0.029
dit_n3309 = 0.4
dit_lcont2 = 0.029
dit_lcont3 = 1
dit_lcont4 = 0.029
dit_braon = 3.2

# number of coadds
coadd_h2oice2 = 1
coadd_lcont1 = 1
coadd_n3309 = 1
coadd_lcont2 = 1
coadd_lcont3 = 1
coadd_lcont4 = 1
coadd_braon = 1

# sequences per nod position (1 sequence includes n coadds)
seq_h2oice2 = 3
seq_lcont1 = 1
seq_n3309 = 2
seq_lcont2 = 1
seq_lcont3 = 1
seq_lcont4 = 3
seq_braon = 1

# nod amplitudes (abs())
x_nod_amplitude = 0.0
y_nod_amplitude = 4.5

# number of nod pairs (up+down) to do per filter
nod_pairs_per_filter = 1

# END PARAMETERS SET BY USER 
##############################
##############################


import time
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
	time.sleep(0.05) 
        if rstatus == "AORunning" and lstatus == "AORunning":
            break

#turn off continuous acquisition
pi.setINDI("LMIRCAM.Command.text","0 contacq")
#turn on save data
pi.setINDI("LMIRCAM.Command.text", "1 savedata 0 autodispwhat 0 loglevel", wait=True)

# timeouts to allow filters to move into place
filter_timeout = 500
sleeptime=0.5

################################
# H20 ICE2

#set and obstype filters to H2O ICE2
print 'SWITCHING TO H2O ICE 2...'
pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=filter_timeout, wait=True) # 'home' is the same as 'Open'
pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=filter_timeout, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "H2O-Ice2", timeout=filter_timeout, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=DRK;Comment=SCI/CAL/DRK/FLT") # for inserting comment into FITS header

# for loop for saving data, nodding
for j in range(nod_pairs_per_filter):

  # save frames in up nod
  # the below line sets integ time, coadds, and sequences'
  pi.setINDI("LMIRCAM.Command.text", "%f %d %d lbtintpar 500 sleep" % (dit_h2oice2, coadd_h2oice2, seq_h2oice2), timeout=300)
  print 'TAKING H20ICE2 FRAMES, UP NOD....'
  pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)
  # use the last frame as a background
  pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)
  time.sleep(sleeptime) # in case camera receives overlapping commands 

  # nod down       
  #pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", x_nod_amplitude, "LBTO.OffsetPointing.OffsetY", -y_nod_amplitude, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 
  # wait for AO to close loop and stabilize for a second before taking next set
  #wait4AORunning()

  # save frames in the down nod
  pi.setINDI("LMIRCAM.Command.text","1000 sleep")
  print 'TAKING H20ICE2 FRAMES, DOWN NOD....'
  pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
  pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)
  time.sleep(sleeptime) # in case camera receives overlapping commands 

  # nod up in prep for next set
  #pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", x_nod_amplitude, "LBTO.OffsetPointing.OffsetY", y_nod_amplitude, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 
  #wait4AORunning() 
  pi.setINDI("LMIRCAM.Command.text","1000 sleep")


################################
# L-CONT1

#set filters and datatype to L-CONT1
print 'SWITCHING TO L-CONT 1...'
#pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=filter_timeout, wait=True) # (already home)
pi.setINDI("Lmir.LMIR_FW3.command", "Lcont1", timeout=filter_timeout, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "_home_", timeout=filter_timeout, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

# for loop for saving data, nodding
for j in range(nod_pairs_per_filter):

  # save frames in up nod
  # the below line sets integ time, coadds, and sequences'
  pi.setINDI("LMIRCAM.Command.text", "%f %d %d lbtintpar 500 sleep" % (dit_lcont1, coadd_lcont1, seq_lcont1), timeout=300)
  print 'TAKING L-CONT1 FRAMES, UP NOD....'
  pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)
  # use the last frame as a background
  pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)
  time.sleep(sleeptime) # in case camera receives overlapping commands 

  # nod down       
  #pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", x_nod_amplitude, "LBTO.OffsetPointing.OffsetY", -y_nod_amplitude, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 
  # wait for AO to close loop and stabilize for a second before taking next set
  #wait4AORunning()

  # save frames in the down nod
  pi.setINDI("LMIRCAM.Command.text","1000 sleep")
  print 'TAKING L-CONT1 FRAMES, DOWN NOD....'
  pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
  pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)
  time.sleep(sleeptime) # in case camera receives overlapping commands 

  # nod up in prep for next set
  #pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", x_nod_amplitude, "LBTO.OffsetPointing.OffsetY", y_nod_amplitude, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 
  #wait4AORunning() 
  pi.setINDI("LMIRCAM.Command.text","1000 sleep")

################################
# N3309

#set filters and datatype to N3309
print 'SWITCHING TO N3309...'
#pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=filter_timeout, wait=True) # (already home)
pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=filter_timeout, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "N03309-8", timeout=filter_timeout, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

# for loop for saving data, nodding
for j in range(nod_pairs_per_filter):

  # save frames in up nod
  # the below line sets integ time, coadds, and sequences'
  pi.setINDI("LMIRCAM.Command.text", "%f %d %d lbtintpar 500 sleep" % (dit_n3309, coadd_n3309, seq_n3309), timeout=300)
  print 'TAKING N3309 FRAMES, UP NOD...' 
  pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)
  # use the last frame as a background
  pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)
  time.sleep(sleeptime) # in case camera receives overlapping commands 

  # nod down       
  #pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", x_nod_amplitude, "LBTO.OffsetPointing.OffsetY", -y_nod_amplitude, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 
  # wait for AO to close loop and stabilize for a second before taking next set
  #wait4AORunning()

  # save frames in the down nod
  pi.setINDI("LMIRCAM.Command.text","1000 sleep")
  print 'TAKING N3309 FRAMES, DOWN NOD....'
  pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
  pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)
  time.sleep(sleeptime) # in case camera receives overlapping commands 

  # nod up in prep for next set
  #pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", x_nod_amplitude, "LBTO.OffsetPointing.OffsetY", y_nod_amplitude, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 
  #wait4AORunning() 
  pi.setINDI("LMIRCAM.Command.text","1000 sleep")

################################
# L-CONT2

#set filters and datatype to L-CONT2
print 'SWITCHING TO L-CONT 2...'
pi.setINDI("Lmir.LMIR_FW2.command", "L-cont2", timeout=filter_timeout, wait=True)
#pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=filter_timeout, wait=True) # (already home)
pi.setINDI("Lmir.LMIR_FW4.command", "_home_", timeout=filter_timeout, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

# for loop for saving data, nodding
for j in range(nod_pairs_per_filter):

  # save frames in up nod
  # the below line sets integ time, coadds, and sequences'
  pi.setINDI("LMIRCAM.Command.text", "%f %d %d lbtintpar 500 sleep" % (dit_lcont2, coadd_lcont2, seq_lcont2), timeout=300)
  print 'TAKING L-CONT2 FRAMES, UP NOD...' 
  pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)
  # use the last frame as a background
  pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)
  time.sleep(sleeptime) # in case camera receives overlapping commands 

  # nod down       
  #pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", x_nod_amplitude, "LBTO.OffsetPointing.OffsetY", -y_nod_amplitude, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 
  # wait for AO to close loop and stabilize for a second before taking next set
  #wait4AORunning()

  # save frames in the down nod
  pi.setINDI("LMIRCAM.Command.text","1000 sleep")
  print 'TAKING L-CONT2 FRAMES, DOWN NOD...'
  pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
  pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)
  time.sleep(sleeptime) # in case camera receives overlapping commands 

  # nod up in prep for next set
  #pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", x_nod_amplitude, "LBTO.OffsetPointing.OffsetY", y_nod_amplitude, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 
  #wait4AORunning() 
  pi.setINDI("LMIRCAM.Command.text","1000 sleep")

################################
# L-CONT3

#set filters and datatype to L-CONT3
print 'SWITCHING TO L-CONT 3...'
pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=filter_timeout, wait=True)
#pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=filter_timeout, wait=True) # (already home)
pi.setINDI("Lmir.LMIR_FW4.command", "Lcont3", timeout=filter_timeout, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

# for loop for saving data, nodding
for j in range(nod_pairs_per_filter):

  # save frames in up nod
  # the below line sets integ time, coadds, and sequences'
  pi.setINDI("LMIRCAM.Command.text", "%f %d %d lbtintpar 500 sleep" % (dit_lcont3, coadd_lcont3, seq_lcont3), timeout=300)
  print 'TAKING L-CONT3 FRAMES, UP NOD...' 
  pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)
  # use the last frame as a background
  pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)
  time.sleep(sleeptime) # in case camera receives overlapping commands 

  # nod down       
  #pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", x_nod_amplitude, "LBTO.OffsetPointing.OffsetY", -y_nod_amplitude, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 
  # wait for AO to close loop and stabilize for a second before taking next set
  #wait4AORunning()

  # save frames in the down nod
  pi.setINDI("LMIRCAM.Command.text","1000 sleep")
  print 'TAKING L-CONT3 FRAMES, DOWN NOD...'
  pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
  pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)
  time.sleep(sleeptime) # in case camera receives overlapping commands 

  # nod up in prep for next set
  #pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", x_nod_amplitude, "LBTO.OffsetPointing.OffsetY", y_nod_amplitude, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 
  #wait4AORunning() 
  pi.setINDI("LMIRCAM.Command.text","1000 sleep")

################################
# L-CONT4

#set filters and datatype to L-CONT4
print 'SWITCHING TO L-CONT 4...'
pi.setINDI("Lmir.LMIR_FW2.command", "L-cont4", timeout=filter_timeout, wait=True)
#pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=filter_timeout, wait=True) # (already home)
pi.setINDI("Lmir.LMIR_FW4.command", "_home_", timeout=filter_timeout, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

# for loop for saving data, nodding
for j in range(nod_pairs_per_filter):

  # save frames in up nod
  # the below line sets integ time, coadds, and sequences'
  pi.setINDI("LMIRCAM.Command.text", "%f %d %d lbtintpar 500 sleep" % (dit_lcont4, coadd_lcont4, seq_lcont4), timeout=300)
  print 'TAKING L-CONT4 FRAMES, UP NOD...' 
  pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)
  # use the last frame as a background
  pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)
  time.sleep(sleeptime) # in case camera receives overlapping commands 

  # nod down       
  #pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", x_nod_amplitude, "LBTO.OffsetPointing.OffsetY", -y_nod_amplitude, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 
  # wait for AO to close loop and stabilize for a second before taking next set
  #wait4AORunning()

  # save frames in the down nod
  pi.setINDI("LMIRCAM.Command.text","1000 sleep")
  print 'TAKING L-CONT4 FRAMES, DOWN NOD...'
  pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
  pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)
  time.sleep(sleeptime) # in case camera receives overlapping commands 

  # nod up in prep for next set
  #pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", x_nod_amplitude, "LBTO.OffsetPointing.OffsetY", y_nod_amplitude, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 
  #wait4AORunning() 
  pi.setINDI("LMIRCAM.Command.text","1000 sleep")

################################
# BRA-ON

#set filters and datatype to BRA-ON
print 'SWITCHING TO BRA-ON...'
pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=filter_timeout, wait=True)
#pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=filter_timeout, wait=True) # (already home)
pi.setINDI("Lmir.LMIR_FW4.command", "Br-Alpha-On", timeout=filter_timeout, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

# for loop for saving data, nodding
for j in range(nod_pairs_per_filter):

  # save frames in up nod
  # the below line sets integ time, coadds, and sequences'
  pi.setINDI("LMIRCAM.Command.text", "%f %d %d lbtintpar 500 sleep" % (dit_braon, coadd_braon, seq_braon), timeout=300)
  print 'TAKING BRA-ON FRAMES, UP NOD...' 
  pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)
  # use the last frame as a background
  pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)
  time.sleep(sleeptime) # in case camera receives overlapping commands 

  # nod down       
  #pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", x_nod_amplitude, "LBTO.OffsetPointing.OffsetY", -y_nod_amplitude, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 
  # wait for AO to close loop and stabilize for a second before taking next set
  #wait4AORunning()

  # save frames in the down nod
  pi.setINDI("LMIRCAM.Command.text","1000 sleep")
  print 'TAKING BRA-ON FRAMES, DOWN NOD...'
  pi.setINDI("LMIRCAM.Command.text","go",timeout=300,wait=True)
  pi.setINDI("LMIRCAM.Command.text","rawbg",timeout=300,wait=True)
  time.sleep(sleeptime) # in case camera receives overlapping commands 

  # nod up in prep for next set
  #pi.setINDI("LBTO.OffsetPointing.CoordSys", "DETXY","LBTO.OffsetPointing.OffsetX", x_nod_amplitude, "LBTO.OffsetPointing.OffsetY", y_nod_amplitude, "LBTO.OffsetPointing.Side", "both", "LBTO.OffsetPointing.Type", "REL", timeout=400) 
  #wait4AORunning() 
  pi.setINDI("LMIRCAM.Command.text","1000 sleep")
  print 'Done with one iteration of the final for-loop'

################################

print 'DONE WITH INTEGRATIONS!'

#turn off save data
pi.setINDI("LMIRCAM.Command.text", "0 savedata 1 autodispwhat 1 loglevel", wait=True)
