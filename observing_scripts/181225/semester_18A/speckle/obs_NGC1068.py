# Script for speckle interferometry of NGC1068's galaxy core (PI: G. Weigelt).
# This will nod and integrate, but will request pausing and resuming the AO loop.
#
# Instructions:
# - Use 512 pix FoV (left on the detector left so right of it will be another usable 512x512 area), single sided observations, K band.
# - Center the star in the FoV.
# - Find good integration time:
#   as short as posible, still getting reasonable SNR in the speckles, 0.146 sec requested by PI.
#   do NOT saturate.
# - Update script parameters in the 'USER DEFINED PARAMETERS' section.
# - Close the AO loop.
# - Start script and follow instructions.
#
# In case of a failure during execution: Fix the problem. Then:
# - Set up in the nod position you were in at the time of the failure.
# - Update the parameter 'i_nods_done' below as prompted by the script during the last execution.
# - Set parameter 'skip_first_int' to 'True' to start with a nod, or to 'False' to start with an integration in this position.
# - Restart script and follow instructions.

from lmircam_tools import pi
from lmircam_tools.exposures import get_lmircam_frames
from lmircam_tools.utils import nod, rawbg, setFLAG
from lmircam_tools.print_toold import *
from time import sleep

#################################################
# USER DEFINED PARAMETERS                       #
#################################################

# camera
dit = 0.146          # Minimum DIT, may need to be changed depending on SNR (reasonable SRN without saturating, DIT 
coadds = 1           # Do not change!
nseqs = 300          # Do not change!
savedata = True      # Save data? Can be 'True' or 'False'

# telesecope
nod_x = 5            # arcseconds in detector coords, might need updating
nod_y = 0            # arcseconds in detector coords, might need updating
side = 'left'        # singe sided observations, update which side is used
ao_operation = 'manual'   # resume/pause the AO loop manually or automatically

# nod sequence
i_nods_done = 0      # number of nods finished (see Instructions above on how to use)
skip_first_int = False   # set to 'True' if the script is restarted and should start with a nod rather than an integration

#################################################
# COMPUTATIONS/DEFINITIONS                      #
#################################################

nod_names = ['NOD_A','NOD_B']

#################################################
# COMMAND SEQUENCE                              #
#################################################

#=====================
# Start of nod cycles
#=====================

i_nod_start = i_nods_done
for i_nod in range(i_nods_done, 8):
  setFLAG(nod_names[i_nod % 2])
  if i_nod != i_nod_start or skip_first_int == False:
    for i_ao in range(0, 3):
      if ao_operation == 'manual':
        request('Please close/resume AO loop for 5 sec, then pause, wait 5 sec.')
        print 'Hit [RETURN] when done.'; raw_input()
        print ''
      else:
        info('Cycling the AO.')
        if side == 'left' or side = 'both':
          pi.setINDI('ao_indi_sx_ice.resume.arg', '1', wait=True)
        if side == 'right' or side = 'both':
          pi.setINDI('ao_indi_dx_ice.resume.arg', '1', wait=True)
        sleep(5)
        if side == 'left' or side = 'both':
          pi.setINDI('ao_indi_sx_ice.pause.arg', '1', wait=True)
        if side == 'right' or side = 'both':
          pi.setINDI('ao_indi_dx_ice.pause.arg', '1', wait=True)
        sleep(5)
      info('Taking data.') 
      print ''
      pi.setINDI('LMIRCAM.Command.text', '0 contacq')
      pi.setINDI('LMIRCAM.Command.text', '%f %i %i lbtintpar' % (dit, coadds, nseqs), wait=True)
      if savedata:
        pi.setINDI('LMIRCAM.Command.text', '1 savedata')
      else:
        pi.setINDI('LMIRCAM.Command.text', '0 savedata')
      pi.setINDI('LMIRCAM.Command.text','go')
  
  # Nodding
  if ao_operation == 'manual':
    request('Please close/resume AO loop.')
    print 'Hit [RETURN] when done.'; raw_input()
    print ''
  else:
    info('Resuming the AO for a nod.')
    if side == 'left' or side = 'both':
      pi.setINDI('ao_indi_sx_ice.resume.arg', '1', wait=True)
    if side == 'right' or side = 'both':
      pi.setINDI('ao_indi_dx_ice.resume.arg', '1', wait=True)

  rawbg()
  nod(nod_x * ((i_nod % 2) * -2 + 1),    nod_y * ((i_nod % 2) * -2 + 1),    side)
  i_nods_done = i_nods_done + 1
  info('Number of nods executed (parameter i_nods_done): ' + str(i_nods_done))
  print '' 
  pi.setINDI('LMIRCAM.Command.text', '0 savedata')
  pi.setINDI('LMIRCAM.Command.text', '%f %i %i lbtintpar' % (dit, coadds, 1), wait=True)
  pi.setINDI('LMIRCAM.Command.text','1 contacq')

#=============
# We're done!
#=============
setFLAG('')
request('Script finished. Please start new observation.')
