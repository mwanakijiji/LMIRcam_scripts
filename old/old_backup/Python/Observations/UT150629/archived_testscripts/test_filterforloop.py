#!/usr/bin/python
#Darks/flats/linearity script
#AS-131019
#DD-150206-added datatype and wait statements
#AS-15001-corrected data types
#ES-150628-modified for more filters, specific to Pluto observation


################################
################################
# PARAMETERS TO BE SET BY USER 

# notes
# 1. prereq: start with LMIR FW1 LargeDualAperture
# 2. prereq: start in up nod
# 3. prereq: as usual, make sure NIL BEAMDIV, DICHROIC are +,- (trichroic, imaging)

# detector integration times (if not multiples of 0.029 sec, camera will round to nearest one)
dit_h2oice2 = 0.029
dit_lcont1 = 0.029
dit_n3309 = 0.029
dit_lcont2 = 0.029
dit_lcont3 = 0.029
dit_lcont4 = 0.029
dit_braon = 0.029

# number of coadds
coadd_h2oice2 = 1
coadd_lcont1 = 1
coadd_n3309 = 1
coadd_lcont2 = 1
coadd_lcont3 = 1
coadd_lcont4 = 1
coadd_braon = 1

# sequences per nod position (1 sequence includes n coadds)
seq_h2oice2 = 1
seq_lcont1 = 1
seq_n3309 = 1
seq_lcont2 = 1
seq_lcont3 = 1
seq_lcont4 = 1
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

################################

# for loop for saving data, nodding
for j in range(20):
    print j
    pi.setINDI("Lmir.LMIR_FW3.command", "Lcont1", timeout=filter_timeout, wait=True)
    time.sleep(0.5) 
    #pi.setINDI("Lmir.LMIR_FW4.command", "_home_", timeout=filter_timeout, wait=True)
    #time.sleep(0.5) 

    pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=filter_timeout, wait=True)
    time.sleep(0.5) 
    #pi.setINDI("Lmir.LMIR_FW4.command", "_home_", timeout=filter_timeout, wait=True)
    #time.sleep(0.5) 
