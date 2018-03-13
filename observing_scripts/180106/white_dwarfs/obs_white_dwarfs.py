# Script for white dwarf planet imaging (PI: S. Ertel).
# This will only nod and request you to do the integrations manually (for robustness).
#
# Instructions:
# - Use the 'Mostly Unvignetted' FoV, single sided observations, H band.
# - Targets are faint, be aware of the long integration times and potential AO problems.
# - Center the star in the lower-left corner of the FoV [550,400].
# - Find good integration time:
#   as long as posible, considering:
#     do not saturate beyond 0.2 arcsec from peak
#     do not integrate >60sec for stability and to avoid too much rotational smearing of any companions
# - Update script parameters in the 'USER DEFINED PARAMETERS' section.
# - Start script and follow instructions.
#
# In case of a failure during execution: Fix the problem. Then you have two options:
#  a) - Set up in the nod position you were in at the time of the failure.
#     - Update the parameter 'i_nods_done' below as prompted by the script during the last execution.
#     - Restart script and follow instructions (e.g., take more frames if needed).
#  b) - Set up in the next nod position.
#     - Update the parameter 'i_nods_done' below as prompted by the script during the last execution, but add 1 for the manual nod.
#     - Restart script and follow instructions (e.g., take frames in this position).

from lmircam_tools import pi
from lmircam_tools.exposures import get_lmircam_frames
from lmircam_tools.utils import nod, rawbg, setFLAG
from lmircam_tools.print_tools import *
from time import sleep

#################################################
# USER DEFINED PARAMETERS                       #
#################################################

#camera
dit_bkg = 10          # DIT for background and source positioning. May need updating based on source brightness.
dit = 30             # May need to be changed depending on saturation (remember to also change nseqs!)
coadds = 1           # Do not change!
nseqs = 20           # Change according to dit change: dit * nseqs = 600
savedata = True      # Save data? Can be 'True' or 'False'

#telesecope
nod_x = 6            # arcseconds in detector coords, might need updating
nod_y = 5            # arcseconds in detector coords, might need updating
side = 'left'        # singe sided observations, update which side is used
i_nods_done = 2      # number of nods finished (see Instructions above on how to use)

#################################################
# COMPUTATIONS/DEFINITIONS                      #
#################################################

nod_names = ['NOD_A','NOD_B']
x_dither = [0.0, 0.1, 0.0, 0.0,  0.0, -0.1, 0.0]
y_dither = [0.0, 0.0,  0.0, 0.1, 0.0, 0.0,   0.0]

#################################################
# COMMAND SEQUENCE                              #
#################################################

pi.setINDI('LMIRCAM.Command.text', '0 contacq')
pi.setINDI('LMIRCAM.Command.text', '%f %i %i lbtintpar' % (dit, coadds, nseqs), wait=True)
if savedata:
  pi.setINDI('LMIRCAM.Command.text', '1 savedata')
else:
  pi.setINDI('LMIRCAM.Command.text', '0 savedata')

#=====================
# Start of nod cycles
#=====================

for i_nod in range(i_nods_done, 8):
  # Requesting to take data
  setFLAG(nod_names[i_nod % 2])
  request('Nod position ' + str(i_nod + 1) + ' of 8. Please integrate:')
  print '  Verify source position.'
  print '  Turn off background.'
  print '  Take data (dit x nseqs should be ~10 min).'
  print 'Hit [RETURN] when done.'; raw_input()
  print ''

  # Nodding
  pi.setINDI('LMIRCAM.Command.text', '0 contacq')
  pi.setINDI('LMIRCAM.Command.text', '0 savedata')
  pi.setINDI('LMIRCAM.Command.text', '%f 1 1 lbtintpar' % dit_bkg, wait=True)
  sleep(1)
  pi.setINDI('LMIRCAM.Command.text','go',timeout=100000,wait=True)
  rawbg()
  nod(nod_x * ((i_nod % 2) * -2 + 1) + x_dither[i_nod],    nod_y * ((i_nod % 2) * -2 + 1) + y_dither[i_nod],    side)
  i_nods_done = i_nods_done + 1
  info('Number of nods executed (parameter i_nods_done): ' + str(i_nods_done))
  print ''
  sleep(1)
  pi.setINDI('LMIRCAM.Command.text','go',timeout=100000,wait=True)
  pi.setINDI('LMIRCAM.Command.text', '%f %i %i lbtintpar' % (dit, coadds, nseqs), wait=True)
  if savedata:
    pi.setINDI('LMIRCAM.Command.text', '1 savedata')
  else:
    pi.setINDI('LMIRCAM.Command.text', '0 savedata')

#=============
# We're done!
#=============
setFLAG('')
request('Script finished. Please start new observation.')

