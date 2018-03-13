from lmircam_tools import pi
from lmircam_tools.align_spec import align_spec
from lmircam_tools.exposures import get_lmircam_frames
from lmircam_tools.utils import nod, rawbg, setFLAG
from lmircam_tools.print_tools import *

#################################################
# USER DEFINED PARAMETERS                       #
#################################################

# camera
dit = 0.0            # DIT. 0.0 for minimum, should be standard.
ndit_fringes = 2000  # Number of integrations per nod on fringes.
ndit_spec = 200      # Number of integrations per nod on not overlapped spectra.
coadds = 1           # Do not change!
nnods_fringes = 1    # Number of nod pairs on fringes.
savedata = True      # Save data? Can be 'True' or 'False'
inner_loop_max = 10  # Maximum number of frames taken at once.

# telesecope
nod_x = 1.3          # arcseconds in detector coords
i_nods_done = 0      # number of nods finished (see Instructions above on how to use)

# bands
do_lband = True      # take L band data? (True/False)
do_nband = True      # take N band data? (True/False)

#################################################
# COMPUTATIONS/DEFINITIONS                      #
#################################################

nod_names = ['LEFT','RIGHT']

#################################################
# COMMAND SEQUENCE                              #
#################################################

print ''
request('Please set up for observations:')
print '  Field of view: "FIZEAU_spec_L", (for both L OR M band!)'
print '  Grism "Lgrism6AR", filter "Janos3.0-5.0" (for both L OR M band!)'
print '  L band (top long part, for both L OR M band!) of Spectra vertically centered'
print '  and approx. horizontally overlapped on column ~195,'
print '  Fringes approx. upright.'
print '  Hit [RETURN] when done.'; raw_input()



if do_lband:

# Take fringe data in left nod position in L band.
# Nod right
# Take fringe data in right nod position in L band.
# Nod left
# Take fringe data in left nod position in M band.
# Nod right
# Take fringe data in right nod position in M band.
# Nod left and separate spectra (left side left)
# Take spectra data in left nod position in L band.
# Nod right
# Take spectra data in right nod position in L band.
# Nod left
# Take spectra data in left nod position in M band.
# Nod right
# Take spectra data in right nod position in L band.
# Reset nod position
# Reset camera
#Reset fits keywords

