# Script for white dwarf planet imaging (PI: S. Ertel).
# This will only nod and request you to do the integrations manually (for robustness).
#
# Instructions:
# - Use the 'Mostly Unvignetted' FoV, single sided observations, H band, fast mode.
# - !!! USE DX if possible !!! (SX heavily vignetted)
# - Targets are faint, be aware of the long integration times and potential AO problems.
# - Put the star near pixel [x=550, y=400] if using DX ([x=1250, y=500] if using SX).
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
#  NOTE: When nodding manually, don't worry about the dither (and don't worry if you don't know what
#        this is). Just nod lower-left to upper right with x offest = 6acrsec, y offset = 5 arcsec.

from lmircam_tools import pi
from lmircam_tools.exposures import get_lmircam_frames, get_lmircam_bg
from lmircam_tools.utils import nod, setFLAG
from lmircam_tools.print_tools import *
from time import sleep

#################################################
# USER DEFINED PARAMETERS                       #
#################################################

#camera
dit_bkg = 10         # DIT for background and source positioning. May need updating based on source brightness.
dit = 60000          # DIT in sec, may need to be changed depending on saturation (remember to also change nseqs!)
coadds = 1           # Do not change!
nseqs = 10           # Change according to dit change: dit * nseqs = 600
savedata = True      # Save data? Can be 'True' or 'False'
use_bg = 1           # Use background? 1 - Yes, 2 - No.

#telesecope
nod_x = 6            # arcseconds in detector coords, might need updating
nod_y = 5            # arcseconds in detector coords, might need updating
side = 'right'       # singe sided observations, update which side is used
i_nods_done = 0      # number of nods finished (see instructions above on how to use)

#################################################
# COMPUTATIONS/DEFINITIONS                      #
#################################################

nod_names = ['NOD_A','NOD_B']
x_dither = [0.0, 0.1, 0.0, 0.0,  0.0, -0.1, 0.0]
y_dither = [0.0, 0.0,  0.0, 0.1, 0.0, 0.0,   0.0]

#################################################
# COMMAND SEQUENCE                              #
#################################################

pi.setINDI("LMIRCAM.stop.value=Off")                                        #  Make sure the camera is not running.

#=====================
# Start of nod cycles
#=====================

for i_nod in range(i_nods_done, 8):
  setFLAG(nod_names[i_nod % 2])
  try:
    get_lmircam_frames(dit, coadds, nseqs-1, use_bg=use_bg, save_data=savedata)
  except:
    request('Something happened.  Please recover error.')
    print('  When done, manually take remaining frames in this position.')
    print('  Hit [RETURN] when ready to nod (will take ne more frame in this position).'); raw_input()
    print('')
  get_lmircam_bg(dit, coadds, save_data=savedata)
  
  # Nodding
  nod(nod_x * ((i_nod % 2) * -2 + 1) + x_dither[i_nod],    nod_y * ((i_nod % 2) * -2 + 1) + y_dither[i_nod],    side)
  i_nods_done = i_nods_done + 1
  info('Number of nods executed (parameter i_nods_done): ' + str(i_nods_done))
  print ''
  sleep(1)

#=============
# We're done!
#=============
setFLAG('')
request('Script finished. Please start new observation.')

