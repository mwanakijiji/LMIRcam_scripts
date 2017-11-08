#!/usr/bin/python
#Darks/flats/linearity script
#AS-131019
#DD-150206-added datatype and wait statements
#AS-15001-corrected data types
#ES-150628-modified for more filters, specific to Pluto observation

# for now, this script includes a different section for each filter
# (later we can compactify each section into a function)

# integration time, coadds
params = [[0 for x in range(2)] for x in range(8)] 

params[0] = [0.204,4]
params[1] = [0.204,5]
params[2] = [0.291,5]
params[3] = [0.495,1]
params[4] = [0.495,2]
params[5] = [0.99,1]
params[6] = [10,1]
params[7] = [15,1]

n_sequences = 100

import time
from pyindi import * 

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

#turn off continuous acquisition
pi.setINDI("LMIRCAM.Command.text","0 contacq")
#turn on save data
pi.setINDI("LMIRCAM.Command.text", "1 savedata 0 autodispwhat 0 loglevel", wait=True)


# for loop for saving data
for j in range(len(params)):

  # save frames in up nod
  # the below line sets integ time, coadds, and sequences'
  pi.setINDI("LMIRCAM.Command.text", "%f %d %d lbtintpar 500 sleep" % (params[j][0], params[j][1], n_sequences), timeout=300)
  pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)

  pi.setINDI("LMIRCAM.Command.text","1000 sleep")

#turn off save data
pi.setINDI("LMIRCAM.Command.text", "0 savedata 1 autodispwhat 1 loglevel", wait=True)
